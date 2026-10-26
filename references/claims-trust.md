# Claims & Trust (Auditor, Council Trust Officer)

Classify every claim in the draft and in every option. Record each one in `audit.claims` with `type`, `action`, `status` (the evidence label: `observed`, `source_supported`, `creator_attested`, `unsupported` or `not_factual`; table in `research.md` §6), `sources` (opened source ids) and, when kept, `evidence` (for other actions, `evidence` may say why it couldn't be kept, e.g. "no source found").

| Type | Example | Allowed actions |
|---|---|---|
| **opinion** (professional stance) | «المشكلة بالسكربت، مو بالكاميرا» | `keep`. **Keep it firm.** A confident opinion powers a hook. Don't soften it to "sometimes". |
| **factual** (statistic, causal claim about the viewer or the world) | «أغلب الناس ما يعرفون...», "doubles your views" | `soften`, `replace` (with something demonstrable), `remove`, or `keep_with_evidence` + a named source |
| **result** (product output, earnings, before/after) | «مبيعاته زادت 300%», «يثبت 24 ساعة» | `keep_with_evidence` only when the real result is declared proof shown on screen, or a planned proof shot films it (`evidence: "proof_shots[0] — unedited screen recording"`); otherwise `soften`, `replace` or `remove` |
| **offer** ("free", "limited", "I'll send it") | | `keep` after confirming access conditions; remind the creator to test any automation from a second account |

`keep` on a factual or result claim is a hard validator failure, and it also caps the self-assessed score at 69.

## Research
Fact checks, angle research and audience research live in `research.md` (Stage 1b). In short: a `factual` claim kept with evidence needs an **opened** source (`source_supported`) or must be shown on screen (`observed`); a snippet is not evidence; without a search tool every unverified factual claim is treated as unverified, and the audit says so.

## Regulated niches (set `idea.regulated: true`)
Health, supplements, weight loss, medical or mental-health advice, investing, trading, crypto, loans and credit, legal advice, and income or "guaranteed results" claims. **Not** regulated by itself: everyday tools such as budgeting or expense-tracking apps, productivity and AI tools. Their factual and result claims still follow the table above. In these niches:
- No result or factual claim survives without proof the viewer can see. The validator fails it.
- No guarantees, no "cure", no "risk-free", no income figures. The validator scans every option, overlay, the final script, the ElevenLabs clips, the tight cut, the shot list's voice and overlays, the cover text, the caption, the pinned comment and the comment automation (keyword, variants, public replies, DM) on its own, whatever `audit.claims` says, and fails `regulated_guarantee` on any promise word from the list in `scripts/craft.json` (`regulated_guarantee`): «نتيجة مضمونة», «علاج نهائي», "guaranteed", "risk-free".
- **An honest disclaimer passes, and it builds trust: use one.** The scan lets a phrase through only when a negator is the nearest word before it (ignoring fillers like «في أي شي» / "any"), in the same clause: «ما في أي شي مضمون», «هذا مو علاج نهائي», "I can't guarantee results", "there's no cure". Put the negator right before the word: "nothing here is guaranteed" fails, "it's not guaranteed" passes. "No risk, guaranteed results" and «لا تفوّت: علاج نهائي» still fail: the comma and the colon start a new clause, so the promise stands alone.
- Add the platform's relevant disclosure to `publish.guideline_flags`.

## No unmeasured claims in the voice
Speed («بثانية», "instantly"), "unedited" («تسجيل بدون قص») and exact understanding («فاهم رسالتك بالضبط») are claims. In a blind test on real drafts, these were the deciding deductions. Unless they were timed, filmed or sourced, let the demo show it instead of saying it. `unmeasured_claim` is a hard failure unless the claim is in `audit.claims` as `observed` or `source_supported`. Text quoted from the demo itself («نراجع طلبك فوراً») is shown, not claimed, and it's fine. A model doesn't "understand" exactly: say it "wrote a reply that fits" («كتبت رد يناسب الرسالة»).

## Keep the creator's premise
When the creator demonstrates a tool they already built or use, the Reel stays a demonstration of that existing thing (`creator_attested` until shown). Never turn it into a "how to build it" tutorial or a future promise because the files weren't attached. If one fact genuinely changes the script, ask for that one fact. Keep an existing offer conditional rather than swapping in a different resource.

## Proof honesty
- Proof options use only evidence declared in `intake.proof`, listed in each option's `proof_uses`.
- **"Try it yourself", "trust me" and "it really works" are not proof.** An invitation to try belongs in the CTA. With no declared proof, the proof option is a demonstration flagged `needs_footage`, and `production.proof_shots` says exactly what to film (`production.md`).
- "This video is the result" is valid only if the tool really took part in making it. If the claim is broader than what happened, suggest a precise wording (e.g. «مرّرت سكربت هالفيديو عليها» instead of «سويت الفيديو كله بيها»).
- Never simulate a review, reaction, test, or number.

## AI disclosure and consent
If the voice is AI-generated or the footage is photorealistic AI, set `publish.ai_label: true` and remind the creator to switch on the platform's AI label. For cloned voices: **only clone your own voice, or one you have written permission to use.**
