#!/usr/bin/env python3
"""Parse pasted Instagram Insights text (English or Arabic labels) into an intake.performance item.

    python scripts/insights.py insights.txt --label best [--transcript-file t.txt] [--length 28]

--length is the video length in seconds (needed with avg watch time for watch_through).
"""
import argparse, json, re, sys
from pathlib import Path

_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹٫٬٪،", "01234567890123456789.,%,")
_MARKS = re.compile("[‎‏‪-‮⁦-⁩ ​﻿؜]")
_DASHES = re.compile("[‐‑‒–−]")
_HAMZA = str.maketrans("أإآ", "ااا")


def _clean(s):
    return _MARKS.sub(" ", s).strip()


def _norm(s):
    s = _DASHES.sub("-", _clean(s)).lower().translate(_HAMZA)
    return re.sub(r"\s+", " ", s)


# label -> key. "follower_pct"/"nonfollower_pct" are routed by the preceding anchor (views / interactions).
_RAW_LABELS = {
    "views": "views", "مرات الظهور": "views", "المشاهدات": "views",
    "viewers": "viewers", "المشاهدون": "viewers",
    "interactions": "interactions", "التفاعلات": "interactions",
    "likes": "likes", "الإعجابات": "likes",
    "comments": "comments", "التعليقات": "comments",
    "saves": "saves", "مرات الحفظ": "saves", "الحفظ": "saves",
    "shares": "shares", "المشاركات": "shares",
    "accounts engaged": "accounts_engaged", "الحسابات المتفاعلة": "accounts_engaged",
    "profile activity": "profile_activity", "نشاط الملف الشخصي": "profile_activity",
    "follows": "follows", "المتابعات": "follows", "متابعات جديدة": "follows",
    "reels interactions": "ignore", "تفاعلات الريلز": "ignore",  # duplicates Interactions
    "average watch time": "avg_watch_s", "avg watch time": "avg_watch_s",
    "متوسط وقت المشاهدة": "avg_watch_s",  # Arabic labels provisional
    "3-second hold": "hold_3s_pct", "3 second hold": "hold_3s_pct", "hook rate": "hold_3s_pct",
    "نسبة المشاهدة لأول ٣ ثواني": "hold_3s_pct",  # provisional
    "skip rate": "skip_rate_pct",  # Reels Insights (2025): share of views that left within the first 3 seconds
    "معدل التخطي": "skip_rate_pct", "نسبة التخطي": "skip_rate_pct",  # provisional
    "followers": "follower_pct", "المتابعون": "follower_pct",
    "non-followers": "nonfollower_pct", "non followers": "nonfollower_pct", "nonfollowers": "nonfollower_pct",
    "غير المتابعين": "nonfollower_pct",
}
LABELS = {_norm(k): v for k, v in _RAW_LABELS.items()}
PCT_KEYS = ("follower_pct", "nonfollower_pct")
_NUM = re.compile(r"^(%)?\s*([0-9][0-9,]*(?:\.[0-9]+)?)\s*(k|m|%|ألف|الف|مليون)?$", re.I)
_SECS = r"(?:seconds?|secs?|s|ثانية|ثواني|ثوان|ث)"
_TAIL = re.compile(r"^(.*?\D)\s+([0-9٠-٩۰-۹][0-9٠-٩۰-۹,٬.٫،:]*\s*(?:[kKmM%٪]|ألف|الف|مليون|" + _SECS + r")?)$", re.I)
_TIME = re.compile(r"^(?:([0-9]+):([0-9]{1,2})|([0-9]+(?:\.[0-9]+)?)\s*" + _SECS + r"?)$", re.I)


def _number(tok):
    """-> (value, is_pct) or None. Accepts thousands commas, Arabic-Indic digits, K / M suffixes."""
    m = _NUM.match(_clean(tok).translate(_DIGITS))
    if not m:
        return None
    v = float(m.group(2).replace(",", ""))
    suf = (m.group(3) or "").lower()
    if m.group(1):
        suf = "%"  # leading percent sign
    if suf in ("k", "ألف", "الف"):
        v *= 1000
    elif suf in ("m", "مليون"):
        v *= 1000000
    return v, suf == "%"


def _seconds(tok):
    """'16 sec', '16s', '0:16', '1:05', '١٦ ثانية' -> seconds, else None."""
    m = _TIME.match(_clean(tok).translate(_DIGITS))
    if not m:
        return None
    if m.group(1) is not None:
        return int(m.group(1)) * 60 + int(m.group(2))
    v = float(m.group(3))
    return int(v) if v == int(v) else v


def parse_with_warnings(text):
    out, warnings = {}, []
    toks = []
    for raw in text.splitlines():
        line = _clean(raw)
        if not line:
            continue
        m = _TAIL.match(line)  # "Views 6,866" on one line
        if m and _norm(m.group(1)) in LABELS:
            toks += [m.group(1), m.group(2)]
        else:
            toks.append(line)
    seen_pairs = {"views": 0, "interactions": 0}
    anchor, pending, prev = None, None, None
    for line in toks:
        if pending == "avg_watch_s":
            sec = _seconds(line)
            n = None if sec is None else (sec, False)
        else:
            n = _number(line)
        if n is None:
            nl = _norm(line)
            if nl == prev:
                continue  # "Views\nViews" collapses
            prev = nl
            pending = LABELS.get(nl)
            if pending is None:
                warnings.append(f"unparsed line: {line}")
            elif pending in ("views", "interactions"):
                anchor = pending
            continue
        prev = None
        key, pending = pending, None
        if key is None:
            warnings.append(f"number with no label: {line}")
            continue
        val, is_pct = n
        if key in PCT_KEYS:
            scope = anchor
            if scope is None or f"{scope}_{key}" in out:
                scope = next((s for s in ("views", "interactions") if f"{s}_{key}" not in out), None)
            if scope is None:
                warnings.append(f"extra {key} ignored: {line}")
                continue
            out[f"{scope}_{key}"] = round(val, 2)
        elif key == "ignore":
            continue
        elif key == "avg_watch_s":
            out[key] = val
        elif key in ("hold_3s_pct", "skip_rate_pct"):
            if is_pct:
                out[key] = round(val, 2)
            else:
                warnings.append(f"{key} needs a percentage, ignored: {line}")
        elif is_pct:
            warnings.append(f"percentage given for count '{key}' ignored: {line}")
        else:
            out[key] = int(round(val))
    if "views" not in out:
        warnings.append("Views number not found")
    return out, warnings


def parse(text):
    return parse_with_warnings(text)[0]


def to_performance(text, label, transcript="", length_s=None):
    d = parse(text)
    if "views" not in d:
        raise ValueError("no Views number found in the pasted Insights")
    item = {"label": label}
    item.update(d)
    if transcript:
        item["transcript"] = transcript
    if length_s is not None:
        item["length_s"] = length_s
    return item


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("file"); ap.add_argument("--label", required=True, choices=["best", "weak", "other"])
    ap.add_argument("--transcript-file"); ap.add_argument("--length", type=float)
    a = ap.parse_args(argv[1:])
    text = Path(a.file).read_text(encoding="utf-8")
    _, warnings = parse_with_warnings(text)
    for w in warnings:
        print("warning: " + w, file=sys.stderr)
    tr = Path(a.transcript_file).read_text(encoding="utf-8").strip() if a.transcript_file else ""
    try:
        item = to_performance(text, a.label, tr, a.length)
    except ValueError as e:
        print("error: " + str(e), file=sys.stderr); return 1
    print(json.dumps(item, ensure_ascii=False, indent=2)); return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv))
