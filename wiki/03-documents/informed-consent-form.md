---
title: "Informed Consent Form (21 CFR 50.25; Common Rule Key Information; eConsent)"
section: "03-documents"
status: mixed
governing_authority:
  - "21 CFR 50.20, 50.25, 50.27 (FDA informed consent)"
  - "45 CFR 46.116, 46.117 (Common Rule informed consent + key information)"
  - "21 CFR 312.60 (investigator duty to obtain consent)"
  - "FDA, Informed Consent: Guidance for IRBs, Clinical Investigators, and Sponsors (August 2023)"
  - "FDA/OHRP Use of Electronic Informed Consent Q&A (2016)"
  - "21 CFR Part 11 (electronic signatures)"
tags: [cfr/50, cfr/11, cfr/312, lifecycle/activation, lifecycle/conduct, role/investigator, ossicro/gating, status/confirmed, status/interpretive]
aliases: ["ICF", "informed consent", "informed consent form", "consent form", "eConsent", "50.25"]
updated: 2026-07-09
---

# Informed Consent Form (21 CFR 50.25; Common Rule Key Information; eConsent)

> [!authority] Governing authority
> **21 CFR 50.20** (general requirements), **21 CFR 50.25** (elements — basic + additional), **21 CFR 50.27** (documentation); **45 CFR 46.116** (Common Rule elements + **key-information** summary), **45 CFR 46.117** (documentation); **21 CFR 312.60** (no subject enrolled without legally effective consent); **FDA Informed Consent guidance (August 2023)** on benefit framing and understandable language; **FDA/OHRP 2016 eConsent Q&A**; **21 CFR Part 11** for the electronic signature. Status: **Mixed** — the consent **elements** are confirmed black-letter; the document-vs-event boundary is a confirmed legal distinction OSSICRO foregrounds; eConsent mechanics, the readability/calibration validation rules, and OSSICRO's authoring role are flagged interpretive.

The **informed consent form (ICF)** is the written document that records the information a prospective subject must receive and the subject's (or legally authorized representative's) voluntary agreement to participate. It is distinct from **informed consent itself**, which is a **process** — the human conversation in which a qualified person gives the subject the opportunity to consider participation, answers questions, and confirms voluntary, uncoerced, competent agreement. OSSICRO drafts, version-controls, and completeness-checks the **document**; it must never conduct or substitute for the **event**. This bright line is the single most important gate in the system ([[informed-consent-document-vs-event]], [[non-delegable-functions-and-gates]]).

> [!warning] Non-delegable
> Obtaining informed consent is a **non-delegable subject-facing human act**. 21 CFR 312.60 forbids an [[investigator]] from involving a human as a subject unless **legally effective informed consent** is obtained; 21 CFR 50.20 requires that consent be sought under circumstances that give the subject sufficient opportunity to decide **without coercion or undue influence**. OSSICRO generates and maintains the ICF and can drive an eConsent presentation flow, but the consent **conversation, comprehension confirmation, and the qualified person's judgment that consent is valid** stay with a human on the delegation-of-authority log ([[delegation-of-authority-log]]). No AI action satisfies the consent requirement.

## 1. General requirements — 21 CFR 50.20

Except as provided in 50.23 (emergency) and 50.24 (planned emergency research), no investigator may involve a human as a subject unless the investigator has obtained the legally effective informed consent of the subject or the subject's **legally authorized representative (LAR)**. Consent must be:

- sought only under circumstances giving the prospective subject sufficient **opportunity to consider** whether to participate and **minimizing the possibility of coercion or undue influence**;
- in **language understandable** to the subject or the representative;
- free of **exculpatory language** through which the subject waives or appears to waive any legal rights or releases the investigator, sponsor, institution, or agents from liability for negligence.

## 2. Basic elements — 21 CFR 50.25(a)

The ICF must contain each of the eight basic elements (FDA numbering; the Common Rule at 45 CFR 46.116(b) is harmonized):

