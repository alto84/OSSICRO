---
title: "Informed Consent — the Document vs the Event"
section: "04-coordination"
status: mixed
governing_authority:
  - "21 CFR Part 50 (esp. 50.20, 50.25, 50.27)"
  - "45 CFR 46.116-46.117 (Common Rule, where applicable)"
  - "FDA/OHRP eConsent Q&A guidance (December 2016); 21 CFR Part 11"
tags: [lifecycle/conduct, role/investigator, cfr/50, cfr/11, ossicro/gating, ossicro/engine, status/interpretive]
aliases: [consent-document-vs-event, consent-bright-line]
updated: 2026-07-09
---

# Informed Consent — the Document vs the Event

> [!authority] Governing authority
> 21 CFR Part 50 (general requirements 50.20; elements 50.25; documentation 50.27), 45 CFR 46.116-46.117 for federally supported research (key-information requirement), FDA/OHRP joint guidance *Use of Electronic Informed Consent in Clinical Investigations — Questions and Answers* (December 2016), 21 CFR Part 11 for electronic signatures. Status: **Mixed** — the consent requirements are black-letter; the document/event division of labor is OSSICRO's foundational design position.

Informed consent is two distinguishable things that regulation deliberately couples: a **document** — the written form whose content 21 CFR 50.25 specifies and whose signature 50.27 requires — and an **event** — the process by which a qualified person gives a prospective subject the opportunity to understand, ask, weigh, and voluntarily agree (21 CFR 50.20). OSSICRO drafts, checks, versions, translates-with-verification, and tracks the document. The event is a human act between the investigator (or a qualified delegated person) and the patient, and it is the single brightest line in the entire system: **no OSSICRO component may conduct, simulate, augment-in-the-moment, or substitute for the consent conversation.** This is the operating rule behind [[enrollment-and-consent]] and a first-order entry in [[non-delegable-functions-and-gates]].

## The document — what 21 CFR 50.25 requires

### Basic elements — 50.25(a)

1. A statement that the study involves research, an explanation of its purposes, the expected duration of participation, a description of the procedures, and identification of any procedures that are experimental;
2. A description of reasonably foreseeable risks or discomforts;
3. A description of benefits to the subject or others that may reasonably be expected;
4. Disclosure of appropriate alternative procedures or courses of treatment;
5. A statement describing the extent of confidentiality of records, noting the possibility that FDA may inspect the records;
6. For research involving more than minimal risk, an explanation as to whether compensation and medical treatments are available if injury occurs, and what they consist of or where further information may be obtained;
7. Whom to contact for answers about the research and subjects' rights, and whom to contact in the event of research-related injury;
8. A statement that participation is voluntary, that refusal involves no penalty or loss of benefits, and that the subject may discontinue at any time without penalty.

### Additional elements when appropriate — 50.25(b)

Unforeseeable risks; circumstances under which the investigator may terminate participation; additional costs to the subject; consequences of withdrawal and procedures for orderly termination; a statement that significant new findings will be provided; and the approximate number of subjects.

### The ClinicalTrials.gov statement — 50.25(c)

For "applicable clinical trials," the form must include the exact regulatory statement: *"A description of this clinical trial will be available on http://www.ClinicalTrials.gov, as required by U.S. Law. This Web site will not include information that can identify you. At most, the Web site will include a summary of the results. You can search this Web site at any time."* See [[clinicaltrials-gov-registration]].

### Common Rule overlay — key information

