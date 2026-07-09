---
title: "Data and Safety Monitoring Plan"
doc_id: "data-safety-monitoring-plan"
category: "safety"
governing_citations: ["ICH E6(R3) 3.10", "NIH DSMP Policy"]
owner: "sponsor-investigator"
receiver: "irb"
gate: "none"
status: template
updated: 2026-07-09
---

# Data and Safety Monitoring Plan — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [ICH E6(R3) § 3.10 (Safety Assessment and Reporting)](https://www.ich.org/page/efficacy-guidelines) and the [NIH Policy for Data and Safety Monitoring (NOT-98-084)](https://grants.nih.gov/grants/guide/notice-files/not98-084.html), as elaborated by [NIH Further Guidance on Data and Safety Monitoring (NOT-OD-00-038)](https://grants.nih.gov/grants/guide/notice-files/NOT-OD-00-038.html). Related: [21 CFR 312.32](https://www.law.cornell.edu/cfr/text/21/312.32) (IND safety reporting), [21 CFR 312.66](https://www.law.cornell.edu/cfr/text/21/312.66) (investigator's assurance of IRB reporting). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** The Data and Safety Monitoring Plan (DSMP) describes how participant safety and data integrity will be monitored throughout the trial: who monitors, what data are reviewed, how often, and how findings are escalated and reported. It is submitted to the IRB with the initial protocol package and is required for NIH-funded clinical trials; the level of monitoring must be commensurate with study risk.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing.

## Template

### DATA AND SAFETY MONITORING PLAN

| | |
|---|---|
| **Protocol Title** | {{protocol_title}} |
| **Protocol Number** | {{protocol_number}} |
| **Protocol Version / Date** | {{protocol_version}} / {{protocol_date}} |
| **IND Number** | {{ind_number}} [INSTRUCTION: Enter "Not applicable — exempt" with basis if no IND.] |
| **Sponsor-Investigator** | {{investigator_name}}, {{investigator_degrees}} |
| **Site** | {{site_name}} |
| **DSMP Version / Date** | {{dsmp_version}} / {{dsmp_date}} |

#### 1. Risk Assessment

{{risk_assessment}}

