# Voice & Dialect (Auditor and Writer)

Contents: 1. Voice source priority · 2. Clarity over flavor · 3. No voice sample · 4. Dialect lexicons · 5. Spelling pass · 6. Other rules · 7. Language level (`meta.register`) · 8. Audit findings (Stage 2)

## 1. Voice source priority
1. The **voice sample** and **best-performing script**: the creator's real words. Highest authority.
2. The stated dialect.
3. The **draft**: lowest authority. Drafts are often written by AI or by someone else.

When the draft conflicts with the voice sample, follow the sample and list every replaced word in `audit.voice.replaced`.

**A draft the user pastes is still a draft**, even if they say "my script". Only a separate voice sample (lines they actually said) or a best-performing script counts as the creator's real words. With no sample, set `audit.voice.source` to `draft_only`; with nothing at all (an idea only), use `none`.

## 2. Clarity over flavor
A dialect word earns its place only if most speakers of that dialect understand it instantly. Replace regional, rare, or ambiguous words with widely understood ones, and list the swap. Never add extra dialect markers for "authenticity". «دا تطوف» came from an AI draft, and the creator himself didn't understand it.

## 3. No voice sample given
- List **every dialect-specific word in the final script**, including words kept from the draft, in `audit.voice.confirm_words`.
- Tell the creator that a voice sample would make the script sound like them.

## 4. Dialect lexicons
Never mix markers across dialects. The validator scans for these lists (`scripts/dialects.json` is the source the code reads) and reports hits as **warnings** (`dialect_foreign`), not failures: many words are shared across dialects (e.g. «عشان» is Egyptian *and* common in Saudi/Gulf speech). The Voice Guardian decides, using the voice sample.

| Dialect | Typical markers (keep) | Foreign markers (flag) |
|---|---|---|
| Iraqi | هسه، ماكو، اكو، شلون، شنو، هواي، أدزلك، راح، هاي، بيها، كلش، شكد | الحين، وايد، يبا، إيش، دلوقتي، كده، عشان، هلق، منيح |
| Gulf (Emirati, Kuwaiti, Qatari, Bahraini) | الحين، وايد، يبا، يطرش، شو (Emirati)، عقب، لين، ربعك | هسه، ماكو، دلوقتي، كده، هلق، منيح |
| Saudi | الحين، إيش، وش، مره، كذا، أبغى، عشان، زي | هسه، ماكو، دلوقتي، هلق، منيح، وايد |
| Egyptian | دلوقتي، كده، عشان، إزاي، إيه، أوي، بتاع، عايز | هسه، الحين، وايد، هلق، شلون، ماكو |
| Levantine | هلق، شو، كتير، منيح، هيك، بدي | هسه، الحين، دلوقتي، وايد، شلون، ماكو |

`msa` and `pan_arab` have no "keep" markers. They flag strong regional markers (هسه، ماكو، وايد، دلوقتي، هلق…) so the script stays understandable everywhere. Maghrebi dialects are not supported yet; say so, and offer pan-Arab conversational Arabic.

### Native corrections
`scripts/dialect_corrections.json` holds word swaps per dialect: `wrong` → `right`, with `why`, `status` and (when verified) `verified_by`. The validator scans the final script, every beat option and the ElevenLabs clips (`dialect_correction`):
- `native_verified` is **hard**: the build is refused until the word is swapped. Example: Iraqi «طالعت» → «باوعت» (verified by the owner).
- `provisional` is a **warning**: a likely fix no native speaker has confirmed yet. The Voice Guardian decides, using the voice sample.