For federally supported research, 45 CFR 46.116(a)(5)(i) requires consent to begin with a **concise and focused presentation of key information** most likely to help a reasonable person decide whether to participate, organized to facilitate comprehension. FDA-only trials are not bound by 46.116 today, but the 2022 FDA harmonization proposal would align the regimes ([87 FR 58733](https://www.federalregister.gov/documents/2022/09/28/2022-21088/protection-of-human-subjects-and-institutional-review-boards)); OSSICRO includes a key-information section by default because dual regulation is common and the section serves comprehension in any case (interpretive design choice).

### Documentation — 50.27

Consent is documented by a written form approved by the IRB and signed and dated by the subject or the subject's legally authorized representative (LAR), with a copy given to the signer (50.27(a)). Two forms are permitted: the **long form** embodying all 50.25 elements, or the **short form** stating that the elements were presented orally — requiring a witness to the oral presentation, an IRB-approved written summary, witness signatures on both documents, and the subject's signature on the short form (50.27(b)). The short form is the standard mechanism for unexpected non-English-speaking enrollees, paired with a translated short form and an interpreter.

## The event — what 21 CFR 50.20 requires

No investigator may involve a human being as a subject unless the investigator has obtained the **legally effective informed consent** of the subject or the subject's LAR — and only under circumstances that provide **sufficient opportunity to consider** whether to participate and that **minimize the possibility of coercion or undue influence**. The information must be **in language understandable** to the subject, and no consent may include **exculpatory language** waiving rights or releasing the investigator, sponsor, or institution from liability for negligence (50.20). The investigator personally commits to obtaining consent on [[form-fda-1572-statement-of-investigator|Form FDA 1572]], and 21 CFR 312.60 makes it an enforceable investigator obligation. Exceptions exist only in narrow codified forms: 50.23 (specified emergency/military circumstances), 50.24 (emergency research with IRB-approved exception and community consultation), and 50.22 (IRB waiver/alteration for certain **minimal-risk** investigations, added by FDA final rule in December 2023 — essentially never available for an early-phase drug trial). Pediatric enrollment additionally requires parental permission and child assent per 21 CFR Part 50 Subpart D (50.55).

The event is not one signature moment. It is capacity assessment, disclosure, dialogue, comprehension checking, an answer to every question, an uncoerced decision — and it **continues** across the study: significant new findings (50.25(b)(5)), IB updates that change the risk profile, and protocol amendments trigger consent-form revision, IRB approval of the revision, and re-consent of ongoing subjects with the new version.

> [!warning] Non-delegable
> The consent event — assessing capacity, conveying and testing understanding, answering questions, and receiving voluntary agreement — belongs to the investigator or a qualified delegated human (documented on the [[delegation-of-authority-log]]). No OSSICRO component conducts or stands in for any part of that conversation: no chatbot consent dialogue, no AI answers to a prospective subject's questions during consent, no auto-advancing eConsent flow that substitutes for human availability. Software that crossed this line would place the trial in violation of 21 CFR 50.20/312.60 and the subject at real risk of uncomprehended enrollment.

## eConsent — permitted mechanics, same bright line

The FDA/OHRP joint guidance (December 2016) authorizes electronic consent processes: electronic presentation of consent information (text, video, interactive modules), comprehension assessments, remote consent, and electronic signatures — provided the eConsent materials are IRB-reviewed, subjects can ask questions of a qualified human, a copy is provided, and the e-signature satisfies 21 CFR Part 11 ([[part-11-and-ai-credibility]]). eConsent changes the *medium* of the document and its execution; it does not relocate the event. OSSICRO's eConsent module presents IRB-approved materials, records Part 11-compliant signatures with full audit trail, and schedules the human conversation — it never replaces it.

## Division of labor

| Function | OSSICRO (software) | Qualified human |
|---|---|---|
| Draft ICF with all 50.25(a)-(c) elements; key-information summary | ✔ drafts for review ([[draft-provenance-model]]) | reviews, owns content |
| Element-completeness and readability check | ✔ validates | — |
| IRB approval of the form and all revisions | routes the package ([[irb-review-workflow]]) | **IRB decides** |
| Version control; ensuring only the current approved version is in use | ✔ hard-gates stale versions | — |
| Capacity assessment, disclosure conversation, comprehension, voluntariness | **never** | **investigator/delegate** |
| Answering subject questions during consent | **never** | **investigator/delegate** |
| Signature capture (paper or Part 11 e-signature) and copy to subject | ✔ records and files | subject/LAR signs; human present per protocol |
| Re-consent triggering on amendments/new findings | ✔ detects trigger, drafts revision, tracks who needs re-consent | investigator conducts; IRB approves revision |
| Consent-before-any-procedure gate | ✔ enforces (no study activity logged without current signed ICF) | — |

> [!interpretive] OSSICRO position
> The document/event split is OSSICRO's clearest instance of the general thesis: the *paperwork* around consent (drafting, element-checking, translation management, versioning, re-consent tracking, filing) is high-burden, error-prone, and fully automatable to draft stage; the *act* of consent is a protected human relationship the system is architected to be incapable of performing. A consent form OSSICRO drafts is COMPLETE in the [[completeness-ledger]] sense only after IRB approval and human review — never merely because generation finished.

## Related

- [[informed-consent-form]] — the document explainer (template anatomy, eConsent build)
- [[enrollment-and-consent]] — where the event sits in the lifecycle
- [[irb-review-workflow]] — approval of the form and its every revision
- [[non-delegable-functions-and-gates]] — the master gating matrix this page anchors
- [[patient]] — the consent event from the subject's side
- [[part-11-and-ai-credibility]] — e-signature and audit-trail requirements for eConsent
- [[hipaa-and-privacy-gating]] — the separate HIPAA authorization that accompanies consent

## Sources

- [21 CFR 50.20 — General requirements for informed consent (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/50.20)
- [21 CFR 50.25 — Elements of informed consent (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/50.25)
- [21 CFR 50.27 — Documentation of informed consent (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/50.27)
- [21 CFR Part 50 (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50)
- [45 CFR 46.116 — General requirements for informed consent (eCFR)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46/subpart-A/section-46.116)
- [FDA/OHRP — Use of Electronic Informed Consent in Clinical Investigations: Questions and Answers (Dec. 2016)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-electronic-informed-consent-clinical-investigations-questions-and-answers)
- [FDA — Informed Consent guidance for IRBs, investigators, and sponsors (Aug. 2023)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/informed-consent)
- [21 CFR Part 11 (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)
