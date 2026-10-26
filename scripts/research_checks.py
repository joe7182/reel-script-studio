"""Research, evidence basis and claim-status checks (rss-2.2).

Every recommendation carries a `basis` that a reader can check: an opened source, the creator's own
numbers or words, or a named craft rule. These checks verify that each reference resolves. They cannot
prove a page was really read; the dashboard says so.
"""
import json
import re
from pathlib import Path
from urllib.parse import urlparse

from textkit import tokens

CRAFT = json.loads((Path(__file__).resolve().parent / "craft.json").read_text(encoding="utf-8"))
RULES = CRAFT["rules"]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
APOS = str.maketrans({"’": "'", "‘": "'"})
FIRST_PERSON = {"انا", "أنا", "اني", "آني", "عندي", "جربت", "جربتها", "سويت", "كنت", "i", "i'm", "i've", "my", "me", "we", "our"}


def _sources(r):
    return {s["id"]: s for s in (r.get("research") or {}).get("sources") or []}


def _metrics(r):
    """Metric names the creator's performance analysis actually holds a value for."""
    pa = r.get("performance_analysis") or {}
    names = {c.get("metric") for c in pa.get("contrast") or []}
    for p in pa.get("posts") or []:
        names |= {k for k, v in (p.get("rates") or {}).items() if v is not None}
        names |= {k for k, v in p.items() if isinstance(v, (int, float)) and not isinstance(v, bool)}
    return {n for n in names if n}


def valid_basis(r, basis):
    """None when `basis` resolves to real evidence in this result, else a one-line reason."""
    if not isinstance(basis, dict) or not basis.get("type"):
        return "no basis given"
    kind, ref = basis.get("type"), (basis.get("ref") or "").strip()
    if not ref:
        return f"{kind} basis has an empty ref"
    if kind == "research":
        s = _sources(r).get(ref)
        if not s:
            return f"research source '{ref}' does not exist in research.sources"
        if s.get("retrieval") != "opened":
            return f"research source '{ref}' was not opened (snippet only), so it can't be evidence"
        return None
    if kind == "creator_data":
        scope, _, name = ref.partition(":")
        if scope == "performance":
            return None if name in _metrics(r) else f"'{name}' is not in performance_analysis"
        if scope == "fingerprint":
            fp = (r.get("intake") or {}).get("voice_fingerprint") or {}
            if fp.get("status") != "ok":
                return "no usable voice fingerprint"
            return None if name in fp and name != "status" else f"'{name}' is not a fingerprint measurement"
        if scope == "intake":
            val = (r.get("intake") or {}).get(name)
            return None if val not in (None, "", [], {}) else f"intake.{name} is empty"
        return "creator_data ref must start with performance:, fingerprint: or intake:"
    if kind == "craft_rule":
        return None if ref in RULES else f"'{ref}' is not a rule in scripts/craft.json"
    if kind == "creator_said":
        return None
    return f"unknown basis type '{kind}'"


def require_basis(r, rep, where, basis):
    if basis is None:
        rep.fail("basis_missing", where, "No basis. Name the evidence: an opened source, your own numbers or words, or a craft rule.")
        return
    msg = valid_basis(r, basis)
    if msg:
        rep.fail("basis_invalid", where, f"Basis doesn't resolve: {msg}.")


def check(r, rep):
    research = r.get("research") or {}
    sources = research.get("sources") or []
    by_id = {}
    for i, s in enumerate(sources):
        where = f"research.sources[{i}]"
        if s["id"] in by_id:
            rep.fail("source_id", where, f"Source id '{s['id']}' is used twice.")
        by_id[s["id"]] = s
        u = urlparse(s.get("url") or "")
        if u.scheme not in ("http", "https") or not u.netloc:
            rep.fail("source_url", where, f"Source URL must be http(s) with a host: «{s.get('url')}».")
        if not DATE_RE.match(s.get("accessed") or ""):
            rep.warn("source_date", where, "accessed should be a date like 2026-10-13.")
        if not [x for x in s.get("used_for") or [] if x.strip()]:
            rep.warn("research_unused", where, f"«{s.get('title')}» changed no decision. Research for appearance; drop it or say what it changed.")
    opened = {k: s for k, s in by_id.items() if s.get("retrieval") == "opened"}
    status = research.get("status")
    if status == "completed":
        if not research.get("questions") or len(opened) < 2 or not any(s["kind"] == "angle" for s in opened.values()):
            rep.fail("research_incomplete", "research", "Completed research needs the decision questions, at least 2 opened sources and at least 1 opened angle source.")
        aa = (r.get("idea") or {}).get("avoided_angle")
        if not aa:
            rep.fail("avoided_angle", "idea.avoided_angle", "Name the common angle this Reel avoids, citing an opened angle source.")
        elif opened.get(aa.get("source"), {}).get("kind") != "angle":
            rep.fail("avoided_angle", "idea.avoided_angle", f"avoided_angle must cite an opened 'angle' source; '{aa.get('source')}' isn't one.")
    else:
        if not (research.get("limitations") or "").strip():
            rep.fail("research_limits", "research.limitations", f"Research is '{status}': say what wasn't checked, so advice isn't mistaken for researched.")
        if status in ("unavailable", "declined") and opened:
            rep.fail("research_status", "research.status", f"Research is '{status}' but sources are marked opened. Set the real status (completed or partial), or remove the sources.")
        aa = (r.get("idea") or {}).get("avoided_angle")
        if aa and opened.get(aa.get("source"), {}).get("kind") != "angle":
            rep.fail("avoided_angle", "idea.avoided_angle", f"avoided_angle must cite an opened 'angle' source; '{aa.get('source')}' isn't one.")

    for i, f in enumerate((r.get("audit") or {}).get("findings") or []):
        require_basis(r, rep, f"audit.findings[{i}]", f.get("basis"))

    final_lines = [ln["text"] for ln in (r.get("final_script") or {}).get("lines") or []]
    for i, c in enumerate((r.get("audit") or {}).get("claims") or []):
        where = f"audit.claims[{i}]"
        st, kept = c.get("status"), c.get("action") in ("keep", "keep_with_evidence")
        ids = c.get("sources") or []
        for sid in ids:
            if sid not in by_id:
                rep.fail("claim_evidence", where, f"«{c['text']}» cites source '{sid}', which isn't in research.sources.")
        if st == "source_supported" and (not ids or any(by_id.get(x, {}).get("retrieval") != "opened" for x in ids)):
            rep.fail("claim_evidence", where, f"«{c['text']}» is source_supported but cites no opened source.")
        if st == "unsupported" and kept:
            rep.fail("claim_unsupported", where, f"«{c['text']}» is unsupported, so it can't be kept. Remove it or rewrite it as something you can show.")
        if c["type"] == "factual" and c["action"] == "keep_with_evidence" and st not in ("source_supported", "observed"):
            rep.fail("claim_evidence", where, f"Factual claim «{c['text']}» needs an opened source (source_supported) or to be shown on screen (observed).")
        if st == "creator_attested" and c["action"] == "keep_with_evidence":
            line = next((t for t in final_lines if " ".join(tokens(c["text"])) in " ".join(tokens(t))), None)
            if line is not None and not FIRST_PERSON & {t.translate(APOS).strip(".,!?؟،") for t in tokens(line)}:
                rep.warn("attested_not_first_person", where, f"«{c['text']}» rests on your word only; say it as your experience («جربتها أنا…», \"I tried…\").")
