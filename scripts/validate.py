#!/usr/bin/env python3
"""Reel Script Studio validator.

Checks every measurable rule in result.json and writes the report into its
`validation` key. Standard library only, so it runs in any sandbox.

    python scripts/validate.py rss_work/<slug>/result.json

Exit code 0 = no hard failures, 1 = hard failures (fix them in Stage 3), 2 = unreadable input.
Hard failures block the build. Soft findings are warnings the council reads.
"""
import itertools
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from textkit import (TAG_RE, BREAK_RE, PAUSE_RE, SLOT_RE, SLOT_WORDS, unslot, unnegated_hits, normalize, strip_markup, tokens, stem,  # noqa: E402,F401
                     number_words, sentences, count_words, count_pauses, key_terms, bigrams, starts_with_any, contains_any)
import craft_checks  # noqa: E402
import research_checks  # noqa: E402
import viewer_checks  # noqa: E402
import performance  # noqa: E402
import voice_fingerprint  # noqa: E402

VERSION = "rss-2.2"
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

BEAT_ORDER = ["hook", "retention", "problem", "solution", "proof", "cta"]
OPTION_COUNT = {"hook": 5, "retention": 3, "problem": 3, "solution": 3, "proof": 3, "cta": 3}
DEFAULT_PACING = {"ar": {"hook": 150, "body": 128, "cta": 115},
                  "en": {"hook": 175, "body": 145, "cta": 130}}
PAUSE_SECONDS = 0.5
OVER_TARGET = 1.10
MAX_CARD_WORDS = 6
MAX_COVER_WORDS = 4
COUNCIL = ["Strategy Director", "Creative Director", "Voice Guardian", "Performance Analyst", "Trust Officer"]
RUBRIC = {"Strategy Director": ["goal_fit", "awareness_fit"], "Creative Director": ["distinctiveness", "hook_strength"],
          "Voice Guardian": ["dialect_accuracy", "naturalness", "clarity"], "Performance Analyst": ["takeaway_value", "dropoff_risk"],
          "Trust Officer": ["claims", "proof"]}
STRUCTURED_TYPES = {"tutorial", "tips", "product"}
RISKY_CLAIMS = {"factual", "result"}


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


DIALECTS = load_json(HERE / "dialects.json")
EL_RULES = load_json(HERE / "elevenlabs_rules.json")
CORRECTIONS = load_json(HERE / "dialect_corrections.json")
STYLES = load_json(HERE / "styles.json")
SCHEMA = load_json(ROOT / "schemas" / "result.schema.json")

# ------------------------------------------------------------ mini JSON schema

def schema_errors(data, schema, path="$", root=None):
    root = root or schema
    if "$ref" in schema:
        name = schema["$ref"].split("/")[-1]
        return schema_errors(data, root["$defs"][name], path, root)
    errs = []
    types = {"object": dict, "array": list, "string": str, "boolean": bool}
    t = schema.get("type")
    if isinstance(t, list):
        def _is(x, name):
            if name == "null":
                return x is None
            if name == "integer":
                return isinstance(x, int) and not isinstance(x, bool)
            if name == "number":
                return isinstance(x, (int, float)) and not isinstance(x, bool)
            return name in types and isinstance(x, types[name])
        if not any(_is(data, n) for n in t):
            return [f"{path}: expected one of {t}"]
        t = None
    if t in types and not isinstance(data, types[t]):
        return [f"{path}: expected {t}"]
    if t == "integer" and (not isinstance(data, int) or isinstance(data, bool)):
        return [f"{path}: expected integer"]
    if t == "number" and (not isinstance(data, (int, float)) or isinstance(data, bool)):
        return [f"{path}: expected number"]
    if "const" in schema and data != schema["const"]:
        errs.append(f"{path}: must be {schema['const']!r}")
    if "enum" in schema and data not in schema["enum"]:
        errs.append(f"{path}: {data!r} not in {schema['enum']}")
    if isinstance(data, (int, float)) and not isinstance(data, bool):
        if "minimum" in schema and data < schema["minimum"]:
            errs.append(f"{path}: below minimum {schema['minimum']}")
        if "maximum" in schema and data > schema["maximum"]:
            errs.append(f"{path}: above maximum {schema['maximum']}")
    if isinstance(data, dict):
        for k in schema.get("required", []):
            if k not in data:
                errs.append(f"{path}: missing required key '{k}'")
        for k, sub in schema.get("properties", {}).items():
            if k in data:
                errs += schema_errors(data[k], sub, f"{path}.{k}", root)
    if isinstance(data, list):
        if "minItems" in schema and len(data) < schema["minItems"]:
            errs.append(f"{path}: needs at least {schema['minItems']} items")
        if "maxItems" in schema and len(data) > schema["maxItems"]:
            errs.append(f"{path}: allows at most {schema['maxItems']} items")
        if "items" in schema:
            for i, item in enumerate(data):
                errs += schema_errors(item, schema["items"], f"{path}[{i}]", root)
    return errs


# ------------------------------------------------------------------ validator

class Report:
    def __init__(self):
        self.hard, self.soft = [], []

    def fail(self, check, where, message):
        self.hard.append({"check": check, "where": where, "message": message})

    def warn(self, check, where, message):
        self.soft.append({"check": check, "where": where, "message": message})


