---
title: "Interim Monitoring Visit Report"
doc_id: "interim-monitoring-visit-report"
category: "monitoring"
governing_citations: ["21 CFR 312.56(a)", "ICH E6(R3) 3.11"]
owner: "cro"
receiver: "sponsor"
gate: "none"
status: template
updated: 2026-07-09
---

# Interim Monitoring Visit Report — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 312.56(a)](https://www.law.cornell.edu/cfr/text/21/312.56) (sponsor shall monitor the progress of all clinical investigations being conducted under its IND); [ICH E6(R3) §3.11](https://www.ich.org/page/efficacy-guidelines) (monitoring; §3.11.4 monitoring reports). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** The interim monitoring visit (IMV) report is the monitor's written record of a routine monitoring visit during trial conduct: what was reviewed (consents, source data, IP accountability, safety reporting, site file), what was found, and what actions the site or sponsor must take. It is the primary evidence that the sponsor's 312.56(a) monitoring obligation is being discharged.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing.

## Template

### INTERIM MONITORING VISIT REPORT

| | |
|---|---|
| **Protocol number / title** | {{protocol_number}} / {{protocol_title}} |
| **Site number / name** | {{site_number}} / {{site_name}} |
| **Principal investigator** | {{investigator_name}} |
| **Visit date(s)** | {{visit_date}} |
| **Visit number / mode** | IMV {{visit_number}} / {{visit_mode}} [INSTRUCTION: on-site / remote / hybrid, per the monitoring plan.] |
| **Monitor (author)** | {{monitor_name}}, {{monitor_title}} |
| **Report date** | {{report_date}} |
| **Previous visit date** | {{previous_visit_date}} |

#### 1. Site status at visit

| Metric | Value |
|---|---|
| Subjects screened (cumulative) | {{subjects_screened}} |
| Subjects enrolled (cumulative) | {{subjects_enrolled}} |
| Subjects active / completed / withdrawn | {{subjects_active}} / {{subjects_completed}} / {{subjects_withdrawn}} |
| Subjects reviewed this visit | {{subjects_reviewed}} [INSTRUCTION: List subject codes reviewed and the SDV/SDR scope applied per the monitoring plan.] |

#### 2. Review conducted

[INSTRUCTION: Mark each area reviewed (Y/N/NA) and summarize observations. The scope must match the risk-based monitoring plan; deviations from planned scope must be explained.]

| Area | Reviewed (Y/N/NA) | Summary |
|---|---|---|
| Informed consent: current IRB-approved version used; signed/dated before procedures; process documented | | |
| Eligibility: enrollment criteria verifiable in source | | |
| Source data verification per plan (critical data: primary endpoint, safety labs) | | |
| AE/SAE identification: source reviewed for unreported events; SAE reports timely per 21 CFR 312.64(b) | | |
| IP accountability: dispensing log reconciles; storage conditions and temperature log in range | | |
| Protocol deviations: log current; new deviations identified this visit | | |
| IRB correspondence: approvals current; continuing review not lapsed | | |
| Delegation log and training records current for active staff | | |
| ISF / regulatory binder complete and current | | |
| Open action items from previous visit | | |

#### 3. Findings

{{findings}}

