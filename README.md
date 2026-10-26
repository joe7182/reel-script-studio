# Reel Script Studio — a Claude Skill

Turns a Reel idea or draft into a script you can record today, in your own dialect (Iraqi, Gulf, Saudi, Egyptian, Levantine, MSA) or English. It researches the topic first, writes 5 hooks and 3 options for every other beat, then **simulates three real-world viewers (your target viewer, a stranger who doesn't follow you, and a skeptic who has seen this topic before) second by second through the first 3 seconds** of the strongest hooks, including your own, and picks the one that holds them. Every recommendation names its evidence: your own numbers, a source it opened, or a named craft rule. Code checks the measurable rules, a five-angle review has a trust veto, and you get one interactive dashboard: script builder, Viewer Mind, teleprompter, ElevenLabs-ready text, shot table, caption and an `.srt` subtitle file.

Free tool by [@yousif_aljbouri](https://www.instagram.com/yousif_aljbouri/). Share it.

## Requirements
- **Claude** (claude.ai, Claude Desktop/Cowork, or Claude Code). This skill does not run in ChatGPT.
- **Code execution turned on.** On claude.ai: *Settings → Capabilities → Code execution and file creation*. Without it, the skill tells you and stops; it never fakes its checks.
- **Recommended: web search on** (Claude's web search or a Perplexity connector). The skill researches the common angles, checks facts and reads platform guidance before writing. Without it, it says so and works from craft rules and your own data only.

## Install
- **claude.ai / Desktop:** zip the `reel-script-studio` folder, then go to *Settings → Capabilities → Skills → Upload skill*.
- **Claude Code:** copy the folder to `~/.claude/skills/reel-script-studio/`.

Then just paste your script or idea: «عندي فكرة ريل عن…» or "Here's my Reel script…".

## What it can't do
- It reads text and computes timing. **It can't hear your voice, tone or emotion.**
- The "council" is one model reviewing from five angles with written rules, not a team of humans. (In Claude Code, the five run as separate subagents.)
- **No predictions of views, reach or virality.** The Viewer Mind is a simulation that explains *why* a viewer would stay or leave; it never says how many will.
- It records the sources it opened and checks that each one is tied to a decision; it can't prove a page was read.
- **It won't invent your stories or numbers.** When it has none that fit, the script holds a highlighted `{{…}}` blank saying exactly what to fill in, and the dashboard reminds you before you copy or record.
- Dialogue skits and Maghrebi dialects aren't supported yet.

## What it asks the first time, and why
One message, at most 7 short questions, each with ready options (or reply "continue" for defaults):
1. **Language level** (Arabic only): strong dialect, simple dialect every Arab understands, or simplified MSA.
2. **Your niche, audience and content type** (tech, education, travel, food, comedy…): it shapes the vocabulary and what counts as proof.
3. **Up to 2 of your Reels**, ideally one that did well and one that didn't: paste the Insights screen as it appears (English or Arabic), what you said (auto-captions), and the comment keyword if you asked viewers to comment one. The skill reads the numbers itself and shows the clearest differences, e.g. "Shares N vs 0: only your best post has this", how much of each post's reach came from non-followers, and follows gained. Comments that answer a keyword CTA are marked as response to the offer, not proof the content was engaging. Your words teach it how you really talk; the numbers show what worked *for you*. Followers and watch time matter more than likes: they show whether the video reached new people and whether they stayed. Two posts are signals, not proof, and it never predicts views.
4. **Your speaking style**: Yapping, Infotainment, ASMR / whisper, Professional, Hype, Deadpan or Relaxed narrator.
5. **How you record** (own voice, voice-over, screen, or an ElevenLabs model).
6. **Where you post.**
7. **One real story or number** from your work (optional, but it makes the biggest difference).

After that, each new script asks only its goal, the proof you have, and the style as one tap (your usual one pre-selected).

## Tip: your creator profile
After the first run, download **creator-profile.json** from the dashboard's Overview tab (after measuring your real pace in the teleprompter). It keeps your style, content type, how you talk, and what your posts showed. Upload it next time and the intake questions are skipped. Older (v2) profiles are upgraded automatically.

## For maintainers
```
python -m unittest discover -s tests -v                       # validator tests
python scripts/validate.py tests/fixtures/golden.json --dry-run
python scripts/build_dashboard.py tests/fixtures/golden.json --out _preview
```
- ElevenLabs rules live in `scripts/elevenlabs_rules.json` + `references/elevenlabs-tags.md`. Update both together, and update the date.
- Dialect word lists live in `scripts/dialects.json`; native-verified word swaps in `scripts/dialect_corrections.json` (how to add one: `references/voice-dialect.md`, Native corrections).
- `python scripts/insights.py <file> --label best|weak` turns pasted Instagram Insights into an `intake.performance` item.
- Before publishing a change, run the scenarios in `tests/scenarios.md` on claude.ai.

## License
MIT — see [LICENSE](LICENSE). © 2026 Yousif Al-Jbouri ([@yousif_aljbouri](https://www.instagram.com/yousif_aljbouri/)).

دليل الاستخدام بالعربية: [docs/guide-ar.md](docs/guide-ar.md)
