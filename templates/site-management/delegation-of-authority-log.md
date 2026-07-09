---
title: "Delegation of Authority / Site Responsibility Log"
doc_id: "delegation-of-authority-log"
category: "site-management"
governing_citations: ["ICH E6(R3) 2.7", "FDA Guidance: Investigator Responsibilities (2009)"]
owner: "investigator"
receiver: "site-file"
gate: "none"
status: template
updated: 2026-07-09
---

# Delegation of Authority / Site Responsibility Log — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [ICH E6(R3) §2.7](https://www.ich.org/page/efficacy-guidelines) (investigator supervision and delegation of trial-related activities) and [FDA Guidance for Industry: Investigator Responsibilities — Protecting the Rights, Safety, and Welfare of Study Subjects (October 2009)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/investigator-responsibilities-protecting-rights-safety-and-welfare-study-subjects). See also [21 CFR 312.60](https://www.law.cornell.edu/cfr/text/21/312.60) (general responsibilities of investigators). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** Documents which study tasks the investigator has delegated to which qualified site staff, for what period, under the investigator's continuing supervision. Established at site startup before any delegated task is performed, and maintained as a living document for the duration of the study.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing.

## Template

### Study Identification

| Field | Value |
|---|---|
| Protocol number | {{protocol_number}} |
| Protocol version / date | {{protocol_version}} |
| Protocol title | {{protocol_title}} |
| IND number | {{ind_number}} |
| Site name | {{site_name}} |
| Principal Investigator | {{investigator_name}} |
| Log effective date | {{effective_date}} |

[INSTRUCTION: The effective date must be on or before the date of the first delegated task performed under this protocol at this site. If a prior version of this log exists, supersede it explicitly and retain the prior version in the Investigator Site File.]

### Study Task Codes

[INSTRUCTION: Edit this task list to match the protocol. Delete tasks not applicable to this study; add protocol-specific tasks with new codes. Tasks involving medical judgment (eligibility determinations requiring clinical assessment, adverse event causality/severity assessment, IP dose decisions) may be delegated only to licensed physicians, or to other licensed practitioners where the task is within their scope of practice, per the 2009 FDA guidance §III.A. The investigator's supervisory responsibility itself is not delegable.]

| Code | Delegated study task |
|---|---|
| 1 | Obtain informed consent (21 CFR 50.20; 312.60) |
| 2 | Assess eligibility / inclusion-exclusion review |
| 3 | Medical history and physical examination |
| 4 | Adverse event identification and documentation |
| 5 | Adverse event severity / causality assessment [INSTRUCTION: physician or qualified licensed practitioner only] |
| 6 | Investigational product prescription / dose decisions [INSTRUCTION: licensed prescriber only] |
| 7 | Investigational product dispensing / accountability |
| 8 | Vital signs and study-specific assessments |
| 9 | Specimen collection, processing, shipment |
| 10 | CRF/eCRF data entry |
| 11 | Query resolution |
| 12 | Regulatory document maintenance (ISF) |
| 13 | Randomization / IWRS transactions |
| 14 | {{additional_task_description}} |

### Delegation Entries

| Name (printed) | Role / title | Task codes delegated | Signature | Initials | Start date | End date | PI authorization (initials / date) |
|---|---|---|---|---|---|---|---|
| {{staff_name}} | {{staff_role}} | {{delegated_task_codes}} | | | {{delegation_start_date}} | {{delegation_end_date}} | |
| | | | | | | | |
| | | | | | | | |

[INSTRUCTION: One row per staff member. The PI initials and dates each row BEFORE the individual performs any listed task. Start date must not precede the individual's documented training on the protocol and GCP. End date is completed when the individual leaves the study or a delegation is withdrawn; do not leave rows open after departure. Wet-ink or Part 11-compliant electronic signatures only.]

### Principal Investigator Attestation

I confirm that each individual listed above is qualified by education, training, and experience to perform the tasks delegated; that each has been trained on the current protocol version; and that I will maintain adequate supervision of all delegated activities (ICH E6(R3) 2.7; FDA Guidance 2009).

| | |
|---|---|
| PI signature | ______________________ |
| PI name (printed) | {{investigator_name}} |
| Date | ______________________ |

## Fields
| placeholder | source (study-record path) | citation |
|---|---|---|
| {{protocol_number}} | study.protocol.number | ICH E6(R3) Appendix C |
| {{protocol_version}} | study.protocol.version | ICH E6(R3) Appendix C |
| {{protocol_title}} | study.protocol.title | ICH E6(R3) Appendix C |
| {{ind_number}} | study.ind.number | 21 CFR 312.23(a)(1) |
| {{site_name}} | site.name | ICH E6(R3) 2.7 |
| {{investigator_name}} | site.principal_investigator.name | 21 CFR 312.60 |
| {{effective_date}} | site.delegation_log.effective_date | ICH E6(R3) 2.7 |
| {{additional_task_description}} | site.delegation_log.custom_tasks[] | FDA Guidance: Investigator Responsibilities (2009) §III.A |
| {{staff_name}} | site.staff[].name | ICH E6(R3) 2.7 |
| {{staff_role}} | site.staff[].role | ICH E6(R3) 2.7 |
| {{delegated_task_codes}} | site.staff[].delegated_tasks[] | FDA Guidance: Investigator Responsibilities (2009) §III.A |
| {{delegation_start_date}} | site.staff[].delegation_start | ICH E6(R3) 2.7 |
| {{delegation_end_date}} | site.staff[].delegation_end | ICH E6(R3) 2.7 |

## Related
- [[03-documents/delegation-of-authority-log]]
- [[03-documents/site-signature-initial-log]]
- [[03-documents/investigator-cv-and-qualifications]]
- [[03-documents/form-fda-1572-statement-of-investigator]]