1. A statement that the study involves **research**, an explanation of its **purposes**, the **expected duration** of participation, a description of the **procedures**, and identification of any procedures that are **experimental**.
2. A description of any **reasonably foreseeable risks or discomforts** — consistent with the [[investigators-brochure|Investigator's Brochure]] risk section.
3. A description of any **benefits** to the subject or to others that may reasonably be expected — stated without overstatement; see §7 below for the early-phase calibration rules.
4. A disclosure of appropriate **alternative** procedures or courses of treatment.
5. A statement describing the extent to which **confidentiality** of records will be maintained, and noting the possibility that **FDA may inspect** the records.
6. For research involving more than minimal risk, an explanation of whether **compensation** and **medical treatment for injury** are available.
7. An explanation of whom to **contact** for questions about the research and research subjects' rights, and whom to contact in the event of a **research-related injury**.
8. A statement that participation is **voluntary**, that refusal involves no penalty or loss of benefits, and that the subject may **discontinue at any time** without penalty or loss of benefits.

## 3. Additional elements — 21 CFR 50.25(b)

When appropriate, one or more of the additional elements must be provided, including: unforeseeable risks (including to an embryo/fetus); circumstances under which participation may be terminated by the investigator; additional costs to the subject; consequences of withdrawal and orderly-termination procedures; a statement that significant new findings will be provided; the approximate number of subjects; and — for applicable clinical trials — the mandatory **ClinicalTrials.gov statement** required by 21 CFR 50.25(c) (referencing 42 U.S.C. 282(j); see [[clinicaltrials-gov-registration]]).

## 4. Key-information summary — 45 CFR 46.116(a)(5)

Under the revised **Common Rule** (2018 requirements), consent must **begin with a concise and focused "key information"** presentation — the information a reasonable person would want in order to make an informed decision (purpose, voluntariness, risks, benefits, alternatives) — organized to **facilitate comprehension**, before the full detail. FDA has moved to harmonize (2022–2023 alignment activity under the Cures Act §3023); OSSICRO drafts the ICF with a **key-information front section** as the default so a single template satisfies both frameworks. Where a study is **both** FDA-regulated **and** HHS-supported, both 21 CFR 50 **and** 45 CFR 46 apply and the stricter requirement governs.

## 5. Documentation — 21 CFR 50.27 / 45 CFR 46.117

Informed consent must be **documented** by a written consent form approved by the [[irb-iec|IRB]] and **signed and dated** by the subject or the LAR at the time of consent; a copy is given to the person signing. Both frameworks permit two forms: the **long form** embodying all required elements (21 CFR 50.27(b)(1); 45 CFR 46.117(b)(1)), or the **short form** — a written document stating that the required elements have been **presented orally**, with a **witness to the oral presentation**, an **IRB-approved written summary** of what is to be said, the subject's signature on the short form, and the witness's signature on both the short form and a copy of the summary (21 CFR 50.27(b)(2); 45 CFR 46.117(b)(2)). The short form paired with a translated version and an interpreter is the standard mechanism for the unexpected non-English-speaking enrollee (§6 below). The signed form is filed in the subject's records and the [[regulatory-binder-isf-index|ISF]]; the fact and date of consent are recorded in the case history (21 CFR 312.62(b)).

## 6. Understandable language — readability, plain-language transformation, translation

50.20's requirement that consent be **in language understandable to the subject** binds the document as strictly as the eight elements do — and it is the requirement an auto-drafting system is most likely to violate, because [[investigators-brochure|IB]] risk sections are written for regulators, not patients. Piping IB text into an ICF verbatim produces a legally complete, humanly incomprehensible form. The FDA August 2023 informed consent guidance directs that information be presented in language an average person can understand, with medical and scientific terms explained.

> [!interpretive] OSSICRO validation rules — machine-checkable proxies for 50.20
> The [[generate-check-validate-engine]] enforces the following on every generated ICF. These are proxies: passing them does not discharge 50.20 — the IRB and the consenting human own the comprehension judgment.
>
> - **Readability ceiling.** The ICF body (excluding signature blocks and the verbatim 50.25(c) statement) must score at or below **grade 8 on the Flesch-Kincaid Grade Level metric** — the check's named default, consistent with the 6th-to-8th-grade reading standard most IRBs apply. Sections exceeding the ceiling **block the check pass** and are returned for plain-language revision; an above-ceiling release requires a recorded human justification.
> - **Mandatory plain-language transformation of IB-derived text.** Risk and procedure text sourced from the IB or protocol is never inserted verbatim. Each statement receives a plain-language rendering, with its [[draft-provenance-model|provenance triple]] preserved to the IB source span so the human reviewer can confirm the transformation is faithful (nothing minimized, nothing omitted) — fidelity review of the transformation is part of the qualified reviewer's sign-off, not a machine determination.
> - **Translation and short form as gated artifacts.** For sites expecting non-English-speaking populations, the translated full ICF is a first-class gated artifact: qualified-translator certification (or translation plus back-translation), human verification, and IRB approval of the translated version before use. For the unexpected non-English enrollee, OSSICRO produces the **short-form artifact set** — translated short form, IRB-approved English summary, interpreter arrangement record, and the witness-signature checklist per 50.27(b)(2)/46.117(b)(2) — as a gated workflow, and hard-stops enrollment until each artifact is in place.

## 7. Early-phase benefit framing — calibration, not just completeness

For the FIH-to-Phase-2 trials OSSICRO targets, a benefits description that is merely *present* can still be misleading. The FDA August 2023 informed consent guidance warns that statements **overstating the possibility of benefit** may unduly influence prospective subjects, and that framing an investigation as a "**therapeutic trial**" can contribute to the misunderstanding that participation will directly benefit the subject's condition. In Phase 1, direct benefit is typically unlikely or unknown; the 50.25(a)(3) element must say so honestly.

> [!interpretive] OSSICRO early-phase rules
> - **Required template language.** For FIH and dose-escalation protocols, the benefits section must state that the study's **primary purpose is safety, tolerability, and dose-finding** (as applicable), and that **direct benefit to the subject cannot be assured and may be unlikely**. The element-completeness check fails if this statement is absent from an early-phase ICF.
> - **Dose-escalation and cohort language.** The procedures/risks sections must explain cohort-based dose assignment in plain language, including that early cohorts may receive doses **below any pharmacologically active level**, and sentinel-dosing arrangements where the protocol uses them.
> - **Calibration validation.** The validate step flags **superlatives and unqualified benefit claims** in the generated benefits and risks sections (e.g., "promising," "breakthrough," "will improve"), and blocks "therapeutic" descriptors applied to the trial itself. For FIH protocols, a benefits section **disproportionately long relative to the risks section** is flagged and cannot pass without recorded human justification. An LLM drafting a benefits section from a protocol synopsis will, unconstrained, produce optimistic prose; these rules exist because **completeness checking alone would pass it**. Calibration is verified as its own gate.

## 8. Electronic informed consent (eConsent)

> [!interpretive] OSSICRO position — eConsent mechanics vs. the human event
> The **FDA/OHRP 2016 "Use of Electronic Informed Consent" Q&A** authorizes electronic delivery and electronic signature of consent, subject to: IRB review and approval of the eConsent **materials and process**; methods to promote and **confirm comprehension** (e.g., interactive elements, questions); confirmation of the **identity** of the signatory; subject **access to a copy**; and an electronic signature that satisfies **21 CFR Part 11** (unique attribution, authentication, non-repudiation, audit trail — [[part-11-and-ai-credibility]]). OSSICRO can present the eConsent flow, administer IRB-approved comprehension-check instruments, capture the Part-11-compliant e-signature, and file the executed record with an ALCOA++ audit trail. **What OSSICRO does not do:** replace the qualified person who conducts the consent discussion, answers questions in real time, and judges voluntariness, capacity, and comprehension. eConsent changes the medium, not the human requirement. Flagged interpretive; grounded in the 2016 guidance and Part 11.

> [!warning] Comprehension checks — where the bright line runs
> [[informed-consent-document-vs-event]] forbids any OSSICRO component to conduct, simulate, **augment-in-the-moment**, or substitute for the consent conversation. Administering a comprehension check is compatible with that rule only under all four of the following conditions, which OSSICRO enforces:
>
> 1. **The instrument is IRB-approved static content.** Comprehension questions are part of the IRB-reviewed eConsent materials — versioned, approved before use, and **never generated or altered by AI at consent time**. Adaptive or generative questioning during the event is on the forbidden side of the line.
> 2. **A passing score never substitutes for the human judgment.** Quiz results are an **input** the qualified consenting person reviews during the conversation and must **independently confirm**; the recorded basis of the comprehension finding is the qualified person's own assessment, not the automated score.
> 3. **A failing score hard-stops the flow.** The eConsent presentation cannot auto-advance past a failed check; the flow halts and routes the subject to the human discussant. Re-attempt occurs only after that discussion.
> 4. **The audit trail records both.** The instrument result and the human's independent comprehension confirmation are logged as distinct entries, so no inspection can read the machine score as the consent-validity determination.

## 9. Special populations

- **Children (Subpart D)** — 21 CFR 50.50–50.56 (and 45 CFR 46 Subpart D) impose additional protections and require, in addition to parental permission, the **assent** of the child where appropriate. Directly relevant where the enrolling clinician's population is pediatric; OSSICRO produces the parental-permission and age-appropriate assent documents as separate gated artifacts.
- **LAR / impaired capacity** — where the subject cannot consent, consent is obtained from a legally authorized representative per applicable law; OSSICRO surfaces this as a documented eligibility branch, not an automated determination.

## 10. The OSSICRO gate

The ICF is generated by the [[generate-check-validate-engine]]: **generate** the document from the [[clinical-protocol-and-synopsis|protocol synopsis]] and IB risk data (each span carrying a [[draft-provenance-model|provenance triple]] to its source and CFR citation, with the mandatory plain-language transformation of §6); **check** all eight 50.25(a) elements plus applicable (b)/(c) additions, the key-information summary, and — for early-phase protocols — the required benefit-framing language of §7; **validate** against 56.111/50.20 via the machine-checkable proxies: exculpatory-language pattern screening, the readability ceiling (§6), and the benefit-calibration rules (§7). "Language understandable to the subject" is ultimately the IRB's and the consenting human's judgment; the validate step narrows the gap, it does not close it. The completed ICF then enters the [[irb-submission-package|IRB package]] for **approval**, and enrollment is gated on documented IRB approval **and** the executed, human-conducted consent event. Both the IRB approval and the consent event are non-automatable ([[completeness-ledger]] renders them as **amber** human-judgment gates).

## Related
- [[informed-consent-document-vs-event]]
- [[investigators-brochure]]
- [[clinical-protocol-and-synopsis]]
- [[irb-submission-package]]
- [[irb-iec]]
- [[investigator]]
- [[enrollment-and-consent]]
- [[delegation-of-authority-log]]
- [[regulatory-binder-isf-index]]
- [[clinicaltrials-gov-registration]]
- [[part-11-and-ai-credibility]]
- [[hipaa-and-privacy-gating]]
- [[patient]]
- [[generate-check-validate-engine]]
- [[draft-provenance-model]]
- [[non-delegable-functions-and-gates]]

## Sources
- [21 CFR 50.20 — General requirements for informed consent](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50/subpart-B/section-50.20)
- [21 CFR 50.25 — Elements of informed consent](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50/subpart-B/section-50.25)
- [21 CFR 50.27 — Documentation of informed consent](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50/subpart-B/section-50.27)
- [45 CFR 46.116 — General requirements for informed consent (Common Rule, incl. key information)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46/subpart-A/section-46.116)
- [45 CFR 46.117 — Documentation of informed consent](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46/subpart-A/section-46.117)
- [21 CFR 312.60 — General responsibilities of investigators](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.60)
- [FDA — Informed Consent: Guidance for Institutional Review Boards, Clinical Investigators, and Sponsors (August 2023)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/informed-consent)
- [Federal Register — Informed Consent Guidance; Availability (Aug. 16, 2023)](https://www.federalregister.gov/documents/2023/08/16/2023-17594/informed-consent-guidance-for-institutional-review-boards-clinical-investigators-and-sponsors)
- [FDA/OHRP (2016) — Use of Electronic Informed Consent: Questions and Answers](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-electronic-informed-consent-clinical-investigations-questions-and-answers)
- [21 CFR Part 11 — Electronic Records; Electronic Signatures](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)