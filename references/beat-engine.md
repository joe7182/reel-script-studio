# Stage 3 — Beat Engine (Writer)

Read `craft-standards.md` first: it sets the bar these rules serve.

**Order of work:** 1. the concept card (`craft-standards.md` §1) → 2. confirm `idea.takeaway` can be said aloud → 3. the beats, each better than the original and the common angle → 4. the Hook Lab: simulate the strongest hooks plus the original and choose (`viewer-mind.md` §5) → 5. presets, final script, self-assessment.

Contents: 1. The six beats · 2. Hook rules · 3. Retention · 4. Problem, Solution, Proof, CTA · 5. Option rules · 6. Interchangeability · 7. Presets · 8. Naturalness and duration · 9. Writer persona

## 1. The six beats
| # | Beat | Job | Options |
|---|---|---|---|
| 1 | **Hook** | Earn the first 1–3 seconds | **5** |
| 2 | **Retention** | Raise stakes or make a promise that earns the next 5 seconds | 3 |
| 3 | **Problem** | One specific, relatable moment, with its cost | 3 |
| 4 | **Solution** | The clearest fix, concrete; the product named once | 3 |
| 5 | **Proof** | Evidence the viewer can see; real only | 3 |
| 6 | **CTA** | One action that serves the goal | 3 |

Option counts are exact: **5 hooks, 3 options for every other beat** (the validator fails anything else). For a complex tutorial or story, a beat may hold two short sentences, but the six beats always exist. They keep the builder and the validator working.

### Slot labels by Reel type
The six `beats[].id` values never change. Slots 3–5 change **job and label** (`beats[].label`) with the Reel type, so a story doesn't get forced into problem → solution → proof:

| Reel type | Slot 3 (`problem`) | Slot 4 (`solution`) | Slot 5 (`proof`) |
|---|---|---|---|
| Tutorial · Tips · Product · UGC ad | Problem | Solution / Steps | Proof |
| Case study / Result | Before | What changed | Result shown |
| Story / Personal | Setup | Turn | Lesson |
| Opinion / Hot take | The common belief | My take | Example that shows why |
| News / Update | What happened | Why it matters | What to do now |
| Comparison / Review | Option A | Option B | Verdict + evidence |
| Behind the scenes | The goal | The messy middle | What it looks like now |

Proof-honesty rules apply to slot 5 whatever its label: anything the viewer is told they'll "see" must be declared proof.

### Proof by speaking style
The proof beat never disappears; it protects trust. Its delivery follows `intake.style` (`speaking-styles.md` §1):

| Style | How the proof lands |
|---|---|
| `yapping` | **The receipt:** the creator stops talking and shows the thing, mid-chat |
| `infotainment` | The fact on screen: the setting, the source, the number in context |
| `asmr_whisper` | **Show, barely tell:** the result on screen, a few words at most |
| `professional` | The document or number, named once, plainly |
| `hype` | The result on screen, fast, ideally before the explanation |
| `deadpan` | **The proof is the punchline:** the plain shot that shows the truth |
| `relaxed_narrator` | The footage carries it; the narrator names the detail that makes it real |

## 2. Hook rules
Each hook option is a **package**: the spoken line (`text`, first 1–3 seconds), the first-frame `visual` (already moving, on-topic; required on every hook), and the overlay (`onscreen`, 2–6 words, readable muted). The overlay adds a number, a label or the stakes; it never repeats the spoken line (hard `overlay_echo_recommended` on the Recommended script, soft `overlay_echo` elsewhere) or describes the hook's own visual (`overlay_echo_visual`, soft). Examples: `craft-standards.md` §4. The Recommended hook's `visual` becomes the opening frame; the cover is chosen separately (`production.md`).
- Put the payoff-relevant idea in the first 3 spoken words where possible. No greetings, no "in this video".
- The first sentence carries tension, stakes, or a specific observable moment.
- **No opening hedges:** «مرات», «ممكن», «مو كل», "sometimes", "maybe", "not every". (The validator rejects these.)
- Name a concrete behavior and moment the viewer recognizes, not an abstract outcome ("people leave your video in the first second" beats "your video doesn't reach").
- Conditionals («إذا...», "if...") are allowed; they let the viewer opt in.
- Match the awareness stage: Unaware → surprise or contrast · Problem-aware → name the pain · Solution-aware → a better way · Product-aware → demonstration or result.
- **Replacement rule:** if the audit criticized the original hook for a weakness (say, vagueness), every new hook must fix that exact weakness. Never swap one vague word for another.

