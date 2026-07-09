---
title: "Screening / Enrollment / Withdrawal Log"
doc_id: "screening-enrollment-withdrawal-log"
category: "site-management"
governing_citations: ["ICH E6(R3) Appendix C"]
owner: "investigator"
receiver: "site-file"
gate: "none"
status: template
updated: 2026-07-09
---

# Screening / Enrollment / Withdrawal Log — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [ICH E6(R3) Appendix C](https://www.ich.org/page/efficacy-guidelines) (essential records — subject screening log documenting identification of subjects who entered pre-trial screening, and subject enrolment log documenting chronological enrolment by trial number). See also [21 CFR 312.62(b)](https://www.law.cornell.edu/cfr/text/21/312.62) (adequate and accurate case histories). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** Chronological site record of every candidate who entered screening, the screening outcome, enrollment/randomization, and any withdrawal — establishing the accountable denominator for enrollment and demonstrating unbiased subject selection. Maintained continuously through the conduct phase.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing.

## Template

### Study Identification

| Field | Value |
|---|---|
| Protocol number | {{protocol_number}} |
| Site name | {{site_name}} |
| Principal Investigator | {{investigator_name}} |

### Log Entries

| Screening # | Date consent signed | Date screened | Eligible? (Y/N) | Screen-fail reason (criterion #) | Subject / randomization # | Enrollment date | Withdrawal date | Withdrawal reason | Status (screening / enrolled / completed / withdrawn / screen-fail) | Staff initials |
|---|---|---|---|---|---|---|---|---|---|---|
| {{screening_number}} | {{consent_date}} | {{screening_date}} | {{eligible_flag}} | {{screen_fail_reason}} | {{subject_number}} | {{enrollment_date}} | {{withdrawal_date}} | {{withdrawal_reason}} | {{subject_status}} | |
| | | | | | | | | | | |
| | | | | | | | | | | |

[INSTRUCTION: This log carries only the study-assigned screening and subject numbers — NO subject names, initials, or other direct identifiers, because copies may be provided to the sponsor/monitor. The link between screening/subject numbers and identities lives exclusively in the confidential Subject Identification Code List retained at the site.]

[INSTRUCTION: Assign screening numbers sequentially and chronologically; never reuse a number, including for re-screened subjects (assign a new screening number and cross-reference the prior one in the screen-fail reason column). Informed consent must be documented BEFORE any protocol-specific screening procedure (21 CFR 50.20; 312.60).]

[INSTRUCTION: Withdrawal reason categories — subject withdrew consent; lost to follow-up; adverse event; investigator decision; sponsor termination; death; other (specify). "Withdrew consent" and "lost to follow-up" are distinct: do not record lost-to-follow-up as consent withdrawal. Enrollment counts from this log feed the IRB continuing-review progress report.]

## Fields
| placeholder | source (study-record path) | citation |
|---|---|---|
| {{protocol_number}} | study.protocol.number | ICH E6(R3) Appendix C |
| {{site_name}} | site.name | ICH E6(R3) Appendix C |
| {{investigator_name}} | site.principal_investigator.name | ICH E6(R3) Appendix C |
| {{screening_number}} | site.subjects[].screening_number | ICH E6(R3) Appendix C |
| {{consent_date}} | site.subjects[].consent_date | 21 CFR 50.27 |
| {{screening_date}} | site.subjects[].screening_date | ICH E6(R3) Appendix C |
| {{eligible_flag}} | site.subjects[].eligible | ICH E6(R3) Appendix C |
| {{screen_fail_reason}} | site.subjects[].screen_fail_reason | ICH E6(R3) Appendix C |
| {{subject_number}} | site.subjects[].subject_number | ICH E6(R3) Appendix C |
| {{enrollment_date}} | site.subjects[].enrollment_date | ICH E6(R3) Appendix C |
| {{withdrawal_date}} | site.subjects[].withdrawal_date | ICH E6(R3) Appendix C |
| {{withdrawal_reason}} | site.subjects[].withdrawal_reason | ICH E6(R3) Appendix C |
| {{subject_status}} | site.subjects[].status | ICH E6(R3) Appendix C |

## Related
- [[03-documents/screening-enrollment-withdrawal-log]]
- [[03-documents/subject-identification-code-list]]
- [[03-documents/informed-consent-form-part50]]
- [[03-documents/irb-continuing-review-progress-report]]
