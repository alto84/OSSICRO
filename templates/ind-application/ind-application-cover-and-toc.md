---
title: "IND Application - Cover Letter and Table of Contents"
doc_id: "ind-application-cover-and-toc"
category: "ind-application"
governing_citations: ["21 CFR 312.23(a)(1)", "21 CFR 312.23(a)(2)"]
owner: "sponsor-investigator"
receiver: "fda"
gate: "submission-to-fda"
status: template
updated: 2026-07-09
---

# IND Application - Cover Letter and Table of Contents  — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 312.23(a)(1)](https://www.law.cornell.edu/cfr/text/21/312.23) (cover sheet — Form FDA 1571 transmittal) and [21 CFR 312.23(a)(2)](https://www.law.cornell.edu/cfr/text/21/312.23) (table of contents), assembled under the general principles of [21 CFR 312.22](https://www.law.cornell.edu/cfr/text/21/312.22) and submitted per [21 CFR 312.40](https://www.law.cornell.edu/cfr/text/21/312.40). Form FDA 1571 is the signed transmittal: [FDA Form 1571](https://www.fda.gov/media/72335/download). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** This is the transmittal cover letter and complete table of contents that accompanies an original IND submission (or any subsequent serial submission) to FDA. The cover letter identifies the submission, states its purpose, and orients the reviewing division; the table of contents (312.23(a)(2)) provides the navigable index required for the assembled application. It travels attached to the signed [[form-fda-1571-ind-cover|Form FDA 1571]], which carries the binding sponsor attestation.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing.

## Template

[INSTRUCTION: The cover letter is placed on the sponsor's letterhead. For a sponsor-investigator IND (21 CFR 312.3(b)), the sponsor and the signing individual are the same physician.]

**{{sponsor_name}}**
{{sponsor_address}}

{{submission_date}}

Food and Drug Administration
Center for Drug Evaluation and Research (CDER)
Central Document Room
5901-B Ammendale Road
Beltsville, MD 20705-1266

[INSTRUCTION: Route to CBER (Center for Biologics Evaluation and Research) instead if the product is a biological product. Confirm the current addressee and whether electronic (eCTD) submission is required for this IND type before finalizing.]

**RE: {{submission_type}} — Investigational New Drug Application**
**IND Number: {{ind_number}}**   [INSTRUCTION: For an original IND write "IND Number: Pre-assignment requested / To be assigned." For all subsequent serial submissions, enter the assigned IND number.]
**Serial Number: {{serial_number}}**   [INSTRUCTION: Original IND = 0000; each subsequent submission increments sequentially.]
**Drug/Biologic: {{drug_name}}**
**Proposed Indication: {{indication}}**
**Review Division: {{review_division}}**

Dear Sir or Madam:

On behalf of {{sponsor_name}}, and pursuant to 21 CFR Part 312, enclosed please find {{submission_type}} for the above-referenced investigational new drug, submitted for the conduct of a Phase {{phase}} clinical investigation of {{drug_name}} in {{indication}}.

This submission comprises the following, transmitted under the enclosed signed Form FDA 1571:

- Form FDA 1571 (signed) and this cover letter
- Table of contents (below, per 21 CFR 312.23(a)(2))
- {{submission_contents_summary}}   [INSTRUCTION: One-line summary of what this serial submission contains — e.g., "the complete original IND: introductory statement and general investigational plan, Investigator's Brochure, clinical protocol, CMC information, and pharmacology/toxicology information."]

[INSTRUCTION: For an original IND, include the 30-day statement below. Omit for amendments that are not subject to a new 30-day wait.]
The sponsor understands that the clinical investigation described herein may not be initiated until 30 days after the date of FDA receipt of this application, unless earlier notified by FDA that the studies may proceed, and provided the IND has not been placed on clinical hold (21 CFR 312.40, 312.42).

Please direct any questions or requests for additional information regarding this submission to the regulatory contact identified below.

Sincerely,

_________________________________________
{{contact_name}}
{{contact_title}}
{{sponsor_name}}
Telephone: {{contact_phone}}
Email: {{contact_email}}

---

## Table of Contents — 21 CFR 312.23(a)(2)

[INSTRUCTION: The table of contents must index every section of the assembled IND. The rows below follow the codified content order of 21 CFR 312.23(a). Populate {{toc_sections}} from the assembled study record; enter the actual page or eCTD node reference for each item present in this submission and mark items "Not applicable" or "To be submitted" where appropriate for the phase and submission type.]

| Section | 21 CFR citation | Document | Location/Node |
|---|---|---|---|
| Cover sheet (Form FDA 1571) | 312.23(a)(1) | [[form-fda-1571-ind-cover|Form FDA 1571]] | {{toc_1571_location}} |
| Table of contents | 312.23(a)(2) | This document | {{toc_toc_location}} |
| Introductory statement | 312.23(a)(3)(i)-(iii) | [[ind-introductory-statement|Introductory Statement]] | {{toc_intro_location}} |
| General investigational plan | 312.23(a)(3)(iv) | [[ind-general-investigational-plan|General Investigational Plan]] | {{toc_gip_location}} |
| Investigator's brochure | 312.23(a)(5) | [[investigators-brochure|Investigator's Brochure]] | {{toc_ib_location}} |
| Protocol(s) | 312.23(a)(6) | [[clinical-protocol-ich-m11-ceshharp|Clinical Protocol]] | {{toc_protocol_location}} |
| Chemistry, manufacturing, and control (CMC) | 312.23(a)(7) | {{toc_cmc_document}} | {{toc_cmc_location}} |
| Pharmacology and toxicology | 312.23(a)(8) | {{toc_pharmtox_document}} | {{toc_pharmtox_location}} |
| Previous human experience | 312.23(a)(9) | {{toc_prior_human_document}} | {{toc_prior_human_location}} |
| Additional information | 312.23(a)(10) | {{toc_additional_document}} | {{toc_additional_location}} |
| Relevant information (if requested by FDA) | 312.23(a)(11) | {{toc_relevant_document}} | {{toc_relevant_location}} |

