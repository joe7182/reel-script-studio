# Production (Stage 7)

## Shot table
Four columns, exactly: **Time · Visual (A-roll / B-roll) · Voice line · On-screen text**.
- Row length: 3–5 s for Reels ≤ 30 s; 5–8 s for 30–60 s; one row per beat beyond 60 s.
- Row 1 is the **opening frame**: the Recommended hook's `visual`, already moving and on-topic, with no logo or fade.
- Tag each visual with its beat (Hook, Retention, Problem, Solution, Proof, CTA, Re-hook).
- **Say it, show it:** every voice line has a visual that shows or proves it. The Proof row shows real output only.
- **On-screen text: 6 words max per card.** Split long lines into several cards. (The validator rejects anything longer.)

## Proof shots (`production.proof_shots`)
Whenever a proof option is flagged `needs_footage`, list exactly what to film so the proof line becomes real. The validator fails `proof_shots_missing` otherwise. Each entry:
- `shot`: what the viewer must see («الطلب الحي داخل الـProject», "the live request inside the Project").
- `how`: how to capture it so it convinces: an unedited screen recording, the real account, the date or counter visible, no cuts at the moment of the result.
- `duration`: how long it runs on screen («6 ث», "6 s").

One entry per thing the proof promises, usually 1–3. If the shot can't be filmed honestly (the result doesn't exist yet), the Trust Officer replaces the proof line; never fake or re-enact a result. In the dashboard, proof shots are highlighted on the Shoot screen.

## Cover (separate from the opening frame)
Creators can pick a frame or upload a cover. Recommend the content (an expression, an object, 2–4 bold words), centered so the profile-grid crop doesn't cut it.

## Safe zones (vertical 9:16)
Keep text and faces out of the top ~10% (platform header) and the bottom ~20% (caption and buttons). Keep key text slightly away from the right edge, where the action buttons sit. Put this as one line in `production.safe_zone_note`.

## Recording order
1. **Proof first**: the `proof_shots`, screen recordings and real results. Without them, the proof line can't be said.
2. Screen demos.
3. A-roll: all talking lines, with the hook recorded three times.
4. B-roll.