Matching is literal. Only the listed `wrong` and its optional `forms` (other conjugations, e.g. `"forms": ["طالعنا", "يطالع"]`) match, plus attached prefixes on the first word («وطالعت»). An entry matches the listed word, or it with an attached prefix; a word of 3 letters or fewer takes only «و» as a prefix, so list any other prefixed variants of it in `forms` (and «لين» doesn't hit «فلين» or «كلين»). `wrong` may be a phrase («شو هاد»): its words must appear together, in order.

**Adding an entry.** When the owner or a native reviewer corrects a word, add it to that dialect's list with `why`, `"status": "native_verified"` and `"verified_by": "<who> <date>"`; list the conjugations to catch in `forms`. A suggestion no native speaker has confirmed stays `provisional`. Run the test suite after editing.

## 5. Spelling pass (matters most for AI voices)
Fix spelling without changing the dialect. Text-to-speech reads spelling literally.
- Ta marbuta vs ha: «يكملة» → «يكمّله», «نفسة» → «نفسه».
- Hamza: «اجرب» → «أجرب», «الاداة» → «الأداة».
- Split words: «الك» → «إلك».
- Add shadda or a vowel **only** where a word is likely to be misread: «محّد», «أدِزّلك», «بِنيت». Don't diacritize everything; it sounds formal.
- If a word can be read two ways, prefer an unambiguous synonym (e.g. «سوّيت» instead of «بنيت» if «بنيت» keeps being read «بُنيت»).

### Dialect diacritics for AI voices (ElevenLabs clips only)
Clips need **more** marking than the on-screen script, because undiacritized text drifts toward MSA pronunciation. Mark the vowels where the dialect differs from MSA, and pair them with the accent tag (`elevenlabs-tags.md`). Tested Iraqi example:
> «بَدَل ما تِشرَح شُغلَك كُلّ مَرّة مِن الصِّفِر... خَلّيه يِتذَكَّر عَنَّك. هَسَّه شوف.»

Iraqi patterns: the present-tense prefix with kasra («يِتذَكَّر»، «تِشرَح»), the helping vowel in final clusters («الصِّفِر»), shadda on doubled letters («خَلّيه»، «هَسَّه»، «عَنَّك»), «گ» for the Iraqi g sound where the creator uses it. Keep the script options and the teleprompter undiacritized; only `voice.elevenlabs.clips` get this treatment.

## 6. Other rules
- **Keep each draft's own register.** A draft in broad conversational Arabic stays broad. Never turn it Iraqi (or any dialect) just because an earlier script in the chat was, or because the creator is Iraqi. Change the register only when the creator asks. (This failed in a real test of another version.)
- Keep English technical terms exactly as the creator writes them (Arabic or Latin script).
- Keep code-switching consistent with the sample.
- Keep the product's grammatical gender consistent («الأداة» is feminine throughout).
- Never stiffen spoken Arabic into formal written Arabic.
- Low dialect confidence → clear pan-Arab conversational Arabic, flagged.

## 7. Language level (`meta.register`)
The creator picks one of three levels in onboarding (`intake.md` §4). `meta.dialect` stays the creator's dialect at every level; the level decides how local the words are.

| Level | What it means | How to write it |
|---|---|---|
| `heavy` (عامية قوية) | Full local speech for a home audience | The creator's own words and markers, as they really talk. Still no rare words they wouldn't use (§2) |
| `light` (عامية بسيطة، مفهومة عربياً) | The dialect any Arab viewer can follow | Keep the dialect's grammar and connectors (هسه، شلون، بس، يعني…). Swap strongly local vocabulary for widely understood words, and list every swap in `audit.voice.replaced` |
| `simplified_msa` (فصحى مبسطة) | Pan-Arab, closest to MSA | Short spoken sentences. No stiff written forms («إن», «حيث», «يُعدّ», long idafa chains). No regional markers |

One Iraqi line at the three levels:
- `heavy`: «ماكو داعي تعيد الشرح كل يوم، أحسن شي تسوي ملف واحد وخلص.»
- `light`: «ما يحتاج تعيد الشرح كل يوم، سوّي ملف واحد وخلص.» (swaps: «ماكو داعي» → «ما يحتاج», «أحسن شي تسوي» → «سوّي»)
- `simplified_msa`: «لا تحتاج أن تعيد الشرح كل يوم. يكفي ملف واحد، وتنتهي المشكلة.»

The voice sample outranks the level: if the creator says a "heavy" word in their sample, it may stay at `light`, and the Voice Guardian notes why.

**The `heavy_only` lists are provisional.** At `light` and `simplified_msa`, the validator warns (`register_heavy_word`) when a word from the dialect's `heavy_only` list in `scripts/dialects.json` appears. The lists are a first draft and need review by native speakers of each dialect, the same process as the accent tags. Treat a hit as a question for the Voice Guardian, not a verdict, and never swap a word the voice sample uses.

ElevenLabs: the accent tag applies at `heavy` and `light`; at `simplified_msa` there is none (`elevenlabs-tags.md`).

## 8. Audit findings (Stage 2)
The audit reads the draft the way a viewer watches it: second by second. Each finding in `audit.findings` has:
- `second`: where in the timeline the viewer is (estimate from the pacing in `beat-engine.md` §8).
- `viewer_thought`: what the viewer thinks at that moment, in their words and in the user's language («تحية… أسحب للفيديو الجاي», "another AI tip, swipe").
- `line` (quoted exactly), `issue`, `severity`, `fix`, `reason`.

Rules:
- **Every real finding, and only real ones**, spread across the timeline, never five versions of one problem. A strong draft may have two. Don't invent a finding to fill a quota. With only an idea, findings are optional.
- **Every finding carries a `basis`** (`research.md` §6): the creator's data, an opened source, or a craft rule id. A finding you can't base is an opinion; drop it.
- The Viewer Mind's Before run (`viewer-mind.md` §4) shows where each persona leaves the original; put findings at those seconds.
- Cover the craft bar too: generic openers, stock retention lines, "not X, it's Y", overlays that repeat the line, proof that is only "try it yourself", a missing takeaway (`craft-standards.md`).
- `top_fixes` is the three findings that change the most, in order.
- The audit is diagnosis only. Stage 3 writes the fixes.
- **Coaching is not the audit.** The coaching in `recording-coach.md` names habits for the next Reels (how this creator tends to open, pace, or close), each with an exercise. It never repeats this script's line fixes.

Example *(golden)*: second 0, «هلا بيكم، اليوم راح احجيلكم», the viewer thinks «تحية… أسحب للفيديو الجاي», critical, fix: «ابدأ بالمشكلة مباشرة». English: second 0, "Hey guys, today I want to talk about…", the viewer thinks "intro, skip", critical, fix: open on the problem.
