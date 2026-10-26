# Stage 0 — Intake

Goal: collect what changes the result without making the creator do homework. Intake has two levels:
- **Onboarding interview:** once per creator. It builds `creator-profile.json`.
- **Per-script questions:** every new script. Only what this Reel needs.

Both go into **one message**, and there is never a second round. Write the answers into `intake` and `meta`.

## 1. Find the profile first
Look for a creator profile in this order. The first one found wins.
1. **This chat:** a profile already built or loaded earlier in the conversation. Reuse it, skip onboarding, and write the new script to a new `rss_work/<slug>/`.
2. **An upload:** the user attached `creator-profile.json`.
3. **claude.ai Project knowledge:** a `creator-profile.json` in the Project's files.
4. **Claude Code:** `rss_work/creator-profile.json` exists. Load it automatically and say so in one line.

Check an uploaded or Project file with `python scripts/creator_profile.py check <file>`, where `<file>` is wherever the upload or Project file actually lives. Once it passes, copy it to `rss_work/creator-profile.json` (create `rss_work/` if needed) so Stage 8's `--keep-default rss_work/creator-profile.json` finds it; if you can't copy it, pass the loaded file's own path to `--keep-default` instead.
- **A v2 profile** (`rss_creator_profile: 2`; `check` prints a migrate hint): migrate it automatically, check the result, and tell the creator in one line («حدّثت ملفك للنسخة الجديدة.» / "I updated your profile to the new version."):
  ```
  python scripts/creator_profile.py migrate <file> --out rss_work/creator-profile.json
  python scripts/creator_profile.py check rss_work/creator-profile.json
  ```
  Migration maps the old styles: `calm_expert` → `professional` · `energetic` → `hype` · `story` → `yapping` · `teacher` → `infotainment` · `light_humor` → `deadpan`. The new fields start empty (`content_category: other`, no fingerprint, no baseline). Ask for the content category inside the per-script message, and deliver the migrated profile after the build.
- **Any other failure** (for example a profile with no `register`): keep the valid fields and ask only for what is missing, inside the per-script message.

