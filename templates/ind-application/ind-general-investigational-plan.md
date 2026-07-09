---
title: "IND - General Investigational Plan"
doc_id: "ind-general-investigational-plan"
category: "ind-application"
governing_citations: ["21 CFR 312.23(a)(3)(iv)"]
owner: "sponsor-investigator"
receiver: "fda"
gate: "none"
status: template
updated: 2026-07-09
---

# IND - General Investigational Plan  — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 312.23(a)(3)(iv)](https://www.law.cornell.edu/cfr/text/21/312.23) (general investigational plan), within the IND content-and-format requirements of [21 CFR 312.23](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.23). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** The general investigational plan states the sponsor's rationale for the drug and the research, the indication(s) to be studied, the general approach to evaluating the drug, the kinds of clinical trials to be conducted in the first year following submission, the estimated number of subjects, and any risks of particular severity or seriousness anticipated from toxicological or prior human data. It is a **plan, not a binding commitment** — its detail is proportionate to early-phase uncertainty (21 CFR 312.23(a)(3)(iv)).

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing.

## Template

## General Investigational Plan — 21 CFR 312.23(a)(3)(iv)

### 1. Rationale for the drug and the research study
{{rationale}}

[INSTRUCTION: State the scientific rationale — the mechanism, the unmet need, and why the drug is a plausible candidate in this indication. Ground claims in the pharmacology/toxicology and prior human experience summarized elsewhere in the IND; do not overstate efficacy expectations for an early-phase program.]

### 2. Indication(s) to be studied
{{indication}}

[INSTRUCTION: Identify the indication(s) the investigation will address. If the plan spans more than one indication or population, enumerate each.]

### 3. General approach to evaluating the drug
{{general_approach}}

[INSTRUCTION: Describe the overall development approach — e.g., dose-escalation strategy, the sequence from safety/tolerability to preliminary activity, the general study designs contemplated, and how the phases build on one another. This is the strategic arc, not a protocol.]

### 4. Clinical trials planned in the first year following submission
{{planned_studies_next_year}}

[INSTRUCTION: Describe the kinds of clinical trials to be conducted during the first year after submission. For a single-protocol early-phase IND, this may be the one Phase {{phase}} study described in the accompanying protocol. List each planned study with its design in brief and, where known, its identifier.]

| Planned study | Phase | Design (brief) | Estimated subjects | Planned start |
|---|---|---|---|---|
| {{planned_study_title}} | {{phase}} | {{planned_study_design}} | {{estimated_subjects}} | {{planned_start}} |

[INSTRUCTION: Add one row per planned study for the first year. If only the accompanying protocol is planned, a single row suffices.]

### 5. Estimated number of subjects
{{estimated_subjects_total}}

[INSTRUCTION: Give the estimated total number of subjects to be given the drug across the first-year plan. This is an estimate; note that it is proportionate to the early-phase scope.]

### 6. Anticipated risks of particular severity or seriousness
{{anticipated_serious_risks}}

[INSTRUCTION: Describe any risks of particular severity or seriousness anticipated on the basis of the toxicological data or prior human experience with this drug or related drugs. If the nonclinical/clinical data do not indicate risks of particular severity beyond those in the IB and protocol, state that and reference the Investigator's Brochure risk section. The seriousness/benefit-risk characterization is a sponsor medical judgment drafted here for human sign-off.]

> [!note] Plan, not commitment
> The general investigational plan describes intent at the level of detail available at submission. The sponsor may modify the plan as the program develops; material changes to a specific protocol are made through protocol amendments (21 CFR 312.30) and the plan is updated in the [[ind-annual-report-312-33|annual report]] (21 CFR 312.33(c)). No gate attaches to this section; it is submitted as part of the gated IND package.

## Fields
| placeholder | source (study-record path) | citation |
|---|---|---|
| {{rationale}} | study.investigational_plan.rationale | 21 CFR 312.23(a)(3)(iv)(a) |
| {{indication}} | study.indication | 21 CFR 312.23(a)(3)(iv)(b) |
| {{general_approach}} | study.investigational_plan.general_approach | 21 CFR 312.23(a)(3)(iv)(c) |
| {{planned_studies_next_year}} | study.investigational_plan.planned_studies[] | 21 CFR 312.23(a)(3)(iv)(d) |
| {{planned_study_title}} | study.investigational_plan.planned_studies[].title | 21 CFR 312.23(a)(3)(iv)(d) |
| {{planned_study_design}} | study.investigational_plan.planned_studies[].design | 21 CFR 312.23(a)(3)(iv)(d) |
| {{planned_start}} | study.investigational_plan.planned_studies[].planned_start | 21 CFR 312.23(a)(3)(iv)(d) |
| {{phase}} | study.phase | 21 CFR 312.23(a)(3)(iv)(d) |
| {{estimated_subjects}} | study.investigational_plan.planned_studies[].estimated_subjects | 21 CFR 312.23(a)(3)(iv)(d) |
| {{estimated_subjects_total}} | study.investigational_plan.estimated_subjects_total | 21 CFR 312.23(a)(3)(iv)(d) |
| {{anticipated_serious_risks}} | study.investigational_plan.anticipated_serious_risks | 21 CFR 312.23(a)(3)(iv)(e) |

## Related
- [[ind-application-312-23]]
- [[ind-introductory-statement]]
- [[investigators-brochure]]
- [[clinical-protocol-ich-m11-ceshharp]]
- [[ind-annual-report-312-33]]
- [[annual-reporting-and-amendments]]
- [[pre-ind-and-ind-preparation]]
