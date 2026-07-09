---
title: "Form FDA 3674 - Certification of Compliance with ClinicalTrials.gov Requirements"
doc_id: "form-fda-3674-clinicaltrials-gov-certification"
category: "fda-forms"
governing_citations: ["42 U.S.C. 282(j)(5)(B)", "Form FDA 3674"]
owner: "sponsor-investigator"
receiver: "fda"
gate: "submission-to-fda"
status: template
updated: 2026-07-09
---

# Form FDA 3674 - Certification of Compliance with ClinicalTrials.gov Requirements — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [42 U.S.C. 282(j)(5)(B)](https://www.law.cornell.edu/uscode/text/42/282) (certification to accompany specified FDA submissions that the section 402(j) registration and results-reporting requirements have been met), the databank regulations at [42 CFR Part 11](https://www.law.cornell.edu/cfr/text/42/part-11), and Form FDA 3674 itself — obtain the current OMB-approved version from the [FDA Forms index](https://www.fda.gov/about-fda/reports-manuals-forms/forms); FDA's [guidance on Form FDA 3674 certifications (2017)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/form-fda-3674-certifications-accompany-drug-biological-product-and-device-applicationssubmissions) governs when the certification is required. This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** Form FDA 3674 certifies, for a submission to FDA (initial IND, new clinical protocol to an IND, NDA/BLA and efficacy supplements, among others), that the ClinicalTrials.gov registration and results-reporting requirements of PHS Act section 402(j) (42 U.S.C. 282(j)) have been met for the applicable clinical trials referenced in the submission — or that they do not apply. An "applicable drug clinical trial" is, in general, a controlled clinical investigation of a drug (other than a phase 1 study) subject to FDA regulation; registration is due not later than 21 days after enrollment of the first participant.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing. Values are transcribed onto the current OMB-approved Form FDA 3674; this markdown template is the structured worksheet, not the form of record. [INSTRUCTION: The check-box option wording and lettering below follow the current form's structure; verify against the version of Form FDA 3674 in force at the time of submission before transcribing.]

## Template

**CERTIFICATION OF COMPLIANCE, UNDER 42 U.S.C. § 282(j)(5)(B), WITH REQUIREMENTS OF CLINICALTRIALS.GOV DATA BANK (42 U.S.C. § 282(j))**

**FDA application/submission this certification accompanies:** {{submission_reference}} [INSTRUCTION: Identify the IND (or NDA/BLA) number if assigned, and the submission type — e.g., "Initial IND," "New protocol submission to IND {{ind_number}}."]

**Certification** [INSTRUCTION: Check exactly ONE option. Choose based on whether any clinical trial referenced in the accompanying submission is an "applicable clinical trial" under 42 U.S.C. 282(j)(1)(A) and 42 CFR 11.22. Most non-phase-1 interventional drug trials with a U.S. nexus are applicable clinical trials. Phase 1 trials and expanded-access uses are generally NOT applicable clinical trials, but an expanded access record has its own databank obligations for the manufacturer — confirm with the 2017 guidance.]

- [ ] **A.** I certify that the requirements of 42 U.S.C. § 282(j), Section 402(j) of the Public Health Service Act, **do not apply** to any clinical trial referenced in or that forms the basis of this application/submission. [INSTRUCTION: E.g., the submission references only phase 1 studies or nonclinical data.]

- [ ] **B.** I certify that the requirements of 42 U.S.C. § 282(j) **apply** to one or more of the clinical trials referenced in or that form the basis of this application/submission, and that **those requirements have been met** — the applicable clinical trials are registered (and, where required, results have been submitted) in the ClinicalTrials.gov data bank.

  ClinicalTrials.gov registration number(s) (NCT number(s)): {{nct_number}}

- [ ] **C.** I certify that the requirements of 42 U.S.C. § 282(j) **apply** to one or more of the clinical trials referenced in this submission, but that the deadline for submission of the required registration information **has not yet arrived** (for an applicable clinical trial submitted with an IND, registration is required not later than 21 days after the first participant is enrolled). Registration will be completed by the statutory deadline. [INSTRUCTION: This is the usual option for an initial IND or new-protocol submission filed before first enrollment. Create the ClinicalTrials.gov record promptly; the OSSICRO milestone tracker sets the 21-days-after-first-enrollment deadline from the enrollment event.]

**Warning statement** [INSTRUCTION: The form carries this verbatim; do not alter.]

> A willfully and knowingly false statement is a criminal offense under 18 U.S.C. § 1001. Failure to submit the certification required by 42 U.S.C. § 282(j)(5)(B), and knowingly submitting a false certification, are prohibited acts under 21 U.S.C. § 331(jj), subject to civil money penalties under 21 U.S.C. § 333(f)(3).

**Name of person certifying:** {{certifier_name}}

**Title:** {{certifier_title}} [INSTRUCTION: The certifier signs on behalf of the sponsor/applicant; in a sponsor-investigator study this is the sponsor-investigator personally or their documented authorized representative.]

**Signature:** ______________________________

**Date:** {{certification_date}}

> [!warning] Non-delegable
> Submission to FDA is executed by the sponsor-investigator (21 CFR 312.20, 312.23, 312.40; FD&C Act 505(i)). Transmitting this certification to FDA — and the certification signature itself, given its 18 U.S.C. § 1001 exposure — is an explicit human-authorized act. OSSICRO assembles the package and verifies the NCT record exists and matches the protocol; it never files, and the engine cannot finalize this document without a recorded human sign-off.

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{submission_reference}} | document.parent_submission.reference | Form FDA 3674; 42 U.S.C. 282(j)(5)(B) |
| {{ind_number}} | ind.number | Form FDA 3674 |
| {{nct_number}} | study.registration.nct_number | 42 CFR 11.28; 42 U.S.C. 282(j)(2) |
| {{certifier_name}} | study.sponsor_investigator.authorized_signer.name | Form FDA 3674 |
| {{certifier_title}} | study.sponsor_investigator.authorized_signer.title | Form FDA 3674 |
| {{certification_date}} | gates.submission-to-fda.discharge_date | Form FDA 3674 |

## Related

- [[form-fda-3674-clinicaltrialsgov-certification]] (wiki document page)
- [[clinicaltrials-gov-registration]]
- [[pre-ind-and-ind-preparation]]
- [[fda-interactions-meetings-holds]]
