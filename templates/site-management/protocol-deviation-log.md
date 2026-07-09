---
title: "Protocol Deviation Log"
doc_id: "protocol-deviation-log"
category: "site-management"
governing_citations: ["ICH E6(R3) Appendix C", "21 CFR 312.66"]
owner: "investigator"
receiver: "site-file"
gate: "none"
status: template
updated: 2026-07-09
---

# Protocol Deviation Log — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [ICH E6(R3) Appendix C](https://www.ich.org/page/efficacy-guidelines) (essential records — documentation of deviations from the protocol) and [21 CFR 312.66](https://www.law.cornell.edu/cfr/text/21/312.66) (investigator shall not make changes in the research without IRB approval, except where necessary to eliminate apparent immediate hazards; investigator promptly reports to the IRB changes and unanticipated problems). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** Running site record of every departure from the IRB-approved protocol — planned or unplanned — with its assessment, corrective/preventive action, and reporting disposition. Maintained continuously through the conduct phase and reconciled at monitoring visits and close-out.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing.

## Template

### Study Identification

| Field | Value |
|---|---|
| Protocol number | {{protocol_number}} |
| Site name | {{site_name}} |
| Principal Investigator | {{investigator_name}} |

### Deviation Entries

| Dev # | Subject code | Date of deviation | Date identified | Description of deviation | Category | Important? (Y/N) | Root cause | Corrective / preventive action | Reported to sponsor (date) | Reported to IRB (date or N/A per IRB policy) | PI initials / date |
|---|---|---|---|---|---|---|---|---|---|---|---|
| {{deviation_number}} | {{subject_code}} | {{deviation_date}} | {{identified_date}} | {{deviation_description}} | {{deviation_category}} | {{important_flag}} | {{root_cause}} | {{capa_description}} | {{sponsor_report_date}} | {{irb_report_date}} | |
| | | | | | | | | | | | |
| | | | | | | | | | | | |

[INSTRUCTION: Category values — informed consent; eligibility; visit window; procedure omitted/added; investigational product (dosing, storage, accountability); safety reporting; randomization/blinding; other. "Important" deviations (ICH E6(R3): those that significantly affect subject rights, safety, or well-being, or the reliability of trial results) require prompt sponsor notification and reporting to the IRB per the IRB's policy and 21 CFR 312.66. Do not pre-judge a deviation as non-important to avoid reporting; when in doubt, the PI decides and documents the rationale.]

[INSTRUCTION: A change made WITHOUT prior IRB approval to eliminate an apparent immediate hazard to subjects is permitted under 21 CFR 312.66 but must be reported promptly to the IRB and sponsor — log it here and reference the emergency circumstances in the description.]

[INSTRUCTION: If no deviations occurred during a monitoring interval, do not fabricate entries; the monitor documents "no deviations identified" in the visit report. Never white-out or overwrite an entry — correct with single-line strike-through, initials, and date.]

### Periodic PI Review

| Review date | Entries reviewed through Dev # | PI signature | Comments |
|---|---|---|---|
| {{review_date}} | {{last_reviewed_deviation_number}} | | |

[INSTRUCTION: The PI reviews the log at a defined cadence (at minimum before each monitoring visit and each IRB continuing review) and signs. Deviation summaries feed the IRB continuing-review progress report.]

## Fields
| placeholder | source (study-record path) | citation |
|---|---|---|
| {{protocol_number}} | study.protocol.number | ICH E6(R3) Appendix C |
| {{site_name}} | site.name | ICH E6(R3) Appendix C |
| {{investigator_name}} | site.principal_investigator.name | 21 CFR 312.66 |
| {{deviation_number}} | site.deviations[].number | ICH E6(R3) Appendix C |
| {{subject_code}} | site.deviations[].subject_code | 21 CFR 312.62(b) |
| {{deviation_date}} | site.deviations[].occurred_date | ICH E6(R3) Appendix C |
| {{identified_date}} | site.deviations[].identified_date | ICH E6(R3) Appendix C |
| {{deviation_description}} | site.deviations[].description | ICH E6(R3) Appendix C |
| {{deviation_category}} | site.deviations[].category | ICH E6(R3) Appendix C |
| {{important_flag}} | site.deviations[].important | ICH E6(R3) (important deviations) |
| {{root_cause}} | site.deviations[].root_cause | ICH E6(R3) 3.10 (CAPA context) |
| {{capa_description}} | site.deviations[].capa | ICH E6(R3) 3.10 (CAPA context) |
| {{sponsor_report_date}} | site.deviations[].sponsor_reported_date | ICH E6(R3) 2.7 |
| {{irb_report_date}} | site.deviations[].irb_reported_date | 21 CFR 312.66 |
| {{review_date}} | site.deviations_log.reviews[].date | ICH E6(R3) Appendix C |
| {{last_reviewed_deviation_number}} | site.deviations_log.reviews[].through_number | ICH E6(R3) Appendix C |

## Related
- [[03-documents/protocol-deviation-log]]
- [[03-documents/irb-continuing-review-progress-report]]
- [[03-documents/unanticipated-problem-report-to-irb]]
- [[03-documents/interim-monitoring-visit-report]]
