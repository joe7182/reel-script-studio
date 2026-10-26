# Speaking Styles (Writer, Council, Voice Director)

Read this before Stage 3. The style is how the script *sounds*: sentence length, questions, energy and pace. The six beats, the hook rules and every craft rule in `craft-standards.md` apply in every style; the style changes how each rule is delivered, never whether it applies.

The numbers live in `scripts/styles.json`, and the validator reads them from there. This file explains them; if the two ever disagree, the JSON wins and this file gets fixed.

Contents: 1. The 7 styles · 2. Choosing a style · 3. Style × recording · 4. Content categories · 5. How the validator enforces it

About the examples: Arabic lines are Iraqi at the `light` register; creator details are **hypothetical**. For other dialects, write the same move in the creator's dialect (`voice-dialect.md`); non-Iraqi phrasings of these examples are not native-checked, so a native review is recommended before reusing them as models.

## 1. The 7 styles

| Key | Label | Words per sentence (mean) | Max questions | Fillers | Energy | Pace factor | Body wpm ar / en |
|---|---|---|---|---|---|---|---|
| `yapping` | دردشة عفوية · Yapping (casual ramble) | 6–18 | 3 | yes | 3 | ×1.08 | 138 / 157 |
| `infotainment` | معلومة سريعة · Infotainment (hook & drop) | 5–12 | 2 | no | 4 | ×1.12 | 143 / 162 |
| `asmr_whisper` | همس ASMR · ASMR / whisper | 3–9 | 1 | no | 1 | ×0.8 | 102 / 116 |
| `professional` | مهني هادئ · Professional (measured) | 7–16 | 1 | no | 2 | ×1.0 | 128 / 145 |
| `hype` | حماس عالي · Hype (high-octane) | 3–10 | 2 | yes | 5 | ×1.15 | 147 / 167 |
| `deadpan` | جاف ساخر · Deadpan (flat, ironic) | 4–12 | 1 | no | 1 | ×0.92 | 118 / 133 |
| `relaxed_narrator` | راوي هادئ · Relaxed narrator | 8–18 | 1 | no | 2 | ×0.88 | 113 / 128 |

