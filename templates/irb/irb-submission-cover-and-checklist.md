---
title: "IRB Submission Cover and Checklist"
doc_id: "irb-submission-cover-and-checklist"
category: "irb"
governing_citations: ["21 CFR 56.109", "21 CFR 312.66"]
owner: "investigator"
receiver: "irb"
gate: "none"
status: template
updated: 2026-07-09
---

# IRB Submission Cover and Checklist — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 56.109](https://www.law.cornell.edu/cfr/text/21/56.109) (IRB review of research); [21 CFR 312.66](https://www.law.cornell.edu/cfr/text/21/312.66) (assurance of IRB review — the investigator must assure that an IRB compliant with Part 56 is responsible for initial and continuing review and approval). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** Cover letter and document inventory transmitted by the investigator to the reviewing IRB with an initial submission (new protocol), so the IRB receives a complete, versioned package sufficient to conduct review under 21 CFR 56.109 and 56.111. It creates the auditable record of exactly what was submitted, in what version, on what date.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing.

## Template

{{submission_date}}

{{irb_name}}
{{irb_address}}

**Re: Initial submission for review — Protocol {{protocol_number}}**

**Protocol title:** {{protocol_title}}
**Protocol version/date:** {{protocol_version}}, dated {{protocol_date}}
**Investigational product:** {{drug_name}}
**IND number:** {{ind_number}} [INSTRUCTION: If the IND is not yet in effect, state "IND submitted {{ind_submission_date}}; 30-day review period per 21 CFR 312.40(b)(1)". If exempt, state the basis for exemption under 21 CFR 312.2(b).]
**Sponsor / sponsor-investigator:** {{sponsor_name}}
**Phase:** {{phase}}
**Principal Investigator:** {{investigator_name}}, {{investigator_degrees}}
**Site:** {{site_name}}, {{site_address}}

Dear IRB Chair / IRB Administrator:

I am submitting the above-referenced protocol for initial review and approval by {{irb_name}} pursuant to 21 CFR Part 56. As investigator, I provide my assurance under 21 CFR 312.66 that an IRB in compliance with 21 CFR Part 56 will be responsible for the initial and continuing review and approval of this clinical investigation, that I will promptly report to the IRB all changes in the research activity and all unanticipated problems involving risk to human subjects or others, and that I will not make any changes in the research without IRB approval, except where necessary to eliminate apparent immediate hazards to human subjects.

**Type of review requested:** {{review_type_requested}} [INSTRUCTION: "Convened (full board)" for greater-than-minimal-risk drug studies; expedited review under 21 CFR 56.110 is available only for the categories on the FDA/OHRP expedited list and minimal-risk research — most IND studies require full board.]

### Document checklist

