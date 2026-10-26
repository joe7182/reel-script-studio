"""Viewer Mind and concept-card checks (rss-2.2).

The Viewer Mind simulates three specific viewers (target, stranger, skeptic) second by second through
the first 3 seconds of each hook candidate. It is a simulation from research and the creator's data,
not a prediction. These checks keep it honest: what a viewer "heard" must be the real words at the real
pace, what they "see" at second 0 must be the planned first frame, every verdict needs evidence, and the
chosen hook must be the one the simulation actually favours.
"""
import re

from research_checks import CRAFT, require_basis
from textkit import PAUSE_RE, contains_any, key_terms, strip_markup, tokens, unslot

PERSONAS = ("target", "stranger", "skeptic")
SECONDS = [0, 1, 2, 3]
HOLDING = ("hooked", "curious")
PUNCT = ".,!?؟،؛;:…\"'«»()[]{}-—–"
PERCENT = re.compile(r"[%٪]|\bper ?cent\b|بالمي[هة]|بالمئ[هة]|في المي[هة]", re.I)
MIN_WHO_WORDS = 4
MAX_LOGLINE_WORDS = 35


def spoken_tokens(text):
    """Words as spoken: no ElevenLabs markup, pause marks, slots braces or punctuation."""
    clean = PAUSE_RE.sub(" ", strip_markup(unslot(text or "")))
    return [w for w in (t.strip(PUNCT) for t in tokens(clean)) if w]


def max_words(wpm, second):
    """How many words a viewer can have heard by `second` at `wpm`, with a two-word allowance."""
    return int(wpm / 60 * second) + 2


def _contiguous(needle, hay):
    n = len(needle)
    return n > 0 and any(hay[i:i + n] == needle for i in range(len(hay) - n + 1))


def _norm(text):
    return " ".join(spoken_tokens(text))


def _lexicon(key):
    return CRAFT[key]["ar"] + CRAFT[key]["en"]


def _check_personas(vm, rep):
    personas = vm["personas"]
    if sorted(p["id"] for p in personas) != sorted(PERSONAS):
        rep.fail("viewer_personas", "viewer_mind.personas", f"Simulate exactly these three viewers: {list(PERSONAS)}.")
    seen = set()
    for p in personas:
        where = f"viewer_mind.personas.{p['id']}"
        for field in ("who", "context", "want"):
            if not (p.get(field) or "").strip():
                rep.fail("viewer_persona_generic", where, f"{field} is empty. A simulated viewer needs a real situation.")
        who = _norm(p.get("who"))
        generic = contains_any(p.get("who") or "", _lexicon("generic_persona"))
        if len(who.split()) < MIN_WHO_WORDS or generic:
            rep.fail("viewer_persona_generic", where,
                     f"«{p.get('who')}» is too generic. Name who they are, where they live or work, and what they already know.")
        if who in seen:
            rep.fail("viewer_persona_generic", where, "Two personas have the same description; each one must be a different viewer.")
        seen.add(who)


