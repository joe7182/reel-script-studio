# Stage 5 — Council

The council sees the full picture (`intake`, `research`, `idea`, `audit`, `concept`, `viewer_mind`, `beats`, `presets`, `final_script`, `self_assessment`, `validation`) and decides. In a single context it is one model reviewing from five angles with written criteria: its strength is discipline, not independence. Describe it to users that way. Set `council.mode` to `single_context` or `subagents`.

## Members
| Member | Checks | Scores | Power |
|---|---|---|---|
| **Strategy Director** | Serves the goal and the audience's awareness stage? CTA matches the goal and destination? | `goal_fit`, `awareness_fit` | approve / revise |
| **Creative Director** | Is every line better than the creator's original and than the common angles in `research`? Did the Viewer Mind test the strongest hooks fairly, and is the chosen one the Recommended one? Does the payoff (`concept.payoff_line`) land before the CTA? Do slot labels fit the Reel type? Runs the adversarial hook step. | `distinctiveness`, `hook_strength` | approve / revise |
| **Voice Guardian** | Sounds like this creator, in their dialect, **at the chosen register**? Any unclear, foreign or too-local word (`dialect_foreign`, `register_heavy_word`)? Any AI tell (`craft-standards.md` §3)? Spelling pass done? Can every «هو / هي / this / it» be traced to something the viewer already heard or saw, and does the viewer get the input before what the tool does with it? | `dialect_accuracy`, `naturalness`, `clarity` | approve / revise |
| **Performance Analyst** | Can the viewer act on `idea.takeaway` from the voice lines alone? Beats the creator's best script on what made it win? Biggest drop-off risk? Re-hook every 5–8 s? A `human_texture` line (or a `{{…}}` slot) in the Recommended script? | `takeaway_value`, `dropoff_risk` | approve / revise |
| **Trust Officer** | Any claim without evidence? Proof line without footage, or "try it yourself" standing in for proof? `proof_shots` exact enough to film? Overpromise? **Does every Retention promise get delivered in every combination (by every Solution or every Proof option)?** Regulated niche handled? | `claims`, `proof` | approve / revise / **reject (veto)** |

## Rubric (1–5 per criterion)
Score each criterion against these anchors. 5 is earned, not assumed: a 5 needs a reason that names what earns it.

| Criterion | 5 | 4 | 3 | 2 | 1 |
|---|---|---|---|---|---|
| **goal_fit** | Every beat moves toward the stated goal; the CTA sends people to the stated destination | Serves the goal; one beat drifts | Only the CTA serves the goal | The CTA asks for a different action than the goal | No visible goal |
| **awareness_fit** | Hook and CTA match the stage exactly (problem-aware opens on the pain, not the product) | Matches; one beat assumes slightly more or less knowledge | Roughly right; the hook explains what the viewer already knows | The hook assumes knowledge the viewer lacks | Wrong audience |
| **distinctiveness** (vs the common angles and the original) | No line could sit in the typical Reel on this topic (`research` angle sources); creator-specific detail throughout | One line is interchangeable with the typical Reel | Distinct structure, but half the lines are generic | The common angle in nicer words | It is the common angle |
| **hook_strength** | The package stops a muted viewer and a viewer with sound on; visual and overlay each add; the Recommended hook is the top-scored one | Strong spoken line; visual or overlay only supports it | Clear but no tension, or the overlay echoes the line | Vague or slow start | Greeting or generic opener |
| **dialect_accuracy** (incl. register) | Every word fits the dialect and `meta.register`; swaps listed; spelling pass done | One word to confirm | Two or three words off-register or from another dialect | Mixed dialects, or stiff written Arabic in a dialect script | Wrong dialect |
| **clarity** | Every pronoun and «هاي / this» has a subject the viewer already has; information comes in the order the viewer needs it (input before process, problem before fix) | One reference the viewer must guess for a second | Two unclear references, or one step that needs a later line to make sense | The viewer has to rebuild the order themselves | Can't follow without the caption |
| **naturalness** | Sounds spoken: uneven rhythm, the sample's connectors, no AI tells | One tell (a list of three, a mirrored pair) | Two tells, or every sentence the same length | Reads as written text; several tells | A template |
| **takeaway_value** | The viewer can act on `idea.takeaway` tonight from the voice lines alone | Actionable, but one detail lives only in the caption | The viewer knows what to do, not how | An insight with no action | Nothing to take away |
| **dropoff_risk** (5 = low risk) | A turn or new visual every 5–8 s; a Retention line specific to this Reel | One slow stretch | A stock Retention line, or a long flat middle beat | The payoff is given away in the hook, or a flat stretch of 10 s or more | No reason to stay past second 3 |
| **claims** | Every factual or result claim is shown, sourced or first-person; opinions stay firm | One claim softened that could have been shown | An unverified claim, softened but still leaned on | A claim kept that needs evidence | A false or regulated claim kept |
| **proof** | Slot 5 shows it happening, with declared footage or exact `proof_shots` to film | A real screenshot or result, static | First-person telling with no visual | "Try it yourself" or "trust me" as the proof | Simulated, or claimed proof with no footage |

