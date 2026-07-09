---
title: "Subject Identification Code List (confidential)"
doc_id: "subject-identification-code-list"
category: "site-management"
governing_citations: ["21 CFR 312.62(b)", "ICH E6(R3) Appendix C"]
owner: "investigator"
receiver: "site-file"
gate: "none"
status: template
updated: 2026-07-09
---

# Subject Identification Code List (confidential) — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 312.62(b)](https://www.law.cornell.edu/cfr/text/21/312.62) (investigator prepares and maintains adequate and accurate case histories) and [ICH E6(R3) Appendix C](https://www.ich.org/page/efficacy-guidelines) (essential records — subject identification code list, retained by the investigator/institution, permitting identification of all subjects enrolled in the trial in case follow-up is required, kept in a confidential manner). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** The confidential key linking each study-assigned subject code to the subject's identity, so the site can re-identify subjects for safety follow-up, record verification, or recall. Retained ONLY at the site; it is the single document that de-anonymizes the trial record.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing.

## Template

> **CONFIDENTIAL — SITE COPY ONLY.** This document is never transmitted to the sponsor, CRO, or any external party. Monitors and inspectors may review it on-site but do not copy or remove it. Store under restricted access separate from documents that leave the site.

### Study Identification

| Field | Value |
|---|---|
| Protocol number | {{protocol_number}} |
| Site name | {{site_name}} |
| Principal Investigator | {{investigator_name}} |

### Code Entries

| Subject study code | Screening # | Subject full name | Date of birth | Medical record number | Date of consent | Staff initials / date of entry |
|---|---|---|---|---|---|---|
| {{subject_number}} | {{screening_number}} | {{subject_full_name}} | {{subject_dob}} | {{medical_record_number}} | {{consent_date}} | |
| | | | | | | |
| | | | | | | |

[INSTRUCTION: One row per consented subject, entered at the time the screening or subject number is assigned. Entries are made only by staff delegated regulatory-document tasks on the Delegation of Authority Log. Corrections use single-line strike-through with initials and date — never obliterate an identity linkage, because the whole purpose of this list is durable re-identification for safety follow-up.]

[INSTRUCTION: Retention — this list is part of the investigator's records under 21 CFR 312.62(c): retain for 2 years following the date a marketing application is approved for the drug for the indication studied, or, if no application is filed or it is not approved, 2 years after the investigation is discontinued and FDA is notified. Do not destroy at study close-out; record its archive location in the Record Retention and Archival Statement.]

[INSTRUCTION: Privacy — the identifiers on this list are protected health information; handle per the site's HIPAA policies and the study's HIPAA authorization (45 CFR 164.508). Access is limited to delegated site staff and, on-site, to monitors/auditors/FDA per the consent's confidentiality disclosure.]

## Fields
| placeholder | source (study-record path) | citation |
|---|---|---|
| {{protocol_number}} | study.protocol.number | ICH E6(R3) Appendix C |
| {{site_name}} | site.name | ICH E6(R3) Appendix C |
| {{investigator_name}} | site.principal_investigator.name | 21 CFR 312.62(b) |
| {{subject_number}} | site.subjects[].subject_number | ICH E6(R3) Appendix C |
| {{screening_number}} | site.subjects[].screening_number | ICH E6(R3) Appendix C |
| {{subject_full_name}} | site.subjects[].identity.full_name (site-local store only — never synced off-site) | 21 CFR 312.62(b) |
| {{subject_dob}} | site.subjects[].identity.dob (site-local store only — never synced off-site) | 21 CFR 312.62(b) |
| {{medical_record_number}} | site.subjects[].identity.mrn (site-local store only — never synced off-site) | 21 CFR 312.62(b) |
| {{consent_date}} | site.subjects[].consent_date | 21 CFR 50.27 |

## Related
- [[03-documents/subject-identification-code-list]]
- [[03-documents/screening-enrollment-withdrawal-log]]
- [[03-documents/hipaa-authorization]]
- [[03-documents/record-retention-and-archival-statement]]
