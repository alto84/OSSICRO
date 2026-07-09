---
title: "SAE Report - Investigator to Sponsor"
doc_id: "sae-report-investigator-to-sponsor"
category: "safety"
governing_citations: ["21 CFR 312.64(b)"]
owner: "investigator"
receiver: "sponsor"
gate: "sae-causality"
status: template
updated: 2026-07-09
---

# SAE Report — Investigator to Sponsor — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 312.64(b)](https://www.law.cornell.edu/cfr/text/21/312.64) — the investigator must *immediately* report to the sponsor any serious adverse event, whether or not considered drug related, including a causality assessment; study-endpoint SAEs are reported per the protocol unless there is evidence suggesting a causal relationship. Definitions per [21 CFR 312.32(a)](https://www.law.cornell.edu/cfr/text/21/312.32) and [ICH E2A](https://www.ich.org/page/efficacy-guidelines). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** The site-level report the investigator sends the sponsor(-investigator) immediately upon learning of a serious adverse event. It carries the minimum reportable case (identifiable subject, reporter, suspect drug, event) plus the investigator's causality assessment, and starts the sponsor's regulatory clock.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing. Never enter the subject's name or direct identifiers — use the study code only.

## Template

### SERIOUS ADVERSE EVENT REPORT — INVESTIGATOR TO SPONSOR

