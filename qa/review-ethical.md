# QA Review — ETHICAL reviewer — research-ethics / IRB chair (Belmont, Common Rule, Helsinki)

**Model:** Claude Code | claude-fable-5  
**Verdict:** The document-vs-event bright line is genuinely well-built and correctly cited, but the system's paperwork ethics are far more mature than its relational ethics: the guiding scenario's core conflict — the treating physician who becomes sponsor-investigator to get their own patient in — and the therapeutic misconception it invites are nowhere examined in the consent or patient materials, and two files quietly contradict the bright line on AI comprehension-checking.

## Strengths
- The document/event split (wiki/04-coordination/informed-consent-document-vs-event.md) is the strongest ethics artifact in the set: correct authority (50.20 vs 50.25/50.27), an explicit division-of-labor table, and a prohibition list that names the real failure modes (chatbot consent dialogue, AI answers during consent, auto-advancing eConsent). Most commercial eConsent vendors do not state this line this clearly.
- Consistent, honest epistemic labeling — every page separates confirmed black-letter law from OSSICRO interpretive positions with inline callouts. This is exactly the transparency an IRB wants from a sponsor's system documentation.
- hipaa-and-privacy-gating.md is legally accurate on 164.512(i) preparatory review (including the commonly-misunderstood no-removal and no-outsider-recruitment limits) and the code-enforced looking/enrolling state machine deliberately exceeds the regulatory floor — architectural rather than procedural mitigation of the worst privacy failure mode is the right instinct.
- patient.md frames the patient as the protected subject rather than a user to be converted: no trial recommendations direct to patient, matching output routed to the HCP, coded identities never in logs, and the correct statement that expanded access is treatment-not-research while Part 50/56 protections still apply.
- The regulatory content sampled is accurate on hard details reviewers usually get wrong: 46.109(f)(1) continuing-review relief having no FDA counterpart, the December 2023 addition of 50.22, 164.524(a)(2)(iii) access suspension, and compound consent-authorization under 164.508(b)(3)(i).

## Findings
### [HIGH] wiki/06-personas/patient.md
**Issue:** The system's foundational scenario — a treating physician becomes sponsor-investigator specifically to get their own identified patient into an early-phase trial — is the textbook setup for therapeutic misconception and dual-role conflict of interest, and none of the assigned files acknowledges it. The patient's entry question is framed as 'can my doctor get me in,' i.e., research is presented as a treatment-access pathway from the first screen. The person who initiated the study to treat this patient is then the person who conducts that patient's consent conversation and judges its voluntariness. Belmont's respect-for-persons and Helsinki para. 27 (physician-dependent relationship; consent should be sought by an appropriately qualified individual independent of the relationship where dependence is a concern) are directly implicated. 56.111(a)(3) equitable selection is also strained in an n-of-1 site built around a preselected patient — the wiki quotes the criterion but never confronts what it means when the trial exists for one person.

**Recommendation:** {f.get('recommendation','')}

### [HIGH] wiki/03-documents/informed-consent-form.md
**Issue:** Section 6 and section 8 permit OSSICRO to 'run comprehension checks' during eConsent, while informed-consent-document-vs-event.md (the master page) forbids any component to 'augment-in-the-moment' the consent event and states the human 'judges voluntariness and capacity.' These are in tension: an automated comprehension assessment administered during consent IS in-the-moment participation in the event, and its pass/fail output will de facto substitute for — or anchor — the qualified person's comprehension judgment. Neither page says who acts on a failed check, whether a passed automated quiz may be recorded as evidence of comprehension, or whether AI-generated comprehension questions are themselves IRB-reviewed content. The bright line is drawn beautifully and then smudged in the one place regulators and boards will look hardest.

**Recommendation:** {f.get('recommendation','')}