[INSTRUCTION: Delete rows for sections not included in this particular serial submission, or retain and mark "Not included in this submission." Add {{toc_sections}} rows for any supplemental items (e.g., financial disclosure Forms 3454/3455, Form FDA 3674 ClinicalTrials.gov certification, environmental assessment or categorical-exclusion claim).]

> [!warning] Non-delegable
> Submission to FDA is executed by the sponsor-investigator (21 CFR 312.20, 312.23, 312.40; FD&C Act 505(i)). OSSICRO assembles a complete, validated package and drafts this cover letter and table of contents; the engine cannot finalize it without a recorded human sign-off. Transmitting the IND — and applying the Form FDA 1571 signature that binds it — is an explicit human-authorized act, and software cannot be the sponsor (21 CFR 312.52).

## Fields
| placeholder | source (study-record path) | citation |
|---|---|---|
| {{sponsor_name}} | study.sponsor.name | 21 CFR 312.23(a)(1) |
| {{sponsor_address}} | study.sponsor.address | 21 CFR 312.23(a)(1) |
| {{submission_date}} | submission.date | 21 CFR 312.23(a)(2) |
| {{submission_type}} | submission.type | 21 CFR 312.23 |
| {{ind_number}} | study.ind.number | 21 CFR 312.23(a)(1) |
| {{serial_number}} | submission.serial_number | 21 CFR 312.23(d) |
| {{drug_name}} | study.drug.name | 21 CFR 312.23(a)(1) |
| {{indication}} | study.indication | 21 CFR 312.23(a)(3) |
| {{review_division}} | submission.review_division | 21 CFR 312.23(d) |
| {{phase}} | study.phase | 21 CFR 312.23(a)(3) |
| {{submission_contents_summary}} | submission.contents_summary | 21 CFR 312.23(a)(2) |
| {{contact_name}} | study.sponsor.regulatory_contact.name | 21 CFR 312.23(a)(1) |
| {{contact_title}} | study.sponsor.regulatory_contact.title | 21 CFR 312.23(a)(1) |
| {{contact_phone}} | study.sponsor.regulatory_contact.phone | 21 CFR 312.23(a)(1) |
| {{contact_email}} | study.sponsor.regulatory_contact.email | 21 CFR 312.23(a)(1) |
| {{toc_sections}} | submission.toc[] | 21 CFR 312.23(a)(2) |
| {{toc_*_location}} | submission.toc[].location | 21 CFR 312.23(a)(2) |
| {{toc_*_document}} | submission.toc[].document | 21 CFR 312.23(a)(2) |

## Related
- [[ind-application-312-23]]
- [[form-fda-1571-ind-cover]]
- [[ind-introductory-statement]]
- [[ind-general-investigational-plan]]
- [[investigators-brochure]]
- [[ind-submission-and-30-day-clock]]
- [[pre-ind-and-ind-preparation]]
- [[non-delegable-functions-and-gates]]
