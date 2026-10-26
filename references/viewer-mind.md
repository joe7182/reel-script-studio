# Viewer Mind: the first 3 seconds (Stage 2 "Before", Stage 3 Hook Lab)

Writes `viewer_mind`. Three specific viewers watch the first 3 seconds of each hook candidate, second by second: what they **see**, what they have **heard so far**, what they **think**, and whether they stay. The hook that holds them goes into the script.

This is a **simulation from research and the creator's own data, not a prediction.** It never produces percentages, view counts or "this will go viral" (`viewer_prediction` is a hard failure). Its job is to make the writer look at the opening through other people's eyes before the creator records it.

Contents: 1. Why 3 seconds · 2. The three personas · 3. Running a candidate · 4. Stage 2: Before · 5. Stage 3: Hook Lab loop · 6. Honesty rules · 7. Example

## 1. Why the first 3 seconds
- **What the platforms measure:** Instagram's Reels Insights show a **skip rate**: the share of views that left within the first 3 seconds. When the creator pastes it, cite it as `creator_data` (`performance:skip_rate_pct`).
- **What the platforms advise:** TikTok's creative guidance says to introduce the content proposition in the first 3 seconds and land the hook within the first 6. The craft rule `hook-proposition-3s` summarises this. When research ran and you opened the page, cite the source itself instead.
- **The order a viewer meets the Reel:**

| Second | What the viewer has | The question in their head | What the hook must give |
|---|---|---|---|
| **0** | Only the first frame and any text on it. Sound may be off. | "What is this?" | A situation they recognise, or a result, on screen. Not a face waiting to talk, and not a logo. (`hook-first-frame`, `sound-off-overlay`) |
| **1** | The first 2–4 words | "Is this for me?" | Their problem or goal, in their words. A greeting or "today I'll talk about" spends this second on nothing. |
| **2** | Most of the first sentence | "Why should I keep watching?" | Tension: a gap, a stake, a contradiction, or a number that needs explaining. |
| **3** | The first sentence, with the frame and overlay | "What will I get?" | The proposition: what they'll know or be able to do. (`hook-proposition-3s`) |

## 2. The three personas (`viewer_mind.personas`)
Write them once per script, during Stage 2. Each one has:
- `who`: at least 4 words, with no generic phrase («أي شخص», "people interested in AI")
- `context`: what they were doing a second ago
- `want`: what they want right now
- `swipe_trigger`: what makes them leave

They must be three different people.

| id | Who | Build it from |
|---|---|---|
| `target` | The viewer this Reel is for | `intake.audience`, the niche, `content_category`, and the awareness stage (`idea.awareness_stage`) |
| `stranger` | Someone who has never seen this creator and follows nobody like them | The non-follower share in `performance_analysis` when it exists ("98.2% of your best Reel's views were non-followers"). They may be watching muted, so the frame and overlay must carry the opening alone. |
| `skeptic` | Someone who has seen this topic many times | The common angles found in research (`research.sources` of kind `angle`), or `idea.angles` when there was no research. They leave at the first familiar line. |

- Weak: `who`: «شخص مهتم بالذكاء الاصطناعي» · "Someone interested in productivity"
- Strong: `who`: «صانع محتوى عراقي يكتب سكربتاته ويا الذكاء الاصطناعي كل يوم», `context`: «بالليل، خلّص تصوير وفاتح إنستغرام يرتاح شوية» *(golden)* · "A freelance designer in Dubai who bills by the hour", `context`: "between two client calls, phone in one hand"
- Why: a specific person gives specific reactions. A generic persona agrees with everything, so it tests nothing.

## 3. Running one candidate (`viewer_mind.candidates[]`)
A candidate copies a hook option **exactly**: `ref` (the option id), `text`, `visual` and `onscreen`. The creator's own opening is `ref: "original"`. Its `text` is their first sentence, word for word from `intake.original_draft`; its `visual` is `""` unless the draft describes one.

For each persona, write one run with four moments (seconds 0, 1, 2, 3):
- **`sees`:** what is on screen at that second. At second 0 it must describe the candidate's `visual` or `onscreen` text (`viewer_first_frame`).
- **`heard_so_far`:** the exact first words of the hook, as far as the voice has got. It's empty at second 0 unless one word fits. It only grows. At the creator's hook pace it can't run ahead (`viewer_heard`):

| Hook pace | By 1 s | By 2 s | By 3 s |
|---|---|---|---|
| 150 wpm (Arabic default) | ≤ 4 words | ≤ 7 | ≤ 9 |
| 175 wpm (English default) | ≤ 4 | ≤ 7 | ≤ 10 |

  With a measured pace, the limit is `int(wpm / 60 × second) + 2`. For a text-only Reel, `heard_so_far` is always empty.
