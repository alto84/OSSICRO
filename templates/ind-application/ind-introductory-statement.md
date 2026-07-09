---
title: "IND - Introductory Statement"
doc_id: "ind-introductory-statement"
category: "ind-application"
governing_citations: ["21 CFR 312.23(a)(3)"]
owner: "sponsor-investigator"
receiver: "fda"
gate: "none"
status: template
updated: 2026-07-09
---

# IND - Introductory Statement  — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 312.23(a)(3)(i)-(iii)](https://www.law.cornell.edu/cfr/text/21/312.23) (introductory statement content), within the IND content-and-format requirements of [21 CFR 312.23](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.23) and the general principles of [21 CFR 312.22](https://www.law.cornell.edu/cfr/text/21/312.22). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** The introductory statement is the opening narrative section of the IND. It identifies the drug and its active ingredients, states the drug's pharmacological class and formulation, and describes the broad objectives and planned duration of the proposed investigation(s), together with a brief summary of prior human experience bearing on safety. It orients the FDA reviewer before the detailed sections (IB, protocol, CMC, pharm/tox) that follow.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing. The level of detail is graded to phase — early-phase statements are concise; the safety floor is never waived.

## Template

## 1. Introductory Statement — 21 CFR 312.23(a)(3)

### 1.1 Drug identity
- **Drug/biologic name:** {{drug_name}}
- **All active ingredients:** {{active_ingredients}}
- **Pharmacological class:** {{pharmacological_class}}
- **Structural formula (if known):** {{structural_formula}}   [INSTRUCTION: For a well-characterized small molecule, provide the structural formula. For a biologic, describe the molecular entity; write "Not applicable / see CMC section" where a structural formula is not meaningful.]
- **Dosage form / formulation:** {{dosage_form}}
- **Route of administration:** {{route_of_administration}}

### 1.2 Objectives and planned duration of the investigation
{{investigation_objectives}}

[INSTRUCTION: State the broad objectives of the proposed clinical investigation(s) and the planned duration. This is a high-level statement of intent, not the protocol's detailed objectives. Example register: "The objective of the proposed Phase {{phase}} investigation is to evaluate the safety, tolerability, and preliminary pharmacokinetics of {{drug_name}} in adults with {{indication}}. The planned duration of the initial investigation is approximately {{planned_duration}}."]

- **Proposed indication:** {{indication}}
- **Development phase:** Phase {{phase}}
- **Planned duration of the proposed investigation(s):** {{planned_duration}}

### 1.3 Summary of previous human experience
{{prior_human_experience_summary}}

[INSTRUCTION: Summarize previous human experience with the drug, emphasizing safety and any experience bearing on the safety of the proposed investigation. Reference other INDs, NDAs, BLAs, or the approved label where the drug is marketed. If there is no prior human experience (first-in-human), state that explicitly and point to the pharmacology/toxicology basis for the "reasonably safe to proceed" conclusion.]

### 1.4 References to other applications
{{related_applications}}

[INSTRUCTION: Reference any other IND, NDA, BLA, DMF, or Master File relied upon or cross-referenced (with letters of authorization where a right of reference is invoked). Write "None" if no other applications are referenced.]

### 1.5 Foreign marketing / withdrawal history
{{foreign_marketing_history}}

[INSTRUCTION: If the drug has been withdrawn from investigation or marketing in any country for any reason related to safety or effectiveness, identify the country(ies) and the reason(s) for withdrawal (21 CFR 312.23(a)(3)(iii)). Write "The drug has not been withdrawn from investigation or marketing in any country for reasons related to safety or effectiveness" if none.]

> [!note] Marketed-drug / sponsor-investigator note
> Where {{drug_name}} is a lawfully marketed drug being studied for a new use under a sponsor-investigator IND, the introductory statement should summarize the approved-labeling human experience and clearly delineate what is new about the proposed investigational use. The scientific conclusion that available data make it reasonably safe to proceed (21 CFR 312.23(a)(8)) is a non-delegable sponsor judgment, drafted here for human sign-off, not asserted by the engine.

## Fields
| placeholder | source (study-record path) | citation |
|---|---|---|
| {{drug_name}} | study.drug.name | 21 CFR 312.23(a)(3)(i) |
| {{active_ingredients}} | study.drug.active_ingredients[] | 21 CFR 312.23(a)(3)(i) |
| {{pharmacological_class}} | study.drug.pharmacological_class | 21 CFR 312.23(a)(3)(i) |
| {{structural_formula}} | study.drug.structural_formula | 21 CFR 312.23(a)(3)(i) |
| {{dosage_form}} | study.drug.dosage_form | 21 CFR 312.23(a)(3)(i) |
| {{route_of_administration}} | study.drug.route | 21 CFR 312.23(a)(3)(i) |
| {{investigation_objectives}} | study.investigation.objectives | 21 CFR 312.23(a)(3)(i) |
| {{indication}} | study.indication | 21 CFR 312.23(a)(3)(i) |
| {{phase}} | study.phase | 21 CFR 312.23(a)(3) |
| {{planned_duration}} | study.investigation.planned_duration | 21 CFR 312.23(a)(3)(i) |
| {{prior_human_experience_summary}} | study.drug.prior_human_experience | 21 CFR 312.23(a)(3)(ii) |
| {{related_applications}} | study.drug.related_applications[] | 21 CFR 312.23(a)(3)(ii) |
| {{foreign_marketing_history}} | study.drug.foreign_marketing_history | 21 CFR 312.23(a)(3)(iii) |

## Related
- [[ind-application-312-23]]
- [[ind-general-investigational-plan]]
- [[investigators-brochure]]
- [[ind-application-cover-and-toc]]
- [[pre-ind-and-ind-preparation]]
- [[ind-submission-and-30-day-clock]]