def _check_candidate(r, c, rep, hook_opts, draft_tokens, wpm, text_only):
    where = f"viewer_mind.candidates.{c['ref']}"
    spoken = spoken_tokens(c["text"])
    if c["ref"] == "original":
        if not draft_tokens:
            rep.fail("viewer_candidate", where, "There is no original draft, so there is no 'original' candidate.")
        elif not _contiguous(spoken, draft_tokens):
            rep.fail("viewer_candidate", where, "The original candidate must be the creator's real opening, word for word from intake.original_draft.")
    else:
        o = hook_opts.get(c["ref"])
        if o is None:
            rep.fail("viewer_candidate", where, f"'{c['ref']}' is not a hook option.")
        elif (spoken != spoken_tokens(o["text"]) or (c.get("visual") or "").strip() != (o.get("visual") or "").strip()
              or [s.strip() for s in c.get("onscreen") or []] != [s.strip() for s in o.get("onscreen") or []]):
            rep.fail("viewer_candidate", where, f"The candidate must copy hook option {c['ref']} exactly (text, visual, onscreen).")

    if sorted(x["persona"] for x in c["runs"]) != sorted(PERSONAS):
        rep.fail("viewer_runs", where, f"Each candidate needs one run per persona: {list(PERSONAS)}.")
    frame_terms = set(key_terms(" ".join([c.get("visual") or ""] + list(c.get("onscreen") or [])), r["meta"]["language"]))
    thinks_at = {}
    for x in c["runs"]:
        rw = f"{where}.{x['persona']}"
        ms = x["moments"]
        if [m["second"] for m in ms] != SECONDS:
            rep.fail("viewer_moments", rw, "Moments must be seconds 0, 1, 2, 3 in order.")
            continue
        thinks = [_norm(m["thinks"]) for m in ms]
        if not all(thinks) or len(set(thinks)) != len(thinks):
            rep.fail("viewer_moments", rw, "Every second needs its own thought; the viewer's mind moves.")
        for m, t in zip(ms, thinks):
            if t and t in thinks_at.setdefault(m["second"], set()):
                rep.fail("viewer_moments", rw, f"Second {m['second']}: two personas think the identical thing. Different viewers react differently.")
            thinks_at[m["second"]].add(t)
        prev = 0
        for m in ms:
            heard = spoken_tokens(m["heard_so_far"])
            if text_only:
                if heard:
                    rep.fail("viewer_heard", rw, "A text-only Reel has no voice: heard_so_far must be empty.")
                continue
            if heard != spoken[:len(heard)]:
                rep.fail("viewer_heard", rw, f"Second {m['second']}: heard_so_far must be the first words of the hook, exactly as spoken.")
            elif len(heard) > max_words(wpm, m["second"]):
                rep.fail("viewer_heard", rw, f"Second {m['second']}: {len(heard)} words can't be heard yet at {wpm} wpm (max {max_words(wpm, m['second'])}).")
            elif len(heard) < prev:
                rep.fail("viewer_heard", rw, f"Second {m['second']}: the viewer can't un-hear words; heard_so_far only grows.")
            prev = max(prev, len(heard))
        if not text_only and spoken:
            cut = 3 if x["verdict"] == "stays" else x["decided_at"]
            least = min(len(spoken), max(0, int(wpm / 60 * cut) - 3))
            if len(spoken_tokens(ms[cut]["heard_so_far"])) < least:
                rep.fail("viewer_heard", rw, f"By second {cut} the viewer has heard at least {least} words at {wpm} wpm; heard_so_far is too short.")
        if frame_terms and not frame_terms & set(key_terms(ms[0]["sees"], r["meta"]["language"])):
            rep.fail("viewer_first_frame", rw, "At second 0 the viewer sees the planned first frame: describe the candidate's visual or on-screen text.")
        if not (x.get("reason") or "").strip():
            rep.fail("viewer_verdict", rw, "Say why the viewer stays or swipes.")
        if x["verdict"] == "swipes" and ms[x["decided_at"]]["state"] != "leaving":
            rep.fail("viewer_verdict", rw, f"Swipes at second {x['decided_at']}, but the state there isn't 'leaving'.")
        if x["verdict"] == "stays" and ms[3]["state"] not in HOLDING:
            rep.fail("viewer_verdict", rw, "Stays, but at second 3 the viewer isn't hooked or curious.")
        require_basis(r, rep, rw, x.get("basis"))
        for m in ms:
            if PERCENT.search(m["thinks"]):
                rep.fail("viewer_prediction", rw, "No percentages in a viewer's thoughts: this is a simulation, not a forecast.")
        if PERCENT.search(x.get("reason") or "") and (x.get("basis") or {}).get("type") != "creator_data":
            rep.fail("viewer_prediction", rw, "A percentage in a reason must come from the creator's own numbers (creator_data basis).")


def _stays(c, personas=PERSONAS):
    return sum(1 for x in c["runs"] if x["persona"] in personas and x["verdict"] == "stays")


