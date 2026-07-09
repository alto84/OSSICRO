---
title: "Enrollment and Consent"
section: "02-lifecycle"
status: mixed
governing_authority:
  - "21 CFR Part 50 (esp. 50.20, 50.25, 50.27)"
  - "21 CFR 312.62(b)"
  - "21 CFR 56.111(a)(4)-(5)"
  - "45 CFR 46.116–46.117 (where the Common Rule applies)"
  - "45 CFR 164.508, 164.512(i) (HIPAA)"
  - "ICH E6(R3) Annex 1 §2 and Appendix C"
tags: [lifecycle/conduct, cfr/50, cfr/56, cfr/312, ich/e6r3, ossicro/gating, status/confirmed, status/interpretive]
aliases: ["informed consent", "subject enrollment", "screening and enrollment"]
updated: 2026-07-09
---

# Enrollment and Consent

> [!authority] Governing authority
> [21 CFR Part 50](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50) (informed consent: general requirements 50.20, elements 50.25, documentation 50.27); [21 CFR 312.62(b)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.62) (case histories must document that consent was obtained prior to participation); 45 CFR 46.116–46.117 where federal funding attaches; HIPAA 45 CFR 164.508/164.512(i); ICH E6(R3) Annex 1 §2. Status: **Mixed** — consent requirements are confirmed black-letter law; OSSICRO's eligibility pre-screen and consent-version gating are interpretive design positions.

Enrollment is where the trial touches a human being, and it is governed by the brightest line in the OSSICRO system: **the consent *document* is drafted by software; the consent *event* — a qualified person obtaining a prospective subject's legally effective, voluntary agreement — is non-delegable to software under any configuration** (see [[informed-consent-document-vs-event]]). This page covers the preconditions to first screening, the consent event and its content, eligibility determination, the screening/enrollment record set, and re-consent.

## Preconditions to screening the first subject

All of the following gates must be closed before any protocol-driven procedure is performed on any person:

1. **IND may-proceed** — 30-day clock elapsed or FDA earlier notification; no clinical hold (21 CFR 312.40, 312.42; [[ind-submission-and-30-day-clock]]).
2. **Documented IRB approval** — approval letter on file and the consent form in use is the exact IRB-approved current version (21 CFR 56.103(a), 312.66; [[irb-submission-and-approval]]).
3. **[[site-activation|Site activated]]** — 1572 signed, delegation log live, staff trained, drug accountable.
4. **HIPAA basis transitioned** — identification of candidates may proceed under the review-preparatory-to-research provision (45 CFR 164.512(i)(1)(ii)), but contact, screening, and use of PHI for the trial itself require the subject's written authorization (45 CFR 164.508) or an IRB/Privacy Board waiver (45 CFR 164.512(i)(1)(i)). OSSICRO logs this transition as a hard state change — see [[privacy-state-machine]] and [[hipaa-and-privacy-gating]].

Where screening itself involves protocol-required procedures beyond standard care, consent (a screening consent or the main ICF) must precede those procedures; 312.62(b) requires the case history to document that consent was obtained **prior to participation in the study**.

## The consent event

**General requirements (21 CFR 50.20).** No investigator may involve a human being as a subject unless the investigator has obtained the legally effective informed consent of the subject or the subject's legally authorized representative (LAR), under circumstances that provide sufficient opportunity to consider participation and minimize coercion or undue influence, in language understandable to the subject, and containing no exculpatory language waiving the subject's rights or releasing the investigator, sponsor, or institution from liability for negligence. Exceptions exist only under 21 CFR 50.23 (specific life-threatening/military/public-health circumstances) and 50.24 (emergency research with IRB and community safeguards) — narrow, heavily conditioned pathways outside OSSICRO's default flows.

**Who obtains consent.** The investigator is responsible for the consent process (21 CFR 312.60; Form 1572 Field 9 commitment). FDA's 2009 guidance on investigator responsibilities recognizes that the consent *conversation* may be delegated to qualified site staff documented on the [[delegation-of-authority-log]] — but responsibility never transfers, and the delegate must be a qualified human. Nothing in Part 50 permits delegation to software.

> [!warning] Non-delegable
> The consent event is a human act: a qualified individual, accountable through the delegation log to the investigator, conducting a comprehension-checked conversation and obtaining voluntary agreement. OSSICRO drafts and version-controls the ICF, schedules the event, confirms the correct version, and files the executed form — it never conducts, replaces, or simulates the conversation, and it never assesses a subject's comprehension or voluntariness. Likewise, **eligibility determination is the investigator's clinical judgment** (21 CFR 312.60 protocol adherence); OSSICRO's [[matching-eligibility-adjudication|per-criterion adjudication]] is decision support that must surface, never settle, the call. See [[non-delegable-functions-and-gates]].

**Required content (21 CFR 50.25).** The eight basic elements of 50.25(a): (1) a statement that the study involves research, its purposes, expected duration, procedures, and identification of any experimental procedures; (2) reasonably foreseeable risks or discomforts; (3) benefits reasonably to be expected; (4) appropriate alternative procedures or treatments; (5) the extent of confidentiality of records, noting the possibility of FDA inspection; (6) for more-than-minimal-risk research, whether compensation and medical treatments are available if injury occurs; (7) whom to contact about the research, subjects' rights, and research-related injury; (8) that participation is voluntary, refusal involves no penalty or loss of benefits, and the subject may discontinue at any time. The additional elements of 50.25(b) apply where appropriate (unforeseeable risks; involuntary-termination circumstances; additional costs; withdrawal consequences; the commitment that **significant new findings** affecting willingness to continue will be provided — the re-consent trigger; approximate number of subjects). For applicable clinical trials, 50.25(c) mandates the verbatim ClinicalTrials.gov statement ([[clinicaltrials-gov-registration]]). Where the revised Common Rule also applies, consent must begin with the concise key-information presentation (45 CFR 46.116(a)(5)). See [[informed-consent-form]] for the drafting template.