Scoring rules (the validator enforces the first two):
- Each verdict carries `scores` with that member's keys (the Voice Guardian has three). The validator checks that all of them are present and numeric (a missing or non-numeric score is a hard failure); keeping to whole numbers on the 1–5 anchors is the council's own discipline.
- **Approve requires every score ≥ 4** (`council_score_inconsistent`). Any score below 4 means **revise, with a concrete rewrite** in `changes`: the exact old line → the exact new line, not "make it punchier".
- Round 1 is a real critique. Read it as the `skeptic` persona would, compare it with the creator's original, and ask what a top creator in this niche would still change. Approving with 4s is fine; a round 1 where everyone gives 5 everywhere triggers `council_rubber_stamp`. In the test runs, the council approved everything in round 1 in 9 of 10 runs.

## Adversarial hook step (Creative Director)
The Creative Director writes one better hook package; if it outscores the Recommended hook, it replaces it in the next round.
- The challenger is a full package: spoken line, `visual`, overlay, and a mechanism of its own (rule below). Score both on clarity, tension, relevance and credibility, **before** looking at which one is tagged Recommended.
- The challenger's mechanism must differ from every hook that stays, or equal the mechanism of the Bold hook it replaces (`mechanism_repeat` is a hard failure).
- If the challenger's total is higher, vote revise. The change: the challenger becomes the Recommended hook, the old Recommended becomes Bold and replaces the weakest Bold hook. That keeps 5 hooks with 5 different mechanisms and leaves the Safe edit untouched.
- If it isn't higher, say so in `reason` with both totals. That is evidence the Recommended hook was tested.
- Run it in every round except the last, where no revision can follow.

## Verdict format (one per member, every round)
```json
{"member":"Performance Analyst","verdict":"revise","scores":{"takeaway_value":3,"dropoff_risk":4},"reason":"The spoken solution never says what goes in the file; the takeaway lives only in the caption.","quote":"وحط بيه ملف واحد عنك وعن أسلوبك","weakest_line":"وحط بيه ملف واحد عنك وعن أسلوبك","changes":["s1: «…وحط بيه ملف واحد عنك وعن أسلوبك.» → «…وارفع ملف واحد: منو إنت، جمهورك، وأمثلة من كلامك.»"]}
```
- `quote`: the **exact** text the verdict is about. `weakest_line`: the weakest line in the script, quoted exactly, **even when approving**. An approval that can't name a weakness hasn't looked. (The validator checks quotes in the **last** round only and warns when one isn't found in the script; earlier rounds quote lines that later revisions changed.)
- Reasons point at specific beats or option ids. Never "could be stronger".
- **Every verdict in the last round carries a `basis`** (`research.md` §6): the opened source, the creator's data or the craft rule the verdict rests on (`basis_missing` / `basis_invalid` are hard). Example: `"basis": {"type": "research", "ref": "r1"}`.
- When `viewer_mind.unresolved` is set, the decision is `ship_with_issues` at best, with the issue in `open_issues`.
- Check that the Recommended tag sits on the top-scored hook.

## Decision rules
1. **Trust beats creativity.** A Trust Officer reject blocks shipping.
2. **The goal beats taste.** When Strategy and Creative disagree, the option that serves the stated goal wins.
3. Any **hard** validator failure still open → automatic revise.
4. All approve → **ship**. Approvals with noted weaknesses → **ship_with_issues** listing them in `open_issues`.

## Revision loop
- A second round happens **only** when a member votes revise or reject, including a won adversarial hook step. Never add rounds for their own sake.
- "Revise" sends the merged `changes` list back to Stage 3, then the validator runs, then the council reviews again.
- Revision rounds: **Full: at most 2. Quick: at most 1.** After the last round, ship the best version as `ship_with_issues` and list what's unresolved. Never loop forever; never hide what's left.
- Record every round in `council.rounds`.

## Trust veto fallback (never ship a vetoed claim)
If the Trust Officer still rejects after the last round:
1. Remove the claim from every option it appears in. Replace a proof or result line with a demonstration option flagged `needs_footage` (with `proof_shots`), or with an honest opinion.
2. Mark the claim's action `remove` in `audit.claims`, re-run the validator, and have the Trust Officer review once more.
3. If the Reel cannot work without the claim, set `final_decision: "blocked_claim"`, put the exact line and the evidence it needs in `open_issues`, and tell the user plainly. The validator fails any other decision after a final-round veto.

## Running members as subagents (opt-in)
Only when the Agent tool exists **and** the user asked for independent reviews (e.g. "use subagents", "independent council"); it costs roughly five times as much. Otherwise run `single_context`; that's the default and is fully valid. When opted in, dispatch five subagents **in parallel**, one per member. Give each one only:
- the path to `result.json`, with an instruction to read it and not to edit it;
- that member's row from the Members table, its two rubric rows, and the verdict format (plus the adversarial hook step for the Creative Director);
- "Return exactly one JSON verdict object and nothing else."

Merge the five verdicts into the round yourself, apply the decision rules, and set `council.mode` to `subagents`. Separate contexts give genuinely independent readings; the decision rules stay the same.

## Output (`council`)
`mode`, `rounds` (each with `round`, `verdicts`, `decision`), `final_decision` (ship / ship_with_issues / blocked_claim), `open_issues`, `summary` (three lines in the user's language, for the chat reply).
