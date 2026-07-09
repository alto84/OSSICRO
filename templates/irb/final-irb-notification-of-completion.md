---
title: "Final IRB Notification of Study Completion"
doc_id: "final-irb-notification-of-completion"
category: "irb"
governing_citations: ["21 CFR 56.109", "ICH E6(R3) Appendix C"]
owner: "investigator"
receiver: "irb"
gate: "none"
status: template
updated: 2026-07-09
---

# Final IRB Notification of Study Completion — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 56.109](https://www.law.cornell.edu/cfr/text/21/56.109) (IRB review of research, including the continuing-review obligation that closure formally ends); [ICH E6(R3) Appendix C](https://www.ich.org/page/efficacy-guidelines) (essential records — the investigator's final report to the IRB is an essential record of the trial). Investigator reporting duty: [21 CFR 312.66](https://www.law.cornell.edu/cfr/text/21/312.66). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** The investigator's written notification to the reviewing IRB that the study is complete (or terminated) at the site, with final enrollment and safety figures. It closes the IRB's continuing-review obligation for the protocol, and the IRB's acknowledgment plus this letter are filed in the investigator site file and TMF as essential records.

[INSTRUCTION: Do not close with the IRB until all subject-facing activity AND analysis of individually identifiable data at the site are complete. If the study is being terminated early, say so and give the reason — early termination for safety must also be handled under the unanticipated-problem pathway, and the sponsor notifies FDA separately (21 CFR 312.38).]

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing.

## Template

{{notification_date}}

{{irb_name}}
{{irb_address}}

**Re: Final report and notification of study completion — Protocol {{protocol_number}}**

**Protocol title:** {{protocol_title}}
**Principal Investigator:** {{investigator_name}}, {{investigator_degrees}}
**Site:** {{site_name}}
**Last IRB approval period:** {{current_approval_date}} through {{current_expiration_date}}

Dear IRB Chair / IRB Administrator:

This letter is the investigator's final report for the above-referenced study and formal notification that the study is {{closure_type}} at this site, effective {{completion_date}}.

[INSTRUCTION: {{closure_type}} is "completed as planned" or "terminated early". If terminated early, add one sentence stating the reason (enrollment futility, sponsor decision, safety) and cross-reference any unanticipated-problem report already submitted.]

**Final enrollment and disposition ({{final_enrollment}}):**

| Metric | Final count |
|---|---|
| Subjects screened | {{screened_total}} |
| Subjects enrolled | {{enrolled_total}} |
| Subjects who completed the study | {{completed_total}} |
| Subjects withdrawn / discontinued | {{withdrawn_total}} |

**Date of last subject's last visit / contact:** {{last_subject_last_visit_date}}

**Final safety summary:** {{final_safety_summary}} [INSTRUCTION: Cumulative SAE count at the site, whether all were previously reported to the IRB per its reporting policy, any unanticipated problems over the life of the study, and confirmation that no safety issues remain outstanding. Do not report new, previously unreported events in a closure letter — those go through the standard reporting pathway first.]

**Summary of results, if available:** {{results_summary}} [INSTRUCTION: Brief and factual; "analysis ongoing; a summary will be provided on request" is acceptable when the CSR is not yet written.]

**Status at closure.** I confirm that at this site: all enrolled subjects have completed protocol-specified activities or been appropriately withdrawn; all adverse events and unanticipated problems required to be reported to the IRB have been reported; investigational product has been reconciled and returned or destroyed per the sponsor's instructions; and there will be no further enrollment, subject contact, or use of individually identifiable data under this protocol at this site.

**Record retention.** Study records will be retained per 21 CFR 312.62(c) — at least 2 years after a marketing application is approved for the drug for the studied indication, or, if no application is filed or it is not approved, 2 years after the investigation is discontinued and FDA is notified — and per any longer sponsor or institutional requirement. Custodian and archive location: {{records_custodian}}, {{archive_location}}.

I request the IRB's written acknowledgment of study closure for filing in the investigator site file.

Sincerely,

______________________________  Date: ____________
{{investigator_name}}, {{investigator_degrees}}
Principal Investigator

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{notification_date}} | submissions.irb_closure.date | 21 CFR 56.109 |
| {{irb_name}} / {{irb_address}} | study.irb.name / .address | 21 CFR 312.66 |
| {{protocol_number}} / {{protocol_title}} | study.protocol.number / .title | 21 CFR 56.109 |
| {{investigator_name}} / {{investigator_degrees}} | study.investigator.name / .degrees | 21 CFR 312.66 |
| {{site_name}} | study.site.name | — |
| {{current_approval_date}} / {{current_expiration_date}} | irb.current_approval.approval_date / .expiration_date | 21 CFR 56.109(f) |
| {{closure_type}} | closeout.closure_type | ICH E6(R3) Appendix C |
| {{completion_date}} | closeout.completion_date | ICH E6(R3) Appendix C |
| {{final_enrollment}} (table: {{screened_total}}, {{enrolled_total}}, {{completed_total}}, {{withdrawn_total}}) | site.enrollment.final.* | ICH E6(R3) Appendix C |
| {{last_subject_last_visit_date}} | closeout.last_subject_last_visit | ICH E6(R3) Appendix C |
| {{final_safety_summary}} | closeout.final_safety_summary | 21 CFR 56.108(b) |
| {{results_summary}} | closeout.results_summary | ICH E6(R3) Appendix C |
| {{records_custodian}} | closeout.records.custodian | 21 CFR 312.62(c) |
| {{archive_location}} | closeout.records.archive_location | 21 CFR 312.62(c) |

## Related

- [[irb-submission-package]] — wiki document page covering the IRB document set
- [[closeout]] — lifecycle page for study closeout
- [[record-retention-and-archival]] — lifecycle page; pairs with the retention statement above
- [[closeout-tmf-checklist]] — this letter and the IRB's acknowledgment are essential records
- [[irb-continuing-review-progress-report]] — the recurring obligation this notification ends