**Documentation (21 CFR 50.27).** Consent is documented by a written form approved by the IRB and **signed and dated by the subject or the subject's LAR at the time of consent**; a copy is given to the person signing. 50.27(b)(2) permits a short-form oral presentation with a witness and an IRB-approved written summary. Electronic consent is permissible under the joint FDA/OHRP 2016 eConsent Q&A, with Part 11 controls on the e-signature and record ([[part-11-and-ai-credibility]]). The executed ICF is an essential record ([[conduct-tmf-checklist]]); the case history must show consent preceded participation (312.62(b)).

## Eligibility determination and the enrollment decision

Eligibility is adjudicated criterion-by-criterion against the IRB-approved protocol version. OSSICRO's adjudication layer produces a three-valued pre-screen (met / not-met / indeterminate-needs-data) with chart and criterion citations ([[matching-eligibility-adjudication]]); indeterminate items become explicit questions for the investigator. The investigator signs the eligibility confirmation; protocol waivers of entry criteria are not within the investigator's gift — an exception requires a protocol amendment or documented sponsor and IRB action, and enrolling an ineligible subject is a reportable deviation ([[conduct-and-monitoring]]).

## Screening and enrollment records

Three logs account for every person who approaches the trial (21 CFR 312.62(b); ICH E6(R3) Appendix C; E6(R2) §8.3.20–8.3.22):

- **Subject screening log** — every candidate screened, with screen-failure reasons; evidences equitable selection (56.111(a)(3)) and supports CONSORT-style accounting.
- **Subject identification code list** — the confidential key linking coded subject IDs to identities; held at the site only, never transmitted to the sponsor, never entered into OSSICRO logs (subject identities are coded throughout the [[data-model]]).
- **Subject enrollment log** — chronological record of enrollment with subject codes.

Each consent event generates: the executed ICF (original to the ISF, copy to the subject), the case-history note documenting the process and its timing relative to first procedure, and — where eConsent is used — the Part-11 audit-trail record.

## Re-consent

Re-consent (or an IRB-approved addendum) is required when significant new findings develop that may relate to the subject's willingness to continue (50.25(b)(5)) — typically new safety information from [[safety-reporting-lifecycle|IND safety reports]] or IB updates — and when a protocol amendment alters the risk-benefit information previously presented ([[annual-reporting-and-amendments]]). The IRB approves the revised ICF before use; OSSICRO tracks which enrolled subjects consented on which version and flags every subject due for re-consent — but a qualified human conducts each re-consent conversation.

## Vulnerable populations

Enrollment of children engages 21 CFR Part 50 Subpart D (50.50–50.56: risk categories, parental permission, assent); other vulnerable groups engage the additional-safeguards requirement of 56.111(b). These pathways add IRB findings and consent-document variants that OSSICRO templates but never adjudicates.

> [!interpretive] OSSICRO position
> Two mechanisms on this page are OSSICRO design positions rather than regulatory requirements: (1) code-enforced version gating — the system refuses to print or present any ICF that is not the IRB-approved current version, and blocks the enrollment workflow for a subject whose executed ICF version predates an approved amendment requiring re-consent; (2) the three-valued eligibility pre-screen. Both are built *on top of* confirmed requirements (56.109 version approval; 312.60 protocol adherence) and both fail toward a human, never past one.

## Related

- [[informed-consent-document-vs-event]] — the bright line, in full
- [[informed-consent-form]] — the 50.25 drafting template and eConsent treatment
- [[irb-submission-and-approval]] · [[site-activation]] — the gates that precede this stage
- [[matching-eligibility-adjudication]] · [[patient-trial-matching]] — upstream discovery and pre-screen
- [[hipaa-and-privacy-gating]] · [[privacy-state-machine]] — the preparatory→enrollment privacy transition
- [[conduct-and-monitoring]] — where enrolled subjects' data live
- [[delegation-of-authority-log]] — who may conduct the consent conversation
- [[conduct-tmf-checklist]] · [[non-delegable-functions-and-gates]]
- [[patient|Patient persona]] — the subject's-eye view of these protections

## Sources

- [21 CFR Part 50 — Protection of Human Subjects (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50)
- [21 CFR 312.62 — Investigator recordkeeping and record retention (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.62)
- [45 CFR 46.116 — General requirements for informed consent (eCFR)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46/subpart-A/section-46.116)
- [45 CFR 164.508 / 164.512 — HIPAA authorization and research provisions (eCFR)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164)
- [FDA/OHRP Guidance — Use of Electronic Informed Consent in Clinical Investigations: Questions and Answers (2016)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-electronic-informed-consent-clinical-investigations-questions-and-answers)
- [FDA Guidance — Investigator Responsibilities: Protecting the Rights, Safety, and Welfare of Study Subjects (2009)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/investigator-responsibilities-protecting-rights-safety-and-welfare-study-subjects)
- [ICH E6(R3) Guideline for Good Clinical Practice, Step 4 Final (6 Jan 2025)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
