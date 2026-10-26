# Stage 1 — Idea Strategist

The first agent decides whether the idea deserves a script at all, and in what form. Write results into `idea`.

## 1. Reel type
One of: Tutorial / How-to · Tips / List · Product or Offer · Case study / Result · Story / Personal · Opinion / Hot take · News / Update · Comparison / Review · Behind the scenes · UGC-style ad.

## 2. Routing
| Kind | `routing` | Support |
|---|---|---|
| Spoken (voice-over or talking head) | `spoken` | Full |
| Dialogue / multi-character skit | `spoken` | Not supported in this version. Say so, then script the creator's own lines only, as a single voice |
| Non-speech (dance, trend audio, music-only, silent visual) | `text_only` | Say plainly that the skill is built for spoken scripts. Write the six beats as **text cards of 6 words max** (each option's `text` is the card; `onscreen` repeats it). Set `intake.recording.method: "none"`, leave `voice` as `{}`, and omit `voice` in shot rows. No duration checks, and proof cards don't need footage flags |

Set `idea.regulated: true` for the niches listed in `claims-trust.md` (health, supplements, investing, crypto, loans, legal, income claims). Everyday tools like budgeting apps are not regulated by themselves.

## 3. Five scores (1–5), each with one reason tied to this script
| Criterion | 1 | 3 | 5 |
|---|---|---|---|
| **Clarity** | Several ideas competing | One idea, a fuzzy promise | One sentence says it all |
| **Viewer value** | Viewer gains nothing concrete | Useful but generic | A specific gain or feeling for a specific person |
| **Angle** | Same as countless Reels | A familiar topic with a twist | A fresh angle the audience hasn't seen |
| **Audience fit** | Wrong audience or awareness stage | Roughly right | Exactly the target viewer at their stage |
| **Provability** | Nothing can be shown | Partly demonstrable | The main claim can be seen on screen |

Awareness stages: Unaware · Problem-aware · Solution-aware · Product-aware · Most-aware. The hook and CTA must match the stage.

## 4. Verdict rule (apply literally)
- **Rethink:** Clarity ≤ 2 **or** Viewer value ≤ 2.
- **Strong:** no score below 3 **and** average ≥ 4.
- **Sharpen:** everything else.

For Sharpen or Rethink, propose **2–3 sharper angles**, choose one, and say why in one line — before Stage 3 writes anything.

## 4a. Honest take: say it, then respect the decision
A senior writer tells the creator the truth about the idea, kindly and once. Whenever the verdict is not **Strong**, write `idea.honest_take` in the user's language, in 2–3 sentences:
1. what is weak, named specifically ("the angle is the same setup walkthrough everyone posts", not "it could be better")
2. what would be better (the strongest sharper angle)
3. that the decision is theirs

The validator fails `honest_take_missing`, and prediction words fail here too: never "this won't get views".

- Weak: «فكرة حلوة بس ممكن تتحسن شوية 👍»
- Strong: «بصراحة، الفكرة بشكلها الحالي مكررة: نفس شرح الإعدادات اللي ينشر كل يوم، فالغريب ما عنده سبب يوقف. أنصحك تبدأ من موقف المشاهد نفسه (يكتب نفس الشرح للمرة الثالثة). بس القرار قرارك، وإذا تحب نكمل بفكرتك مثل ما هي، أكتبها بأحسن شكل.»
- English: "Honestly, this idea is the same 'top 5 tools' list the feed is full of, so a stranger has no reason to stop. I'd open on the one tool that saved you an hour, shown on screen. It's your call: if you want to keep your idea as it is, I'll write the best version of it."

**Rethink** means the idea itself is the problem. Stop before writing. Give the honest take and the 2–3 better angles, and ask **one** question: keep the idea as it is, or use the suggested angle? Record the answer in `idea.creator_choice` (`as_is` or `suggested_angle`; `creator_choice_missing` is hard). This is the one exception to "never ask a second round". If the creator already said "write it anyway", record `as_is` and don't ask.

**Sharpen** means the idea works with a fix. Write the honest take, apply the sharper angle, and say in one line that their original framing is available on request.

**When the creator chooses `as_is`, write their idea at full quality.** Never sandbag it to prove the point. The honest take stays visible in the dashboard. Being honest and being helpful are not in conflict.

## 4b. Angle research (Stage 1b, `research.md`)
When research ran, the opened `angle` sources show what is already widely posted. Name the one this Reel deliberately avoids in `idea.avoided_angle` (`{angle, source}`) and say in `direction` how the chosen angle differs. The **Angle** score uses this: an angle that matches the most common one scores 3 at best. The same angles become the `skeptic` persona's memory in the Viewer Mind (`viewer-mind.md`). Without a search tool, `research.status` is `unavailable`, `avoided_angle` is left out, and `direction` says angle research was skipped. (`idea.angles_seen` is still accepted for older results; new results use `research.sources`.)

## 4c. Takeaway
Write `idea.takeaway`: the one thing the viewer can **do** (or know and use) after watching, in one sentence, in the user's language. It is hard-required for tutorial, tips and product Reels (`takeaway_missing`), and recommended for every type. A takeaway names the object, the amount and the moment.
- Weak: «استخدم Claude Projects بذكاء.» / "Batch your content."
- Strong: «سوّي Project واحد بـClaude وارفع بيه ملف «عنّي» بثلاث فقرات: منو إنت، جمهورك، وأمثلة من كلامك.» / "Film all four hooks on Sunday in one sitting, then edit them on Monday."

If you can't write a concrete takeaway, the idea isn't ready: Viewer value is at most 2, and the verdict is Rethink. Stage 3 must deliver the takeaway in the spoken lines, not only in the caption.

## 5. Direction (3–5 lines)
Recommended structure, format (voice-over / talking head / screen demo / mixed), target length, CTA move, and **the single most important thing that will make this Reel work**.

## 6. Basis statement (shown once in the dashboard, in the user's language)
"Every suggestion names its basis (your data, an opened source, or a named craft rule). They are based first on your own material (your voice sample, best-performing script and its numbers, the facts and proof you gave), then on established short-form craft principles. They do not use live platform data and do not predict views." If web search was used to check facts, add: "Factual claims were checked against the sources listed in the audit." If it was used for angle research, add: "The angle was chosen after looking at what is already posted (sources in the Idea tab)."

## 7. Past-success analysis (if a best-performing script was given)
Extract why it worked: hook mechanism, length, structure, CTA type, and any numbers given. The new script must **match or beat** it on the criterion that made it win. Record this as `idea.benchmark`. When `performance_analysis.contrast` exists (best vs weak post, from `scripts/performance.py`), lead with a zero contrast if there is one ("Shares N vs 0: only your best post has this"), then the non-follower share of reach (best vs weak), then follows gained; mention keyword-driven comments (`comments_cta_driven`) as response to the offer, not proof. Add the script difference that likely explains them, as a signal from 1–2 posts, not proof. Flags `hook_lost_viewers` (3-second hold under 60%) and `middle_lost_viewers` (watch-through under 0.4) are rules of thumb; say so. When both posts have a skip rate (`skip_rate_pct`, lower is better), it's the most direct signal about openings: cite it in the Viewer Mind as `performance:skip_rate_pct`.
