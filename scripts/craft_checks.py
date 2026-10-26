"""Craft checks: the senior-writer bar. Hard = AI tells; soft = weak craft the council weighs."""
import json
import re
from pathlib import Path

from textkit import normalize, tokens, stem, key_terms, contains_any, unslot, sentences, starts_with_any, strip_markup

CRAFT = json.loads((Path(__file__).resolve().parent / "craft.json").read_text(encoding="utf-8"))
STYLE_MAX_Q = {k: v["max_questions"] for k, v in json.loads((Path(__file__).resolve().parent / "styles.json").read_text(encoding="utf-8")).items()
               if isinstance(v, dict) and "max_questions" in v}


BODY_WPM = {"ar": 128, "en": 145}
DIGIT = re.compile(r"[0-9٠-٩۰-۹]")
QUOTED = re.compile(r"«[^»]*»|\"[^\"]*\"|“[^”]*”")  # quoted demo text is shown, not claimed
LATIN_WORD = re.compile(r"[A-Za-z]{2,}")
NAME_EN = re.compile(r"(?<=[a-z,;:] )[A-Z][A-Za-z]+")  # a capitalised word mid-sentence: a name or brand


def _both(key):
    return CRAFT[key]["ar"] + CRAFT[key]["en"]


def _specific(text, lang):
    """A concrete marker: a digit, a name (Latin-script in Arabic; capitalised mid-sentence in English), or a unit/time/money word."""
    text = strip_markup(text)
    if DIGIT.search(text) or (LATIN_WORD.search(text) if lang == "ar" else NAME_EN.search(text)):
        return True
    return bool(_soft_hits(text, _both("specific_markers")))


def _soft_hits(text, phrases):
    """Like contains_any, but also matches a word carrying the Arabic definite article (السر -> سر)."""
    plain = " ".join(tokens(text))
    unarticled = " ".join(t[2:] if t.startswith("ال") and len(t) >= 4 else t for t in tokens(text))
    return [p for p in phrases if " " + normalize(p) + " " in " " + plain + " "
            or " " + normalize(p) + " " in " " + unarticled + " "]


def _overlap(a, b, lang):
    ta, tb = set(key_terms(a, lang)), set(key_terms(b, lang))
    return len(ta & tb) / len(ta) if len(ta) >= 2 else 0.0


