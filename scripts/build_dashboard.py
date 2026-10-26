#!/usr/bin/env python3
"""Build the Reel Script Studio dashboard from result.json.

    python scripts/build_dashboard.py rss_work/<slug>/result.json --out <dir>

Runs the validator first and refuses to build while any hard check fails,
so a broken script never reaches the creator. Standard library only.
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import validate as V  # noqa: E402
import research_checks  # noqa: E402

VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip() if (ROOT / "VERSION").exists() else "dev"
TEMPLATE = ROOT / "assets" / "dashboard-template.html"
PLACEHOLDER = "/*__RSS_DATA__*/"
CREDIT = "Built by @yousif_aljbouri — free tool, share it."
FEEDBACK_URL = "https://www.instagram.com/yousif_aljbouri/"
STYLE_FIELDS = ("label_ar", "label_en", "mean_ar", "mean_en", "energy", "pace_factor", "sentence_words")
UNUSED = ("final_script",)  # result fields the dashboard never reads; left out to keep it under the size cap


def styles_meta(style):
    """The creator's style as the dashboard shows it (label, meaning, energy, pace, sentence length)."""
    raw = json.loads((HERE / "styles.json").read_text(encoding="utf-8"))
    return {k: {f: v[f] for f in STYLE_FIELDS if f in v} for k, v in raw.items() if k == style}


def embedded(data):
    """result.json minus what the page never reads: raw post inputs (incl. transcripts) and final_script."""
    d = {k: v for k, v in data.items() if k not in UNUSED}
    d["intake"] = {k: v for k, v in data["intake"].items() if k != "performance"}
    return d


def minify(template):
    """Drop /* ... */ comments and leading indentation; lines stay separate, the data placeholder stays."""
    head, sep, tail = template.partition(PLACEHOLDER)

    def squeeze(s):
        s = re.sub(r"/\*(?!__RSS_DATA__)[\s\S]*?\*/", "", s)
        return "\n".join(line.strip() for line in s.splitlines() if line.strip())
    return squeeze(head) + sep + squeeze(tail)


def safe_json(obj):
    """Valid JSON that cannot close or comment out the <script> it lives in: every "<" becomes \\u003c."""
    s = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    return s.replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def build(result_path, out_dir):
    result_path = Path(result_path)
    data = json.loads(result_path.read_text(encoding="utf-8"))
    report = V.validate(data)
    result_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    if not report["passed"]:
        print("Build refused: hard validation failures. Fix them in Stage 3, then build again.")
        for item in report["hard"]:
            print(f"  HARD [{item['check']}] {item['where']}: {item['message']}")
        return None

    template = minify(TEMPLATE.read_text(encoding="utf-8"))
    if template.count(PLACEHOLDER) != 1:
        raise SystemExit("Template is missing its data placeholder.")
    payload = {
        "result": embedded(data),
        "elevenlabs_rules": V.EL_RULES,
        "styles": styles_meta(data["intake"].get("style")),
        "craft_rules": research_checks.RULES,
        "config": {"version": VERSION, "credit": CREDIT, "feedback_url": FEEDBACK_URL},
    }
    html = template.replace(PLACEHOLDER, safe_json(payload))
    slug = "".join(c if c.isalnum() or c == "-" else "-" for c in (data["meta"].get("slug") or "reel").lower()).strip("-") or "reel"
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{slug}-dashboard.html"
    out.write_text(html, encoding="utf-8")
    print(f"Built {out} ({len(html.encode('utf-8')) // 1024} KB). {len(report['soft'])} warnings are shown in the Council tab.")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("result")
    ap.add_argument("--out", default=".")
    args = ap.parse_args()
    return 0 if build(args.result, args.out) else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
