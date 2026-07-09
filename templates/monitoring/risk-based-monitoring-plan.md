---
title: "Risk-Based Monitoring Plan"
doc_id: "risk-based-monitoring-plan"
category: "monitoring"
governing_citations: ["ICH E6(R3) 3.11", "FDA Guidance: Risk-Based Approach to Monitoring (2013)", "21 CFR 312.50"]
owner: "sponsor-investigator"
receiver: "sponsor"
gate: "none"
status: template
updated: 2026-07-09
---

# Risk-Based Monitoring Plan — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [ICH E6(R3) §3.11 (Monitoring)](https://www.ich.org/page/efficacy-guidelines); [FDA Guidance for Industry: Oversight of Clinical Investigations — A Risk-Based Approach to Monitoring (Aug. 2013)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/oversight-clinical-investigations-risk-based-approach-monitoring) and the companion Q&A guidance (Apr. 2023); [21 CFR 312.50](https://www.law.cornell.edu/cfr/text/21/312.50) (general sponsor responsibility to monitor the progress of all clinical investigations). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** The monitoring plan documents how the sponsor (here, a sponsor-investigator) will ensure the protection of subjects and the reliability of trial results through a monitoring strategy proportionate to the risks of the trial. It is prepared at startup, before the first subject is screened, and is revised whenever the risk profile of the trial changes.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing.

## Template

### RISK-BASED MONITORING PLAN

| | |
|---|---|
| **Protocol number** | {{protocol_number}} |
| **Protocol title** | {{protocol_title}} |
| **Protocol version / date** | {{protocol_version}} / {{protocol_date}} |
| **IND number** | {{ind_number}} |
| **Sponsor-investigator** | {{sponsor_investigator_name}} |
| **Monitoring entity** | {{monitoring_entity}} [INSTRUCTION: Name the individual, internal group, or contract monitor/CRO who executes this plan. If monitoring obligations are transferred to a CRO, cross-reference the TORO per 21 CFR 312.52.] |
| **Plan version / date** | {{plan_version}} / {{plan_date}} |

#### 1. Scope and objectives

This plan governs monitoring of protocol {{protocol_number}} at {{number_of_sites}} site(s). Its objectives, per ICH E6(R3) §3.11.1, are to verify that: (a) the rights, safety, and well-being of subjects are protected; (b) reported trial data are accurate, complete, and verifiable against source records; and (c) the conduct of the trial complies with the approved protocol/amendments, GCP, and applicable regulatory requirements.

#### 2. Risk assessment

