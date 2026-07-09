---
title: "Protocol Amendment - Change in Protocol"
doc_id: "protocol-amendment-change-in-protocol"
category: "protocol"
governing_citations: ["21 CFR 312.30(b)"]
owner: "sponsor-investigator"
receiver: "fda"
gate: "submission-to-fda"
status: template
updated: 2026-07-09
---

# Protocol Amendment - Change in Protocol — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 312.30(b)](https://www.law.cornell.edu/cfr/text/21/312.30) (protocol amendments — change in protocol), which requires the sponsor to submit a protocol amendment describing any change in a Phase 1 protocol that significantly affects the safety of subjects, or any change in a Phase 2 or 3 protocol that significantly affects the safety of subjects, the scope of the investigation, or the scientific quality of the study. A change may be implemented only after submission to FDA and, per [21 CFR 312.30(b)(2)(i)](https://www.law.cornell.edu/cfr/text/21/312.30), after IRB approval — except when necessary to eliminate an apparent immediate hazard to subjects, which may be implemented first and reported afterward. This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** This document memorializes a change to an active clinical protocol under IND, states the regulatory basis for the change, and packages it for submission to FDA under the existing IND and to the reviewing IRB. It updates the controlling protocol ([[03-documents/clinical-protocol-ich-m11-ceshharp]]); the amended protocol becomes the version against which the investigator conducts the trial.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing. Determine and record whether the change is (a) a §312.30(b)(2) protocol change requiring submission before implementation and IRB approval, or (b) an immediate-hazard change under §312.30(b)(2)(i) implemented first and reported. Do not conflate a change-in-protocol amendment with a new-investigator amendment (§312.30(c)) or an information amendment (§312.31).

## Template

### PROTOCOL AMENDMENT — CHANGE IN PROTOCOL

**Submitted under IND {{ind_number}} — 21 CFR 312.30(b)**

| | |
|---|---|
| **IND Number** | {{ind_number}} |
| **Serial Number** | {{serial_number}} [INSTRUCTION: the sequential IND submission serial number; every submission to the IND is numbered consecutively per 21 CFR 312.23(a)(1).] |
| **Protocol Number** | {{protocol_number}} |
| **Protocol Title** | {{protocol_title}} |
| **Current Protocol Version / Date** | {{current_protocol_version}} / {{current_protocol_date}} |
| **Amendment Number** | {{amendment_number}} |
| **Amended Protocol Version / Date** | {{amended_protocol_version}} / {{amended_protocol_date}} |
| **Investigational Product** | {{drug_name}} |
| **Sponsor-Investigator** | {{sponsor_investigator_name}} |
| **Date of Amendment** | {{amendment_date}} |

#### 1. Classification of Change

**Amendment type:** {{amendment_type}} [INSTRUCTION: select — "Change in protocol (21 CFR 312.30(b)(2)) — submit before implementation; IRB approval required first" OR "Immediate-hazard change (21 CFR 312.30(b)(2)(i)) — implemented to eliminate an apparent immediate hazard; submitted and reported to IRB after the fact."]

**Significance determination:** {{significance_determination}} [INSTRUCTION: State, per the phase, whether the change significantly affects (Phase 1) subject safety, or (Phase 2/3) subject safety, the scope of the investigation, or the scientific quality of the study. This determination is a human medical/scientific judgment; record its basis. Changes that do NOT meet the §312.30(b) significance threshold need not be submitted as protocol amendments but must still be recorded and IRB-handled per local policy.]

**Affected safety of subjects?** {{affects_subject_safety}} (Yes/No)
**Affected scope of investigation?** {{affects_scope}} (Yes/No)
**Affected scientific quality?** {{affects_scientific_quality}} (Yes/No)

#### 2. Description of Change

{{change_description}}

[INSTRUCTION: Describe each change precisely. Present as a change table for traceability: protocol section | current text/requirement | amended text/requirement. Reference exact section numbers of the M11-structured protocol.]

| Protocol section | Current | Amended |
|---|---|---|
| {{change_section_1}} | {{change_current_1}} | {{change_amended_1}} |

[INSTRUCTION: add one row per discrete change.]

#### 3. Rationale for Change

{{rationale}}

[INSTRUCTION: State the scientific, safety, operational, or regulatory reason for each change. If driven by a safety signal, cross-reference the triggering IND safety report(s) ([[03-documents/ind-safety-report-7-15-day]]) or DSMB recommendation ([[03-documents/dsmb-meeting-minutes-and-recommendation]]). If driven by an FDA request or clinical-hold response, cite the correspondence.]

#### 4. Impact Assessment

