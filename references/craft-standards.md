# Craft Standards (Writer, Council)

Read this before Stage 3. The Creative Director and the Performance Analyst score against it. The validator catches the measurable tells (`scripts/craft.json`). This file covers what code can't see: whether a line sounds like a person who knows the work.

These rules hold in every speaking style. The style (`speaking-styles.md`) sets the delivery on top of them: sentence length, how many questions, fillers, energy, and how the proof beat lands.

About the examples: the Arabic ones are Iraqi at the `light` register, and lines marked *(golden)* come from `tests/fixtures/golden.json`. Creator details in the other examples are **hypothetical**. In a real script they come from the profile, the voice sample or the user's message. Never invent a number or a story and present it as the creator's.

Contents: 1. The bar · 2. Human texture · 3. AI tells · 4. Hook packages · 5. Retention moves · 6. CTA moves · 7. Proof that is real · 8. Captions that add · 9. Last pass before Stage 4

## 1. The bar
One question decides: **would a top creator in this niche post this unedited?** "After a few changes" means no. Three tests make the question concrete.

**Specificity.** Every script holds at least one named moment (a time, a place, an action), one number or object, and one visual or sensory detail. Abstract nouns («النجاح»، «الإنتاجية», "results", "growth") don't count.
- Weak: «الذكاء الاصطناعي يوفّر وقتك ويخليك أكثر إنتاجية.»
- Strong: «أنا كنت أكتب نفس الفقرة عن جمهوري كل صبح. / لمن حسبتها: ربع ساعة يومياً.» *(golden)*
- Why: a morning, a paragraph and a counted quarter-hour. The viewer can picture it, and only this creator could say it.
- Weak: "This app will transform how you manage your money."
- Strong: "Every Sunday night I'd open my banking app and close it before the balance loaded."
- Why: a day, a gesture and a feeling, with no promise attached.

**Takeaway.** After 30 seconds the viewer can *do* one thing, from the spoken lines alone. Write it in `idea.takeaway` before writing the beats (hard-required for tutorial, tips and product). Test: cover the caption and read only the voice lines. Could someone act on them tonight?
- Weak: «استخدم Claude Projects بذكاء.»
- Strong: «سوّي Project واحد بـClaude وارفع بيه ملف «عنّي» بثلاث فقرات: منو إنت، جمهورك، وأمثلة من كلامك.» *(golden)*
- Weak: "Batch your content."
- Strong: "Film all four hooks on Sunday in one sitting, then edit them on Monday."
- Why: the strong versions name the object, the amount and the moment. "Use it smartly" names nothing.

**Distinctiveness.** Measure each line against two real things, not a caricature: the creator's own original, and the common angles found in research (`research.md`). If a line could be swapped into the typical Reel on this topic and nobody would notice, rewrite it. If the original's line is already stronger, keep it. A rewrite must earn its change.
- The typical Reel on this topic *(golden, `r1`)*: a setup walkthrough: create a Project, write the instructions, upload files.
- The script's hook: «بدل ما تشرح شغلك كل مرة من الصفر. / خليه يتذكر عنك.» *(golden)*
- Baseline: "Struggling to stay consistent? In today's fast-paced world, batching is a game changer. Here are 3 tips to level up your content!"
- The script's hook: "I filmed a month of Reels on one Sunday. Here's the one thing I'd do differently."
- Why: the typical version walks through settings or sells a feeling with stock words. The script opens on the viewer's own situation, then the creator's move.

**Concept card (`concept`).** Before the beats, write what the Reel *is*, so every line serves one idea:
- `logline`: one sentence (max 35 words) saying what the viewer sees, learns and feels.
- `promise`: what the hook promises.
- `payoff_beat` and `payoff_line`: where that promise is paid, as exact words from the final script. The payoff comes before the CTA (`concept_payoff`).
- `turn`: the moment the viewer's understanding changes.
- `journey`: 3–6 short lines of what the viewer feels from hook to CTA.
- `details`: when the creator gave a draft, where each important detail went: `speech`, `visual`, `caption` or `cut`, with a reason (`concept_details`). Say on screen what the screen can show, and don't speak what the screen already shows. Never drop the named audience or the core offer silently.
- Weak logline: «ريل عن ميزة Projects بـClaude.»
- Strong *(golden)*: «صانع محتوى يشوف نفسه يكتب نفس الشرح للمرة الثالثة، يسوي ملف واحد يخلي Claude يتذكره، ويشوف النتيجة حيّة بلهجته.»
- Why: the strong one names what the viewer sees, the turn and the proof. Every beat can be checked against it.

