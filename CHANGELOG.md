# Changelog

## 2.2.2 — 2026-10-15 (public release)
- LICENSE: MIT (open source).
- Arabic user guide for all Arab readers (docs/guide-ar.md).

## 2.2.1 — 2026-10-13 (from the owner's first claude.ai test)
- Quick mode now shows the Idea (research and sources) and Viewer Mind tabs too (6 tabs). The first real test ran Quick without being asked and hid them.
- Quick runs only when the creator literally says "quick" or «سريع».

## 2.2.0 — 2026-10-13 ("Research + Viewer Mind")
- **Research stage (Stage 1b):**
  - the skill writes decision questions, then researches the common angles, the facts, the audience's words and current platform guidance
  - every opened source is recorded with what it changed
  - the Reel names the common angle it avoids
  - without a search tool it says so and uses craft rules and your data only
- **Viewer Mind:**
  - three specific viewers (your target viewer, a stranger who doesn't follow you, and a skeptic who has seen the topic) are simulated second by second through the first 3 seconds of the strongest hooks and your own opening: what they see, what they've heard so far, what they think, and whether they stay
  - the hook that holds them becomes the Recommended one
  - if your original wins, it stays
  - code checks that "heard so far" matches the real words at the real pace, that the first frame matches the planned visual, and that the choice matches the simulation
  - no percentages and no predictions
- **Evidence on every recommendation:** audit findings, Viewer Mind verdicts and the council's final verdicts each name a basis: your data, an opened source, or a named craft rule. Claims carry an evidence status (shown on screen, from a source, your word, no evidence, opinion).
- **Concept card:** a logline, the promise, the exact payoff line (before the CTA), the turn, the viewer's journey, and where each detail of your draft went.
- **Writing checks:**
  - flat rhythm
  - a hook that opens on a bare pronoun
  - a first frame that only illustrates the words
  - a hook package with no number, name or concrete object
  - a rewrite that grows a draft that already filled its time
  - "stop scrolling" openers (hard)
- **Council:** the Voice Guardian also scores clarity (pronouns, information order).
- **Instagram skip rate** is read from pasted Insights and compared between your posts (lower is better).
- **Request routing:** a quick edit gets a direct answer; "audit only" gets findings plus the Viewer Mind Before; new scripts get the full pipeline. The audit has no finding quota.
- **Dashboard:**
  - new Viewer Mind tab (persona cards, a 0–3 s strip, Before/After)
  - concept card
  - research sources with links
  - evidence chips
  - a "not re-checked" banner after you edit text
- **Schema `rss-2.2`:** `generic_baseline` is now optional. A 2.0 result gets one clear message to re-run Stages 1–3.
- Permanent regression probes from the 3.0.0-rc3 comparison (that validator passed «طالعت», «نتيجة مضمونة» and greeting hooks).
- **Honesty:** a weak idea gets an honest take (what is weak, what is better, your call). On Rethink, the skill asks once and then writes your choice at full quality.
- **Exact words you ask to keep** (series name, keyword) are hard-checked. Unmeasured claims in the voice ("in one second", "unedited", "understands exactly") are blocked unless evidenced. `{{…}}` slots are optional, never forced.
- **Blind test on the owner's real drafts** (tests/release-report.md): round 1 lost on honesty; after fixes, round 2 scored 25/30 and 28/30, at parity with 3.0.0-rc3/rc2 (52) and above 2.1.1 (42), within single-judge noise.
- 324 tests.

## 2.1.1 — 2026-10-07 (fixes from the first real-creator test)
- **Instagram Insights reader** (`scripts/insights.py`): paste the Insights screen as-is (English or Arabic UI); reads views, follower/non-follower split, interactions, likes, comments, saves, shares, accounts engaged, profile activity, follows, average watch time and 3-second hold. Handles Arabic-Indic digits, direction marks, K/M/«ألف»/«مليون».
- **Clearer signals:** "only your best post has this" contrasts (e.g. shares N vs 0), non-follower reach, follows gained; comments flagged as CTA-driven when a comment keyword was used. Shown in the Your DNA panel.
- **Voice fingerprint:** the weak post's transcript is used when it's in the creator's own informal voice (dropped only when formal/MSA).
- **Native dialect corrections** (`scripts/dialect_corrections.json`): «طالعت» → «باوعت» verified by a native Iraqi speaker (hard check); provisional entries warn.
- Progress rule: the skill updates its stage list as it works.
- 200 tests.

## 2.1.0 — 2026-10-07 ("Studio v2" + "Creator DNA")

**Added**
- Craft layer: code checks for AI-tell clichés, overlays that repeat the voice (hard on the Recommended script), stock retention lines, "not X, it's Y" overuse, question overload, caption echo, CTA monotony.
- Schema v2: language level (strong / simple dialect / simplified MSA), takeaway, hook visuals, council rubric scores, proof shot lists, generic-AI baseline, human texture.
- Creator DNA: 7 speaking styles as data (pace, sentence length, questions, ElevenLabs tags); voice fingerprint from the creator's real transcripts (with drift warnings); performance analysis of a strong vs weak post (signals, not proof); content category; creator profile v3 with automatic v2 migration; style asked as one tap on every script.
- Honest fill-in slots `{{…}}`: when the creator gave no real detail, the script asks for one instead of inventing it; the dashboard highlights slots and warns before copy/record.
- Regulated niches: an independent, negation-aware scan for guarantee wording across every viewer-facing field.
- Studio Night dashboard: redesigned UI, Claw Crew animated council, dedicated ElevenLabs tab (tag chips, copy-for-ElevenLabs), Your DNA panel, Before → After panel, blocked-claim state, SRT, pace calibration, light/dark, RTL/LTR.
- Release audit: 5 end-to-end scenarios, blind A/B vs plain Claude (skill won 2/2), blind craft scoring; 162 tests.

**Changed**
- Dashboard size cap 200 KB (the old 130 KB limit came from the prompt era).
- Council approvals require rubric scores ≥ 4; subagent council is opt-in.

**Known limits (see tests/release-report.md)**
- Hook visuals/overlays still sometimes restate the voice (craft score 3 on one scenario).
- Gulf/Saudi/Egyptian/Levantine wording and accent tags need native review; Iraqi wording needs a native pass (planned v2.2 dialect memory).

## 1.1.0 — 2026-10-02
First complete build of the Skill (it grew out of the Reel Voice-Over Studio prompt, v7.2).

**Added**
- `scripts/validate.py`: standard-library validator covering the schema, exact option counts, all 1,215 beat combinations (duration and repeated phrases, with Arabic normalization), on-screen word limits, hook hedges and greetings, proof honesty, claims and the trust cap, council consistency, ElevenLabs markup per model, and the AI label.
- `scripts/build_dashboard.py` + `assets/dashboard-template.html`: the dashboard, which refuses to build while hard checks fail. Builder with presets, teleprompter, **real-pace calibration**, **SRT export**, **creator-profile download**, Council tab with the validator report, ElevenLabs tab with the rules' verified date, Arabic RTL and English LTR, and copy/download fallbacks.
- Test suite: 47 tests (golden fixture plus one seeded flaw per hard rule).
- Slot labels by Reel type (Story: Setup / Turn / Lesson, and so on).
- Trust veto fallback: a vetoed claim is removed or the result is `blocked_claim`; it never ships.
- Optional fact-checking with any web search tool (e.g. Perplexity).
- Regulated-niche rules, voice-cloning consent, an injection-safety line, and a code-execution requirement.
- Saudi dialect; Eleven v4 Turbo and an "other model" fallback.
- Dialect accent tags for ElevenLabs (`[strong Iraqi accent]` verified by ear on v4) plus dialect diacritics for clips. Tested: `<break>` is silently ignored on v4.
- Intake now asks who the Reel is for and where the CTA sends people.

- End-to-end run of all 10 scenarios (each in a fresh test session); all pass. Fixes from those runs: a `--stage writer` validator mode (the old order made Stage 4 impossible to pass before the council), multi-word product names no longer count as repeated phrases, council quotes are checked in the last round only, trailing punctuation no longer splits words, text-only Reels have no Voice tab, regulated niches are narrowed (budgeting apps aren't "finance"), council subagents are opt-in, and the code-execution stop message is in the user's language.

**Changed**
- Description rewritten as trigger-only.
- Dialect checks are warnings, not failures (shared words caused false positives).
- Quick mode now uses at most 1 revision round.
- Output goes to `rss_work/<slug>/` so scripts don't overwrite each other.

**Removed**
- References to `analyze_media.py` (not built yet; the skill no longer promises it).
- Dialogue routing (unsupported for now; it was promised but had no data shape).