[INSTRUCTION: The table below is the submission inventory. One row per enclosed document; the engine populates it from {{documents_list}}. Check the reviewing IRB's own submission form/portal requirements — many IRBs require their institution-specific application form in addition to this inventory.]

| # | Document | Version | Date | Enclosed |
|---|----------|---------|------|----------|
| 1 | Clinical protocol | {{protocol_version}} | {{protocol_date}} | ☐ |
| 2 | Informed consent form (ICF) | {{icf_version}} | {{icf_date}} | ☐ |
| 3 | HIPAA authorization (if separate from ICF) | {{hipaa_version}} | {{hipaa_date}} | ☐ |
| 4 | Investigator's Brochure (or package insert if approved drug) | {{ib_edition}} | {{ib_date}} | ☐ |
| 5 | Investigator CV and medical license | — | {{cv_date}} | ☐ |
| 6 | Form FDA 1572 (copy) | — | {{form_1572_date}} | ☐ |
| 7 | Recruitment materials / advertisements | {{recruitment_version}} | {{recruitment_date}} | ☐ |
| 8 | Subject-facing materials (diaries, instruction sheets) | {{subject_materials_version}} | {{subject_materials_date}} | ☐ |
| 9 | Data and safety monitoring plan | {{dsmp_version}} | {{dsmp_date}} | ☐ |
| 10 | {{additional_document}} | {{additional_document_version}} | {{additional_document_date}} | ☐ |

[INSTRUCTION: Delete rows that do not apply and add rows for any other enclosed item ({{documents_list}} is the authoritative set). Advertisements are considered part of the informed consent/subject-selection process and require IRB review before use.]

### Study summary for the reviewer

{{study_summary}} [INSTRUCTION: 1-2 paragraphs — population, design, intervention, primary endpoint, principal risks, and risk-mitigation. Written to help the board apply the 21 CFR 56.111 approval criteria; do not oversell benefit.]

**Conflict-of-interest statement:** {{coi_statement}} [INSTRUCTION: Disclose any financial interest of the investigator or sub-investigators relevant to 21 CFR Part 54; state "none" affirmatively if none.]

Please direct questions and the IRB's written determination (21 CFR 56.109(e)) to the contact below.

Sincerely,

______________________________  Date: ____________
{{investigator_name}}, {{investigator_degrees}}
Principal Investigator

**Regulatory contact:** {{contact_name}}, {{contact_phone}}, {{contact_email}}

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{submission_date}} | submissions.irb_initial.date | 21 CFR 56.109 |
| {{irb_name}} | study.irb.name | 21 CFR 312.66 |
| {{irb_address}} | study.irb.address | 21 CFR 312.66 |
| {{protocol_number}} | study.protocol.number | 21 CFR 56.109 |
| {{protocol_title}} | study.protocol.title | 21 CFR 56.109 |
| {{protocol_version}} | study.protocol.version | 21 CFR 56.109 |
| {{protocol_date}} | study.protocol.date | 21 CFR 56.109 |
| {{drug_name}} | study.product.name | 21 CFR 312.23(a)(1) |
| {{ind_number}} | study.ind.number | 21 CFR 312.40 |
| {{ind_submission_date}} | study.ind.submission_date | 21 CFR 312.40(b)(1) |
| {{sponsor_name}} | study.sponsor.name | 21 CFR 312.3 |
| {{phase}} | study.protocol.phase | 21 CFR 312.21 |
| {{investigator_name}} | study.investigator.name | 21 CFR 312.66 |
| {{investigator_degrees}} | study.investigator.degrees | 21 CFR 312.53(c)(2) |
| {{site_name}} | study.site.name | 21 CFR 312.53 |
| {{site_address}} | study.site.address | 21 CFR 312.53 |
| {{review_type_requested}} | submissions.irb_initial.review_type | 21 CFR 56.108(c), 56.110 |
| {{documents_list}} | submissions.irb_initial.documents[] | 21 CFR 56.109 |
| {{icf_version}} / {{icf_date}} | documents.icf.version / .date | 21 CFR 50.27 |
| {{hipaa_version}} / {{hipaa_date}} | documents.hipaa_authorization.version / .date | 45 CFR 164.508 |
| {{ib_edition}} / {{ib_date}} | documents.ib.edition / .date | 21 CFR 312.55 |
| {{cv_date}} | study.investigator.cv_date | 21 CFR 312.53(c)(2) |
| {{form_1572_date}} | documents.form_1572.date | 21 CFR 312.53(c)(1) |
| {{recruitment_version}} / {{recruitment_date}} | documents.recruitment.version / .date | 21 CFR 56.109 |
| {{subject_materials_version}} / {{subject_materials_date}} | documents.subject_materials.version / .date | 21 CFR 56.109 |
| {{dsmp_version}} / {{dsmp_date}} | documents.dsmp.version / .date | ICH E6(R3) 3.10 |
| {{additional_document}} (+version/date) | submissions.irb_initial.documents[].name | 21 CFR 56.109 |
| {{study_summary}} | study.protocol.synopsis | 21 CFR 56.111 |
| {{coi_statement}} | study.investigator.coi_statement | 21 CFR Part 54 |
| {{contact_name}} / {{contact_phone}} / {{contact_email}} | study.contacts.regulatory.* | — |

## Related

- [[irb-submission-package]] — wiki document page for the IRB submission package
- [[irb-submission-and-approval]] — lifecycle page (startup)
- [[irb-review-workflow]] — coordination page for the review cycle
- [[informed-consent-form]] — the consent document enclosed with this submission