**Rhythm and order.** Vary sentence length: let one line run, cut another to two or three words (`rhythm_flat` warns when every sentence is about the same length). Give the viewer the input before what the tool does with it, and the problem before the fix. Never open the hook on a bare «هو / هي / it / they» (`hook_bare_pronoun`): a stranger doesn't know who that is yet.

## 2. Human texture
Every script carries at least one line **only this creator could say**: a story, number, client moment or mistake from the profile's `human_texture`, the voice sample, or the user's message. Mark that option `human_texture: true` and put it where it does work, usually Problem, Proof or the hook. When the creator gave a real detail, **the Recommended script carries it**; `creator_detail_missing` warns otherwise. `human_texture_missing` also warns when no option at all carries one.
- Weak: «كثير من صنّاع المحتوى يعانون من هالمشكلة.»
- Strong: «أول ريل نزّلته عن هالموضوع، حذفته بعد ساعة. / ما عرفت شنو أگول بعد أول جملة.»
- Weak: "A lot of freelancers struggle with pricing."
- Strong: "My first client paid me in pizza. I said yes."
- Why: a confession with a time stamp is believable. A claim about "many people" is a statistic nobody can check.

**No real detail that fits? Never a made-up fact, and the script must still record today.** Write strong lines without one (a demo, a concrete example, the viewer's situation). Use a `{{…}}` slot only when one specific fact would clearly lift the script, and add an open issue asking for it. In a blind test on real drafts, forced slots cost recordability points. The slot is the creator's homework, so make it answerable in ten seconds:
- Iraqi: «لمن حسبتها أول مرة، طلعت {{رقمك الحقيقي: كم دقيقة باليوم تعيد نفس الشرح؟}} كل يوم.»
- English: "The week I counted, it came to {{your real number: minutes a day spent re-typing the same brief}}."
- Weak slot: `{{قصة}}`, `{{add a story}}`. The creator can't tell what fits the line.

How slots behave: each one is timed as 4 spoken words, so the real answer should be about that long; the words inside are ignored by the repeat, sentence and question checks. Slots belong only in spoken option text: one in an overlay, the caption, the cover text, a shot or a proof shot fails `slot_misplaced`, and one left in an ElevenLabs clip warns `el_unfilled_slot`. The dashboard highlights every slot and warns before the creator copies or records the script.

**Uneven rhythm.** Real speech mixes a 3-word sentence with a 12-word one. AI writes every sentence at the same length. Vary it on purpose, especially in the middle beats.
- Weak: «هاي الطريقة سهلة وسريعة. تقدر تطبقها بأي وقت. النتيجة راح تعجبك.»
- Strong: «جرّبتها. / ثلاث أيام أكتب نفس الطلب، والجواب يرجع بارد مثل أول مرة.»
- Weak: "It's simple to set up. It works on any device. You'll love the results."
- Strong: "I tried it. Three mornings in a row I sent the same request, and the answer came back like it had never met me."
- Why: three equal sentences are a written list. A short line and then a long one sound like someone remembering.

**Spoken asides** («بصراحة»، «والله», "honestly", "look") appear only where the voice sample uses them, at most once per script, and only in styles that allow fillers (`yapping`, `hype`). Asides sprinkled in for warmth are a tell of their own.

**The fingerprint is where human texture starts.** When `intake.voice_fingerprint` has `status: "ok"`, it holds how this creator really talks: their connectors, their signature phrases (repeated 2–3-word chunks), their usual sentence length and how much English they mix in. Use one signature phrase where it would naturally fall (golden: the creator says «هسه أراويك شلون» in both posts, so a demo beat can open with it), keep at least one of their top connectors, and stay near their sentence length and English mix. Don't paste every phrase in: one, in the right place, sounds like them; five sounds like an impression. The validator warns `voice_drift` when the script drifts from the fingerprint.

## 3. AI tells to avoid
Code flags some of these: `cliche_hard` (hard), and `cliche_soft`, `contrast_cliche`, `rhetorical_overload`, `tricolon` (soft). The council should catch the pattern even when the wording slips past the lists.

| Tell | Why it sounds machine-made |
|---|---|
| "Not X, it's Y" more than once | It's the default AI way to manufacture an insight. By the second one, the viewer hears the formula. It appeared in 4 of 5 test scripts as «المشكلة مو بالأداة، المشكلة ب…». |
| Three-item lists | The rule of three is the model's default cadence. People usually list one or two things. A list is fine when it *is* the content (the three parts of a file, numbered steps); the tell is the decorative list of adjectives or benefits. |
| Rhetorical-question chains | Questions stall. More than two in a script sounds like a sales page. Most styles allow fewer; yapping allows three, and then three is the cap (`speaking-styles.md` §1). These are questions *in the script*, unrelated to the per-script intake questions asked of the creator. |
| Hype words | They name an emotion instead of causing one («مذهل», «سر», "insane", "hack"). |
| Symmetric sentence pairs | Mirrored halves («كل ما… كل ما…», "the more you X, the more you Y") read as written, not spoken. |
| Generic openers | «في عالم اليوم», «هل تعلم», «دعونا», "did you know", "let's dive in" delay the point and announce AI in the first second. |
| A moral at the end of every beat | It turns a story into a sermon. Let the proof make the point. |

Human rewrites:
- «المشكلة مو بالأداة، المشكلة بطريقة استخدامك.» → «إنت تفتح شات جديد كل مرة، فهو ينسى كل شي گلته أمس.» Show the cause instead of announcing a reversal.
- "It's not about the camera, it's about the script." → "I shot this on a five-year-old phone. The script did the work."
- «أسرع، أسهل، وأرخص.» → «وأهم شي: مجاني.» Keep the one advantage the viewer will remember.
- "Faster, easier, and cheaper." → "And it's free."
- «تعبت؟ ملّيت؟ تريد حل؟» → «إذا كتبت نفس الطلب ثلاث مرات اليوم، هذا الفيديو إلك.» Turn the questions into one condition the viewer can recognise.
- "Tired? Overwhelmed? Want a fix?" → "If you've typed the same prompt three times today, watch the next ten seconds."
- «سر خطير محد يعرفه» → «زر صغير بالإعدادات، أنا ما شفته سنتين.» Replace the hype word with the concrete thing it stands for.
- "This insane hack" → "A setting buried three menus deep."
- «كل ما تكتب أكثر، كل ما تتعلم أكثر.» → «بأول شهر كتبت ثلاثين سكربت. خمسة بس نفعت.» Replace the mirror with an uneven, real count.
- "The more you post, the more you grow." → "I posted every day in March. Two videos did anything."
- «هل تعلم إن أغلب الناس…» → «البارحة شفت صاحبي يكتب نفس الإيميل للمرة العاشرة.» Open on a moment. The original was also an unverified factual claim.
- "Did you know most people…" → "My friend just rewrote the same email for the tenth time."
- «…وهنا تعرف إن التنظيم هو مفتاح النجاح.» → «…وطلع الجواب بلهجتي من أول طلب.» End on the result, not the lesson.
- "…and that's why consistency is everything." → "…and the reply came back in my own words, first try."

## 4. Hook packages
A hook is **three layers written together**: the spoken line (`text`), the first-frame `visual` (hard-required), and the overlay (`onscreen`, 2–6 words). Muted viewers get the visual and the overlay. Viewers with sound on get all three. Each layer must work alone and add something when combined.

**The overlay is a headline that adds**: a number, a label, the stakes, or the question the line raises. It never repeats its spoken line (70% shared words): on any option of the Recommended script that is a hard failure (`overlay_echo_recommended`), on the other options a warning (`overlay_echo`). A hook's overlay also doesn't describe its own first frame (`overlay_echo_visual`, soft): the picture already says that. The visual is already moving and already on-topic; "face to camera" alone is not a visual idea.

- Weak: spoken «بدل ما تشرح شغلك كل مرة» · overlay «لا تشرح شغلك كل مرة» · visual «وجهك للكاميرا».
- Strong *(golden h1)*: spoken «بدل ما تشرح شغلك كل مرة من الصفر. / خليه يتذكر عنك.» · visual: a screen recording of the cursor typing the same paragraph for the third time, with a counter showing ٣/٣ · overlay «٣ مرات اليوم؟».
- Weak: spoken "Stop pricing by the hour." · overlay "Stop pricing by the hour" · visual: talking head.
- Strong: spoken "Stop pricing by the hour." · visual: a calculator showing 40 × 25, then the total crossed out · overlay "What I charge now: per project".
- Why: in the weak packages the overlay echoes the line and the visual says nothing about the topic.

The same test holds for every beat's overlay:
- Weak: spoken «أنا كنت أكتب نفس الفقرة عن جمهوري كل صبح.» · overlay «نفس الفقرة كل صبح». Strong *(golden p1)*: overlay «≈ ٧ ساعات ونص بالشهر». The line gives the morning; the card adds the monthly cost.
- Weak: visual "phone 25 cm from the mouth, slid to 5 cm" · overlay "Moving the phone closer". Strong: overlay "25 cm → 5 cm". The card gives the number the eye can't measure.

Eight packages across Reel types (creator details hypothetical):

| Type | Spoken line | First-frame visual | Overlay | Mechanism |
|---|---|---|---|---|
| Tutorial | «صوت ريلك ضعيف لأن المايك بعيد عنك شبر.» | Phone on a table 25 cm away; a hand slides it to 5 cm and the waveform jumps | «٢٥ سم ← ٥ سم» | Mistake |
| Tips | "Cut the breath before your first word." | Timeline zoomed in: the silence before the first word highlighted, then deleted | "Before: 0.5 s of nothing" | Specific tip |
| Product | «هذا الدفتر بيه فكرة كل ريل نزّلته هالسنة.» | Hand flipping pages full of crossed-out hooks | «٤٧ فكرة · ٩ نزلت» | Demonstration |
| Case study | "I changed one caption. Look at the comments." | Split screen: the two posts' comment counts (real screenshots only; the overlay uses their real numbers) | "2 comments → 40" | Result (proof-safe) |
| Story | «أول عميل دفعلي، رجّعتله فلوسه بعد يومين.» | Face to camera, then a blurred transfer screen held up | «ليش رجّعتها؟» | Curiosity gap |
| Opinion | "Stop writing your hook first." | Creator deleting the first line of a doc | "Write the ending first" | Strong opinion |
| Comparison | «جرّبت تطبيقين للمونتاج أسبوع كامل. / واحد حذفته باليوم الثالث.» | Two phones side by side, one app icon dragged to the trash | «اليوم ٣: انحذف» | Contrast |
| Behind the scenes | "This is take fourteen." | File list scrolling past take_01 … take_14 | "Takes 1–13: deleted" | Pattern break |

The five hooks in a beat use five different mechanisms. The Recommended hook's `visual` becomes `production.opening_frame`.

## 5. Retention move bank
The line after the hook earns the middle. Write it for **this** Reel: a line that would fit any Reel is a template.

**Banned stock lines:** «وبالآخر راح تشوف», «خليك للآخر», "stick around", "wait for it", "by the end you'll see" (`cross_beat_template` warns). «وبالآخر راح تشوف» appeared in 4 of 5 test scripts. The three Retention options use three different moves, and each may promise only what the script delivers in every combination (`beat-engine.md` §3).

- Weak: «وبالآخر راح تشوف النتيجة.» → Strong: «والحل أقصر من المشكلة: تكتبه نوبة، وترتاح منها.» *(golden)*
- Weak: "Stick around till the end." → Strong: "The fix is shorter than the problem: you write it once and you're done."
- Why: the strong line names what is coming and why it's surprising: the end of a problem the viewer is about to recognise. The stock line only asks for patience.

**Promise the payoff the viewer already wants.** At second 3 the viewer has only the hook. A retention line about "the receipt", "the result" or "the proof" means nothing yet, because nobody wants evidence for a problem they haven't felt. Promise the payoff of the problem that comes next instead.
- Weak: "Wait till you see the receipt." Strong: "Two minutes of setup, and you never type that brief again."
- Weak: «وبالآخر أراويك الإيصال.» Strong: «والإعداد كله ياخذ دقيقتين، / تسويه مرة وما ترجعله.» *(golden)*

| Move | What it does | Iraqi | English |
|---|---|---|---|
| **Open loop** | Names the payoff, then delays it | «وگبل لا تسكّر: أگلك السطر الوحيد اللي لازم يدخل بالملف.» | "Before you scroll: there's one line that has to go in that file." |
| **Stake escalation** | Raises the cost of not fixing it | «وكل دقيقة تعيدها، تروح من وقت التصوير.» *(golden)* | "And every month you wait, that client keeps paying last year's rate." |
| **Mid-reveal** | Gives part of the answer early, so the rest feels earned | «والإعداد كله ياخذ دقيقتين، / تسويه مرة وما ترجعله.» *(golden)* | "The fix is one file. What goes in it is where people get it wrong." |
| **Counter-intuitive turn** | The answer goes against what the viewer expects | «والحل أقصر من المشكلة: تكتبه نوبة، وترتاح منها.» *(golden)* | "Weirdly, the fix made my prompts shorter." |
| **List counter** | Numbers the steps so the viewer counts along | «أول شي، وهو اللي محد يسويه: سمّي الملف باسم جمهورك.» | "First one, and it's the one everyone skips: name the file after your audience." |
| **Pattern break** | A visual cut that the line calls out | «لحظة، خلّي أقلب الكاميرا: هذا شكل الملف من جوّا.» | "Hold on, let me flip the camera. This is what the file looks like inside." |

Through the whole script, re-hook every 5–8 seconds: a new visual, a turn, or an on-screen reveal.

## 6. CTA move bank
The CTA comes after the value, asks for one step, and says what the viewer gets. All three options serve the stated goal. Never engagement bait.

**Variety rule:** the three CTA options use **three different moves and three different opening words**. `opener_monotony` warns when all three start the same way. In the test runs every CTA began «احفظ الفيديو و…».

- Weak: «احفظ الفيديو وتابعني للمزيد.» → Strong: «احفظ الفيديو، وسوّي الملف الليلة قبل لا تنسى.» *(golden)*
- Weak: "Save this and follow for more!" → Strong: "Save this for the next time a client asks for 'one small change'."
- Why: the strong line gives the save a reason and a moment. "For more" promises nothing.

| Move | Use when | Iraqi | English |
|---|---|---|---|
| **Save-because-reason** | Goal: Saves | «احفظ الفيديو، وسوّي الملف الليلة قبل لا تنسى.» *(golden)* | "Save this for the next time a client asks for 'one small change'." |
| **Comment keyword** | A real resource exists; fill `publish.automation` | «اكتب «ملف» بالتعليقات وأرسلك القالب اللي أستخدمه.» *(golden)* | "Comment RATES and I'll send you the email I use to raise my prices." |
| **Follow-for-part-2** | Part 2 is really planned | «بالجزء الثاني أفتح الملف سطر سطر. تابعني حتى يوصلك.» | "Part two is the file itself, line by line. Follow so it reaches you." |
| **Try-and-report** | Goal: comments, shares | «جرّبها على شات واحد اليوم، وگلّي بالتعليقات شكد وفّرت.» *(golden)* | "Try it on one email today, then tell me how long it took." |
| **DM resource** | Goal: Leads; the resource exists | «ابعثلي «قالب» بالخاص، وأرسلك نفس النسخة اللي بالفيديو.» | "DM me TEMPLATE and I'll send the exact file from this video." |
| **Loop-back** | Goal: Reach (rewatches) | Last line «وإذا بعدك تكتب نفس الفقرة كل يوم، تذكّر:» flows into the hook «بدل ما تشرح شغلك كل مرة من الصفر…» | Last line "So tomorrow, when you open a blank chat, remember:" flows into the hook "Your AI forgets you every single morning." |

Loop-back test: read the last line, then the first, aloud. They must sound like one sentence. A loop-back asks for no explicit action, so for Saves or Leads goals use it as the Bold option only.

## 7. Proof that is real
Demonstration beats claims. In order of strength: the thing happening on screen → a real screenshot or result → the creator's own first-person experience («أنا…») → a claim, which never counts as proof.

**"Try it yourself" is an invitation, not proof.** It belongs in the CTA (try-and-report), never in slot 5 as the evidence. The same goes for "trust me" and "it really works".

When the creator declared no proof, write demonstration options flagged `needs_footage`, and fill `production.proof_shots` with exactly what to film: `shot`, `how`, `duration`. The validator fails `proof_shots_missing` otherwise.
- Weak: «جرّبها بنفسك وراح تشوف الفرق.»
- Strong: «هسه شوف. / كتبت «سكربت ريل عن القهوة»، وطلع بلهجتي مباشرة.» *(golden)*, with the proof shot «الطلب الحي داخل الـProject · تسجيل شاشة كامل بدون قص، الطلب بسطر واحد · 6 ث».
- Weak: "Trust me, it works. Try it yourself."
- Strong: "Here's the request, unedited. Watch the reply come back in my voice.", with the proof shot "Full screen recording, no cuts · 6 s".
- Why: the viewer watches it happen instead of being asked to believe it.

A personal number stays personal: «ربع ساعة يومياً» is the creator's own count, said as «أنا…». It never becomes «راح توفّر ربع ساعة» (a promise about the viewer).

## 8. Captions that add
The caption (`publish.caption`) does a job the video can't: **the steps written out, a resource, or a question that earns comments.** It is never a transcript; `caption_echo` warns at 60% shared words. The first line works alone (about 125 characters show before "more").
- Weak: «بدل ما تشرح شغلك كل مرة، خليه يتذكر عنك! سوّي Project واحتفظ بالفيديو.» It is the script again.
- Strong *(golden)*: «ملف «عنّي» اللي أرفعه بكل Project، بثلاث فقرات:» then the three paragraphs, numbered and spelled out, then «إنت شنو أول سطر راح تكتبه بملفك؟»
- Weak: "Stop re-explaining yourself to AI! Set up a Project once and it remembers you. Save this!"
- Strong: "The 'About me' file I upload to every Project:" then 1. who you are, 2. who you make videos for, 3. three old scripts pasted as they are, then "What's the first line you'd put in yours?"
- Why: the strong caption gives the viewer something to copy and a question with a real answer.

## 9. Last pass before Stage 4
Read the Recommended script aloud once. If you can predict the shape of the next sentence, rewrite it. Then check:
- The concept card is written; the payoff line sits before the CTA; no line could sit in the typical Reel on this topic.
- The Viewer Mind chose the Recommended hook (`viewer-mind.md`), and the Retention line answers what the target viewer wondered at second 3.
- `idea.takeaway` can be acted on from the voice lines alone.
- The Recommended script holds a `human_texture: true` line, or a `{{…}}` slot naming the real detail to add. No invented fact.
- Every hook has a `visual`, and an overlay that adds. No overlay repeats its spoken line, least of all in the Recommended script.
- Three Retention moves, three CTA moves, three different CTA opening words. No stock lines.
- "Not X, it's Y" at most once. At most two questions in the script (fewer if the style says so; yapping allows three). At most one list of three.
- The rhythm, energy and proof move fit the chosen style, and no `voice_drift` warning is left unexplained.
- Proof is footage or declared evidence. If footage is still to be filmed, `proof_shots` says exactly what to film.
- The caption adds something the video doesn't say.
- **The CTA is the last thing said.** Housekeeping (a backup tip, a disclaimer) goes before the ask or into the caption; a blind judge marked down a script that ended on a chore after its CTA.
- **No point is made twice.** If two lines give the same advice, merge them. When the creator's draft already filled its time, the rewrite is not longer (`rewrite_growth`); a real test of another version grew 123 → 146 words by repeating advice.
- The Recommended hook package carries something specific: a number, a name or a concrete object (`hook_specificity`). In a public test of a hook scorer, specificity was the only property that separated stronger hooks from weaker ones.
