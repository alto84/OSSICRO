---
title: "Form FDA 3500A - MedWatch Mandatory Safety Report"
doc_id: "form-fda-3500a-medwatch-safety-report"
category: "safety"
governing_citations: ["21 CFR 312.32", "Form FDA 3500A"]
owner: "sponsor-investigator"
receiver: "fda"
gate: "sae-causality"
status: template
updated: 2026-07-09
---

# Form FDA 3500A — MedWatch Mandatory Safety Report — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 312.32](https://www.law.cornell.edu/cfr/text/21/312.32) (IND safety reporting; 312.32(c)(1)(v) names Form FDA 3500A as an acceptable format for expedited individual case reports) and [Form FDA 3500A (MedWatch mandatory reporting form and instructions)](https://www.fda.gov/safety/medical-product-safety-information/forms-reporting-fda). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs. The wire format filed with FDA is the official 3500A form (or an ICH E2B electronic equivalent); this template is the structured worksheet that populates it field-for-field.

**Purpose.** The individual case safety report attached to a 7-day or 15-day IND safety report. This worksheet mirrors the 3500A's lettered sections (A, B, C, E, G; D and F apply to devices/user facilities and are omitted for drug INDs) so a completed worksheet transfers onto the official form without re-derivation.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing. Use the coded subject identifier only — never a name or medical record number.

## Template

### FORM FDA 3500A WORKSHEET — MANDATORY REPORTING

[INSTRUCTION: Check "Adverse Event" and, on the official form header, indicate this is an IND safety report with the IND number {{ind_number}}.]

#### Section A — Patient Information

| 3500A item | Entry |
|---|---|
| A.1 Patient identifier (coded) | {{subject_code}} [INSTRUCTION: study subject code; confidentiality per 21 CFR 312.62(b).] |
| A.2 Age at time of event (or DOB category) | {{subject_age}} |
| A.3 Sex | {{subject_sex}} |
| A.4 Weight | {{subject_weight}} |

#### Section B — Adverse Event or Product Problem

| 3500A item | Entry |
|---|---|
| B.1 | ☒ Adverse event ☐ Product problem |
| B.2 Outcomes attributed to the event (check all) | {{event_outcomes}} [INSTRUCTION: death (with date), life-threatening, hospitalization (initial or prolonged), disability or permanent damage, congenital anomaly/birth defect, other serious/important medical event, required intervention to prevent permanent impairment.] |
| B.3 Date of event | {{onset_date}} |
| B.4 Date of this report | {{report_date}} |
| B.5 Describe event or problem | {{event_description}} [INSTRUCTION: full clinical narrative — presentation, course, treatment, response, current status, alternative etiologies considered. Attach continuation pages as needed.] |
| B.6 Relevant tests / laboratory data, including dates | {{relevant_labs}} |
| B.7 Other relevant history (pre-existing conditions, allergies, pregnancy, tobacco/alcohol) | {{relevant_history}} |

#### Section C — Suspect Product(s)

| 3500A item | Entry |
|---|---|
| C.1 Name, strength, manufacturer | {{suspect_product}} [INSTRUCTION: investigational product name/code, strength, and manufacturer as in the IND.] |
| C.2 Dose, frequency, route | {{dose_frequency_route}} |
| C.3 Therapy dates (from/to) | {{therapy_dates}} |
| C.4 Diagnosis for use (indication) | {{indication}} |
| C.5 Event abated after use stopped or dose reduced? | ☐ Yes ☐ No ☐ Doesn't apply — {{dechallenge_result}} |
| C.6 Lot number | {{lot_number}} |
| C.7 Expiration date | {{lot_expiration}} |
| C.8 Event reappeared after reintroduction? | ☐ Yes ☐ No ☐ Doesn't apply — {{rechallenge_result}} |
| C.9 NDC or unique ID | {{ndc_or_ind_identifier}} [INSTRUCTION: for investigational drugs, enter the IND number.] |
| C.10 Concomitant medical products and therapy dates (exclude treatment of the event) | {{concomitant_products}} |

#### Section E — Initial Reporter

| 3500A item | Entry |
|---|---|
| E.1 Name, address, phone | {{reporter_name}}, {{reporter_address}}, {{reporter_phone}} |
| E.2 Health professional? | ☐ Yes ☐ No — occupation: {{reporter_occupation}} |
| E.3 Initial reporter also sent report to FDA? | ☐ Yes ☐ No ☐ Unknown |

#### Section G — All Manufacturers / Sponsor