def _check_choice(r, vm, cands, rep):
    chosen = cands.get(vm["chosen"])
    if chosen is None:
        rep.fail("viewer_choice", "viewer_mind.chosen", f"'{vm['chosen']}' is not one of the simulated candidates.")
        return
    rec_id = (r.get("presets") or {}).get("recommended", {}).get("hook")
    rec = next((o for o in r["beats"][0]["options"] if o["id"] == rec_id), None)
    if rec is None or spoken_tokens(rec["text"]) != spoken_tokens(chosen["text"]):
        rep.fail("viewer_choice", "viewer_mind.chosen", "The Recommended hook must be the chosen candidate's text.")
    if _stays(chosen, ("target", "stranger")) < 2:
        if (vm.get("unresolved") or "").strip():
            rep.warn("viewer_unresolved", "viewer_mind.unresolved", f"No candidate holds both the target viewer and the stranger: {vm['unresolved']}")
        else:
            rep.fail("viewer_choice", "viewer_mind.chosen",
                     "The chosen hook loses the target viewer or the stranger. Rewrite the hook (up to 2 rounds), or say why in viewer_mind.unresolved.")
    best = max(_stays(c) for c in cands.values())
    if _stays(chosen) < best:
        rep.fail("viewer_choice", "viewer_mind.chosen", "Another candidate held more viewers in the simulation. Choose it, or fix the simulation.")


def _check_concept(r, rep, has_draft):
    c = r["concept"]
    order = [b["id"] for b in r["beats"]]
    beat = c["payoff_beat"]
    if beat in ("hook", "cta") or order.index(beat) >= order.index("cta"):
        rep.fail("concept_payoff", "concept.payoff_beat", "The hook's promise is paid in the body, before the CTA.")
    line = next((ln["text"] for ln in r["final_script"]["lines"] if ln["beat"] == beat), "")
    if not _contiguous(spoken_tokens(c["payoff_line"]), spoken_tokens(line)):
        rep.fail("concept_payoff", "concept.payoff_line", f"«{c['payoff_line']}» isn't in the final script's {beat} line.")
    if has_draft and not c.get("details"):
        rep.fail("concept_details", "concept.details", "A rewrite must say where each important detail of the draft went (speech, visual, caption or cut).")
    if len(spoken_tokens(c["logline"])) > MAX_LOGLINE_WORDS:
        rep.warn("concept_logline", "concept.logline", f"The logline should be one sentence (max {MAX_LOGLINE_WORDS} words).")


def check(r, rep, pacing, text_only):
    vm = r["viewer_mind"]
    draft = (r["intake"].get("original_draft") or "").strip()
    _check_personas(vm, rep)
    hook_opts = {o["id"]: o for o in r["beats"][0]["options"]}
    cands = {}
    for c in vm["candidates"]:
        if c["ref"] in cands:
            rep.fail("viewer_candidate", f"viewer_mind.candidates.{c['ref']}", f"'{c['ref']}' is simulated twice.")
        cands[c["ref"]] = c
        _check_candidate(r, c, rep, hook_opts, spoken_tokens(draft), pacing["hook"], text_only)
    if draft and "original" not in cands:
        rep.fail("viewer_original_missing", "viewer_mind.candidates",
                 "The creator gave a draft: simulate its real opening as the 'original' candidate (the Before).")
    _check_choice(r, vm, cands, rep)
    _check_concept(r, rep, bool(draft))
    texts = [r["concept"]["logline"], r["concept"]["promise"], r["concept"]["turn"], r["concept"]["payoff_line"], r["idea"].get("direction") or "", r["idea"].get("honest_take") or "", vm.get("unresolved") or ""]
    texts += [p.get(f) or "" for p in vm["personas"] for f in ("who", "context", "want", "swipe_trigger")]
    texts += [x["reason"] for c in vm["candidates"] for x in c["runs"]]
    texts += [m[f] for c in vm["candidates"] for x in c["runs"] for m in x["moments"] for f in ("thinks", "sees")]
    hits = sorted({h for t in texts for h in contains_any(t, _lexicon("prediction_words"))})
    if hits:
        rep.fail("viewer_prediction", "viewer_mind", f"Prediction language {hits}. The skill never forecasts views or virality.")