**Hook mechanisms:** Pain · Contrast · Curiosity gap · Mistake / warning · Demonstration · Result (proof-safe) · Strong opinion · Specific question · Relatable moment · "Instead of X" (the creator's proven «بدل ما...» structure). The five hooks use five different mechanisms; the Recommended hook uses one that fits the style (`hooks` in `scripts/styles.json`, listed per style in `speaking-styles.md` §1). Each gets a 1–5 score on clarity, tension, relevance, and credibility. No generic openers («في عالم اليوم», «هل تعلم», "did you know"): they are hard failures (`cliche_hard`).

## 3. Retention
The line right after the hook decides whether the viewer stays for the middle.
**Moves:** Open loop · Stake escalation · Mid-reveal · Counter-intuitive turn · List counter · Pattern break. Examples: `craft-standards.md` §5. The three options use three different moves, written for this Reel.
- **No stock lines:** «وبالآخر راح تشوف», «خليك للآخر», "stick around", "by the end you'll see" (`cross_beat_template`). Name the payoff instead of asking for patience.
- **Retention options may only promise what the script delivers in every combination**, through every Solution option or every Proof option. Never open a loop that only one specific option closes.
- Through the whole script, add a re-hook every 5–8 seconds: a new visual, a turn («بس هنا الفرق»), or an on-screen reveal.

## 4. Problem, Solution, Proof, CTA
- **Problem:** the target viewer should think "this is exactly me". One relatable moment beats a list. State the cost of leaving it unsolved without inventing numbers.
- **Solution:** say how it works, concretely. If a product or tool is featured, **say its name aloud once** in this beat.
- **Proof:** only evidence declared in `intake.proof`. List what each option needs in `proof_uses` (leave it empty when nothing was declared). With no proof declared, use on-screen demonstration or the visible process, with `flags: ["needs_footage"]`, and write `production.proof_shots` (hard check `proof_shots_missing`). **"Try it yourself" is an invitation, not proof**: it belongs in the CTA. A proof line is spoken only if the footage exists. See `craft-standards.md` §7.
- **CTA:** all three options serve the stated goal. They use **three different moves and three different opening words** (`opener_monotony`; every CTA starting «احفظ…» was a real failure). Moves: save-because-reason · comment keyword · follow-for-part-2 · try-and-report · DM resource · loop-back (`craft-standards.md` §6). The CTA comes after the value, states what the viewer gets, and asks for one step. A comment keyword or DM resource needs a resource that really exists. Never engagement bait ("like if you agree", "tag 10 friends").

## 5. Option rules
- Each beat's options use **different mechanisms**, never synonyms of one idea. Variety is mandatory: options that differ only in wording count as one option.
- When the creator gave a real detail, the Recommended script carries it, marked `"human_texture": true` (`creator_detail_missing` warns; `craft-standards.md` §2). When there is none, the script must still be recordable: a `{{…}}` slot is optional, only when one fact would clearly lift it, naming exactly what to add («{{رقمك الحقيقي: كم دقيقة باليوم تعيد نفس الشرح؟}}», "{{your real number: minutes a day spent re-typing the same brief}}"). Never invent the creator's story or number. Slots go only in spoken option text (`slot_misplaced`).
- Label each option **Recommended**, **Safe edit**, or **Bold**, with its word count and a one-line "why".
- When a draft exists, one option per beat is the **Safe edit**: the creator's own line, lightly fixed. If the draft has no line for that beat, **or its line was a claim the audit removed**, write the closest honest line instead and mark it `"new": true`. With **no draft at all** (an idea only), there is no Safe edit: mark every option `"new": true`, tag the extras Bold, and leave `presets.safe_edit` as `{}`.
- Every option is **1–2 sentences**, a self-contained spoken unit, in plain speech: no `[tags]` or `<break>` (those belong only in ElevenLabs clips).
- Exactly **one Recommended** per beat and **at least one Bold**. Extra options beyond those are tagged Bold.

## 6. Interchangeability (the validator tests every combination)
The builder lets users mix any option from any beat, so **every combination must read as one natural script.**
- **No pronouns pointing to another beat's words.** A Proof option cannot say «جربتها» meaning the tool named in the Solution beat. Use the noun.
- **Anchor-term exception:** the product name or its plain noun, listed in `anchor_terms` (e.g. `["Claude", "كلود"]`), may appear in up to **2 beats** in any single combination. Write options so this holds for every combination (hard check `anchor_overuse`). This rule exists because banning pronouns *and* repetition made product scripts impossible to write.
- **No two-word phrase repeats across beats** (hard check `phrase_repeat`). A single repeated key word is a warning (`word_repeat`, one per word, listing every option that uses it): vary it unless the repetition is deliberate. The validator normalizes Arabic first, so «بالأداة» and «الأداة» count as the same word.
- The product's grammatical gender and number stay consistent everywhere.
- **Duration:** every combination must stay within the target +10%. The validator computes this for all combinations (1,215 = 5 × 3⁵).

## 7. Presets
- **Recommended:** the best option in every beat.
- **Safe edit:** every Safe edit option (the creator's own words, improved).
- **Bold rebuild:** every Bold option. This satisfies the rule that a light edit is never the whole answer.

`final_script` must be **exactly** the Recommended preset, beat by beat. Presets map each beat id to an option id; each must point to an option carrying that tag. Without a draft, `safe_edit` may be `{}`.

## 7b. Self-assessment
Write `self_assessment`: a 0–100 score (labeled in the dashboard as likely optimistic) and **at least two** remaining weaknesses. If a risky claim survives, the score is capped at 69.

## 8. Naturalness and duration
- Write at the chosen language level, `meta.register` (`voice-dialect.md` §7).
- Avoid the AI tells in `craft-standards.md` §3: "not X, it's Y" at most once, at most two questions (or the style's lower limit), at most one list of three, uneven sentence lengths.
- Keep the spoken connectors from the voice sample (فـ، بس، يعني، لهذا، وبعدين...).
- Never compress speech into list fragments, verb-less comma chains, or colon-lists.
- Duration discipline, in order: write naturally → cut whole ideas if over target → allow at most 10% over → beyond that, add a separate `tight_cut` made by removing whole ideas.
- Pacing used by the validator (estimates; `meta.pacing` from a creator profile overrides them):

| | Hook | Body | CTA |
|---|---|---|---|
| Arabic | 150 wpm | 128 wpm | 115 wpm |
| English | 175 wpm | 145 wpm | 130 wpm |

Without `meta.pacing`, the validator multiplies these by the style's `pace_factor` (×0.8 for `asmr_whisper` up to ×1.15 for `hype`). Measured pace always wins. Plus 0.5 s per "/" pause marker. **Numbers count as spoken:** 199 = three words («مية وتسعة وتسعين»), 20% = two words, and an unfilled `{{…}}` slot = four.

## 9. Writer persona
Write like a senior short-form creator: one idea per breath, a turn every few seconds, concrete over abstract, confident without hype, and specific enough that a top creator in this niche would post it unedited (`craft-standards.md` §1). But in the **creator's** voice and dialect, in the speaking style chosen for this script, never in the style of a specific real influencer.