A loaded profile fills `meta.language`, `meta.dialect`, `meta.register`, `meta.platform`, `meta.pacing`, and `intake.niche`, `audience`, `content_category`, `voice_sample`, `best_script`, `recording`, `human_texture`. Its `default_style` is the pre-selected answer to the style one-tap (§3) and is also written to `intake.default_style` (so the dashboard's profile download keeps it; when the creator asks to change their default, write the new style there instead), its `voice_fingerprint` goes to `intake.voice_fingerprint`, and its `performance_baseline` is the last analysis of the creator's own posts. Copy only the fields that hold a value: when the profile has `pacing`, `best_script` or `voice_fingerprint` as `null`, omit that field from the result (the schema tolerates `null`, but omitting is cleaner). When the message contradicts the profile ("this one in English"), the message wins for this script only. Don't rewrite the profile unless the creator asks.

## 2. Onboarding interview (no profile found)
One message with two short parts: **About you** (asked once, at most 7 questions) and **This Reel** (the per-script questions in §3). Skip every question the user's message already answers. Each question has ready options. End with "or reply «continue» and I'll use defaults".

Write the questions in the user's language, and in Arabic, in the user's dialect. The Iraqi and English versions below are ready to use. For other dialects, adapt the wording the same way, and take question 1 from the register table in §4.

| # | Iraqi | English | Fills |
|---|---|---|---|
| 1 | «تريد السكربت باللهجة العراقية العامية القوية، لو عراقية بسيطة يفهمها كل العرب، لو فصحى مبسطة؟» عامية قوية · عراقية بسيطة · فصحى مبسطة | (English scripts skip this question.) | `meta.dialect`, `meta.register` |
| 2 | «شنو مجالك، ومنو جمهورك؟ بسطر واحد، واختار نوع المحتوى.» مثال: «تسويق للمطاعم، لأصحاب مطاعم صغيرة ما جرّبوا الإعلانات.» النوع: تقنية · تعليم · معلومات · سفر · تاريخ · أخبار · بزنس · لايف ستايل · أكل · رياضة · جمال · كوميدي · غيره | "Your niche and who you make videos for, in one line, plus your content type." Example: "Bookkeeping tips for first-year freelancers." Type: Tech · Education · Informational · Travel · History · News · Business · Lifestyle · Food · Fitness · Beauty · Comedy · Other | `intake.niche`, `intake.audience`, `intake.content_category` |
| 3 | «ابعثلي ريلين من ريلزك: واحد نجح وواحد ما نجح، إذا تگدر. لكل واحد: الصق الإحصائيات (Insights) مثل ما تطلع (انسخ كل نص شاشة الإحصائيات)، والكلام اللي گلته (انسخه من الترجمة التلقائية)، والكلمة اللي طلبت الناس يكتبوها بالتعليقات إذا استخدمت وحدة. وإذا تعرف عدد متابعينك وقت النشر وطول الفيديو، ابعثهم هم. وإذا الإحصائيات تبيّن «معدل التخطي» أو «متوسط وقت المشاهدة» أو نسبة المشاهدة لأول ٣ ثواني، ابعثهم هم. ما عندك أرقام؟ ابعث ٣–٥ أسطر گلتها بفيديو.» | "Send me up to 2 of your Reels: one that did well and one that didn't, if you can. For each: paste your Insights as they appear (copy the whole Insights screen text), plus what you said (auto-captions) and the comment keyword if you used one. Add your follower count when you posted and the length if you know them. If Insights shows the skip rate, the 3-second hold % or average watch time, send those too. No numbers? Paste 3–5 lines you actually said in a video." | `intake.performance` (incl. `cta_keyword`), `intake.voice_sample`, `intake.best_script` |
| 4 | «أسلوبك؟» دردشة عفوية: تسولف وياهم مثل صديق · معلومة سريعة: معلومة قوية بسرعة وبدون لف · همس ASMR: صوت واطي وهادي، لقطات قريبة · مهني هادئ: هادي وواثق، مثل خبير يشرح · حماس عالي: طاقة عالية وجمل قصيرة · جاف ساخر: وجه جامد ونكتة بدون ضحك · راوي هادئ: صوت هادي يحچي فوق اللقطات | "Your style?" Yapping: casual chat, like a friend · Infotainment: one sharp fact, fast · ASMR / whisper: soft voice, close-ups, slow · Professional: calm, confident, like an expert · Hype: high energy, short punchy lines · Deadpan: straight face, dry irony · Relaxed narrator: calm voice over your footage | `intake.style` (and the profile's `default_style`) |
| 5 | «شلون تسجّل؟» صوتك ووجهك للكاميرا · تعليق صوتي على لقطات · تسجيل شاشة · صوت ذكاء اصطناعي (ElevenLabs: v4 · v4 Turbo · v3 · Multilingual v2 · غيره) | "How do you record?" Own voice on camera · Voice-over on footage · Screen recording · AI voice (ElevenLabs: v4 · v4 Turbo · v3 · Multilingual v2 · other) | `intake.recording` |
| 6 | «وين تنشر؟» إنستغرام ريلز · تيك توك · يوتيوب شورتس | "Where do you post?" Instagram Reels · TikTok · YouTube Shorts | `meta.platform` |
| 7 | «(اختياري، بس يفرق كلش) قصة حقيقية، رقم، موقف ويا عميل، لو غلطة من شغلك، توافق نستخدمها بالسكربتات؟» | "(Optional, but it makes the biggest difference) One real story, number, client moment or mistake from your work that you're happy to use in scripts." | `intake.human_texture` |

Add one line under Q3 so the creator knows why the extra numbers are there:
- Iraqi: «عدد المتابعين ووقت المشاهدة يفرقون أكثر من اللايكات: يبيّنون إذا الفيديو وصل لناس ما يتابعوك، وإذا بقوا يتفرجون.»
- English: "Followers and watch time matter more than likes: they show whether the video reached people who don't follow you, and whether they kept watching."

Why these matter:
- Q1 sets who can understand the script.
- Q2: the category shapes vocabulary and what counts as proof (`speaking-styles.md` §4).
- Q3 is the most valuable input. The transcripts are the creator's real speech: they answer the voice-sample question by themselves and feed the voice fingerprint, together with `voice_sample`. The `best` and `other` transcripts always count. The `weak` transcript counts too, unless its register is formal (a formal read-out is not how the creator talks); `voice_fingerprint.py into` decides and prints `Transcripts used: …` with anything it skipped. The numbers are compared only with each other (best vs weak), as signals, not proof. Put the transcripts in `intake.performance[].transcript` (not again in `voice_sample`), and the best post's transcript and numbers in `intake.best_script`. Then run the scripts in `SKILL.md` Stage 0.

**Pasted Insights (Q3).** Never retype numbers that are already in the paste. Save each pasted block as it came to `rss_work/<slug>/insights_best.txt` / `insights_weak.txt` (each transcript to `transcript_best.txt` / `transcript_weak.txt`), then run, per block:
```
python scripts/insights.py rss_work/<slug>/insights_best.txt --label best --transcript-file rss_work/<slug>/transcript_best.txt [--length 28]
```
It reads English and Arabic Insights labels, «K/M» and «ألف/مليون», and prints one `intake.performance` item (views, interactions, the follower / non-follower split, accounts engaged, profile activity, follows, likes, comments, saves, shares). Warnings go to stderr: read them. A missing Views number is an error (exit 1): ask the creator to paste the screen again rather than guess. `insights.py` also reads "Average watch time" («متوسط وقت المشاهدة»; `16 sec`, `0:16`, `1:05`, «١٦ ثانية») into `avg_watch_s`, a "3-second hold" / "Hook rate" percentage into `hold_3s_pct`, and the Reels "Skip rate" («معدل التخطي», provisional label) into `skip_rate_pct` (the share of views that left in the first 3 seconds), when the paste has them. When the paste does not include `avg_watch_s`, `hold_3s_pct` or the video length, the creator may type them by hand: pass the length with `--length`, and add the other two to the item. Add `cta_keyword` to the item when the creator named one and `followers` when they gave it, and collect both printed items into the `intake.performance` array (max 2). Then run `performance.py` and `voice_fingerprint.py into` (Stage 0).
- Q4: never assume high energy. Over-excited delivery was a real complaint. The writing rules per style are in `speaking-styles.md`.
- Q5: an AI voice decides which ElevenLabs markup is legal.
- Q7 gives the script its human-texture line (`craft-standards.md` §2). Without it, the script can still be good, but it can't be personal.

After the build (Stage 8), save the profile and deliver it (see `SKILL.md`, Stage 8), but only when at least one onboarding answer came from the creator. When every answer was a default ("continue"), there is nothing of theirs to remember: don't save or deliver a profile, and say in one line that answering the questions next time lets the skill remember them («جاوب على الأسئلة المرة الجاية وأحفظ أسلوبك وما أسألك مرة ثانية.» / "Answer the questions next time and I'll remember them, so you won't be asked again."). Otherwise, explain reuse in one line, in the user's language:
- Iraqi: «هذا ملفك: ارفعه بأي شات جديد، أو خليه بملفات الـProject، وما راح أسألك هالأسئلة مرة ثانية.»
- English: "This is your profile. Upload it in a new chat, or keep it in your Project's knowledge, and I won't ask these questions again."
- Claude Code: "Saved at rss_work/creator-profile.json; I'll load it automatically next time."

Rebuild and re-deliver the profile only when the creator gives new profile information (a new default style, a new story, a measured pace, new post numbers or transcripts), or after migrating a v2 profile. Don't re-deliver it after every script.

## 2b. Words the creator asked to keep
When the creator says to keep something exact (a series name like «حلّها بالـ AI», a comment keyword like «مواعيد», a teaser or a line), copy it word for word into `intake.must_keep`. Each one must be spoken in the final script (`must_keep_missing` is hard). A real test dropped a series name during a rewrite.

## 3. Per-script questions (every new script)
Ask only what the profile and the message don't already answer. Usually that's three: goal, proof and the style one-tap. (These are questions to the creator. They have nothing to do with how many questions the script itself may ask, which the style sets: `speaking-styles.md` §1.)

**A. Goal, and where the CTA sends people**
- Iraqi: «شنو هدف هالفيديو، ووين تودّي الناس؟» الهدف: وصول · حفظ · مشاركة · متابعة · عملاء · مبيعات. الوجهة: رابط بالبايو · كلمة بالتعليقات · الخاص · متابعة · موقع · ولا شي
- English: "What's this Reel for, and where should people go?" Goal: Reach · Saves · Shares · Follows · Leads · Sales. Destination: Link in bio · Comment a keyword · DM · Follow · Website · None
- Fills `intake.goal` and `intake.cta_destination`. It decides the CTA moves and the proof needed.

**B. Proof you really have**
- Iraqi: «شنو الإثبات اللي عندك فعلاً؟» سكرين شوت · قبل وبعد · نتائج أو أرقام حقيقية · تسجيل تجربة حية · بعد ما عندي
- English: "What proof do you actually have?" Screenshots · Before/after · Real results or numbers · Live demo footage · None yet
- Fills `intake.proof`. Proof options may only use what is listed here.

**C. Style, as one tap (every script)**
- Iraqi: «نفس أسلوبك المعتاد (<label>)؟ أو: …» followed by the other six Arabic labels from `scripts/styles.json` (`label_ar`).
- English: "Same style as usual (<label>), or: …" followed by the other six `label_en` labels.
- `<label>` is the label of the profile's `default_style`. Always ask it, even with a profile: it is one tap, and different Reels need different styles. The answer fills `intake.style` for this script only. When saving the profile afterwards, pass `--keep-default rss_work/creator-profile.json` (the copy made in §1, or the loaded file's own path) to `creator_profile.py from-result` unless the creator asked to change their default style (`SKILL.md` Stage 8). In the onboarding message Q4 already asks it, so don't repeat it there. If the chosen style fights the goal, say so in one line and offer an alternative (`speaking-styles.md` §2).

**D. The product, for Product or UGC-ad Reels only**
- Iraqi: «شنو اسم المنتج، وشنو ميزة أو ميزتين حقيقية تگدر تبيّنها بالفيديو؟ (شي مكتوب على العلبة، لو شي تجربه گدام الكاميرا)»
- English: "What's the product called, and which 1–2 real features or label facts can you show on camera?"
- The name goes in `anchor_terms`; the facts go in `intake.human_texture`, worded as the creator gave them. They make the Recommended Problem or Proof line specific. Without them, write a `{{…}}` slot naming the fact to add (`craft-standards.md` §2), never a feature you guessed.

**E. Length**, only when the user hints at something other than 30 seconds.

## 4. The register question in every dialect
Three levels, the same for every dialect. Ask it as onboarding question 1, in the creator's dialect.

| Dialect | Question |
|---|---|
| Iraqi | «تريد السكربت باللهجة العراقية العامية القوية، لو عراقية بسيطة يفهمها كل العرب، لو فصحى مبسطة؟» |
| Gulf | «تبي السكربت باللهجة الخليجية القوية، ولا خليجي بسيط يفهمه كل العرب، ولا فصحى مبسطة؟» |
| Saudi | «تبغى السكربت باللهجة السعودية القوية، ولا سعودي بسيط يفهمه كل العرب، ولا فصحى مبسطة؟» |
| Egyptian | «عايز السكربت بالعامية المصرية الصريحة، ولا مصري بسيط يفهمه كل العرب، ولا فصحى مبسطة؟» |
| Levantine | «بدّك السكربت باللهجة الشامية القوية، ولا شامي بسيط بيفهمه كل العرب، ولا فصحى مبسطة؟» |

Answers map to `meta.register`: strong → `heavy` · simple → `light` · simplified MSA → `simplified_msa`. Keep `meta.dialect` as the creator's dialect at every level. How to write each level is in `voice-dialect.md` §7.

When the dialect isn't known yet, ask it in pan-Arab wording: «بأي لهجة تريد السكربت، وبأي مستوى: عامية قوية، عامية بسيطة يفهمها كل العرب، لو فصحى مبسطة؟» English scripts have no register question: set `register: "light"`. A creator who asks for MSA directly gets `dialect: "msa"`, `register: "simplified_msa"`.

Note: the Gulf, Saudi, Egyptian and Levantine phrasings are not yet native-checked. A native review is recommended before relying on them. The Iraqi phrasing comes from the design spec.

## 5. Defaults (when the user says continue)
| Item | Default |
|---|---|
| Register | `light` for any Arabic dialect; `simplified_msa` for MSA |
| Goal | Saves. CTA destination: none for Saves, Shares, Reach and Follows; link in bio for Sales and Leads |
| Niche, audience | Inferred from the script, flagged in `defaults_used` |
| Style | The profile's `default_style`; without a profile, `professional` |
| Content category | Inferred from the niche, flagged in `defaults_used`; `other` when unclear |
| Past performance | None: no `performance_analysis`, and Stage 1 works from craft principles only |
| Voice | The draft if there is one (`source: draft_only`), flagged **not verified as the creator's voice**. With only an idea, `source: none` and plain conversational wording in the stated dialect |
| Human texture | None. The Recommended script gets a `{{…}}` slot naming the real detail to add (`craft-standards.md` §2), and `open_issues` asks the creator for one real story or number |
| Recording | Own voice on camera; `none` for text-only Reels |
| Proof | None declared: proof options use demonstration only, flagged `needs_footage`, with `production.proof_shots` |
| Depth | Full (Quick only if the user asks for it) |
| Dialect | Stated, or evident from the text; otherwise inferred from context (a Dubai topic → Gulf) and listed in `defaults_used` for the creator to confirm |
| Platform | Instagram Reels |
| Duration | 30 seconds |

State every default used in `intake.defaults_used` so the dashboard shows them. Set `meta.slug` to a short ASCII name, new for every script.

## 6. Measuring the creator's real pace
The dashboard's teleprompter has a **"Measure your real pace"** timer. The creator reads the script aloud, and the measured words per minute replace the default pacing in the dashboard and in the profile they download. Next time, that profile's `pacing` goes into `meta.pacing`, and the validator uses it.