[INSTRUCTION: One row per finding. Grade per the monitoring plan's classification (critical/major/minor). A "critical" grade — e.g., consent process failure, unreported SAE, eligibility violation affecting subject safety — triggers the monitoring plan's escalation path and may require reporting to the sponsor-investigator within 24 hours; under 21 CFR 312.56(b) uncorrected noncompliance obligates the sponsor to secure compliance or end the investigator's participation.]

| # | Finding | Grade | Subject(s) affected | Root cause (if known) | Required action |
|---|---|---|---|---|---|
| 1 | {{finding_1}} | {{finding_grade_1}} | {{finding_subjects_1}} | {{finding_cause_1}} | {{finding_action_1}} |

#### 4. Action items

{{action_items}}

| # | Action | Owner | Due date | Status | Carried from prior visit? |
|---|---|---|---|---|---|
| 1 | {{action_item_1}} | {{action_owner_1}} | {{action_due_1}} | Open | {{action_carryover_1}} |

[INSTRUCTION: Include disposition of every action item open at the previous visit. Items open across two consecutive visits should be escalated per the monitoring plan.]

#### 5. Overall assessment

{{overall_assessment}}

[INSTRUCTION: One paragraph: is the site conducting the trial in compliance with the protocol, GCP, and applicable requirements? Note any recommendation to adjust monitoring intensity (trigger conditions per the monitoring plan §5).]

#### 6. Monitor attestation and sponsor review

Prepared by (monitor): {{monitor_name}} ____________________ Date: ________

Reviewed by (sponsor / sponsor-investigator): {{sponsor_reviewer_name}} ____________________ Date: ________

[INSTRUCTION: Report must be provided to the sponsor in a timely manner and its review documented (ICH E6(R3) §3.11.4). Signatures are human acts — OSSICRO drafts, humans sign.]

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{protocol_number}} | study.protocol.number | ICH E6(R3) 3.11.4 |
| {{protocol_title}} | study.protocol.title | ICH E6(R3) 3.11.4 |
| {{site_number}} | site.number | ICH E6(R3) 3.11.4 |
| {{site_name}} | site.name | ICH E6(R3) 3.11.4 |
| {{investigator_name}} | site.investigator.name | 21 CFR 312.56(a) |
| {{visit_date}} | visit.imv.date | ICH E6(R3) 3.11.4 |
| {{visit_number}} | visit.imv.number | ICH E6(R3) 3.11.4 |
| {{visit_mode}} | visit.imv.mode | ICH E6(R3) 3.11.2 |
| {{monitor_name}} | visit.imv.monitor.name | ICH E6(R3) 3.11.4 |
| {{monitor_title}} | visit.imv.monitor.title | ICH E6(R3) 3.11.4 |
| {{report_date}} | visit.imv.report.date | ICH E6(R3) 3.11.4 |
| {{previous_visit_date}} | visit.imv.previous_date | ICH E6(R3) 3.11.4 |
| {{subjects_screened}} | site.enrollment.screened | ICH E6(R3) 3.11.4 |
| {{subjects_enrolled}} | site.enrollment.enrolled | ICH E6(R3) 3.11.4 |
| {{subjects_active}} | site.enrollment.active | ICH E6(R3) 3.11.4 |
| {{subjects_completed}} | site.enrollment.completed | ICH E6(R3) 3.11.4 |
| {{subjects_withdrawn}} | site.enrollment.withdrawn | ICH E6(R3) 3.11.4 |
| {{subjects_reviewed}} | visit.imv.subjects_reviewed[] | FDA RBM Guidance (2013) §IV.C |
| {{findings}} | visit.imv.findings[] | ICH E6(R3) 3.11.4 |
| {{finding_1}} / {{finding_grade_1}} / {{finding_subjects_1}} / {{finding_cause_1}} / {{finding_action_1}} | visit.imv.findings[].text/.grade/.subjects/.cause/.action | ICH E6(R3) 3.11.4; 21 CFR 312.56(b) |
| {{action_items}} | visit.imv.action_items[] | ICH E6(R3) 3.11.4 |
| {{action_item_1}} / {{action_owner_1}} / {{action_due_1}} / {{action_carryover_1}} | visit.imv.action_items[].text/.owner/.due/.carryover | ICH E6(R3) 3.11.4 |
| {{overall_assessment}} | visit.imv.overall_assessment | ICH E6(R3) 3.11.4 |
| {{sponsor_reviewer_name}} | study.monitoring.report_reviewer.name | ICH E6(R3) 3.11.4 |

## Related

- [[03-documents/interim-monitoring-visit-report]]
- [[03-documents/risk-based-monitoring-plan]]
- [[03-documents/site-initiation-visit-report]]
- [[03-documents/close-out-visit-report]]
- [[03-documents/protocol-deviation-log]]
- [[03-documents/sae-report-investigator-to-sponsor]]
- [[03-documents/drug-accountability-log]]
