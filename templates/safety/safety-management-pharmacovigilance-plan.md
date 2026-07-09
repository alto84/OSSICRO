---
title: "Safety Management / Pharmacovigilance Plan"
doc_id: "safety-management-pharmacovigilance-plan"
category: "safety"
governing_citations: ["21 CFR 312.32", "ICH E2A"]
owner: "sponsor-investigator"
receiver: "sponsor"
gate: "none"
status: template
updated: 2026-07-09
---

# Safety Management / Pharmacovigilance Plan — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 312.32 (IND safety reporting)](https://www.law.cornell.edu/cfr/text/21/312.32) and [ICH E2A (Clinical Safety Data Management: Definitions and Standards for Expedited Reporting)](https://www.ich.org/page/efficacy-guidelines). Related: [21 CFR 312.64(b)](https://www.law.cornell.edu/cfr/text/21/312.64) (investigator safety reports), [FDA Guidance: Safety Reporting Requirements for INDs and BA/BE Studies (2012)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/safety-reporting-requirements-inds-investigational-new-drug-applications-and-babe). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** The Safety Management Plan (SMP) is the operational manual for collecting, assessing, and reporting safety information during the trial. It fixes the definitions, the causality/expectedness workflow, the personnel (medical monitor), and the clock-driven reporting timelines so that every adverse event follows one auditable path from bedside observation to regulatory report.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing.

## Template

### SAFETY MANAGEMENT / PHARMACOVIGILANCE PLAN

| | |
|---|---|
| **Protocol Title** | {{protocol_title}} |
| **Protocol Number** | {{protocol_number}} |
| **IND Number** | {{ind_number}} |
| **Investigational Product** | {{drug_name}} |
| **Sponsor-Investigator** | {{investigator_name}} |
| **Medical Monitor** | {{medical_monitor_name}}, {{medical_monitor_qualifications}} — {{medical_monitor_phone}} / {{medical_monitor_email}} (24/7 coverage: {{after_hours_contact}}) |
| **SMP Version / Date** | {{smp_version}} / {{smp_date}} |

#### 1. Roles and Responsibilities

- **Investigator:** detects, documents, treats, and reports adverse events; reports SAEs to the sponsor-investigator immediately (21 CFR 312.64(b)); provides initial causality opinion.
- **Medical Monitor ({{medical_monitor_name}}):** performs the causality (suspected adverse reaction) and expectedness determinations that drive expedited reporting (21 CFR 312.32(a), (b), (c); ICH E2A). This determination is a non-delegable medical judgment — see gate note below.
- **Sponsor-Investigator ({{investigator_name}}):** promptly reviews all safety information (21 CFR 312.32(b)); authorizes and submits IND safety reports; notifies all participating investigators.
- **Reference safety document:** Investigator's Brochure, edition {{ib_edition}} dated {{ib_edition_date}}. Expectedness is assessed against this document (21 CFR 312.32(a)).

#### 2. Definitions

{{sae_definitions}}

[INSTRUCTION: Reproduce the 21 CFR 312.32(a) / ICH E2A definitions verbatim or by precise paraphrase; do not invent local variants.]

- **Adverse event (AE):** any untoward medical occurrence associated with the use of a drug in humans, whether or not considered drug related.
- **Serious adverse event (SAE):** an AE that results in death; is life-threatening; requires inpatient hospitalization or prolongs existing hospitalization; results in persistent or significant incapacity or substantial disruption of the ability to conduct normal life functions; is a congenital anomaly/birth defect; or is an important medical event that may jeopardize the subject and may require intervention to prevent one of the preceding outcomes (21 CFR 312.32(a)).
- **Life-threatening:** the subject was, in the view of the investigator or sponsor, at immediate risk of death from the event as it occurred.
- **Suspected adverse reaction:** any AE for which there is a *reasonable possibility* that the drug caused it — i.e., evidence to suggest a causal relationship (21 CFR 312.32(a)).
- **Unexpected:** not listed in the IB at the observed specificity or severity, or, if no IB, not consistent with the risk information in the general investigational plan or protocol (21 CFR 312.32(a)).

#### 3. Severity Grading

AEs are graded per {{severity_grading_scale}} [INSTRUCTION: e.g., CTCAE v5.0]. Severity (intensity) is distinct from seriousness (regulatory outcome criteria); a Grade 3 event is not automatically an SAE, and a Grade 1 event meeting a 312.32(a) outcome is.

#### 4. Causality and Expectedness Workflow

1. Investigator records causality opinion on the SAE Report ({{sae_form_reference}}) using the scale: {{causality_scale}} [INSTRUCTION: e.g., related / possibly related / unlikely related / not related].
2. Medical Monitor independently determines whether the event is a **suspected adverse reaction** (reasonable possibility of causation, including single-occurrence events unlikely to be spontaneous, aggregate signals, and events known to be drug-class effects — 21 CFR 312.32(c)(1)(i)) and whether it is **unexpected** against IB edition {{ib_edition}}.
3. The Medical Monitor's determination, its basis, and its date/time are recorded in {{safety_tracking_system}} and drive the reporting decision tree in Section 5.

#### 5. Reporting Timelines

{{reporting_timelines}}

[INSTRUCTION: Confirm every window against current 312.32 text; day 0 = date the sponsor-investigator (or any sponsor staff) first receives the information.]