**Report type:** ☐ Initial ☐ Follow-up #{{followup_number}} ☐ Final
**Date of this report:** {{report_date}} — **Date investigator first aware of event:** {{awareness_date}}
[INSTRUCTION: 21 CFR 312.64(b) requires IMMEDIATE reporting; the interval between awareness and report should not exceed 24 hours per this study's SMP.]

#### A. Study Identification

| | |
|---|---|
| Protocol Number / Title | {{protocol_number}} / {{protocol_title}} |
| IND Number | {{ind_number}} |
| Site | {{site_name}} ({{site_number}}) |
| Investigator | {{investigator_name}} |

#### B. Subject (coded — no direct identifiers)

| | |
|---|---|
| Subject Code | {{subject_code}} |
| Age / Sex | {{subject_age}} / {{subject_sex}} |
| Weight | {{subject_weight}} |
| Relevant medical history | {{relevant_medical_history}} |

#### C. Event

| | |
|---|---|
| Event term (diagnosis preferred over symptoms) | {{event_term}} |
| Onset date/time | {{onset_date}} |
| Resolution date (or "ongoing") | {{resolution_date}} |
| Severity grade ({{severity_grading_scale}}) | {{severity_grade}} |

**Seriousness criteria (check all that apply — 21 CFR 312.32(a)):**
{{seriousness_criteria}}
- ☐ Death (date: {{death_date}}; cause: {{cause_of_death}})
- ☐ Life-threatening
- ☐ Inpatient hospitalization or prolongation of existing hospitalization
- ☐ Persistent or significant incapacity / substantial disruption of normal life functions
- ☐ Congenital anomaly / birth defect
- ☐ Important medical event requiring intervention to prevent one of the above

#### D. Investigational Product

| | |
|---|---|
| Drug name / lot | {{drug_name}} / {{lot_number}} |
| Dose / route / frequency at onset | {{dose_at_onset}} |
| First dose date / last dose before event | {{first_dose_date}} / {{last_dose_date}} |
| Action taken with IP | ☐ None ☐ Interrupted ☐ Dose reduced ☐ Permanently discontinued — {{ip_action}} |
| Dechallenge / rechallenge result (if any) | {{dechallenge_rechallenge}} |
| Blinding status | ☐ Open-label ☐ Blinded, not broken ☐ Unblinded on {{unblinding_date}} |

#### E. Narrative

{{event_narrative}}

[INSTRUCTION: Chronological narrative: presentation, workup, treatment of the event, response, current status. Include relevant labs/imaging with dates and units. State alternative etiologies considered.]

**Concomitant medications:** {{concomitant_medications}}
**Relevant laboratory / diagnostic results:** {{relevant_labs}}

#### F. Investigator Causality Assessment

Is there a reasonable possibility that {{drug_name}} caused the event? ☐ Yes ☐ No
Assessment on study scale ({{causality_scale}}): {{investigator_causality}}
Basis: {{causality_basis_investigator}}

[INSTRUCTION: 21 CFR 312.64(b) requires the report to include an assessment of causality. This is the investigator's clinical opinion; the sponsor-side suspected-adverse-reaction determination for expedited reporting is made separately by the medical monitor (see gate).]

#### G. Outcome at Time of Report

☐ Recovered/resolved ☐ Recovering ☐ Recovered with sequelae ({{sequelae}}) ☐ Not recovered ☐ Fatal ☐ Unknown

#### H. Reporter

| | |
|---|---|
| Reporter name / role | {{reporter_name}} / {{reporter_role}} |
| Phone / email | {{reporter_phone}} / {{reporter_email}} |

**Investigator signature:** ________________ **Date:** ________
[INSTRUCTION: The investigator (not a delegate) signs the causality assessment. Transmit to the sponsor-investigator at {{sponsor_sae_intake}} and file the copy in the ISF.]

> [!warning] Non-delegable
> SAE causality / expectedness determination is executed by the medical-monitor (21 CFR 312.32(a), 312.32(b), 312.32(c); ICH E2A). OSSICRO drafts this template; the engine cannot finalize it without a recorded human sign-off.

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{followup_number}} | safety.case.followup_number | 21 CFR 312.32(d) |
| {{report_date}} | safety.case.report_date | 21 CFR 312.64(b) |
| {{awareness_date}} | safety.case.awareness_date | 21 CFR 312.64(b) |
| {{protocol_number}} | study.protocol.number | 21 CFR 312.64(b) |
| {{protocol_title}} | study.protocol.title | 21 CFR 312.64(b) |
| {{ind_number}} | study.ind.number | 21 CFR 312.32 |
| {{site_name}} | study.site.name | — |
| {{site_number}} | study.site.number | — |
| {{investigator_name}} | study.investigator.name | 21 CFR 312.64(b) |
| {{subject_code}} | safety.case.subject_code | 21 CFR 312.62(b) |
| {{subject_age}} | safety.case.subject_age | ICH E2A (minimum case info) |
| {{subject_sex}} | safety.case.subject_sex | ICH E2A |
| {{subject_weight}} | safety.case.subject_weight | — |
| {{relevant_medical_history}} | safety.case.medical_history | ICH E2A |
| {{event_term}} | safety.case.event_term | ICH E2A |
| {{onset_date}} | safety.case.onset_date | ICH E2A |
| {{resolution_date}} | safety.case.resolution_date | ICH E2A |
| {{severity_grading_scale}} | study.safety.grading_scale | ICH E6(R3) 3.10 |
| {{severity_grade}} | safety.case.severity_grade | protocol-specific |
| {{seriousness_criteria}} | safety.case.seriousness_criteria | 21 CFR 312.32(a) |
| {{death_date}} | safety.case.death_date | 21 CFR 312.64(b) |
| {{cause_of_death}} | safety.case.cause_of_death | 21 CFR 312.64(b) |
| {{drug_name}} | study.product.name | 21 CFR 312.64(b) |
| {{lot_number}} | safety.case.lot_number | 21 CFR 312.62(a) |
| {{dose_at_onset}} | safety.case.dose_at_onset | ICH E2A |
| {{first_dose_date}} | safety.case.first_dose_date | ICH E2A |
| {{last_dose_date}} | safety.case.last_dose_date | ICH E2A |
| {{ip_action}} | safety.case.ip_action | ICH E2A |
| {{dechallenge_rechallenge}} | safety.case.dechallenge_rechallenge | ICH E2A |
| {{unblinding_date}} | safety.case.unblinding_date | protocol-specific |
| {{event_narrative}} | safety.case.narrative | ICH E2A |
| {{concomitant_medications}} | safety.case.concomitant_medications | ICH E2A |
| {{relevant_labs}} | safety.case.relevant_labs | ICH E2A |
| {{causality_scale}} | study.safety.causality_scale | ICH E2A |
| {{investigator_causality}} | safety.case.investigator_causality | 21 CFR 312.64(b) |
| {{causality_basis_investigator}} | safety.case.causality_basis_investigator | 21 CFR 312.64(b) |
| {{sequelae}} | safety.case.sequelae | ICH E2A |
| {{reporter_name}} | safety.case.reporter.name | ICH E2A |
| {{reporter_role}} | safety.case.reporter.role | — |
| {{reporter_phone}} | safety.case.reporter.phone | — |
| {{reporter_email}} | safety.case.reporter.email | — |
| {{sponsor_sae_intake}} | study.safety.sponsor_sae_intake | 21 CFR 312.64(b) |

## Related

- [[03-documents/sae-report-investigator-to-sponsor]]
- [[03-documents/ind-safety-report-7-15-day]]
- [[03-documents/form-fda-3500a-medwatch-safety-report]]
- [[03-documents/safety-management-pharmacovigilance-plan]]
- [[03-documents/unanticipated-problem-report-to-irb]]