| 3500A item | Entry |
|---|---|
| G.1 Contact office (sponsor-investigator) name/address | {{sponsor_name}}, {{sponsor_address}} |
| G.2 Phone | {{sponsor_phone}} |
| G.3 Report source | ☒ Study — protocol {{protocol_number}} |
| G.4 Date received by sponsor (day 0) | {{awareness_date}} |
| G.5 IND number / pre-1938 / OTC | IND {{ind_number}} |
| G.6 If IND, protocol number | {{protocol_number}} |
| G.7 Type of report | ☐ 7-day ☐ 15-day ☐ Follow-up #{{followup_number}} — {{report_type}} |
| G.8 Adverse event term(s) | {{event_term}} |

[INSTRUCTION: The medical monitor's causality determination and the expectedness assessment that made this case expeditable are documented in the accompanying IND Safety Report cover analysis ({{ind_safety_report_reference}}); the 3500A itself carries the case facts.]

**Completed by:** {{preparer_name}} — Date: {{report_date}}
**Reviewed and authorized for submission (Sponsor-Investigator):** {{sponsor_name}} — Signature: ________________ Date: ________

> [!warning] Non-delegable
> SAE causality / expectedness determination is executed by the medical-monitor (21 CFR 312.32(a), 312.32(b), 312.32(c); ICH E2A). OSSICRO drafts this template; the engine cannot finalize it without a recorded human sign-off. Submission of the completed 3500A to FDA is a human-authorized act of the sponsor-investigator.

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{ind_number}} | study.ind.number | 21 CFR 312.32 |
| {{subject_code}} | safety.case.subject_code | 3500A item A.1; 21 CFR 312.62(b) |
| {{subject_age}} | safety.case.subject_age | 3500A item A.2 |
| {{subject_sex}} | safety.case.subject_sex | 3500A item A.3 |
| {{subject_weight}} | safety.case.subject_weight | 3500A item A.4 |
| {{event_outcomes}} | safety.case.seriousness_criteria | 3500A item B.2; 21 CFR 312.32(a) |
| {{onset_date}} | safety.case.onset_date | 3500A item B.3 |
| {{report_date}} | safety.case.report_date | 3500A item B.4 |
| {{event_description}} | safety.case.narrative | 3500A item B.5 |
| {{relevant_labs}} | safety.case.relevant_labs | 3500A item B.6 |
| {{relevant_history}} | safety.case.medical_history | 3500A item B.7 |
| {{suspect_product}} | study.product.name + study.product.manufacturer | 3500A item C.1 |
| {{dose_frequency_route}} | safety.case.dose_at_onset | 3500A item C.2 |
| {{therapy_dates}} | safety.case.first_dose_date + safety.case.last_dose_date | 3500A item C.3 |
| {{indication}} | study.indication | 3500A item C.4 |
| {{dechallenge_result}} | safety.case.dechallenge | 3500A item C.5 |
| {{lot_number}} | safety.case.lot_number | 3500A item C.6 |
| {{lot_expiration}} | safety.case.lot_expiration | 3500A item C.7 |
| {{rechallenge_result}} | safety.case.rechallenge | 3500A item C.8 |
| {{ndc_or_ind_identifier}} | study.ind.number | 3500A item C.9 |
| {{concomitant_products}} | safety.case.concomitant_medications | 3500A item C.10 |
| {{reporter_name}} | safety.case.reporter.name | 3500A item E.1 |
| {{reporter_address}} | safety.case.reporter.address | 3500A item E.1 |
| {{reporter_phone}} | safety.case.reporter.phone | 3500A item E.1 |
| {{reporter_occupation}} | safety.case.reporter.role | 3500A item E.2 |
| {{sponsor_name}} | study.sponsor.name | 3500A section G |
| {{sponsor_address}} | study.sponsor.address | 3500A section G |
| {{sponsor_phone}} | study.sponsor.phone | 3500A section G |
| {{awareness_date}} | safety.expedited.awareness_date | 3500A item G.4; 21 CFR 312.32(c) |
| {{protocol_number}} | study.protocol.number | 3500A item G.6 |
| {{report_type}} | safety.expedited.report_type | 3500A item G.7; 21 CFR 312.32(c) |
| {{followup_number}} | safety.case.followup_number | 21 CFR 312.32(d) |
| {{event_term}} | safety.case.event_term | 3500A item G.8 |
| {{ind_safety_report_reference}} | safety.expedited.cover_report_reference | 21 CFR 312.32(c)(1) |
| {{preparer_name}} | safety.case.preparer | — |

## Related

- [[03-documents/form-fda-3500a-medwatch-safety-report]]
- [[03-documents/ind-safety-report-7-15-day]]
- [[03-documents/sae-report-investigator-to-sponsor]]
- [[03-documents/safety-management-pharmacovigilance-plan]]