[INSTRUCTION: Summarize the risk assessment that drives this plan. Identify risks to critical-to-quality (CtQ) factors — the data and processes on which subject protection and result reliability depend. Rate each risk by likelihood, detectability, and impact. This section is the justification FDA's 2013 guidance expects for the chosen mix of on-site and centralized monitoring.]

**Overall trial risk category:** {{trial_risk_category}} [INSTRUCTION: e.g., low / moderate / high, with one sentence of basis — first-in-human status, population vulnerability, IP toxicity profile, design complexity.]

**Risk summary:**

{{risk_assessment_summary}}

#### 3. Critical data and processes

The following data elements and trial processes are designated critical. Monitoring effort concentrates here.

{{critical_data_processes}}

[INSTRUCTION: Present as a table: critical datum/process | why critical (subject safety / primary endpoint / regulatory) | associated risk | monitoring method. Typical entries: informed consent documentation; eligibility criteria; primary endpoint source data; SAE identification and reporting; IP dosing, accountability, and storage; randomization/blinding integrity; protocol-specified safety labs.]

#### 4. Quality tolerance limits (QTLs) and key risk indicators (KRIs)

| Parameter | Type (QTL/KRI) | Threshold | Data source | Review frequency | Action on breach |
|---|---|---|---|---|---|
| {{qtl_kri_parameter_1}} | {{qtl_kri_type_1}} | {{qtl_kri_threshold_1}} | {{qtl_kri_source_1}} | {{qtl_kri_frequency_1}} | {{qtl_kri_action_1}} |

[INSTRUCTION: Add one row per parameter. QTLs (ICH E6(R3) §3.10.1.2) are trial-level limits (e.g., proportion of subjects with a missing primary-endpoint assessment > X%); KRIs are site- or trial-level signals (e.g., query rate, deviation rate, SAE-reporting latency). Every QTL breach must be evaluated and, if important, summarized in the clinical study report.]

#### 5. Monitoring approach

{{monitoring_approach}}

[INSTRUCTION: Describe the mix and rationale. Cover each of the following.]

- **On-site monitoring.** Visit schedule: {{onsite_visit_frequency}} [INSTRUCTION: e.g., SIV; first IMV within N weeks of first enrollment; then every N weeks/months, trigger-adjusted; COV]. Scope of each visit type is defined in §6.
- **Centralized / remote monitoring.** {{centralized_monitoring_description}} [INSTRUCTION: Describe ongoing remote review of accumulating data — eCRF completeness, edit-check output, KRI dashboards, cross-site comparisons per the 2013 FDA guidance §III.B.2.]
- **Source data verification (SDV) and source data review (SDR).** {{sdv_sdr_strategy}} [INSTRUCTION: State the extent — e.g., 100% SDV of informed consent, eligibility, primary endpoint, and SAEs; targeted/percentage SDV of other data; SDR of consent process, IP handling, and source-document quality. Risk-based reduction from 100% SDV must trace to §2-§3.]
- **Adaptation triggers.** Monitoring intensity increases at a site when: {{intensification_triggers}} [INSTRUCTION: e.g., KRI breach, serious/repeat deviations, staff turnover, for-cause request.]

#### 6. Visit types and required activities

| Visit type | Timing | Core activities | Report template |
|---|---|---|---|
| Site initiation (SIV) | Before site may screen | Training, readiness confirmation per 21 CFR 312.53(b) | [[site-initiation-visit-report]] |
| Interim monitoring (IMV) | {{onsite_visit_frequency}} | Consent review, SDV/SDR per §5, IP accountability, ISF review, deviation review | [[interim-monitoring-visit-report]] |
| Close-out (COV) | After last subject completes | Reconciliation, retention instruction, outstanding-item closure | [[close-out-visit-report]] |

#### 7. Escalation and management of noncompliance

{{escalation_criteria}}

[INSTRUCTION: Define (a) findings classification (e.g., critical / major / minor); (b) who is notified, in what timeframe, for each class; (c) corrective and preventive action (CAPA) expectations; (d) the securing-compliance obligation — under 21 CFR 312.56(b), if an investigator is not complying, the sponsor must promptly secure compliance or discontinue shipments of the drug and end the investigator's participation; (e) when noncompliance that significantly affects subject protection or data reliability requires reporting to FDA/IRB.]

#### 8. Monitoring documentation and reporting

- Every monitoring activity (on-site, remote, centralized) is documented in a timely manner in a written report to the sponsor-investigator containing the date, site, monitor name, activity summary, findings, deviations/deficiencies, and actions taken or required (ICH E6(R3) §3.11.4).
- Reports are filed in the TMF: [[trial-master-file-index]].
- Report review and sign-off: {{report_reviewer_name}}, within {{report_review_timeline}} of receipt.

#### 9. Plan maintenance

This plan is reviewed {{plan_review_frequency}} and after any protocol amendment, QTL breach, or material change in trial risk. Revisions are version-controlled and retained in the TMF.

#### 10. Approval

| Role | Name | Signature | Date |
|---|---|---|---|
| Sponsor-investigator | {{sponsor_investigator_name}} | ____________________ | ________ |
| Lead monitor / CRO representative | {{lead_monitor_name}} | ____________________ | ________ |

[INSTRUCTION: Approval of this plan is a human act of the sponsor-investigator. OSSICRO drafts; it does not approve.]

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{protocol_number}} | study.protocol.number | ICH E6(R3) 3.11.3 |
| {{protocol_title}} | study.protocol.title | ICH E6(R3) 3.11.3 |
| {{protocol_version}} | study.protocol.version | ICH E6(R3) 3.11.3 |
| {{protocol_date}} | study.protocol.date | ICH E6(R3) 3.11.3 |
| {{ind_number}} | study.ind.number | 21 CFR 312.50 |
| {{sponsor_investigator_name}} | study.sponsor_investigator.name | 21 CFR 312.50 |
| {{monitoring_entity}} | study.monitoring.entity | 21 CFR 312.53(d); 21 CFR 312.52 |
| {{plan_version}} | study.monitoring.plan.version | ICH E6(R3) 3.11.3 |
| {{plan_date}} | study.monitoring.plan.date | ICH E6(R3) 3.11.3 |
| {{number_of_sites}} | study.sites.count | ICH E6(R3) 3.11.3 |
| {{trial_risk_category}} | study.monitoring.risk_assessment.category | FDA RBM Guidance (2013) §IV.A |
| {{risk_assessment_summary}} | study.monitoring.risk_assessment.summary | ICH E6(R3) 3.10.1.1 |
| {{critical_data_processes}} | study.monitoring.critical_data_processes | FDA RBM Guidance (2013) §IV.A; ICH E6(R3) 3.10.1 |
| {{qtl_kri_parameter_1}} (row set) | study.monitoring.qtl_kri[] | ICH E6(R3) 3.10.1.2 |
| {{qtl_kri_type_1}} | study.monitoring.qtl_kri[].type | ICH E6(R3) 3.10.1.2 |
| {{qtl_kri_threshold_1}} | study.monitoring.qtl_kri[].threshold | ICH E6(R3) 3.10.1.2 |
| {{qtl_kri_source_1}} | study.monitoring.qtl_kri[].data_source | ICH E6(R3) 3.10.1.2 |
| {{qtl_kri_frequency_1}} | study.monitoring.qtl_kri[].review_frequency | ICH E6(R3) 3.10.1.2 |
| {{qtl_kri_action_1}} | study.monitoring.qtl_kri[].breach_action | ICH E6(R3) 3.10.1.2 |
| {{monitoring_approach}} | study.monitoring.approach | ICH E6(R3) 3.11.2; FDA RBM Guidance (2013) §IV.B |
| {{onsite_visit_frequency}} | study.monitoring.onsite.frequency | ICH E6(R3) 3.11.3 |
| {{centralized_monitoring_description}} | study.monitoring.centralized.description | FDA RBM Guidance (2013) §III.B.2 |
| {{sdv_sdr_strategy}} | study.monitoring.sdv_sdr.strategy | FDA RBM Guidance (2013) §IV.C |
| {{intensification_triggers}} | study.monitoring.intensification_triggers | FDA RBM Guidance (2013) §IV.D |
| {{escalation_criteria}} | study.monitoring.escalation_criteria | 21 CFR 312.56(b); ICH E6(R3) 3.15 |
| {{report_reviewer_name}} | study.monitoring.report_reviewer.name | ICH E6(R3) 3.11.4 |
| {{report_review_timeline}} | study.monitoring.report_review.timeline | ICH E6(R3) 3.11.4 |
| {{plan_review_frequency}} | study.monitoring.plan.review_frequency | ICH E6(R3) 3.11.3 |
| {{lead_monitor_name}} | study.monitoring.lead_monitor.name | ICH E6(R3) 3.11.4 |

## Related

- [[03-documents/risk-based-monitoring-plan]]
- [[03-documents/site-initiation-visit-report]]
- [[03-documents/interim-monitoring-visit-report]]
- [[03-documents/close-out-visit-report]]
- [[03-documents/data-safety-monitoring-plan]]
- [[03-documents/trial-master-file-index]]