- **Impact on risk-benefit:** {{risk_benefit_impact}} [INSTRUCTION: does the change alter the risk-benefit balance established in the current protocol and IB?]
- **Impact on informed consent:** {{consent_impact}} [INSTRUCTION: if the change affects risks, procedures, or duration, the consent form ([[03-documents/informed-consent-form-part50]]) must be revised, IRB-approved, and — where the change is relevant to enrolled subjects' willingness to continue — re-consent obtained (21 CFR 50.25).]
- **Impact on enrolled subjects:** {{enrolled_subject_impact}} [INSTRUCTION: transition plan for participants already on study.]
- **Impact on statistical analysis:** {{statistical_impact}} [INSTRUCTION: if endpoints, sample size, or analysis change, the SAP ([[03-documents/statistical-analysis-plan-ich-e9]]) must be updated; involve the biostatistician.]
- **Impact on registration:** {{registration_impact}} [INSTRUCTION: ClinicalTrials.gov record ([[03-documents/clinicaltrials-gov-registration-record]]) must be updated within 30 days of a change to a required data element per 42 CFR Part 11.]

#### 5. Implementation

- **IRB approval status:** {{irb_approval_status}} [INSTRUCTION: For a §312.30(b)(2) change, IRB approval is obtained BEFORE implementation. For an immediate-hazard change under §312.30(b)(2)(i), the change may be implemented before IRB approval, but the IRB must be notified per 21 CFR 56.108(a)(4) and 312.66.]
- **Planned implementation date:** {{implementation_date}}
- **FDA submission date:** {{fda_submission_date}} [INSTRUCTION: the date this amendment is transmitted to the IND. A §312.30(b)(2) change may be implemented after both FDA submission and IRB approval.]

#### 6. Attachments

{{attachments_list}} [INSTRUCTION: list — amended protocol (clean and redline), revised synopsis, revised consent form, revised SAP, supporting safety data, IRB approval letter, updated 1572 if the investigator/site list changed.]

---

## SPONSOR-INVESTIGATOR SIGNATURE

I certify that the change described above is accurately represented, that I have made the significance determination in Section 1, and that this amendment will be handled in accordance with 21 CFR 312.30(b).

| Role | Name | Signature | Date |
|---|---|---|---|
| Sponsor-Investigator | {{sponsor_investigator_name}} | ____________________ | ________ |

> [!warning] Non-delegable
> Submission to FDA is executed by the sponsor-investigator (21 CFR 312.20, 312.23, 312.40; FD&C Act 505(i)). OSSICRO assembles the complete, validated amendment package and computes the sequencing (IRB-approval-before-implementation vs. immediate-hazard-first); the engine cannot transmit it to FDA without a recorded human sign-off. The significance determination in Section 1 is likewise a human medical/scientific judgment, not a software output.

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{ind_number}} | study.ind.number | 21 CFR 312.30(b) |
| {{serial_number}} | study.ind.next_serial_number | 21 CFR 312.23(a)(1) |
| {{protocol_number}} | study.protocol.number | 21 CFR 312.30(b) |
| {{protocol_title}} | study.protocol.title | 21 CFR 312.30(b) |
| {{current_protocol_version}} | study.protocol.version | 21 CFR 312.30(b) |
| {{current_protocol_date}} | study.protocol.date | 21 CFR 312.30(b) |
| {{amendment_number}} | study.protocol.amendment.number | 21 CFR 312.30(b) |
| {{amended_protocol_version}} | study.protocol.amendment.new_version | 21 CFR 312.30(b) |
| {{amended_protocol_date}} | study.protocol.amendment.new_date | 21 CFR 312.30(b) |
| {{drug_name}} | study.ip.name | 21 CFR 312.30(b) |
| {{sponsor_investigator_name}} | study.sponsor_investigator.name | 21 CFR 312.30(b) |
| {{amendment_date}} | study.protocol.amendment.date | 21 CFR 312.30(b) |
| {{amendment_type}} | study.protocol.amendment.type | 21 CFR 312.30(b)(2); 312.30(b)(2)(i) |
| {{significance_determination}} | study.protocol.amendment.significance | 21 CFR 312.30(b)(2)(ii) |
| {{affects_subject_safety}} | study.protocol.amendment.affects_safety | 21 CFR 312.30(b)(2)(ii) |
| {{affects_scope}} | study.protocol.amendment.affects_scope | 21 CFR 312.30(b)(2)(ii) |
| {{affects_scientific_quality}} | study.protocol.amendment.affects_quality | 21 CFR 312.30(b)(2)(ii) |
| {{change_description}} | study.protocol.amendment.change_description | 21 CFR 312.30(b)(2) |
| {{change_section_1}} (row set) | study.protocol.amendment.changes[].section | 21 CFR 312.30(b)(2) |
| {{change_current_1}} | study.protocol.amendment.changes[].current | 21 CFR 312.30(b)(2) |
| {{change_amended_1}} | study.protocol.amendment.changes[].amended | 21 CFR 312.30(b)(2) |
| {{rationale}} | study.protocol.amendment.rationale | 21 CFR 312.30(b)(2) |
| {{risk_benefit_impact}} | study.protocol.amendment.impact.risk_benefit | ICH E6(R3) 2.4 |
| {{consent_impact}} | study.protocol.amendment.impact.consent | 21 CFR 50.25 |
| {{enrolled_subject_impact}} | study.protocol.amendment.impact.enrolled_subjects | 21 CFR 312.30(b) |
| {{statistical_impact}} | study.protocol.amendment.impact.statistics | ICH E9 |
| {{registration_impact}} | study.protocol.amendment.impact.registration | 42 CFR Part 11 |
| {{irb_approval_status}} | study.protocol.amendment.irb_approval_status | 21 CFR 312.30(b)(2)(i); 312.66 |
| {{implementation_date}} | study.protocol.amendment.implementation_date | 21 CFR 312.30(b) |
| {{fda_submission_date}} | study.protocol.amendment.fda_submission_date | 21 CFR 312.30(b) |
| {{attachments_list}} | study.protocol.amendment.attachments[] | 21 CFR 312.30(b) |

## Related

- [[03-documents/protocol-amendment-change-in-protocol]]
- [[03-documents/clinical-protocol-ich-m11-ceshharp]]
- [[03-documents/informed-consent-form-part50]]
- [[03-documents/statistical-analysis-plan-ich-e9]]
- [[03-documents/ind-safety-report-7-15-day]]
- [[03-documents/dsmb-meeting-minutes-and-recommendation]]
- [[03-documents/clinicaltrials-gov-registration-record]]
- [[02-lifecycle/annual-reporting-and-amendments]]
- [[02-lifecycle/irb-submission-and-approval]]
- [[04-coordination/fda-interactions-meetings-holds]]