### [HIGH] wiki/01-roles-responsibilities/irb-iec.md
**Issue:** Lines 54 and 79 describe the engine as pre-checking the submission package 'against the 56.111 criteria (each element mapped to its supporting document).' The 56.111 criteria are substantive ethical judgments — risks reasonable relative to benefits, equitable selection, adequate safeguards for the vulnerable — not document-presence properties. Mapping each criterion to 'its supporting document' teaches users that satisfying the board is a completeness exercise, and produces submissions optimized to look approval-ready. This is the precise mechanism by which AI-drafted material undermines genuine review: a polished, criterion-keyed package invites the board (and the PI before it) toward rubber-stamp confirmation rather than deliberation. The disclaimer ('asserts nothing about how the IRB will decide') is present but the framing works against it.

**Recommendation:** {f.get('recommendation','')}

### [MEDIUM] wiki/03-documents/informed-consent-form.md
**Issue:** For a system explicitly aimed at FIH-to-Phase-2 trials, the ICF page contains no early-phase-specific consent ethics: nothing on describing benefit honestly when direct benefit is unlikely or unknown (the chronic 50.25(a)(3) overstatement problem in Phase 1), nothing on dose-escalation/cohort language, nothing warning against hope-inflating benefit framing in AI-generated drafts. An LLM drafting a benefits section from a protocol synopsis and IB will, absent constraints, produce optimistic prose — and the element-completeness check will pass it because a benefits description is present. Completeness is being verified; truthful calibration is not.

**Recommendation:** {f.get('recommendation','')}

### [MEDIUM] wiki/01-roles-responsibilities/irb-iec.md
**Issue:** Vulnerable-population treatment is thin across the set: Subparts B (pregnant women) and C (prisoners) appear once in a table row and never again; 56.111(b) additional safeguards is quoted but not operationalized anywhere in the assigned files; and the population the system will actually attract — seriously ill, option-exhausted patients, whom patient.md itself locates in 'under-resourced settings' — is precisely the group most susceptible to undue influence, yet no file analyzes how desperation plus a treatment-access framing interacts with 50.20's undue-influence prohibition. Economic vulnerability and financial toxicity (who pays in Mode B; charging under expanded access per 312.8) are absent beyond the bare 50.25(b)(3) listing.

**Recommendation:** {f.get('recommendation','')}

### [MEDIUM] wiki/04-coordination/informed-consent-document-vs-event.md
**Issue:** Line 19 says OSSICRO 'translates-with-verification' the consent document. AI translation of an ICF is one of the highest-risk comprehension surfaces in the whole system — 50.20's 'language understandable to the subject' is load-bearing — and 'with verification' is asserted without specification: verified by whom, against what standard (certified translator? back-translation?), and IRB-approved in which language versions? The short-form mechanism at 50.27(b) is described, but its relationship to AI-translated long forms is not gated.

**Recommendation:** {f.get('recommendation','')}

### [LOW] wiki/06-personas/patient.md
**Issue:** The interpretive portal design ('your doctor is reviewing candidate programs,' 'consent visit scheduled') manages hope poorly: status updates to a seriously ill patient before IRB approval or physician judgment create expectation pressure that flows back into the consent conversation as undue influence on both parties, and the page says nothing about what the patient sees when the answer is no match or the physician declines.

**Recommendation:** {f.get('recommendation','')}

## Must-fix
- Confront the treating-physician/sponsor-investigator dual-role conflict and therapeutic misconception head-on: dedicated wiki treatment, mandatory research-vs-treatment ICF language, and an independent-consent-discussant design option for Mode B single-patient studies.
- Reconcile the comprehension-check contradiction between informed-consent-form.md and informed-consent-document-vs-event.md so automated comprehension assessment can never stand in for, or anchor, the qualified human's comprehension judgment.
- Reframe the IRB 'pre-check against the 56.111 criteria' (irb-iec.md) as administrative document-completeness only; substantive ethics criteria must never be presented as pre-checkable or mapped one-to-one to documents.
- Add early-phase-specific consent constraints: required no-assured-benefit language for FIH/Phase 1-2 drafts and validation rules against overstated benefit framing in AI-generated ICF text.
