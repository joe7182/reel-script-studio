# ElevenLabs Output (Voice Director)

**Last verified: 2026-10-02** (Eleven v4 and v4 Turbo launched 2026-09-28). ElevenLabs changes models and tag support. When anything here goes stale, update **only this file** and `scripts/elevenlabs_rules.json`; nothing else in the skill depends on these details. The dashboard shows the date to users.

## When to produce it
**Every spoken Reel gets an ElevenLabs version**, even when the creator records with their own voice: the dashboard offers it as "Generate an AI version". Use the model the creator chose; when none was chosen, write it for **Eleven v4**. Text-only Reels have no voice and no clips. `publish.ai_label` is required when the creator chose an AI voice; if a creator who records themselves ends up publishing the AI version, remind them to switch the label on.

## Per-model rules
| Model | Delivery cues | Pauses | Never |
|---|---|---|---|
| **Eleven v4** (recommended) | Audio tags in square brackets, from the allowed list | `...` and `[pause]` / `[long pause]` | `<break>` (tested 2026-10-02: silently ignored, no pause) |
| **Eleven v4 Turbo** | Same as v4 (assumed; confirm with one test generation) | same | `<break>` |
| **Eleven v3** | Audio tags in square brackets, from the allowed list | `...` and `[pause]` / `[long pause]` | `<break>` (confirmed unsupported) |
| **Multilingual v2** | Punctuation only | `<break time="0.4s" />`, at most 2 per clip | **Any square-bracket tag**: v2 reads it aloud |
| **Any other model** (Flash, Turbo v2.5, unknown) | Punctuation only | `...` and commas | Square-bracket tags and `<break>` |

The validator enforces this table (`el_tag_forbidden`, `el_break_forbidden`).

## Dialect accent (v4 / v4 Turbo / v3)
At registers `heavy` and `light`, **start every clip with the dialect's accent tag** and diacritize the dialect words (`voice-dialect.md` §5). Tested 2026-10-02 on Eleven v4 with an Iraqi cloned voice: diacritics alone weren't enough; diacritics **plus** `[strong Iraqi accent]` sounded clearly Iraqi, and the tag was not read aloud.

At `simplified_msa`, use **no regional accent tag**: the script is meant to sound pan-Arab. Don't diacritize toward the dialect either; mark only words likely to be misread. The validator may still warn `el_accent_tag` on these clips; at this register that warning is expected. Say so in `voice.elevenlabs.notes`.

| Dialect | Tag | Status |
|---|---|---|
| Iraqi | `[strong Iraqi accent]` | Verified |
| Gulf | `[strong Gulf accent]` | Provisional: not read aloud; needs a native Gulf listener to confirm the accent. Treated as unverified |
| Saudi | `[strong Saudi accent]` | Provisional: not read aloud; needs a native Saudi listener to confirm the accent. Treated as unverified |
| Egyptian | `[strong Egyptian accent]` | Unverified |
| Levantine | `[strong Levantine accent]` | Unverified |

Only Iraqi is verified. The validator counts a tag as verified only when its `verified` note in `scripts/elevenlabs_rules.json` doesn't start with "provisional", so the Gulf and Saudi tags still raise a soft `el_tag_unverified` until a native review: use them, and tell the creator to delete the tag if it gets read aloud. The validator also warns when a clip lacks the tag (`el_accent_tag`) and fails a tag for the wrong dialect (`el_accent_mismatch`). Accent tags don't count toward the one-emotion-tag limit. On Multilingual v2 and other untagged models, the accent comes only from the voice itself and from spelling: recommend a voice cloned from a speaker of that dialect.

## Allowed tags (v4 / v4 Turbo / v3)
`[pause]` · `[long pause]` · `[excited]` · `[whispers]` · `[sighs]` · `[laughs]`

- **Tags are in English** even when the text is Arabic.
- **Use them sparingly:** at most one emotion tag per clip. `[excited]` easily overshoots; in the `professional` and `deadpan` styles, use none.
- **Only the style's emotion tags** (`el_style_tag` warns otherwise):

| Style | Allowed emotion tags | Suggested | Stability (v4 / v4 Turbo / v3) |
|---|---|---|---|
| `yapping` | `[laughs]` `[sighs]` `[excited]` | `[laughs]` | Natural |
| `infotainment` | `[excited]` | none | Natural |
| `asmr_whisper` | `[whispers]` | `[whispers]` | Robust |
| `professional` | none | none | Robust |
| `hype` | `[excited]` `[laughs]` | `[excited]` | Creative |
| `deadpan` | none | none | Robust |
| `relaxed_narrator` | `[sighs]` | none | Robust |

  The source of truth is `el` in `scripts/styles.json`; update both together. Pause and accent tags are always allowed. For AI-voice settings in `asmr_whisper` and `deadpan`, see `speaking-styles.md` §3.
- **Descriptive tags** such as `[confidently]` or `[calmly]` match the style of ElevenLabs' own examples but **are not on the verified list**. Offer them only as an optional experiment, labeled "unverified: delete it if it gets read aloud". The validator warns on them.
- For **no pause** between sentences, use a comma, not `...` or `[pause]`.
- The script options themselves stay plain speech. Tags live **only** in `voice.elevenlabs.clips`.
- Replace the script's `/` pause markers with `...` or `[pause]` in clips; a raw `/` may be read aloud.

## Pronunciation
Phoneme controls work for English only. For Arabic, pronunciation is controlled **only by spelling**: apply the spelling pass from `voice-dialect.md` and add diacritics only where a word is likely to be misread. Clip wording may differ from the final script only by those spelling or synonym fixes (the validator warns otherwise).

## Starting settings (adjust by ear)
| | v4 / v4 Turbo / v3 | Multilingual v2 |
|---|---|---|
| Stability | Start at the style's value (table above). Toward **Robust** if the accent drifts or the delivery sounds over-excited; toward Creative if it's flat | 0.45–0.65 (top of the range for `asmr_whisper` and `deadpan`) |
| Similarity | 80–90% | 0.80–0.90 |
| Style | n/a | 0–0.2 |
| Audio effects | **Off** (add sound effects in the edit, where you control their timing) | n/a |
| Output | WAV / PCM 44.1 kHz if the plan allows, else the highest MP3 | same |

## Workflow given to the user
The dashboard shows these steps:
1. Generate **each beat as its own clip**, so a bad line costs one regeneration, not the whole script.
2. Generate **3 takes per clip**; keep the one with the right dialect and stress.
3. Name the files `01-hook` … `06-cta`.
4. Listen to the hook clip hardest: it decides whether people stay.
5. If a word keeps being misread, try the diacritized spelling, then an unambiguous synonym.

## Disclosure and consent
A cloned voice is realistic AI audio: set `publish.ai_label: true` (the validator requires it for AI voice). Only clone your own voice, or one you have written permission to use.
