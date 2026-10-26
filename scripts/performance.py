#!/usr/bin/env python3
"""What the creator's own numbers say. Signals, not proof; no benchmarks, no predictions.

    python scripts/performance.py rss_work/<slug>/result.json
"""
import hashlib, json, math, sys
from pathlib import Path

NOTE = "1–2 posts are signals, not proof."
RATES = ["likes", "comments", "shares", "saves"]
ZERO_METRICS = ["shares_per_1k", "saves_per_1k", "follows_per_1k", "comments_per_1k"]
ZERO_NOTE = "only the best post has this"
LOWER_IS_BETTER = {"skip_rate_pct"}  # fewer viewers leaving in the first 3 seconds
CTA_NOTE_MAYBE = ("Comments may include keyword replies to your CTA; they would show response to the offer, "
                  "not that the content was engaging.")
CTA_NOTE = ("Comments include keyword replies to your CTA; they show response to the offer, "
            "not that the content was engaging.")


def input_hash(perf):
    return hashlib.sha256(json.dumps(perf, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:16]


def _per_1k(n, views):
    return None if not views or n is None else round(n / views * 1000, 1)


def _post(p):
    views = p.get("views") or 0
    rates = {f"{k}_per_1k": _per_1k(p.get(k), views) for k in RATES}
    reach = round(views / p["followers"], 2) if p.get("followers") else None
    wt = round(p["avg_watch_s"] / p["length_s"], 2) if p.get("avg_watch_s") is not None and p.get("length_s") else None
    flags, flag_notes = [], {}
    if p.get("hold_3s_pct") is not None and p["hold_3s_pct"] < 60:
        flags.append("hook_lost_viewers")
    if wt is not None and wt < 0.4:
        flags.append("middle_lost_viewers")
    cpk = rates["comments_per_1k"]
    if (p.get("comments") or 0) >= 10 and (p.get("cta_keyword") or (cpk is not None and cpk >= 30)):
        flags.append("comments_cta_driven")
        flag_notes["comments_cta_driven"] = CTA_NOTE if p.get("cta_keyword") else CTA_NOTE_MAYBE
    out = {"label": p.get("label", "other"), "rates": rates, "reach_ratio": reach, "watch_through": wt,
           "hold_3s_pct": p.get("hold_3s_pct"), "skip_rate_pct": p.get("skip_rate_pct"), "nonfollower_pct": p.get("views_nonfollower_pct"),
           "follows": p.get("follows"), "follows_per_1k": _per_1k(p.get("follows"), views),
           "flags": flags, "flag_notes": flag_notes}
    if p.get("cta_keyword"):
        out["cta_keyword"] = p["cta_keyword"]
    return out


def _raw(p):
    """Unrounded metrics, so contrast ranking is not distorted by display rounding."""
    views = p.get("views") or 0
    m = {f"{k}_per_1k": (None if not views or p.get(k) is None else p[k] / views * 1000) for k in RATES}
    m["follows_per_1k"] = None if not views or p.get("follows") is None else p["follows"] / views * 1000
    m["nonfollower_pct"] = p.get("views_nonfollower_pct")
    m["skip_rate_pct"] = p.get("skip_rate_pct")
    m["reach_ratio"] = views / p["followers"] if p.get("followers") else None
    m["watch_through"] = p["avg_watch_s"] / p["length_s"] if p.get("avg_watch_s") is not None and p.get("length_s") else None
    return m


def analyze(perf):
    posts = [_post(p) for p in perf]
    contrast = []
    best = next((x for x in posts if x["label"] == "best"), None)
    weak = next((x for x in posts if x["label"] == "weak"), None)
    if best and weak:
        bp = next(p for p in perf if p.get("label") == "best")
        wp = next(p for p in perf if p.get("label") == "weak")
        braw, wraw = _raw(bp), _raw(wp)
        zero, scored = [], []
        for k, b in braw.items():
            w = wraw.get(k)
            if b is None or w is None:
                continue
            shown_b = round(b, 2 if k in ("reach_ratio", "watch_through") else 1)
            shown_w = round(w, 2 if k in ("reach_ratio", "watch_through") else 1)
            if k in ZERO_METRICS and b > 0 and w == 0:
                meaningful = b >= 5 or (k == "follows_per_1k" and (best["follows"] or 0) >= 10)
                z = {"metric": k, "best": shown_b, "weak": 0, "factor": None, "note": ZERO_NOTE}
                count = k[:-len("_per_1k")]  # raw counts, so the dashboard can say "108 vs 0"
                if bp.get(count) is not None and wp.get(count) is not None:
                    z["best_count"], z["weak_count"] = bp[count], wp[count]
                zero.append((meaningful, b, z))
            elif w > 0 and b > 0:
                lower = k in LOWER_IS_BETTER
                c = {"metric": k, "best": shown_b, "weak": shown_w, "factor": round(w / b if lower else b / w, 1)}
                if lower:
                    c["lower_is_better"] = True
                if k == "nonfollower_pct":
                    c["delta_pp"] = round(b - w, 1)
                scored.append((abs(math.log(b / w)), c))
        zero.sort(key=lambda z: (z[0], z[1]), reverse=True)
        scored.sort(key=lambda s: s[0], reverse=True)
        ordered = [c for m, _, c in zero if m] + [c for _, c in scored] + [c for m, _, c in zero if not m]
        contrast = ordered[:5]
        nf = next((c for c in ordered if c["metric"] == "nonfollower_pct"), None)
        if nf and nf not in contrast:
            if contrast[-1].get("note") == ZERO_NOTE and contrast[-1]["metric"] in {c["metric"] for c, in [(z[2],) for z in zero if z[0]]}:
                contrast.append(nf)  # never evict a meaningful zero contrast
            else:
                contrast[-1] = nf
        skip = next((c for c in ordered if c["metric"] == "skip_rate_pct"), None)
        if skip and skip not in contrast:
            contrast.append(skip)  # the first-3-seconds signal the Viewer Mind cites; always shown
    return {"confidence": "signal", "note": NOTE, "input_hash": input_hash(perf), "posts": posts, "contrast": contrast}


def main(argv):
    if len(argv) < 2:
        print(__doc__); return 2
    path = Path(argv[1]); r = json.loads(path.read_text(encoding="utf-8"))
    perf = r.get("intake", {}).get("performance") or []
    if not perf:
        print("No intake.performance; nothing to analyse."); return 0
    r["performance_analysis"] = analyze(perf)
    path.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(r["performance_analysis"], ensure_ascii=False, indent=2)); return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv))