def _num(x):
    """A rubric score as a number, or None if it is not one (bools and '4/5' are rejected)."""
    if isinstance(x, bool):
        return None
    if isinstance(x, (int, float)):
        return x
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def rate_for(beat_id, pacing):
    return pacing["hook"] if beat_id == "hook" else pacing["cta"] if beat_id == "cta" else pacing["body"]


def seconds_for(text, beat_id, pacing, lang, dialect):
    return count_words(text, lang, dialect) / rate_for(beat_id, pacing) * 60 + count_pauses(text) * PAUSE_SECONDS


LATER_KEYS = ("council", "voice", "production", "publish")


def _accent_verified(accent):
    """Tested by ear: a non-empty note that is not marked provisional."""
    v = accent.get("verified")
    return isinstance(v, str) and bool(v.strip()) and not v.strip().lower().startswith("provisional")


def _guarantee_scan(r):
    """Every place a regulated Reel could promise an outcome, as (kind, where, text).
    Kinds: spoken (options, final script, clips, tight cut, shot voice), overlay (option and shot overlays),
    cover, caption (caption, pinned comment, comment automation)."""
    for b in r["beats"]:
        for o in b["options"]:
            where = f"{b['id']}.{o['id']}"
            yield "spoken", where, o["text"]
            for card in o.get("onscreen", []):
                yield "overlay", f"{where}.onscreen", card
    for ln in r["final_script"]["lines"]:
        yield "spoken", f"final_script.{ln['beat']}", ln["text"]
    for cl in ((r.get("voice") or {}).get("elevenlabs") or {}).get("clips", []):
        yield "spoken", f"voice.elevenlabs.clips.{cl['beat']}", cl["text"]
    for n, ln in enumerate((r.get("tight_cut") or {}).get("lines") or []):
        text = ln.get("text") if isinstance(ln, dict) else ln
        if isinstance(text, str):
            yield "spoken", f"tight_cut.lines[{n}]", text
    for n, shot in enumerate((r.get("production") or {}).get("shots") or []):
        if shot.get("voice"):
            yield "spoken", f"production.shots[{n}].voice", shot["voice"]
        for card in shot.get("onscreen", []):
            yield "overlay", f"production.shots[{n}].onscreen", card
    pub = r.get("publish") or {}
    if pub.get("cover_text"):
        yield "cover", "publish.cover_text", pub["cover_text"]
    for key in ("caption", "pinned_comment"):
        if pub.get(key):
            yield "caption", f"publish.{key}", pub[key]
    auto = pub.get("automation") or {}
    for key in ("keyword", "dm"):
        if auto.get(key):
            yield "caption", f"publish.automation.{key}", auto[key]
    for key in ("variants", "public_replies"):
        for text in auto.get(key) or []:
            yield "caption", f"publish.automation.{key}", text


def _word_is(tok, wrong):
    """tok is `wrong` itself or `wrong` with an attached prefix. `wrong` is never stemmed; a short
    (<=3-letter) word only takes the conjunction «و», so «لين» does not hit «فلين»/«كلين»."""
    if tok == wrong:
        return True
    if len(wrong) <= 3:
        return tok == "و" + wrong
    return stem(tok) == wrong


def _phrase_at(toks, i, q):
    """Normalized phrase q (token list) starts at toks[i]; only the first word may carry a prefix."""
    return (i + len(q) <= len(toks) and _word_is(toks[i], q[0].strip(".'’-"))
            and all(toks[i + j] == q[j].strip(".'’-") for j in range(1, len(q))))