- **`thinks`:** the viewer's inner voice, short, in their own language and dialect, reacting to what they **just** saw or heard.
  - Not "interesting" or "I like it". Every second has its own thought.
  - Two personas never think the identical thing at the same second.
- **`state`:** one of `hooked`, `curious`, `neutral`, `doubting` or `leaving`.

**After a swipe:** freeze `heard_so_far` at what they'd heard at `decided_at`, keep the state `leaving`, and give each later second its own thought (e.g. what's on their screen now).

Then the **verdict**:
- `stays` (the state at second 3 is `hooked` or `curious`), or `swipes` at `decided_at` (the state there is `leaving`)
- a `reason` that names the moment and the cause
- a `basis`: an opened source, the creator's data, or a craft rule id. See `research.md`, "Basis".

## 4. Stage 2: Before
When the creator gave a draft, simulate **its real opening** as the `original` candidate during the audit. That's the Before picture in the dashboard. Be fair: simulate what the draft actually says, not a weaker version. Its swipe moments feed the audit findings at the same seconds. With only an idea, there is no Before.

## 5. Stage 3: Hook Lab loop
1. Write the 5 hook packages (`beat-engine.md`).
2. Choose **2 or 3 candidates**: the 2 strongest new packages by their hook scores, plus the `original` whenever a draft exists.
3. Simulate all three personas on each candidate.
4. **Choose** (`viewer_mind.chosen`) the candidate with the most `stays`. It must hold both `target` and `stranger` (`viewer_choice`).
   - The Recommended hook option is the chosen candidate's text.
   - Never choose a candidate that held fewer viewers than another.
5. **If none holds both `target` and `stranger`,** fix what the swipe moment names, then simulate again (at most 2 rewrites; Quick: 1):
   - **swipe at second 0:** the first frame or overlay
   - **at second 1:** the first words
   - **at seconds 2–3:** the tension or the proposition
6. **Still not held:** choose the best candidate, write `viewer_mind.unresolved` (who still leaves, at which second, and why), and list it in `council.open_issues`. The decision is then `ship_with_issues` at best (`viewer_unresolved_shipped`).
7. **If the original wins, keep it.** The Recommended hook option carries the creator's opening, and the dashboard says so. A rewrite that loses to the original is not an improvement. The one exception: an original that opens with a greeting, "in this video" or a hedge breaks a hard hook rule, so cut that opener and keep the rest of their line.

The simulation shapes the rest of the script:
- The Retention line answers what the `target` was curious about at second 3.
- `concept.promise` is what the chosen hook promised.
- `concept.payoff_line` is where it's paid.

## 6. Honesty rules
- **Simulate; don't cheerlead.** The skeptic is hard to win. A run where all three viewers stay for every candidate has tested nothing; rewrite the personas.
- **A `stays` needs a visible cause** in the moments: the frame showed their situation, or the first words named their problem.
- **No numbers the creator didn't give.** No percentages in `thinks`. A percentage in a `reason` only when its basis is the creator's own data.
- **No predictions anywhere** (`craft.json` → `prediction_words`): no "will go viral", «راح ينتشر», "more views".
- **Never say a source supports a choice it doesn't.** TikTok's guidance supports "say what the viewer gets within 3 seconds". It doesn't support "this hook will win".

## 7. Example *(golden, abridged)*
Candidate `h1`: «بدل ما تشرح شغلك كل مرة من الصفر. / خليه يتذكر عنك.», with the visual «تسجيل شاشة: مؤشر يكتب نفس الفقرة للمرة الثالثة، العدّاد يبيّن ٣/٣».

| s | sees | heard so far | stranger thinks | state |
|---|---|---|---|---|
| 0 | نفس الفقرة تنكتب للمرة الثالثة، والعدّاد ٣/٣ | — | آني هم أكرر نفس الشرح للـAI | curious |
| 1 | النص «٣ مرات اليوم؟» | بدل ما تشرح | الصوت مطفي بس الصورة واضحة | curious |
| 2 | العدّاد ٣/٣ يرمش | بدل ما تشرح شغلك كل مرة | هذا آني بالضبط | hooked |
| 3 | المؤشر يوقف | بدل ما تشرح شغلك كل مرة من الصفر | خلي أشوف الحل | hooked |

Verdict: stays. Reason: «الصورة والنص يشرحون المشكلة بدون صوت، وبدون ما تعرف منو المتكلم.» Basis: `craft_rule` `sound-off-overlay`.

The original opening «هلا بيكم، اليوم راح احجيلكم…» lost all three viewers: the stranger at second 1, because nothing is written on screen, and the target and the skeptic at second 2. That's the Before the creator sees in the dashboard.
