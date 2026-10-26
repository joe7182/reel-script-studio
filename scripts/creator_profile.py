#!/usr/bin/env python3
"""Build or check a creator profile (the onboarding interview's output).

    python scripts/creator_profile.py from-result rss_work/<slug>/result.json --out rss_work/creator-profile.json
    ... from-result ... --keep-default rss_work/creator-profile.json   (keep the saved default style; intake.style was one-off)
    python scripts/creator_profile.py check creator-profile.json
    python scripts/creator_profile.py migrate old-profile.json --out creator-profile.json   (v2 -> v3)
"""
import datetime, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from validate import schema_errors  # noqa: E402

SCHEMA = json.loads((HERE.parent / "schemas" / "profile.schema.json").read_text(encoding="utf-8"))
STYLE_MAP = {"calm_expert": "professional", "energetic": "hype", "story": "yapping", "teacher": "infotainment", "light_humor": "deadpan"}


def build_profile(r, keep_default=None):
    """keep_default: an existing profile whose default_style stays the default (intake.style is a one-off);
    the legacy `style` field then mirrors that default. With no new post numbers or voice sample in the result,
    the kept profile's performance_baseline and voice_fingerprint carry over."""
    i, m = r["intake"], r["meta"]
    kept = keep_default or {}
    default = kept.get("default_style") or kept.get("style") or i.get("default_style") or i["style"]
    keep = bool(keep_default) or bool(i.get("default_style"))
    texture = [o["text"] for b in r["beats"] for o in b["options"] if o.get("human_texture")]
    return {
        "rss_creator_profile": 3,
        "saved": datetime.date.today().isoformat(),
        "language": m["language"], "dialect": m["dialect"], "register": m["register"],
        "platform": m["platform"], "style": default if keep else i["style"], "default_style": default,
        "content_category": i.get("content_category", "other"),
        "niche": i.get("niche", ""), "audience": i.get("audience", ""),
        "voice_sample": i.get("voice_sample", ""), "best_script": i.get("best_script"),
        "recording": i["recording"], "pacing": m.get("pacing"),
        "human_texture": list(dict.fromkeys(i.get("human_texture", []) + texture)),
        "voice_fingerprint": i.get("voice_fingerprint") or kept.get("voice_fingerprint"),
        "performance_baseline": r.get("performance_analysis") or kept.get("performance_baseline"),
    }


def migrate_profile(p):
    """v2 -> v3: map the old style names, add the new fields empty."""
    q = dict(p)
    style = STYLE_MAP.get(q.get("style"), q.get("style") or "professional")
    q.update({"rss_creator_profile": 3, "style": style, "default_style": style,
              "content_category": q.get("content_category", "other"),
              "voice_fingerprint": q.get("voice_fingerprint"), "performance_baseline": q.get("performance_baseline")})
    return q


def check_profile(p):
    return schema_errors(p, SCHEMA)


def _out(argv, default):
    """The --out value, the default when --out is absent, or None when --out has no value."""
    if "--out" not in argv:
        return default
    i = argv.index("--out") + 1
    return argv[i] if i < len(argv) and not argv[i].startswith("--") else None


def _save(p, out):
    errs = check_profile(p)
    if errs:
        print("\n".join(errs)); return 1
    Path(out).write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved {out}"); return 0


def main(argv):
    if len(argv) >= 3 and argv[1] in ("from-result", "migrate"):
        out = _out(argv, "creator-profile.json")
        if out is None:
            print(f"usage: creator_profile.py {argv[1]} <in.json> --out <profile.json>"); return 2
        src = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
        if argv[1] == "migrate":
            return _save(migrate_profile(src), out)
        keep = None
        if "--keep-default" in argv:
            k = argv.index("--keep-default") + 1
            if k >= len(argv) or argv[k].startswith("--"):
                print("usage: creator_profile.py from-result <result.json> --out <profile.json> [--keep-default <existing-profile.json>]"); return 2
            try:
                keep = json.loads(Path(argv[k]).read_text(encoding="utf-8"))
                if not isinstance(keep, dict):
                    raise ValueError("not a profile object")
            except (OSError, ValueError) as e:
                print(f"Note: --keep-default {argv[k]} could not be read ({type(e).__name__}); using intake.style as the default.")
                keep = None
        return _save(build_profile(src, keep), out)
    if len(argv) >= 3 and argv[1] == "check":
        p = json.loads(Path(argv[2]).read_text(encoding="utf-8"))
        if isinstance(p, dict) and p.get("rss_creator_profile") == 2:
            print("v2 profile: run `creator_profile.py migrate`"); return 1
        errs = check_profile(p)
        print("OK" if not errs else "\n".join(errs)); return 0 if not errs else 1
    print(__doc__); return 2

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv))
