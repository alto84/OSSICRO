---
title: "Unanticipated Problem Report to IRB"
doc_id: "unanticipated-problem-report-to-irb"
category: "safety"
governing_citations: ["21 CFR 56.108(b)(1)", "OHRP Guidance on Unanticipated Problems (2007)"]
owner: "investigator"
receiver: "irb"
gate: "none"
status: template
updated: 2026-07-09
---

# Unanticipated Problem Report to IRB — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 56.108(b)(1)](https://www.law.cornell.edu/cfr/text/21/56.108) (IRB must have and follow written procedures for ensuring prompt reporting of unanticipated problems involving risks to human subjects or others) and [OHRP Guidance on Reviewing and Reporting Unanticipated Problems Involving Risks to Subjects or Others and Adverse Events (2007)](https://www.hhs.gov/ohrp/regulations-and-policy/guidance/reviewing-unanticipated-problems/index.html). Related: [21 CFR 312.66](https://www.law.cornell.edu/cfr/text/21/312.66) (investigator's assurance of prompt IRB reporting), [FDA Guidance: Adverse Event Reporting to IRBs — Improving Human Subject Protection (2009)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/adverse-event-reporting-irbs-improving-human-subject-protection). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** The investigator's prompt report to the IRB of an unanticipated problem involving risks to subjects or others (UP) — an incident, experience, or outcome that is unexpected, related or possibly related to the research, and suggests greater risk of harm than previously known. Not every adverse event is a UP; most UPs requiring IRB report are not adverse events (e.g., breaches of confidentiality, dosing errors, lost devices containing PHI).

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing. File within the IRB's prompt-reporting window ({{irb_up_reporting_window}}).

## Template

### UNANTICIPATED PROBLEM REPORT TO THE IRB

| | |
|---|---|
| IRB of record | {{irb_name}} |
| IRB protocol / reference number | {{irb_reference_number}} |
| Protocol Number / Title | {{protocol_number}} / {{protocol_title}} |
| Principal Investigator | {{investigator_name}} |
| Date of occurrence | {{occurrence_date}} |
| Date PI became aware | {{awareness_date}} |
| Date of this report | {{report_date}} [INSTRUCTION: must fall within {{irb_up_reporting_window}} of awareness; if late, explain in Section 4.] |
| Report type | ☐ Initial ☐ Follow-up to report dated {{prior_report_date}} |

#### 1. Description of the Event

{{event_description}}

[INSTRUCTION: Describe factually what happened, who was affected (subject code(s) only — no identifiers), and the immediate consequences. Categories include: serious adverse event; adverse device/drug experience; protocol deviation with risk implications; breach of confidentiality or data security; unintentional disclosure; medication/dosing error; new safety information (IB update, DSMB finding, publication); complaint indicating unrecognized risk.]

Subjects affected (coded): {{affected_subject_codes}} — Number of subjects enrolled to date: {{enrollment_to_date}}

#### 2. Assessment Against the Unanticipated-Problem Criteria

{{assessment}}

[INSTRUCTION: Address each OHRP (2007) criterion explicitly. An event is a UP only if ALL THREE are met.]

| Criterion | Determination | Basis |
|---|---|---|
| (a) Unexpected — in nature, severity, or frequency — given the protocol/IB/consent documents and the studied population | ☐ Yes ☐ No | {{unexpectedness_basis}} |
| (b) Related or possibly related to participation in the research | ☐ Yes ☐ No | {{relatedness_basis}} |
| (c) Suggests the research places subjects or others at greater risk of harm (physical, psychological, economic, or social) than previously known or recognized | ☐ Yes ☐ No | {{greater_risk_basis}} |

Conclusion: ☐ This event IS an unanticipated problem ☐ This event is NOT a UP but is reported per {{irb_name}} policy — {{conclusion_rationale}}

#### 3. Corrective and Preventive Actions

{{corrective_actions}}

