---
title: "IND Safety Report (7-day / 15-day)"
doc_id: "ind-safety-report-7-15-day"
category: "safety"
governing_citations: ["21 CFR 312.32(c)(1)", "21 CFR 312.32(c)(2)", "ICH E2A"]
owner: "sponsor-investigator"
receiver: "fda"
gate: "sae-causality"
status: template
updated: 2026-07-09
---

# IND Safety Report (7-day / 15-day) — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 312.32(c)(1)](https://www.law.cornell.edu/cfr/text/21/312.32) (15-calendar-day written reports of serious and unexpected suspected adverse reactions and other qualifying findings) and [21 CFR 312.32(c)(2)](https://www.law.cornell.edu/cfr/text/21/312.32) (7-calendar-day notification of unexpected fatal or life-threatening suspected adverse reactions); [ICH E2A](https://www.ich.org/page/efficacy-guidelines); [FDA Guidance: Safety Reporting Requirements for INDs and BA/BE Studies (2012)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/safety-reporting-requirements-inds-investigational-new-drug-applications-and-babe). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** The sponsor(-investigator)'s expedited safety report to FDA and all participating investigators: a serious and unexpected suspected adverse reaction (15-day), an unexpected fatal/life-threatening suspected adverse reaction (7-day notification, completed within 15 days), or an aggregate/other-finding report under 312.32(c)(1)(ii)-(iv). It wraps the individual case report (Form FDA 3500A or CIOMS I) with the required analysis of similar prior reports.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing. Day 0 is the date anyone on the sponsor side first received the information; the {{due_date}} is computed from it and is a regulatory deadline.

## Template

### IND SAFETY REPORT

[INSTRUCTION: Mark the submission prominently "IND Safety Report" per 21 CFR 312.32(c)(1)(v).]

**Report classification ({{report_type}}):**
- ☐ 15-day report — serious + unexpected suspected adverse reaction (312.32(c)(1)(i))
- ☐ 7-day report — unexpected fatal or life-threatening suspected adverse reaction (312.32(c)(2)) [INSTRUCTION: the 7-day notification may be by telephone or facsimile/electronic means to the review division; a complete written report follows within 15 calendar days of initial awareness.]
- ☐ 15-day report — findings from other studies (clinical, epidemiological, pooled) suggesting significant human risk (312.32(c)(1)(ii))
- ☐ 15-day report — findings from animal or in-vitro testing suggesting significant human risk (312.32(c)(1)(iii)) [INSTRUCTION: verify subparagraph mapping against the current CFR text before filing; the (ii)/(iii)/(iv) ordering has been renumbered historically.]
- ☐ 15-day report — clinically important increase in the rate of a serious suspected adverse reaction over that listed in the IB/protocol (312.32(c)(1)(iv))
- ☐ Follow-up to report {{prior_report_reference}} (312.32(d))

| | |
|---|---|
| IND Number | {{ind_number}} |
| Sponsor-Investigator | {{investigator_name}}, {{investigator_address}} |
| Drug | {{drug_name}} |
| Protocol(s) affected | {{protocol_number}} |
| Sponsor awareness date (day 0) | {{awareness_date}} |
| **Regulatory due date** | **{{due_date}}** |
| Date submitted | {{submission_date}} |
| Serial number of this submission | {{serial_number}} [INSTRUCTION: matches the Form FDA 1571 serial sequence for this IND.] |

#### 1. Event Summary

| | |
|---|---|
| Event term (MedDRA PT) | {{event_term}} |
| Subject code / study / site | {{subject_code}} / {{protocol_number}} / {{site_number}} |
| Seriousness criteria met | {{seriousness_criteria}} |
| Outcome | {{event_outcome}} |

Individual case report attached: ☐ Form FDA 3500A ☐ CIOMS I ☐ E2B(R3) electronic submission — reference {{case_report_reference}}

#### 2. Basis for Suspected Adverse Reaction (Causality)

{{causality_basis}}