def check_script(r, rep, lang):
    beats = r["beats"]
    rec = (r.get("presets") or {}).get("recommended") or {}
    for b in beats:
        firsts = []
        for o in b["options"]:
            where = f"{b['id']}.{o['id']}"
            recommended = rec.get(b["id"]) == o["id"]
            hits = contains_any(o["text"], _both("cliche_hard"))
            if hits:
                rep.fail("cliche_hard", where, f"AI-tell phrase {hits}. A senior writer never opens or fills with this; say the specific thing instead.")
            soft = _soft_hits(o["text"], _both("cliche_soft"))
            if soft:
                rep.warn("cliche_soft", where, f"Hype word {soft}. Replace with the concrete detail it stands for.")
            for card in o.get("onscreen", []):
                if _overlap(card, o["text"], lang) >= CRAFT["overlay_echo_ratio"]:
                    if recommended:
                        rep.fail("overlay_echo_recommended", where, f"Overlay «{card}» repeats the spoken line of the Recommended script. Make it add something (a number, a label, the payoff).")
                    else:
                        rep.warn("overlay_echo", where, f"Overlay «{card}» repeats the spoken line. Make it add something (a number, a label, the payoff).")
                if b["id"] == "hook" and (o.get("visual") or "").strip() and _overlap(card, o["visual"], lang) >= CRAFT["overlay_echo_ratio"]:
                    rep.warn("overlay_echo_visual", where, f"Overlay «{card}» describes what the first frame already shows. Use it for what the picture can't say.")
            if b["id"] == "hook" and (o.get("visual") or "").strip() and _overlap(o["visual"], o["text"], lang) >= CRAFT["overlay_echo_ratio"]:
                rep.warn("visual_echo", where, "The first frame just illustrates the spoken words. Show the situation or the result the voice can't.")
            if b["id"] == "hook" and recommended and starts_with_any(o["text"], _both("pronoun_openers")):
                rep.warn("hook_bare_pronoun", where, "The hook opens on a bare pronoun; a stranger doesn't know who or what 'it' is yet. Name the subject.")
            t = tokens(o["text"])
            firsts.append(stem(t[0]) if t else "")
        if len(firsts) >= 3 and len(set(firsts)) == 1 and firsts[0]:
            rep.warn("opener_monotony", b["id"], f"Every {b['id']} option starts the same way («{firsts[0]}»). Vary the move, not just the ending.")

    rec_hook = next((o for b in beats if b["id"] == "hook" for o in b["options"] if o["id"] == rec.get("hook")), None)
    if rec_hook and not _specific(" ".join([rec_hook["text"], rec_hook.get("visual") or ""] + list(rec_hook.get("onscreen") or [])), lang):
        rep.warn("hook_specificity", f"hook.{rec_hook['id']}",
                 "The Recommended hook package has no number, name or concrete object. Specific hooks were the only kind a public hook-scorer test could tell apart from weak ones.")

    final = [unslot(ln["text"]) for ln in r["final_script"]["lines"]]
    unquoted = [QUOTED.sub(" ", t) for t in final]
    backed = " ".join(normalize(c["text"]) for c in (r.get("audit") or {}).get("claims") or []
                       if c.get("status") in ("observed", "source_supported") and c.get("action") in ("keep", "keep_with_evidence"))
    claims = sorted({h for t in unquoted for h in contains_any(t, _both("unmeasured_claims")) if normalize(h) not in backed})
    if claims:
        rep.fail("unmeasured_claim", "final_script", f"{claims} claims something nobody measured or filmed yet (speed, 'unedited', exact understanding). "
                 "Let the demo show it, or record the claim in audit.claims as observed/source_supported with its evidence.")
    draft = (r["intake"].get("original_draft") or "").strip()
    if draft:
        rate = BODY_WPM.get(lang, 128)
        d_words, f_words = len(tokens(draft)), sum(len(tokens(t)) for t in final)
        if d_words / rate * 60 >= 0.8 * float(r["meta"]["target_seconds"]) and f_words > d_words * 1.10:
            rep.warn("rewrite_growth", "final_script",
                     f"Your draft already filled its time ({d_words} words) and the rewrite is longer ({f_words}). Merge repeated points instead of adding.")
    lens = [len(tokens(s)) for t in final for s in sentences(t) if tokens(s)]
    if len(lens) >= 4:
        mean = sum(lens) / len(lens)
        cv = (sum((x - mean) ** 2 for x in lens) / len(lens)) ** 0.5 / mean
        if cv < CRAFT["rhythm_min_cv"]:
            rep.warn("rhythm_flat", "final_script", "Every sentence is about the same length, which reads machine-made. Let one line run, cut another to two or three words.")
    by_beat = {ln["beat"]: ln["text"] for ln in r["final_script"]["lines"]}
    if contains_any(by_beat.get("retention", ""), _both("retention_templates")):
        rep.warn("cross_beat_template", "final_script.retention", "Stock retention line. Use an open loop, a stake, or a mid-reveal specific to this Reel.")
    pat_ar = re.compile(CRAFT["contrast_patterns"]["ar"])
    pat_en = re.compile(CRAFT["contrast_patterns"]["en"], re.I)
    contrast = sum(bool(pat_ar.search(" " + normalize(t) + " ") or pat_en.search(t)) for t in final)
    if contrast > 1:
        rep.warn("contrast_cliche", "final_script", f"'Not X, it's Y' used {contrast} times. It's the most recognisable AI rhythm; keep it once at most.")
    questions = sum(t.count("?") + t.count("؟") for t in final)
    # The generic cap; a style that allows more (yapping: 3) raises it. style_questions enforces the style's own limit.
    if questions > max(CRAFT["max_questions"], STYLE_MAX_Q.get(r["intake"].get("style"), 0)):
        rep.warn("rhetorical_overload", "final_script", f"{questions} questions in one script. Answer more, ask less.")
    tricolons = sum(bool(re.search(r"[^،,]+[،,][^،,]+[،,]\s*(?:و|and\s)\S+", t)) for t in final)
    if tricolons > 1:
        rep.warn("tricolon", "final_script", "Lists of three in several beats sound machine-made. Keep one, cut the rest to one or two items.")


def check_publish(r, rep, lang):
    script = " ".join(ln["text"] for ln in r["final_script"]["lines"])
    if _overlap(r["publish"]["caption"], script, lang) >= CRAFT["caption_echo_ratio"]:
        rep.warn("caption_echo", "publish.caption", "The caption repeats the script. Add value instead: the steps written out, a resource, or a question that earns comments.")
