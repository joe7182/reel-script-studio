#!/usr/bin/env python3
"""Voice fingerprint: how this creator actually talks, measured from real transcripts.

    python scripts/voice_fingerprint.py measure --lang ar transcript1.txt [more.txt]
    python scripts/voice_fingerprint.py into rss_work/<slug>/result.json
"""
import json, re, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from textkit import tokens, normalize, sentences, stem, AR_MARKS, STOPWORDS  # noqa: E402

MIN_WORDS = 40
CONNECTORS = {
    "ar": ["يعني", "بس", "لهذا", "بعدين", "هسه", "لان", "مثلا", "حتى", "اصلا", "طبعا", "والله", "بصراحه", "شوف", "المهم", "لكن", "الحين", "دلوقتي", "عشان", "هلق", "خلاص"],
    "en": ["so", "but", "because", "like", "actually", "honestly", "basically", "then", "anyway", "right", "okay", "literally"],
}
LATIN = re.compile(r"[a-z]")
CONN_PREFIXES = ("و", "ف", "ب", "ل")
MSA_MARKERS = ["سأ", "سوف", "حيث", "أصبح", "يعتمد", "العديد", "جميع أنحاء", "الذي", "التي"]
DIALECT_MARKERS = json.loads((HERE / "dialects.json").read_text(encoding="utf-8"))["dialects"]


def _toks(text):
    """textkit tokens minus the sentence-final '.', quotes and hyphens they keep."""
    return [t for t in (x.strip(".'’-") for x in tokens(text)) if t]


def _is_english(t):
    return len(LATIN.findall(t)) >= 2 and not re.search(r"\d", t)


def _conn(t, conn_set):
    """The connector this token is, allowing one attached prefix («وبس»); else None."""
    if t in conn_set:
        return t
    if t[:1] in CONN_PREFIXES and t[1:] in conn_set:
        return t[1:]
    return None


def _quantile(sorted_vals, q):
    if not sorted_vals:
        return 0
    i = min(len(sorted_vals) - 1, max(0, int(round(q * (len(sorted_vals) - 1)))))
    return sorted_vals[i]


def measure(texts, lang):
    texts = [t for t in texts if t and str(t).strip()]
    toks = [t for x in texts for t in _toks(x)]
    n = len(toks)
    if n < MIN_WORDS:
        return {"status": "insufficient", "sample_words": n}
    sents = [s for x in texts for s in sentences(x)]
    lens = sorted(len(_toks(s)) for s in sents) or [n]
    qs = sum(str(x).count("?") + str(x).count("؟") for x in texts)
    conn_set = {normalize(c) for c in CONNECTORS.get(lang, CONNECTORS["en"])}
    conn = Counter(c for c in (_conn(t, conn_set) for t in toks) if c)
    stops = {normalize(w) for w in STOPWORDS["ar" if lang == "ar" else "en"]}
    grams = Counter()
    for s in sents:
        st = _toks(s)
        for k in (2, 3):
            for i in range(len(st) - k + 1):
                g = st[i:i + k]
                if not all(w in stops for w in g):
                    grams[" ".join(g)] += 1
    openers = Counter(_toks(s)[0] for s in sents if _toks(s))
    return {
        "status": "ok", "sample_words": n,
        "sentence_mean": round(sum(lens) / len(lens), 1),
        "sentence_p25": _quantile(lens, 0.25), "sentence_p75": _quantile(lens, 0.75),
        "question_rate": round(qs / max(1, len(sents)), 2),
        "connectors": [[w, c] for w, c in conn.most_common(5)],
        "signature_phrases": [[g, c] for g, c in grams.most_common(5) if c >= 2],
        "code_switch": round(sum(1 for t in toks if _is_english(t)) / n, 2),
        "openers": [[w, c] for w, c in openers.most_common(3) if c >= 2],
    }