[INSTRUCTION: State the medical monitor's determination that there is a *reasonable possibility* the drug caused the event, and the evidence: temporal relationship, dechallenge/rechallenge, known class effect, absence of alternative etiology, single occurrence of an event uncommon and known to be strongly drug-associated (e.g., angioedema, hepatic injury, Stevens-Johnson syndrome), or aggregate imbalance vs. control (312.32(c)(1)(i)(A)-(C)). Determination made by {{medical_monitor_name}} on {{causality_determination_date}}. Events that are serious but for which a reasonable causal possibility cannot be articulated are NOT individually reportable — do not file noise.]

#### 3. Basis for Unexpectedness

{{expectedness_basis}}

[INSTRUCTION: Compare against the reference safety document: IB edition {{ib_edition}} dated {{ib_edition_date}} (or protocol/general investigational plan if no IB). State why the event is not listed, or is observed at greater specificity or severity than listed (21 CFR 312.32(a)).]

#### 4. Analysis of Similar Reports

{{similar_events_analysis}}

[INSTRUCTION: 21 CFR 312.32(c)(1) requires each report to identify all previously submitted IND safety reports concerning a similar suspected adverse reaction and to analyze the significance of this event in light of them. List prior report dates/serial numbers or state "No prior similar reports have been submitted under this IND."]

#### 5. Actions Taken / Planned

{{actions_taken}}

[INSTRUCTION: e.g., protocol amendment, IB update, consent form revision, enrollment pause, DSMB notification, additional monitoring. If none, justify.]

#### 6. Distribution

- FDA review division: {{fda_review_division}}, per 312.32(c)(1)(v)
- All participating investigators: notified on {{investigator_notification_date}} (312.32(c)(1))
- IRB: {{irb_name}}, per 21 CFR 312.66 and the site's unanticipated-problem policy

**Submitted by (Sponsor-Investigator):** {{investigator_name}} — Signature: ________________ Date: ________

> [!warning] Non-delegable
> SAE causality / expectedness determination is executed by the medical-monitor (21 CFR 312.32(a), 312.32(b), 312.32(c); ICH E2A). OSSICRO drafts this template; the engine cannot finalize it without a recorded human sign-off. Transmission to FDA is additionally a human-authorized act of the sponsor-investigator (21 CFR 312.20, 312.23, 312.40).

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{report_type}} | safety.expedited.report_type | 21 CFR 312.32(c)(1), (c)(2) |
| {{prior_report_reference}} | safety.expedited.prior_report_reference | 21 CFR 312.32(d) |
| {{ind_number}} | study.ind.number | 21 CFR 312.32(c) |
| {{investigator_name}} | study.investigator.name | 21 CFR 312.32(c) |
| {{investigator_address}} | study.investigator.address | Form FDA 1571 |
| {{drug_name}} | study.product.name | 21 CFR 312.32(c) |
| {{protocol_number}} | study.protocol.number | 21 CFR 312.32(c) |
| {{awareness_date}} | safety.expedited.awareness_date | 21 CFR 312.32(c) |
| {{due_date}} | safety.expedited.due_date (computed: awareness_date + 7 or 15 calendar days) | 21 CFR 312.32(c)(1), (c)(2) |
| {{submission_date}} | safety.expedited.submission_date | — |
| {{serial_number}} | study.ind.next_serial_number | Form FDA 1571 |
| {{event_term}} | safety.case.event_term | ICH E2A |
| {{subject_code}} | safety.case.subject_code | 21 CFR 312.62(b) |
| {{site_number}} | study.site.number | — |
| {{seriousness_criteria}} | safety.case.seriousness_criteria | 21 CFR 312.32(a) |
| {{event_outcome}} | safety.case.outcome | ICH E2A |
| {{case_report_reference}} | safety.expedited.case_report_reference | 21 CFR 312.32(c)(1)(v) |
| {{causality_basis}} | safety.expedited.causality_basis | 21 CFR 312.32(c)(1)(i) |
| {{medical_monitor_name}} | study.safety.medical_monitor.name | ICH E2A |
| {{causality_determination_date}} | safety.expedited.causality_determination_date | 21 CFR 312.32(b) |
| {{expectedness_basis}} | safety.expedited.expectedness_basis | 21 CFR 312.32(a) |
| {{ib_edition}} | study.product.ib_edition | 21 CFR 312.32(a) |
| {{ib_edition_date}} | study.product.ib_edition_date | 21 CFR 312.32(a) |
| {{similar_events_analysis}} | safety.expedited.similar_events_analysis | 21 CFR 312.32(c)(1) |
| {{actions_taken}} | safety.expedited.actions_taken | ICH E2A |
| {{fda_review_division}} | study.ind.review_division | 21 CFR 312.32(c)(1)(v) |
| {{investigator_notification_date}} | safety.expedited.investigator_notification_date | 21 CFR 312.32(c)(1) |
| {{irb_name}} | study.irb.name | 21 CFR 312.66 |

## Related

- [[03-documents/ind-safety-report-7-15-day]]
- [[03-documents/sae-report-investigator-to-sponsor]]
- [[03-documents/form-fda-3500a-medwatch-safety-report]]
- [[03-documents/safety-management-pharmacovigilance-plan]]
- [[03-documents/unanticipated-problem-report-to-irb]]
