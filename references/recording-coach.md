# Recording Coach (Voice Director)

## 1. Performance sheet (creators who record themselves)
One row per spoken line in the final script:
| Field | Content |
|---|---|
| Energy | 1–5, plus a feeling word (calm, confident, urgent, warm) matching the style chosen in intake |
| Emphasis | **One** word to stress |
| Pace | fast / normal / slow, and where the "/" pause goes |
| Pronunciation | English terms and names, spelled the way they should sound |

**Energy per style** (the baseline from `scripts/styles.json`; the hook and proof may sit one step higher, never two):

| Style | Energy | Feels like | Delivery note |
|---|---|---|---|
| `yapping` | 3 | warm, chatty | Let sentences run on; a real laugh is fine, a forced one isn't |
| `infotainment` | 4 | quick, sure | Land the fact, then move; no lingering on mood lines |
| `asmr_whisper` | 1 | soft, close | Mic close, whisper, no plosives; let the sound fill the pauses |
| `professional` | 2 | calm, confident | Even pace, a firm full stop at each sentence end |
| `hype` | 5 | urgent, bright | Fast, but every number said clearly; breathe before the result |
| `deadpan` | 1 | flat, dry | No smile in the voice; hold a full beat before the punchline |
| `relaxed_narrator` | 2 | unhurried, warm | Read to the footage; slow down on names and places |

Then add: the **energy arc** (where it peaks; usually the hook and the proof), three delivery tips specific to this script, and setup basics: a quiet room, phone mic close, and the hook recorded three times, keeping the most natural take.

## 2. Coaching
**3 habits to keep** (fewer only without the creator's own speech; see below) and exactly **3 to change**, each with:
- **Source:** `your_best_script` (strongest evidence: it worked for this creator) · `craft_rule` (an established short-form principle) · `opinion` (say so plainly).
- **Exercise:** one small, concrete thing to try in the next Reel.

Never call something "wrong" without a source. Coaching without evidence erodes trust.

**Habits to keep need the creator's own speech.** With no voice sample, best script or transcript, you haven't heard any of their habits, so don't invent one. The keep list may then hold fewer than 3, all sourced `craft_rule`, and say so plainly: «ما عندي تسجيل أو سكربت منك، فهاي قواعد عامة مو عاداتك.» / "I haven't seen your own speech yet, so these are general rules, not your habits."

## 3. Real pace instead of estimates
Default pacing is an estimate. The dashboard's **"Measure your real pace"** timer lets the creator read the script aloud and switch every timing to their measured speed. The measured pace is saved in the downloadable creator profile; on the next run it goes into `meta.pacing`, and the validator's durations match how this creator really talks.

The skill cannot hear the recording: it measures **time**, not tone or emotion. Say so if the creator asks for feedback on how they sound.