def drift(fp, texts, lang):
    if not fp or fp.get("status") != "ok":
        return []
    msgs = []
    sents = [s for x in texts for s in sentences(x)]
    lens = [len(_toks(s)) for s in sents]
    if lens and (len(lens) >= 3 or sum(lens) >= 15):
        mean = sum(lens) / len(lens)
        lo, hi = 0.7 * fp["sentence_p25"], 1.4 * fp["sentence_p75"]
        if not (lo <= mean <= hi):
            msgs.append(f"Average sentence is {mean:.1f} words; this creator speaks in {fp['sentence_p25']}–{fp['sentence_p75']}-word sentences.")
    toks = [t for x in texts for t in _toks(x)]
    if toks:
        cs = sum(1 for t in toks if _is_english(t)) / len(toks)
        if abs(cs - fp["code_switch"]) > 0.15:
            msgs.append(f"English mixing is {cs:.0%} here vs {fp['code_switch']:.0%} in their real speech.")
        top = [w for w, _ in fp.get("connectors", [])[:3]]
        if top:
            top_set = set(top)
            if not any(_conn(t, top_set) for t in toks):
                msgs.append(f"None of the creator's usual connectors ({', '.join(top)}) appear; the script won't sound like them.")
    return msgs


def _marker_hits(text, markers):
    """How many distinct markers from the list appear (token or stem match, or phrase)."""
    toks = _toks(text)
    flat = " ".join(toks)
    stems = {stem(t) for t in toks} | set(toks)
    hits = 0
    for m in markers:
        nm = normalize(m)
        if " " in nm:
            hits += nm in flat
        else:
            hits += nm in stems or stem(nm) in stems
    return hits


def is_formal(text, dialect, best_text=""):
    """True when a transcript is formal writing, not the creator's speaking voice:
    >= 2 MSA markers, or no markers of the creator's dialect while the best sample has >= 2."""
    raw = AR_MARKS.sub("", str(text))
    msa = _marker_hits(text, [m for m in MSA_MARKERS if m != "سأ"])
    msa += bool(re.search(r"(?<![\w])سأ\w", raw))  # future «سأتحدث»; hamza kept so Iraqi «ساعدك» is not hit
    if msa >= 2:
        return True
    markers = DIALECT_MARKERS.get(dialect, {}).get("markers", [])
    return bool(markers) and _marker_hits(best_text, markers) >= 2 and _marker_hits(text, markers) == 0


def _into(path):
    r = json.loads(Path(path).read_text(encoding="utf-8"))
    i = r["intake"]
    dialect = r["meta"].get("dialect", "")
    perf = i.get("performance", [])
    # (name, text). Best/other/voice always count. A weak post counts too unless its register is formal:
    # a formal transcript is not how the creator really talks.
    used = [("voice_sample", i.get("voice_sample", ""))]
    used += [(p.get("label", "other"), p.get("transcript", "")) for p in perf if p.get("label", "other") in ("best", "other")]
    best_text = " ".join(t for _, t in used)
    skipped = []
    for p in perf:
        if p.get("label") == "weak" and (p.get("transcript") or "").strip():
            if is_formal(p["transcript"], dialect, best_text):
                skipped.append("weak (formal register)")
            else:
                used.append(("weak", p["transcript"]))
    used = [(n, t) for n, t in used if t and t.strip()]
    new = measure([t for _, t in used], r["meta"]["language"])
    old = i.get("voice_fingerprint")
    if old and old.get("status") == "ok" and new.get("status") != "ok":
        print("Kept the existing voice fingerprint (not enough new transcript text to re-measure).")
        return
    i["voice_fingerprint"] = new
    Path(path).write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Transcripts used: " + ", ".join(n for n, _ in used) + ("; skipped: " + ", ".join(skipped) if skipped else ""))
    print(json.dumps(i["voice_fingerprint"], ensure_ascii=False))


def main(argv):
    if len(argv) >= 3 and argv[1] == "into":
        _into(argv[2]); return 0
    if len(argv) >= 4 and argv[1] == "measure" and "--lang" in argv:
        lang = argv[argv.index("--lang") + 1]
        files = [a for a in argv[2:] if a not in ("--lang", lang)]
        print(json.dumps(measure([Path(f).read_text(encoding="utf-8") for f in files], lang), ensure_ascii=False, indent=2)); return 0
    print(__doc__); return 2


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv))