| Event class | Report | Recipient | Deadline |
|---|---|---|---|
| Any SAE (regardless of causality) | SAE Report - Investigator to Sponsor | Sponsor-Investigator | Immediately upon awareness (21 CFR 312.64(b)) |
| Non-serious AE | Study records / CRF | Sponsor-Investigator | Per protocol schedule ({{nonserious_ae_recording_window}}) |
| Serious + unexpected + suspected adverse reaction | IND Safety Report (Form FDA 3500A or narrative) | FDA + all participating investigators | ≤15 calendar days (21 CFR 312.32(c)(1)) |
| Fatal or life-threatening + unexpected + suspected adverse reaction | IND Safety Report, initial notification | FDA | ≤7 calendar days (21 CFR 312.32(c)(2)); complete report within 15 days |
| Clinically important increase in rate of a serious suspected adverse reaction over IB rate | IND Safety Report (aggregate) | FDA | ≤15 calendar days (21 CFR 312.32(c)(1)(iii)) |
| Findings from other studies / epidemiology / animal or in-vitro suggesting significant human risk | IND Safety Report | FDA | ≤15 calendar days (21 CFR 312.32(c)(1)(ii), (iv)) |
| Follow-up information on a prior IND safety report | Follow-up IND Safety Report | FDA | As soon as available, ≤15 calendar days after receipt (21 CFR 312.32(d)) |
| Unanticipated problem involving risks to subjects or others | UP Report | {{irb_name}} | Promptly per IRB policy ({{irb_up_reporting_window}}) |
| Pregnancy in a subject or partner | Pregnancy report + outcome follow-up | Sponsor-Investigator | {{pregnancy_reporting_window}} |

#### 6. Report Preparation and Transmission

- 15-day and 7-day reports are prepared on Form FDA 3500A (or an ICH E2B-compliant electronic submission / CIOMS I narrative where accepted) and submitted to the reviewing division per 21 CFR 312.32(c)(1)(v).
- Each report is marked "IND Safety Report," identifies all prior similar reports, and analyzes the significance of the event in light of them (21 CFR 312.32(c)(1)).
- Transmission to FDA is a human-authorized act of the sponsor-investigator; OSSICRO assembles the package only.

#### 7. Safety Data Management

- Safety tracking system: {{safety_tracking_system}}; SAE case files retained per 21 CFR 312.57/312.62.
- SAE-to-clinical-database reconciliation: {{reconciliation_frequency}}.
- Coding: {{ae_coding_dictionary}}.

#### 8. Interface with Safety Oversight Bodies

Cumulative safety listings are provided to {{monitoring_entity}} per the DSMP ({{dsmp_reference}}) at each scheduled review; DSMB recommendations (if applicable) are actioned per its Charter.

#### 9. Training

All site staff on the Delegation of Authority Log with safety duties complete training on this SMP before performing those duties; training records are filed in the ISF.

**Approved by (Sponsor-Investigator):** {{investigator_name}} — Signature: ________________ Date: ________
**Acknowledged by (Medical Monitor):** {{medical_monitor_name}} — Signature: ________________ Date: ________

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{protocol_title}} | study.protocol.title | ICH E2A |
| {{protocol_number}} | study.protocol.number | ICH E2A |
| {{ind_number}} | study.ind.number | 21 CFR 312.32 |
| {{drug_name}} | study.product.name | 21 CFR 312.32 |
| {{investigator_name}} | study.investigator.name | 21 CFR 312.32(b) |
| {{medical_monitor_name}} | study.safety.medical_monitor.name | ICH E2A |
| {{medical_monitor_qualifications}} | study.safety.medical_monitor.qualifications | ICH E2A |
| {{medical_monitor_phone}} | study.safety.medical_monitor.phone | — |
| {{medical_monitor_email}} | study.safety.medical_monitor.email | — |
| {{after_hours_contact}} | study.safety.after_hours_contact | — |
| {{smp_version}} | study.safety.smp.version | — |
| {{smp_date}} | study.safety.smp.date | — |
| {{ib_edition}} | study.product.ib_edition | 21 CFR 312.32(a) |
| {{ib_edition_date}} | study.product.ib_edition_date | 21 CFR 312.32(a) |
| {{sae_definitions}} | study.safety.sae_definitions | 21 CFR 312.32(a); ICH E2A |
| {{severity_grading_scale}} | study.safety.grading_scale | ICH E6(R3) 3.10 |
| {{sae_form_reference}} | study.safety.sae_form_reference | 21 CFR 312.64(b) |
| {{causality_scale}} | study.safety.causality_scale | ICH E2A |
| {{safety_tracking_system}} | study.safety.tracking_system | 21 CFR 312.57 |
| {{reporting_timelines}} | study.safety.reporting_timelines | 21 CFR 312.32(c); ICH E2A |
| {{nonserious_ae_recording_window}} | study.safety.nonserious_ae_window | protocol-specific |
| {{irb_name}} | study.irb.name | 21 CFR 312.66 |
| {{irb_up_reporting_window}} | study.irb.up_reporting_window | 21 CFR 56.108(b)(1) |
| {{pregnancy_reporting_window}} | study.safety.pregnancy_reporting_window | protocol-specific |
| {{reconciliation_frequency}} | study.safety.reconciliation_frequency | ICH E6(R3) |
| {{ae_coding_dictionary}} | study.safety.coding_dictionary | ICH E2A |
| {{monitoring_entity}} | study.safety.monitoring_entity | NIH DSMP Policy |
| {{dsmp_reference}} | study.safety.dsmp.reference | NIH DSMP Policy |

## Related

- [[03-documents/safety-management-pharmacovigilance-plan]]
- [[03-documents/data-safety-monitoring-plan]]
- [[03-documents/sae-report-investigator-to-sponsor]]
- [[03-documents/ind-safety-report-7-15-day]]
- [[03-documents/form-fda-3500a-medwatch-safety-report]]