[INSTRUCTION: State the overall risk classification (e.g., minimal risk / greater than minimal risk with prospect of direct benefit) and the basis: phase of investigation, prior human experience with {{drug_name}}, known and anticipated toxicities from the Investigator's Brochure edition {{ib_edition}}, vulnerability of the population, and invasiveness of study procedures. The intensity of monitoring described in Sections 3–6 must be proportionate to this assessment (ICH E6(R3) risk-proportionality principle; NIH NOT-OD-00-038).]

#### 2. Monitoring Entity

The entity responsible for data and safety monitoring for this trial is: **{{monitoring_entity}}**

[INSTRUCTION: Select and describe one — (a) the sponsor-investigator with an independent Medical Monitor; (b) an Independent Safety Officer/Monitor; or (c) a Data and Safety Monitoring Board (DSMB/DMC). Multisite, blinded, or greater-than-minimal-risk trials generally warrant an independent monitor or DSMB (FDA Guidance: Clinical Trial Data Monitoring Committees). If a DSMB is used, cross-reference its Charter and do not duplicate stopping rules inconsistently.]

- Independent Medical Monitor / Safety Officer: {{medical_monitor_name}}, {{medical_monitor_qualifications}}
- Independence statement: [INSTRUCTION: Confirm the monitor has no direct involvement in study conduct and no disqualifying financial interest under 21 CFR Part 54.]

#### 3. Data Reviewed

The following data will be reviewed at each safety review:

1. Enrollment and disposition (screened, enrolled, withdrawn, completed) against the planned accrual of {{planned_enrollment}}.
2. Adverse events and serious adverse events, coded by {{ae_coding_dictionary}} [INSTRUCTION: e.g., MedDRA version] and graded per {{severity_grading_scale}} [INSTRUCTION: e.g., CTCAE v5.0].
3. Protocol deviations affecting safety or data integrity.
4. Laboratory safety parameters: {{safety_lab_parameters}}.
5. Study-halting or dose-modification triggers (Section 6).
6. Data quality indicators: missing data rates, query aging, and eligibility violations.

#### 4. Review Frequency

Safety reviews will occur: **{{review_frequency}}**

[INSTRUCTION: State both a calendar cadence (e.g., quarterly) and event-driven triggers (e.g., after every {{n_subjects_per_cohort}} subjects complete {{sentinel_period}}; after any SAE assessed as related; after any death). For dose-escalation designs, state the cohort-review rule before escalation.]

#### 5. Reporting Plan

{{reporting_plan}}

[INSTRUCTION: Complete each row. Timelines below are regulatory minimums; the protocol or IRB may impose shorter ones.]

| Finding | Reported by | Reported to | Timeline | Authority |
|---|---|---|---|---|
| SAE at site | Investigator | Sponsor(-Investigator) | Immediately | 21 CFR 312.64(b) |
| Serious + unexpected suspected adverse reaction | Sponsor-Investigator | FDA + all participating investigators | ≤15 calendar days | 21 CFR 312.32(c)(1) |
| Fatal or life-threatening + unexpected suspected adverse reaction | Sponsor-Investigator | FDA | ≤7 calendar days | 21 CFR 312.32(c)(2) |
| Unanticipated problem involving risks to subjects or others | Investigator | IRB | Promptly, per {{irb_name}} policy ({{irb_up_reporting_window}}) | 21 CFR 56.108(b)(1); 312.66 |
| Periodic safety summary | {{monitoring_entity}} | IRB (with continuing review) and NIH program officer if applicable | {{periodic_summary_frequency}} | NIH DSMP Policy |
| DSMB recommendation (if applicable) | DSMB Chair | Sponsor-Investigator, then IRB | Within {{dsmb_report_forwarding_window}} of meeting | FDA DMC Guidance |

#### 6. Study Pausing / Stopping Criteria

Enrollment and dosing will pause pending safety review if any of the following occur:

{{stopping_criteria}}

[INSTRUCTION: Enumerate objective triggers — e.g., any Grade ≥4 related AE; ≥{{dlt_threshold}} dose-limiting toxicities within a cohort; any death assessed as possibly related; aggregate rate of {{sentinel_event}} exceeding {{sentinel_rate_threshold}}. State who has authority to pause (the sponsor-investigator and the independent monitor each have unilateral pause authority) and the process for resuming.]

#### 7. Unblinding (if applicable)

[INSTRUCTION: Delete if open-label.] Emergency unblinding is available 24/7 via {{unblinding_mechanism}}. The investigator may unblind without sponsor pre-approval when knowledge of assignment is necessary for emergency management; the sponsor and IRB are notified within {{unblinding_notice_window}}.

#### 8. Confidentiality and Data Integrity

Safety review materials identify subjects only by {{subject_code_format}}. Source-to-CRF verification and data-quality oversight are described in the Risk-Based Monitoring Plan (cross-reference: {{monitoring_plan_reference}}).

#### 9. Plan Amendments

Material changes to this DSMP require sponsor-investigator approval and IRB submission before implementation, except where immediately necessary to eliminate an apparent hazard (21 CFR 312.66).

**Prepared by:** {{preparer_name}} — Date: {{preparation_date}}
**Approved by (Sponsor-Investigator):** {{investigator_name}} — Signature: ________________ Date: ________

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{protocol_title}} | study.protocol.title | ICH E6(R3) 3.10 |
| {{protocol_number}} | study.protocol.number | ICH E6(R3) 3.10 |
| {{protocol_version}} | study.protocol.version | ICH E6(R3) 3.10 |
| {{protocol_date}} | study.protocol.date | ICH E6(R3) 3.10 |
| {{ind_number}} | study.ind.number | 21 CFR 312.32 |
| {{investigator_name}} | study.investigator.name | NIH DSMP Policy |
| {{investigator_degrees}} | study.investigator.degrees | NIH DSMP Policy |
| {{site_name}} | study.site.name | NIH DSMP Policy |
| {{dsmp_version}} | study.safety.dsmp.version | NIH DSMP Policy |
| {{dsmp_date}} | study.safety.dsmp.date | NIH DSMP Policy |
| {{risk_assessment}} | study.safety.risk_assessment | NIH NOT-OD-00-038; ICH E6(R3) |
| {{drug_name}} | study.product.name | 21 CFR 312.23(a)(5) |
| {{ib_edition}} | study.product.ib_edition | 21 CFR 312.55 |
| {{monitoring_entity}} | study.safety.monitoring_entity | NIH DSMP Policy |
| {{medical_monitor_name}} | study.safety.medical_monitor.name | ICH E2A |
| {{medical_monitor_qualifications}} | study.safety.medical_monitor.qualifications | ICH E2A |
| {{planned_enrollment}} | study.design.planned_enrollment | ICH E6(R3) 3.10 |
| {{ae_coding_dictionary}} | study.safety.coding_dictionary | ICH E2A |
| {{severity_grading_scale}} | study.safety.grading_scale | ICH E6(R3) 3.10 |
| {{safety_lab_parameters}} | study.safety.lab_parameters | ICH E6(R3) 3.10 |
| {{review_frequency}} | study.safety.review_frequency | NIH DSMP Policy |
| {{n_subjects_per_cohort}} | study.design.cohort_size | protocol-specific |
| {{sentinel_period}} | study.safety.sentinel_period | protocol-specific |
| {{reporting_plan}} | study.safety.reporting_plan | 21 CFR 312.32; 312.64(b); 56.108(b)(1) |
| {{irb_name}} | study.irb.name | 21 CFR 312.66 |
| {{irb_up_reporting_window}} | study.irb.up_reporting_window | 21 CFR 56.108(b)(1) |
| {{periodic_summary_frequency}} | study.safety.periodic_summary_frequency | NIH DSMP Policy |
| {{dsmb_report_forwarding_window}} | study.dsmb.report_forwarding_window | FDA DMC Guidance |
| {{stopping_criteria}} | study.safety.stopping_criteria | ICH E6(R3) 3.10 |
| {{dlt_threshold}} | study.design.dlt_threshold | protocol-specific |
| {{sentinel_event}} | study.safety.sentinel_event | protocol-specific |
| {{sentinel_rate_threshold}} | study.safety.sentinel_rate_threshold | protocol-specific |
| {{unblinding_mechanism}} | study.design.unblinding_mechanism | ICH E6(R3) 3.10 |
| {{unblinding_notice_window}} | study.design.unblinding_notice_window | protocol-specific |
| {{subject_code_format}} | study.data.subject_code_format | 21 CFR 312.62(b) |
| {{monitoring_plan_reference}} | study.monitoring.plan_reference | ICH E6(R3) 3.11 |
| {{preparer_name}} | study.safety.dsmp.preparer | — |
| {{preparation_date}} | study.safety.dsmp.preparation_date | — |

## Related

- [[03-documents/data-safety-monitoring-plan]]
- [[03-documents/dsmb-charter-single-site-low-risk]]
- [[03-documents/risk-based-monitoring-plan]]
- [[03-documents/safety-management-pharmacovigilance-plan]]