[INSTRUCTION: State actions taken and planned — e.g., subject treated and status; enrollment pause; protocol amendment; consent form revision and re-consent of enrolled subjects; retraining; data-security remediation; notification of sponsor, DSMB, and (if the UP is also a serious and unexpected suspected adverse reaction) FDA under 21 CFR 312.32(c). Include target dates and responsible persons.]

#### 4. Changes Requested of the IRB

- ☐ No changes to protocol or consent required — rationale: {{no_change_rationale}}
- ☐ Protocol amendment submitted / to be submitted by {{amendment_date}}
- ☐ Consent form revision submitted / to be submitted by {{consent_revision_date}} — re-consent plan: {{reconsent_plan}}
- ☐ Other: {{other_requests}}

#### 5. Concurrent Notifications

| Recipient | Notified? | Date |
|---|---|---|
| Sponsor(-Investigator) | ☐ | {{sponsor_notification_date}} |
| DSMB / Safety Monitor (if applicable) | ☐ | {{dsmb_notification_date}} |
| FDA (if reportable under 21 CFR 312.32) | ☐ | {{fda_notification_date}} |

**Principal Investigator:** {{investigator_name}} — Signature: ________________ Date: ________

[INSTRUCTION: The IRB's determination on this report (acknowledgment, required modifications, suspension) is the IRB's own judgment under 21 CFR 56.108-56.111; file its response with this report in the regulatory binder.]

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{irb_name}} | study.irb.name | 21 CFR 56.108(b)(1) |
| {{irb_reference_number}} | study.irb.reference_number | — |
| {{irb_up_reporting_window}} | study.irb.up_reporting_window | 21 CFR 56.108(b)(1) |
| {{protocol_number}} | study.protocol.number | 21 CFR 312.66 |
| {{protocol_title}} | study.protocol.title | 21 CFR 312.66 |
| {{investigator_name}} | study.investigator.name | 21 CFR 312.66 |
| {{occurrence_date}} | safety.up.occurrence_date | OHRP UP Guidance (2007) |
| {{awareness_date}} | safety.up.awareness_date | OHRP UP Guidance (2007) |
| {{report_date}} | safety.up.report_date | 21 CFR 56.108(b)(1) |
| {{prior_report_date}} | safety.up.prior_report_date | — |
| {{event_description}} | safety.up.event_description | OHRP UP Guidance (2007) |
| {{affected_subject_codes}} | safety.up.affected_subject_codes | 21 CFR 312.62(b) |
| {{enrollment_to_date}} | study.enrollment.current | — |
| {{assessment}} | safety.up.assessment | OHRP UP Guidance (2007) |
| {{unexpectedness_basis}} | safety.up.unexpectedness_basis | OHRP UP Guidance (2007) |
| {{relatedness_basis}} | safety.up.relatedness_basis | OHRP UP Guidance (2007) |
| {{greater_risk_basis}} | safety.up.greater_risk_basis | OHRP UP Guidance (2007) |
| {{conclusion_rationale}} | safety.up.conclusion_rationale | OHRP UP Guidance (2007) |
| {{corrective_actions}} | safety.up.corrective_actions | OHRP UP Guidance (2007) |
| {{no_change_rationale}} | safety.up.no_change_rationale | — |
| {{amendment_date}} | safety.up.amendment_date | 21 CFR 312.30(b) |
| {{consent_revision_date}} | safety.up.consent_revision_date | 21 CFR 50.25 |
| {{reconsent_plan}} | safety.up.reconsent_plan | 21 CFR 50.25(b)(5) |
| {{other_requests}} | safety.up.other_requests | — |
| {{sponsor_notification_date}} | safety.up.sponsor_notification_date | 21 CFR 312.64(b) |
| {{dsmb_notification_date}} | safety.up.dsmb_notification_date | FDA DMC Guidance |
| {{fda_notification_date}} | safety.up.fda_notification_date | 21 CFR 312.32(c) |

## Related

- [[03-documents/unanticipated-problem-report-to-irb]]
- [[03-documents/sae-report-investigator-to-sponsor]]
- [[03-documents/ind-safety-report-7-15-day]]
- [[03-documents/irb-continuing-review-progress-report]]
- [[03-documents/protocol-deviation-log]]