def validate(r, stage="full"):
    """stage='writer' checks only what exists after Stage 3 (run before the council);
    stage='full' checks everything (run after Stage 7, and always by the builder)."""
    rep = Report()
    stats = {"stage": stage}
    schema = SCHEMA
    if stage == "writer":
        schema = dict(SCHEMA, required=[k for k in SCHEMA["required"] if k not in LATER_KEYS])

    if isinstance(r.get("meta"), dict) and r["meta"].get("version") == "rss-2.0":
        rep.fail("schema", "meta.version", "This result is rss-2.0; v2.2 needs research, concept and viewer_mind. Re-run Stages 1–3 with the current references.")
        return finish(r, rep, stats)
    for e in schema_errors(r, schema):
        rep.fail("schema", e.split(":")[0], e)
    if rep.hard:  # structure is broken; deeper checks would only add noise
        return finish(r, rep, stats)

    meta, intake, idea = r["meta"], r["intake"], r["idea"]
    lang, dialect = meta["language"], meta["dialect"]
    style = STYLES.get(intake["style"], STYLES["professional"])
    if meta.get("pacing"):
        pacing = dict(DEFAULT_PACING[lang])
        pacing.update(meta["pacing"])
    else:
        pacing = {k: round(v * style["pace_factor"]) for k, v in DEFAULT_PACING[lang].items()}
    target = float(meta["target_seconds"])
    limit = target * OVER_TARGET
    text_only = idea["routing"] == "text_only"
    has_draft = bool((intake.get("original_draft") or "").strip())

    # --- beats and options -------------------------------------------------
    beats = r["beats"]
    ids = [b["id"] for b in beats]
    if ids != BEAT_ORDER:
        rep.fail("beat_order", "beats", f"Beats must be {BEAT_ORDER} in that order; got {ids}.")
        return finish(r, rep, stats)
    by_id = {b["id"]: b for b in beats}
    seen_ids = set()
    for b in beats:
        opts = b["options"]
        want = OPTION_COUNT[b["id"]]
        if len(opts) != want:
            rep.fail("option_count", b["id"], f"{b['id']} needs exactly {want} options; has {len(opts)}.")
        tags = [o["tag"] for o in opts]
        if tags.count("recommended") != 1:
            rep.fail("option_tags", b["id"], f"{b['id']} needs exactly one 'recommended' option; has {tags.count('recommended')}.")
        if "bold" not in tags:
            rep.fail("option_tags", b["id"], f"{b['id']} needs a 'bold' option.")
        if has_draft and tags.count("safe_edit") != 1:
            rep.fail("option_tags", b["id"], f"A draft was given, so {b['id']} needs exactly one 'safe_edit' option.")
        mechs = [normalize(o["mechanism"]).strip() for o in opts]
        if len(set(mechs)) != len(mechs):
            rep.fail("mechanism_repeat", b["id"], f"{b['id']} options must use different mechanisms; got {[o['mechanism'] for o in opts]}.")
        for o in opts:
            where = f"{b['id']}.{o['id']}"
            if o["id"] in seen_ids:
                rep.fail("option_id", where, f"Option id '{o['id']}' is used twice.")
            seen_ids.add(o["id"])
            for card in o["onscreen"]:
                n = count_words(card, lang, dialect)
                if n > MAX_CARD_WORDS:
                    rep.fail("onscreen_words", where, f"On-screen card has {n} words (max {MAX_CARD_WORDS}): «{card}». Split it.")
                if SLOT_RE.search(card):
                    rep.fail("slot_misplaced", where, f"Fill-in slot in an on-screen card: «{card}». Slots belong only in spoken option text.")
            if text_only:
                n = count_words(o["text"], lang, dialect)
                if n > MAX_CARD_WORDS:
                    rep.fail("text_card_words", where, f"Text-only mode: each line is a card of max {MAX_CARD_WORDS} words; this has {n}.")
            if TAG_RE.search(o["text"]) or BREAK_RE.search(o["text"]):
                rep.fail("markup_in_script", where, "Script options must be plain speech. ElevenLabs tags belong only in voice.elevenlabs.clips.")

    # --- hook rules --------------------------------------------------------
    # Both lists always: creators code-switch, so an English hedge can open an Arabic Reel.
    hedges = DIALECTS["hook_hedges"]["ar"] + DIALECTS["hook_hedges"]["en"]
    openers = DIALECTS["hook_banned_openers"]["ar"] + DIALECTS["hook_banned_openers"]["en"]
    for o in by_id["hook"]["options"]:
        where = f"hook.{o['id']}"
        h = starts_with_any(o["text"], hedges)
        if h:
            rep.fail("hook_hedge", where, f"Hook opens with the hedge «{h}». State the opinion firmly or open on a concrete moment.")
        g = starts_with_any(o["text"], openers) or (contains_any(o["text"], [x for x in openers if len(normalize(x).split()) > 1]) or [None])[0]
        if g:
            rep.fail("hook_opener", where, f"Hook uses a greeting or 'in this video' opener («{g}»).")
        if not o.get("scores"):
            rep.warn("hook_scores", where, "Hook has no clarity/tension/relevance/credibility scores.")

    for o in by_id["hook"]["options"]:
        if not (o.get("visual") or "").strip():
            rep.fail("hook_visual_missing", f"hook.{o['id']}", "Every hook is a package: add `visual` (what the first frame shows).")
    if idea["type"] in STRUCTURED_TYPES and not (idea.get("takeaway") or "").strip():
        rep.fail("takeaway_missing", "idea.takeaway", "Tutorials, tips and product Reels need one concrete takeaway the viewer can act on.")
    if idea["verdict"] != "strong" and not (idea.get("honest_take") or "").strip():
        rep.fail("honest_take_missing", "idea.honest_take", "The idea isn't rated strong, so say so honestly: what's weak, what would be better, and that the decision is the creator's.")
    if idea["verdict"] == "rethink" and not idea.get("creator_choice"):
        rep.fail("creator_choice_missing", "idea.creator_choice", "A Rethink idea needs the creator's decision (as_is or suggested_angle) before writing. Ask once, then respect the answer.")
    spoken_final = viewer_checks.spoken_tokens(" ".join(ln["text"] for ln in r["final_script"]["lines"]))
    for phrase in intake.get("must_keep") or []:
        # substring, not whole tokens: Arabic attaches prefixes to names («بـClaude», «بحلّها»)
        if " ".join(viewer_checks.spoken_tokens(phrase)) not in " ".join(spoken_final):
            rep.fail("must_keep_missing", "final_script", f"The creator asked to keep «{phrase}», and the final script doesn't say it.")
    if not any(o.get("human_texture") for b in beats for o in b["options"]):
        rep.warn("human_texture_missing", "beats", "No line only this creator could say. Add their story, number or mistake (mark it human_texture: true).")
    register = meta["register"]
    heavy = {stem(normalize(w)) for w in DIALECTS["dialects"].get(dialect, {}).get("heavy_only", [])}
    lines_preview = r["final_script"]["lines"]
    if register != "heavy" and heavy:
        # Like dialect_foreign: scan every option too, since the creator can swap any of them in.
        scan = [(f"final_script.{ln['beat']}", ln["text"]) for ln in lines_preview]
        scan += [(f"{b['id']}.{o['id']}", o["text"]) for b in beats for o in b["options"]]
        for where, text in scan:
            hits = sorted({t for t in tokens(text) if stem(t) in heavy})
            if hits:
                rep.warn("register_heavy_word", where, f"{hits} may be too local for the '{register}' level. Swap for widely understood words unless the voice sample uses them.")

    for o in by_id["cta"]["options"]:
        bait = contains_any(o["text"], DIALECTS["engagement_bait"]["ar"] + DIALECTS["engagement_bait"]["en"])
        if bait:
            rep.warn("engagement_bait", f"cta.{o['id']}", f"CTA looks like engagement bait ({', '.join(bait)}).")

    # --- proof honesty -----------------------------------------------------
    declared = {p for p in intake["proof"] if p != "none"}
    for o in by_id["proof"]["options"]:
        where = f"proof.{o['id']}"
        uses = set(o.get("proof_uses") or [])
        extra = uses - declared
        if extra:
            rep.fail("proof_undeclared", where, f"Proof option needs {sorted(extra)}, which the creator did not declare. Use declared proof or a demonstration flagged needs_footage.")
        if not declared and not text_only and "needs_footage" not in (o.get("flags") or []):
            rep.fail("proof_unflagged", where, "No proof was declared, so every proof option must carry the 'needs_footage' flag.")

    # --- presets and final script -----------------------------------------
    opt_index = {b["id"]: {o["id"]: o for o in b["options"]} for b in beats}
    for preset, tag in (("recommended", "recommended"), ("safe_edit", "safe_edit"), ("bold", "bold")):
        mapping = r["presets"].get(preset) or {}
        if preset == "safe_edit" and not has_draft and not mapping:
            continue
        for bid in BEAT_ORDER:
            oid = mapping.get(bid)
            o = opt_index[bid].get(oid)
            if o is None:
                rep.fail("preset_ref", f"presets.{preset}.{bid}", f"Preset '{preset}' points to '{oid}', which is not an option of {bid}.")
            elif o["tag"] != tag:
                rep.fail("preset_tag", f"presets.{preset}.{bid}", f"Preset '{preset}' uses '{oid}', which is tagged '{o['tag']}'.")

    lines = r["final_script"]["lines"]
    rec = r["presets"]["recommended"]
    rec_opts = [opt_index[bid].get(rec.get(bid)) for bid in BEAT_ORDER]
    rec_opts = [o for o in rec_opts if o]
    if rec_opts and not any(o.get("human_texture") for o in rec_opts) and not any(SLOT_RE.search(o["text"]) for o in rec_opts):
        rep.warn("creator_detail_missing", "presets.recommended",
                 "The Recommended script has no line only this creator could say. Mark their real story/number line human_texture: true, "
                 "or leave a fill-in slot in one Recommended line, e.g. «{{رقم حقيقي: كم دقيقة تضيع يومياً؟}}».")
    expected = [(bid, opt_index[bid].get(rec.get(bid), {}).get("text", "")) for bid in BEAT_ORDER]
    got = [(ln["beat"], ln["text"]) for ln in lines]
    if [(b, " ".join(tokens(t))) for b, t in got] != [(b, " ".join(tokens(t))) for b, t in expected]:
        rep.fail("final_not_recommended", "final_script", "final_script must be exactly the Recommended preset, beat by beat, in order.")

    # --- counts and durations ----------------------------------------------
    per_line = []
    for ln in lines:
        bid = ln["beat"] if ln["beat"] in BEAT_ORDER else "solution"
        w = count_words(ln["text"], lang, dialect)
        s = 0.0 if text_only else seconds_for(ln["text"], bid, pacing, lang, dialect)
        per_line.append({"beat": ln["beat"], "words": w, "seconds": round(s, 1)})
    final_words = sum(x["words"] for x in per_line)
    final_secs = sum(0.0 if text_only else seconds_for(ln["text"], ln["beat"] if ln["beat"] in BEAT_ORDER else "solution", pacing, lang, dialect) for ln in lines)
    fs = r["final_script"]
    if "declared_words" in fs and fs["declared_words"] != final_words:
        rep.fail("declared_mismatch", "final_script.declared_words", f"Declared {fs['declared_words']} words; the spoken count is {final_words} (numbers count as spoken).")
    if "declared_seconds" in fs and not text_only and abs(fs["declared_seconds"] - final_secs) > 1.0:
        rep.fail("declared_mismatch", "final_script.declared_seconds", f"Declared {fs['declared_seconds']} s; the computed estimate is {final_secs:.1f} s.")
    if not text_only and final_secs < target * 0.6:
        rep.warn("too_short", "final_script", f"Final script is {final_secs:.1f} s for a {target:.0f} s target.")

    # --- every combination -------------------------------------------------
    anchors = {stem(normalize(a)) for a in r.get("anchor_terms") or []}
    anchor_bigrams = set()
    for a in r.get("anchor_terms") or []:
        at = [stem(t) for t in tokens(a)]
        anchor_bigrams |= set(zip(at, at[1:]))
    anchors |= {stem(t) for a in r.get("anchor_terms") or [] for t in tokens(a)}
    info = {}
    for b in beats:
        for o in b["options"]:
            surface = key_terms(o["text"], lang)
            terms = set(surface)
            info[(b["id"], o["id"])] = {
                "secs": 0.0 if text_only else seconds_for(o["text"], b["id"], pacing, lang, dialect),
                "terms": terms - anchors,
                "surface": surface,
                "anchor": bool(terms & anchors),
                "bigrams": bigrams(o["text"], lang) - anchor_bigrams,
            }
    # Repetition is a pairwise property: any two options from different beats meet in some combination.
    phrase_pairs = []
    keys = list(info)
    for (k1, k2) in itertools.combinations(keys, 2):
        if k1[0] == k2[0]:
            continue
        shared_bg = info[k1]["bigrams"] & info[k2]["bigrams"]
        if shared_bg:
            phrase_pairs.append((k1, k2, sorted(" ".join(x) for x in shared_bg)))
    for k1, k2, shared in phrase_pairs:
        rep.fail("phrase_repeat", f"{k1[0]}.{k1[1]} + {k2[0]}.{k2[1]}", f"Repeated phrase across beats: {shared}. These options can be combined, so reword one.")
    # A repeated key word is one finding per word, not one per option pair.
    by_term = {}
    for k in keys:
        for t in sorted(info[k]["terms"]):
            by_term.setdefault(t, []).append(k)
    for t, where in by_term.items():
        beats_hit = list(dict.fromkeys(k[0] for k in where))
        if len(beats_hit) < 2:
            continue
        example = [next(k for k in where if k[0] == bid) for bid in beats_hit[:2]]
        word = info[where[0]]["surface"][t]
        rep.warn("word_repeat", " + ".join(f"{k[0]}.{k[1]}" for k in where),
                 f"«{word}» appears in {len(beats_hit)} beats across options (e.g. {example[0][0]}.{example[0][1]} + {example[1][0]}.{example[1][1]}). Fine if it's the topic; otherwise vary it.")

    combos = list(itertools.product(*[[(b["id"], o["id"]) for o in b["options"]] for b in beats]))
    over, anchor_bad, durations = 0, 0, []
    worst = None
    for combo in combos:
        secs = sum(info[k]["secs"] for k in combo)
        durations.append(secs)
        if not text_only and secs > limit + 1e-9:
            over += 1
            if worst is None or secs > worst[0]:
                worst = (secs, combo)
        if sum(info[k]["anchor"] for k in combo) > 2:
            anchor_bad += 1
    if over:
        rep.fail("combo_over_target", "beats", f"{over} of {len(combos)} combinations run over {limit:.1f} s (target {target:.0f} s + 10%). Longest: {worst[0]:.1f} s = {[k[1] for k in worst[1]]}. Shorten the longest options or cut whole ideas.")
    if anchor_bad:
        rep.fail("anchor_overuse", "beats", f"{anchor_bad} combinations name the product/anchor term in more than 2 beats. Keep it to at most 2 beats in any combination.")
    stats.update({
        "pacing_wpm": pacing,
        "target_seconds": target,
        "limit_seconds": round(limit, 1),
        "final_words": final_words,
        "final_seconds": round(final_secs, 1),
        "per_line": per_line,
        "combos_checked": len(combos),
        "combos_over_target": over,
        "combo_seconds_min": round(min(durations), 1) if durations and not text_only else None,
        "combo_seconds_max": round(max(durations), 1) if durations and not text_only else None,
    })

    # --- dialect -----------------------------------------------------------
    d = DIALECTS["dialects"].get(dialect, {"foreign": []})
    foreign = {stem(normalize(w)): w for w in d["foreign"]}
    if foreign:
        scan = [("final_script", ln["text"]) for ln in lines] + [(f"{b['id']}.{o['id']}", o["text"]) for b in beats for o in b["options"]]
        for where, text in scan:
            hits = sorted({foreign[stem(t)] for t in tokens(text) if stem(t) in foreign} | {foreign[t] for t in tokens(text) if t in foreign})
            if hits:
                rep.warn("dialect_foreign", where, f"Words usually from another dialect for {dialect}: {hits}. Keep only if the creator really says them.")

    # Native-verified word swaps (scripts/dialect_corrections.json): hard when verified, soft when provisional.
    # Only the listed `wrong` + `forms` match (whole tokens or phrases), plus attached prefixes on the first word.
    fixes = [(c, [tokens(f) for f in [c["wrong"]] + list(c.get("forms") or []) if tokens(f)]) for c in CORRECTIONS.get(dialect, [])]
    if fixes:
        scan = [("final_script", ln["text"]) for ln in lines] + [(f"{b['id']}.{o['id']}", o["text"]) for b in beats for o in b["options"]]
        scan += [(f"voice.elevenlabs.clips.{cl['beat']}", cl["text"]) for cl in ((r.get("voice") or {}).get("elevenlabs") or {}).get("clips", [])]
        for where, text in scan:
            toks = [t.strip(".'’-") for t in tokens(text)]
            for c, phrases in fixes:
                if any(_phrase_at(toks, i, q) for q in phrases for i in range(len(toks))):
                    msg = f"«{c['wrong']}» → «{c['right']}»: {c['why']}"
                    (rep.fail if c.get("status") == "native_verified" else rep.warn)("dialect_correction", where, msg)

    # --- claims and trust --------------------------------------------------
    risky_kept = [c for c in r["audit"]["claims"] if c["type"] in RISKY_CLAIMS and c["action"] == "keep"]
    for c in risky_kept:
        rep.fail("claim_unverified", "audit.claims", f"A {c['type']} claim is kept without evidence: «{c['text']}». Soften, replace, remove, or set keep_with_evidence with the evidence.")
    for c in r["audit"]["claims"]:
        if c["action"] == "keep_with_evidence" and not (c.get("evidence") or "").strip():
            rep.fail("claim_no_evidence", "audit.claims", f"«{c['text']}» is marked keep_with_evidence but names no evidence.")
        if c["type"] in RISKY_CLAIMS and c["action"] in ("keep", "keep_with_evidence") and idea.get("regulated") and not declared:
            rep.fail("regulated_claim", "audit.claims", f"Regulated niche: «{c['text']}» needs declared proof the viewer can see.")
    if idea.get("regulated"):
        lexicon = craft_checks.CRAFT["regulated_guarantee"]["ar"] + craft_checks.CRAFT["regulated_guarantee"]["en"]
        found = {}  # (phrase, kind) -> locations: one finding each, not one per mirror of the same line
        for kind, where, text in _guarantee_scan(r):
            for phrase in unnegated_hits(text, lexicon):
                found.setdefault((phrase, kind), []).append(where)
        for (phrase, kind), wheres in found.items():
            rep.fail("regulated_guarantee", " + ".join(dict.fromkeys(wheres)),
                     f"Regulated niche: «{phrase}» promises a guaranteed outcome ({kind}). Say what happened to you or what the evidence shows, never a guarantee or a cure. A disclaimer («ما في شي مضمون») is fine.")
    research_checks.check(r, rep)
    sa = r["self_assessment"]
    if risky_kept and sa["score"] > 69:
        rep.fail("trust_score_cap", "self_assessment.score", "A risky claim survives, so the self-assessed score is capped at 69.")

    perf = intake.get("performance") or []
    if perf:
        pa = r.get("performance_analysis") or {}
        if pa.get("input_hash") != performance.input_hash(perf):
            rep.fail("performance_unanalyzed", "performance_analysis", "Run `python scripts/performance.py <result.json>` after filling intake.performance (missing or stale analysis).")

    final_texts = [unslot(ln["text"]) for ln in r["final_script"]["lines"]]
    sent_lens = [len(tokens(s)) for t in final_texts for s in sentences(t)]
    if sent_lens and not text_only:
        mean = sum(sent_lens) / len(sent_lens)
        lo, hi = style["sentence_words"]
        if not (lo <= mean <= hi):
            rep.warn("style_rhythm", "final_script", f"Average sentence is {mean:.1f} words; the {intake['style']} style sits at {lo}–{hi}. Rewrite the rhythm, not just the words.")
    q = sum(t.count("?") + t.count("؟") for t in final_texts)
    if q > style["max_questions"]:
        rep.warn("style_questions", "final_script", f"{q} questions; the {intake['style']} style uses at most {style['max_questions']}.")

    for msg in voice_fingerprint.drift(intake.get("voice_fingerprint"), final_texts, lang):
        rep.warn("voice_drift", "final_script", msg)

    viewer_checks.check(r, rep, pacing, text_only)
    craft_checks.check_script(r, rep, lang)
    if stage == "writer":
        return finish(r, rep, stats)

    # --- council -----------------------------------------------------------
    c = r["council"]
    rounds = c["rounds"]
    if not rounds:
        rep.fail("council_missing", "council.rounds", "The council has not reviewed yet.")
    max_rounds = 2 if meta["depth"] == "quick" else 3
    if len(rounds) > max_rounds:
        rep.fail("council_rounds", "council.rounds", f"At most {max_rounds - 1} revision round(s) in {meta['depth']} mode.")
    corpus = " ".join(" ".join(tokens(o["text"])) for b in beats for o in b["options"]) + " " + " ".join(" ".join(tokens(ln["text"])) for ln in lines)
    for i, rnd in enumerate(rounds):
        members = [v["member"] for v in rnd.get("verdicts", [])]
        if sorted(members) != sorted(COUNCIL):
            rep.fail("council_members", f"council.rounds[{i}]", f"Each round needs exactly one verdict from each of {COUNCIL}.")
        for v in rnd.get("verdicts", []):
            # Earlier rounds quote text that later revisions changed, so only the last round must match.
            for field in (("quote", "weakest_line") if i == len(rounds) - 1 else ()):
                q = " ".join(tokens(v.get(field, "")))
                if q and q not in corpus:
                    rep.warn("council_quote", f"council.rounds[{i}].{v['member']}", f"{field} is not an exact quote from the script: «{v.get(field)}».")
            if i == len(rounds) - 1:
                research_checks.require_basis(r, rep, f"council.rounds[{i}].{v['member']}", v.get("basis"))
            if v["verdict"] == "reject" and v["member"] != "Trust Officer":
                rep.fail("council_power", f"council.rounds[{i}].{v['member']}", "Only the Trust Officer can reject.")
            want = RUBRIC.get(v["member"], [])
            sc = v.get("scores") or {}
            bad = sorted(k for k, x in sc.items() if _num(x) is None)
            if any(k not in sc for k in want):
                rep.fail("council_scores_missing", f"council.rounds[{i}].{v['member']}", f"Score every rubric item: {want}.")
            elif bad:
                rep.fail("council_score_invalid", f"council.rounds[{i}].{v['member']}", f"Scores must be numbers 1-5; not a number: {bad}.")
            elif v["verdict"] == "approve" and any(_num(sc[k]) < 4 for k in want):
                rep.fail("council_score_inconsistent", f"council.rounds[{i}].{v['member']}", "Approved with a score below 4. Any score < 4 means revise with a concrete rewrite.")
    if rounds and rounds[0].get("verdicts") and all(
            v["verdict"] == "approve" and v.get("scores") and all(_num(x) == 5 for x in v["scores"].values())
            for v in rounds[0]["verdicts"]):
        rep.warn("council_rubber_stamp", "council.rounds[0]", "Everyone gave 5/5 in round 1. Re-read it as the skeptic persona and against the creator's original: what would a top creator still change?")
    if rounds:
        last = rounds[-1]
        trust = next((v for v in last.get("verdicts", []) if v["member"] == "Trust Officer"), None)
        if trust and trust["verdict"] == "reject" and c["final_decision"] != "blocked_claim":
            rep.fail("trust_veto_ignored", "council.final_decision", "The Trust Officer rejected in the last round. Remove the claim and re-run, or set final_decision to blocked_claim. A vetoed script never ships.")
        if (r["viewer_mind"].get("unresolved") or "").strip() and c["final_decision"] == "ship":
            rep.fail("viewer_unresolved_shipped", "council.final_decision", "The Viewer Mind left an unresolved hook problem, so the decision is ship_with_issues at best, with the issue listed.")
        if c["final_decision"] == "ship" and c.get("open_issues"):
            rep.warn("council_open_issues", "council.final_decision", "Decision is 'ship' but open issues are listed; use ship_with_issues.")

    # --- ElevenLabs --------------------------------------------------------
    rec_cfg = intake["recording"]
    voice = r["voice"]
    if not text_only and not voice.get("performance"):
        rep.fail("voice_missing", "voice.performance", "Spoken Reels need a performance sheet.")
    el = voice.get("elevenlabs")
    if not text_only and not el:
        rep.fail("el_missing", "voice.elevenlabs", "Spoken Reels always get an ElevenLabs version (default model v4 when none was chosen).")
    if rec_cfg["method"] == "ai_voice":
        if el and el.get("model") != rec_cfg.get("elevenlabs_model"):
            rep.fail("el_model_mismatch", "voice.elevenlabs.model", f"Clips are for {el.get('model')} but the creator chose {rec_cfg.get('elevenlabs_model')}.")
        if not r["publish"].get("ai_label"):
            rep.fail("ai_label", "publish.ai_label", "An AI voice needs the platform's AI label; set publish.ai_label to true and remind the creator.")
    if el:
        model = EL_RULES["models"].get(el.get("model") or "other", EL_RULES["models"]["other"])
        verified = {normalize(t) for t in EL_RULES["verified_tags"]}
        accent = EL_RULES.get("accent_tags", {}).get(dialect)
        accent_tags = {normalize(a["tag"]) for k, a in EL_RULES.get("accent_tags", {}).items() if not k.startswith("_")}
        verified |= {normalize(accent["tag"])} if accent and _accent_verified(accent) else set()
        pauses = {normalize(t) for t in EL_RULES["pause_tags"]}
        clip_beats = [cl["beat"] for cl in el.get("clips", [])]
        if clip_beats != BEAT_ORDER:
            rep.fail("el_clips", "voice.elevenlabs.clips", f"Generate one clip per beat, in order {BEAT_ORDER}; got {clip_beats}.")
        final_by_beat = {ln["beat"]: ln["text"] for ln in lines}
        for cl in el.get("clips", []):
            where = f"voice.elevenlabs.clips.{cl['beat']}"
            if SLOT_RE.search(cl["text"]):
                rep.warn("el_unfilled_slot", where, "This clip still has a {{…}} slot. Fill in your real detail before generating, or the voice will read the placeholder.")
            tags = [normalize(t[1:-1]).strip() for t in TAG_RE.findall(cl["text"])]
            breaks = BREAK_RE.findall(cl["text"])
            if tags and not model["brackets"]:
                rep.fail("el_tag_forbidden", where, f"{model['label']} reads square-bracket tags aloud. Remove {tags}; use punctuation{' or <break>' if model['break_tag'] else ''}.")
            if breaks and not model["break_tag"]:
                rep.fail("el_break_forbidden", where, f"{model['label']} does not support <break>. Use '...' or [pause].")
            if model.get("max_breaks_per_clip") and len(breaks) > model["max_breaks_per_clip"]:
                rep.warn("el_break_count", where, f"{len(breaks)} <break> tags; too many cause speed glitches.")
            if model["brackets"]:
                for t in tags:
                    if t not in verified:
                        rep.warn("el_tag_unverified", where, f"[{t}] is not on the verified tag list. Label it as an experiment: delete it if it gets read aloud.")
                msa = meta["register"] == "simplified_msa"
                if accent and not msa and normalize(accent["tag"]) not in tags:
                    rep.warn("el_accent_tag", where, f"Start the clip with [{accent['tag']}] so the voice keeps the {dialect} accent.")
                if msa:
                    wrong = [t for t in tags if t in accent_tags]
                else:
                    wrong = [t for t in tags if t in accent_tags and (not accent or t != normalize(accent["tag"]))]
                if wrong:
                    rep.fail("el_accent_mismatch", where, f"Accent tag {wrong} does not match the script's dialect ({dialect}).")
                emotions = [t for t in tags if t not in pauses and t not in accent_tags]
                if len(emotions) > 1:
                    rep.warn("el_tag_density", where, f"{len(emotions)} emotion tags in one clip; use at most one.")
                bad = [t for t in emotions if t not in {normalize(x) for x in style["el"]["emotions"]}]
                if bad:
                    rep.warn("el_style_tag", where, f"{bad} doesn't fit the {intake['style']} style (allowed: {style['el']['emotions'] or 'none'}).")
            if cl["beat"] in final_by_beat:
                a = [stem(t) for t in tokens(cl["text"])]
                b = [stem(t) for t in tokens(final_by_beat[cl["beat"]])]
                if a != b:
                    rep.warn("el_text_drift", where, "Clip wording differs from the final script. Fine for a spelling or synonym fix; otherwise copy the final line.")

    craft_checks.check_publish(r, rep, lang)

    # --- production and publish -------------------------------------------
    needs = any("needs_footage" in (o.get("flags") or []) for o in by_id["proof"]["options"])
    if needs and not text_only and not r["production"].get("proof_shots"):
        rep.fail("proof_shots_missing", "production.proof_shots", "Proof needs footage, so give the exact shots to film (shot, how, duration).")
    for i, shot in enumerate(r["production"]["shots"]):
        for card in shot["onscreen"]:
            n = count_words(card, lang, dialect)
            if n > MAX_CARD_WORDS:
                rep.fail("onscreen_words", f"production.shots[{i}]", f"On-screen card has {n} words (max {MAX_CARD_WORDS}): «{card}».")
            if SLOT_RE.search(card):
                rep.fail("slot_misplaced", f"production.shots[{i}]", f"Fill-in slot in an on-screen card: «{card}». Write the real detail here.")
    if SLOT_RE.search(r["publish"]["caption"]):
        rep.fail("slot_misplaced", "publish.caption", "The caption still has a {{…}} slot. Captions ship as written, so write the real detail.")
    if SLOT_RE.search(r["publish"].get("cover_text") or ""):
        rep.fail("slot_misplaced", "publish.cover_text", "The cover text still has a {{…}} slot. Write the real detail.")
    for i, ps in enumerate(r["production"].get("proof_shots") or []):
        for field in ("shot", "how", "duration"):
            if SLOT_RE.search(str(ps.get(field) or "")):
                rep.fail("slot_misplaced", f"production.proof_shots[{i}].{field}", "Proof shot still has a {{…}} slot. Name the real shot.")
    cover = r["publish"].get("cover_text")
    if cover and count_words(cover, lang, dialect) > MAX_COVER_WORDS:
        rep.warn("cover_words", "publish.cover_text", f"Cover text should be 2–{MAX_COVER_WORDS} words.")
    first_line = r["publish"]["caption"].split("\n")[0]
    if len(first_line) > 125:
        rep.warn("caption_first_line", "publish.caption", "The caption's first line runs past the ~125 characters shown before 'more'.")

    return finish(r, rep, stats)