- **Words per sentence** is the average over the Recommended script, not a limit per sentence. Uneven rhythm (`craft-standards.md` §2) still applies inside the range.
- **Fillers** («يعني»، «بصراحة»، "honestly", "look") only in styles marked yes, and only the ones the creator really uses (their fingerprint's connectors). In the other styles, cut them.
- **Body wpm** is the default body pace × the pace factor. Measured pace (`meta.pacing`) always replaces it.

### `yapping`: casual ramble
- **What it is:** talking to the viewer like a friend over coffee, thinking out loud. **Fits:** lifestyle, comedy, personal stories, opinion; goals Reach, Follows, Comments.
- **Writing:** the longest sentences allowed (6–18), with real connectors and the occasional aside. Up to 3 questions, but each one must be one the creator would really ask. It still has one idea; rambling is the delivery, not the structure.
- **Hooks:** Strong opinion · Specific question · Relatable moment · Instead of X.
- **Proof is "the receipt":** the moment the creator stops talking and shows the thing («شوف، هذا الإيصال»). One concrete artifact in the middle of the chat.
- **ElevenLabs:** allowed `[laughs]`, `[sighs]`, `[excited]`; suggested `[laughs]` once, where the creator would really laugh; stability Natural.
- Weak: «اليوم راح أحچيلكم عن ثلاث نصائح مهمة للتصوير بالموبايل.»
- Strong: «بصراحة، أمس صوّرت نفس اللقطة سبع مرات، / وبالأخير اكتشفت إن الشباك وراي هو اللي خرّبها كلها.»
- Weak: "Today I'm going to share three tips for better phone videos."
- Strong: "Okay, so yesterday I filmed the same shot seven times. The problem was the window behind me the whole time."
- Why: the weak line announces a list; the strong one is a person mid-story, with a count and a culprit.

### `infotainment`: hook & drop
- **What it is:** one sharp fact or fix, delivered fast, then out. **Fits:** tech, education, informational, history, news; goals Saves, Shares.
- **Writing:** short, clean sentences (5–12), no fillers, at most 2 questions. Every sentence moves the fact forward; cut any line that only sets the mood.
- **Hooks:** Curiosity gap · Mistake / warning · Contrast · Demonstration.
- **Proof:** the fact shown on screen: the setting, the source headline, the number in its original context. A sourced fact counts; "trust me" doesn't (`claims-trust.md`).
- **ElevenLabs:** allowed `[excited]`; nothing suggested (the pace carries the energy); stability Natural.
- Weak: «هل تعلم إن أغلب الناس يطلعون من الريل بسرعة؟ تعال أشرحلك ليش.»
- Strong: «قبل أول كلمة بالريل مالتك أكو نص ثانية صمت. قصّها، وراقب الثانية الأولى بالإحصائيات.»
- Weak: "Did you know most people scroll away in the first second? Let me explain why."
- Strong: "There's half a second of silence before your first word. Cut it, then check your 3-second hold."
- Why: the weak line opens on a stock phrase and an unsourced claim; the strong one gives the viewer something to do in the next minute.

### `asmr_whisper`: ASMR / whisper
- **What it is:** soft, slow, close; the sound and the visuals do most of the work. **Fits:** beauty, food, lifestyle, desk and craft routines; goals Reach, Saves.
- **Writing:** very short sentences (3–9), at most 1 question, no fillers, no hype words, no exclamation marks. Leave room for sound: fewer words than the target duration suggests, with `/` pauses.
- **Hooks:** Demonstration · Relatable moment.
- **Proof: show, barely tell.** The proof beat is the result on screen with at most a few words over it. Naming the result is enough; selling it breaks the mood.
- **ElevenLabs:** allowed `[whispers]` only; suggested `[whispers]` at the start of every clip; stability Robust.
- Weak: «هسه راح أوريكم أحلى طريقة لترتيب المكتب، راح تنصدمون من النتيجة!»
- Strong: «هذا الدرج الأول. كل قلم إله مكانه.»
- Weak: "Today I'm showing you the most satisfying desk reset ever, you won't believe it!"
- Strong: "This is the first drawer. Every pen has its own place."
- Why: shouting the promise breaks the spell; the strong line lets the drawer be the hook.

### `professional`: measured
- **What it is:** calm, confident, precise; the expert across the desk. **Fits:** business, education, tech, informational; goals Leads, Sales, Saves.
- **Writing:** complete sentences (7–16), at most 1 question, no fillers, no exclamation marks. Opinions stay firm (`SKILL.md` rule 3); numbers are exact and sourced or first-person.
- **Hooks:** Mistake / warning · Strong opinion · Result · Instead of X.
- **Proof:** the document, the number or the before/after, named once and plainly. The calm delivery makes the evidence the loudest thing in the Reel.
- **ElevenLabs:** no emotion tags; stability Robust.
- Weak: «يا جماعة هاي أهم نصيحة راح تسمعوها بحياتكم عن الفواتير!!»
- Strong: «چنت أرسل الفاتورة بعد التسليم بأسبوع، وأنتظر شهر حتى تندفع. هسه أرسلها بنفس اليوم، وموعد الدفع بأول سطر.»
- Weak: "Hey guys!! This is literally the most important invoicing tip you'll ever hear!"
- Strong: "I used to send invoices a week after delivery and wait a month to get paid. Now they go out the same day, with the due date in the first line."
- Why: the weak line claims importance; the strong one shows the old habit, its cost and the change.

### `hype`: high-octane
- **What it is:** fast, loud, short punches; the result first. **Fits:** fitness, tech launches, transformations, challenges; goals Reach, Shares.
- **Writing:** short sentences (3–10), fillers allowed, at most 2 questions. Energy comes from rhythm and real numbers, **not** from hype words (`craft-standards.md` §3). Short sentences still need verbs: no list fragments.
- **Hooks:** Strong opinion · Result · Demonstration.
- **Proof:** the result on screen, fast, ideally before the explanation. In a regulated niche (`claims-trust.md`), hype is where overpromising happens: every result claim needs declared proof.
- **ElevenLabs:** allowed `[excited]`, `[laughs]`; suggested `[excited]`, at most once per clip; stability Creative.
- Weak: «في هذا الفيديو سوف نتعرف على طريقة رائعة لزيادة سرعة المونتاج.»
- Strong: «ثلاث ساعات مونتاج صارت عشرين دقيقة. شوف، هذا نفس المشروع.»
- Weak: "In this video we will be exploring an amazing way to edit faster."
- Strong: "My edit used to take three hours. Today it took twenty minutes, same project."
- Why: "amazing" names a feeling; the two numbers create it.

### `deadpan`: flat, ironic
- **What it is:** a straight face and a dry fact; the humour is in what is left unsaid. **Fits:** comedy, lifestyle, opinion, relatable work content; goals Shares, Follows.
- **Writing:** short, flat statements (4–12), at most 1 question, no fillers, no exclamation marks, no "lol". Never explain the joke. Put the strongest line last and leave a beat (`/`) before it.
- **Hooks:** Contrast · Strong opinion.
- **The proof is the punchline:** the shot that shows the plain truth (the unused gadget, the empty room) is both the evidence and the joke.
- **ElevenLabs:** no emotion tags; stability Robust. Hard for AI voices (§3).
- Weak: «هههه شوفوا شصار وياي، والله موقف يموّت من الضحك!»
- Strong: «اشتريت ستاند للموبايل بخمسين ألف. صوّرت بيه مرة وحدة. هسه صار يشيل مفاتيح البيت.»
- Weak: "LOL you guys won't believe what happened, this is SO funny!!"
- Strong: "I bought a fifty-dollar phone stand. I used it once. It holds my keys now."
- Why: announcing that something is funny kills it; the flat sequence lets the viewer find the joke.

### `relaxed_narrator`: calm voice-over over visuals
- **What it is:** a calm voice telling what the footage shows, unhurried. **Fits:** travel, history, food, lifestyle; goals Saves, Follows.
- **Writing:** the longest, smoothest sentences (8–18), at most 1 question, no fillers. Write to the footage: each line names something the viewer is seeing or about to see, and adds one thing the picture can't (a name, a date, a smell, a price).
- **Hooks:** Relatable moment · Demonstration.
- **Proof:** the footage carries it; the narrator names the detail that makes it real. Needs real footage of the place or process (`needs_footage` otherwise).
- **ElevenLabs:** allowed `[sighs]`; nothing suggested; stability Robust.
- Weak: «يلا يا شباب! أسرع جولة بشارع المتنبي، لا تفوتكم!!!»
- Strong: «كل جمعة الصبح يفرشون الكتب على الرصيف بشارع المتنبي، / وأول شي يوصلك ريحة الورق القديم.»
- Weak: "Welcome back guys! Today we're checking out the craziest market ever!!!"
- Strong: "Every Friday morning the booksellers lay their books out on the pavement. The first thing that reaches you is the smell of old paper."
- Why: the weak line shouts over the footage; the strong one adds a time and a smell the camera can't film.

## 2. Choosing a style
- **Default:** the profile's `default_style`. Without a profile, the onboarding style question decides; with "continue", `professional`.
- **Every script:** the per-script message always offers the style as a one-tap with the default pre-selected (`intake.md` §3). The answer goes to `intake.style` for this script only. The profile's `default_style` changes only when the creator says so ("make this my default").
- **Mismatch:** when the style fights the goal or the Reel type, say it in one line, offer one alternative, and then do what the creator chose:

| Combination | Why it struggles | Offer |
|---|---|---|
| `asmr_whisper` + Sales or Leads | One soft question at most and no push; the CTA has no energy to land on | `professional`, or keep ASMR with a comment-keyword CTA |
| `hype` + a regulated niche | High energy pushes toward promises the proof can't back | `professional` |
| `deadpan` + a step-by-step tutorial | Flat delivery hides which step matters | `infotainment` |
| `relaxed_narrator` + no footage (talking head only) | The style narrates visuals; without them it drags | `yapping` or `professional` |
| `yapping` + a 15-second target | A ramble needs room; it gets cut into fragments | `infotainment` |

Example: «الهمس صعب يبيع: نخليه مهني هادئ، لو نبقى بالهمس وننهيه بكلمة بالتعليقات؟» / "Whisper is hard to sell with. Switch to professional, or keep the whisper and end on a comment keyword?"

## 3. Style × recording
**Own voice.** The style sets the energy row of the performance sheet (`recording-coach.md` §1). The creator's measured pace beats the style's pace factor.

**AI voice.** Most styles work with the defaults in `elevenlabs-tags.md`. Two don't:
- **`asmr_whisper`:** recommend the creator's own voice. If they use AI: on v4 / v4 Turbo / v3, start every clip with `[whispers]` (after the accent tag for Arabic), stability Robust, similarity 80–90%, pauses as `...`, one sentence per clip, 3 takes per clip. On Multilingual v2 no tags work: clone the voice from a whispered recording, stability 0.65, style 0.
- **`deadpan`:** recommend the creator's own voice; the flat timing is the joke, and AI voices add a smile. If they use AI: no emotion tags, stability Robust, `[pause]` before the punchline, the punchline as its own clip. On Multilingual v2: stability 0.65, style 0, one `<break time="0.4s" />` before the punchline.
- **`hype`** on AI: one `[excited]` per clip at most, stability Creative; if the accent drifts, move toward Natural before removing the tag.

## 4. Content categories
`intake.content_category` is asked once and saved in the profile. It shapes vocabulary and what counts as proof; the format (`idea.type`) is still chosen per script. Scope: content creators.

| Category | Vocabulary | What counts as proof | Common pitfall |
|---|---|---|---|
| `tech` | The exact app, device, setting path; English terms as the creator says them (fingerprint code-switch) | A screen recording of the setting and the result | Reading the spec sheet; speed claims with no test |
| `education` | One concept, in the viewer's words, not the textbook's | A worked example on screen | Three points in 30 seconds |
| `informational` | Plain words; every number said aloud | The source named on screen | "Studies show" with no study |
| `travel` | Place names, prices, times of day, senses | Footage from the place; the ticket or receipt | "Hidden gem" and other stock adjectives |
| `history` | Names, one date, one vivid object | A map, document or photo on screen; source in the caption | A popular myth told as fact |
| `news` | What, when and who said it, in the first lines | The source post or headline with its date | Speculation as fact; stale before it posts |
| `business` | Clients, prices, hours, the actual process | A real (blurred) invoice, dashboard or message | Income claims (regulated: `claims-trust.md`) |
| `lifestyle` | Routines, objects, moments of the day | The routine filmed as it happens | Aspirational vagueness |
| `food` | Ingredients, amounts, texture, sound | The bite, the cross-section, the pan on camera | "Best ever" without showing why |
| `fitness` | Sets, reps, form cues, the body part | A form demo; the creator's own progress | Health claims and guaranteed results (regulated) |
| `beauty` | Product names, shades, skin type | Before/after in the same light, no filter | Skin-health claims; undisclosed ads |
| `comedy` | The audience's everyday words and situations | The punchline landing on camera | Explaining the joke; a CTA that kills the laugh |
| `other` | Taken from the niche line | Whatever the viewer can see happen | Abstract nouns instead of a moment |

## 5. How the validator enforces it
All style checks are **soft**: the council weighs them; they never block a build.
- **`style_rhythm`:** the mean words per sentence of the final script falls outside the style's range. Sentences split at `.` `!` `?` `؟` `…` and line breaks; commas and `/` pauses don't split. Fix the rhythm (split or join sentences), not just the word count.
- **`style_questions`:** more `?` / `؟` in the final script than the style allows.
- **`el_style_tag`:** an emotion tag in an ElevenLabs clip that the style doesn't allow (for example `[excited]` in a deadpan script). Pause and accent tags are exempt.
- **Pace:** durations use the default wpm × the style's `pace_factor`, unless `meta.pacing` (measured) exists. Measured pace always wins.
- **Style vs fingerprint:** `voice_drift` compares the script with how the creator really talks (the fingerprint measures the voice sample, the `best`/`other` transcripts, and the weak post's transcript unless its register is formal, since a formal read-out is not how the creator talks). When the style range and the fingerprint (`sentence_p25`–`sentence_p75`) overlap, write in the overlap. When they don't, the creator's real speech wins (`SKILL.md` rule 1): keep the `style_rhythm` warning and say why in `self_assessment.weaknesses`.