def finish(r, rep, stats):
    report = {
        "version": VERSION,
        "passed": not rep.hard,
        "hard": rep.hard,
        "soft": rep.soft,
        "stats": stats,
    }
    r["validation"] = report
    return report


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    path = Path(argv[1])
    try:
        data = load_json(path)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Cannot read {path}: {e}")
        return 2
    stage = "writer" if "--stage" in argv and argv[argv.index("--stage") + 1:argv.index("--stage") + 2] == ["writer"] else "full"
    report = validate(data, stage)
    if "--dry-run" not in argv:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    s = report["stats"]
    print(f"{'PASS' if report['passed'] else 'FAIL'}: {len(report['hard'])} hard, {len(report['soft'])} soft")
    if s.get("final_words") is not None:
        timing = "text-only cards" if data.get("idea", {}).get("routing") == "text_only" else f"~{s['final_seconds']} s (limit {s['limit_seconds']} s)"
        print(f"[{stage}] Final script: {s['final_words']} words, {timing}; "
              f"{s['combos_checked']} combinations, {s['combos_over_target']} over the limit")
    for item in report["hard"]:
        print(f"  HARD [{item['check']}] {item['where']}: {item['message']}")
    for item in report["soft"]:
        print(f"  soft [{item['check']}] {item['where']}: {item['message']}")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv))

