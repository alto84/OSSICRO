---
title: "Protocol Synopsis"
doc_id: "protocol-synopsis"
category: "protocol"
governing_citations: ["ICH M11"]
owner: "sponsor-investigator"
receiver: "sponsor"
gate: "none"
status: template
updated: 2026-07-09
---

# Protocol Synopsis — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [ICH M11 — Clinical electronic Structured Harmonised Protocol (CeSHarP)](https://www.ich.org/page/multidisciplinary-guidelines), §1.1 (Protocol Synopsis) and the M11 Technical Specification. The synopsis is a defined component of the harmonised protocol; it is not a stand-alone regulatory submission. This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** The synopsis is a concise, self-contained summary of the trial's objectives, design, population, intervention, and statistical plan. It is the front-matter of the full clinical protocol ([[03-documents/clinical-protocol-ich-m11-ceshharp]], Section 1.1) and is frequently circulated on its own for site feasibility, IRB triage, DSMB familiarization, and internal sponsor review. It must remain consistent with the full protocol body, which controls in any conflict.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing. Keep the synopsis to a summary length (typically 3–6 pages); do not introduce any objective, endpoint, or eligibility criterion that is not identical to the full protocol. If a field is not applicable, state "Not applicable" with a brief reason rather than deleting it (M11 convention).

## Template

### PROTOCOL SYNOPSIS

| | |
|---|---|
| **Full Title** | {{title}} |
| **Protocol Number** | {{protocol_number}} |
| **Protocol Version / Date** | {{protocol_version}} / {{protocol_date}} |
| **Investigational Product** | {{drug_name}} |
| **IND Number** | {{ind_number}} |
| **Sponsor-Investigator** | {{sponsor_investigator_name}} |
| **Trial Phase** | {{phase}} |
| **Registry Identifier** | {{nct_number}} [INSTRUCTION: "Pending" until issued.] |

#### 1. Rationale and Background
{{background_rationale}}
[INSTRUCTION: 2–4 sentences: disease, unmet need, and the scientific basis for studying the IP. Summarize; the full protocol Section 2 and the Investigator's Brochure carry the detail.]

#### 2. Objectives and Endpoints

| Type | Objective | Endpoint |
|---|---|---|
| Primary | {{primary_objective}} | {{primary_endpoint}} |
| Secondary | {{secondary_objective}} | {{secondary_endpoint}} |
| Exploratory | {{exploratory_objective}} | {{exploratory_endpoint}} [INSTRUCTION: or "Not applicable."] |

[INSTRUCTION: These must match the full protocol Section 3 verbatim. For a confirmatory primary objective, note the estimand in the design section below.]

#### 3. Trial Design
{{design}}
[INSTRUCTION: One paragraph stating: design type (e.g., open-label / randomized / double-blind / placebo-controlled / dose-escalation), number of arms and allocation ratio, control type, duration of participation per subject, and total planned trial duration. State the estimand strategy at a high level for confirmatory trials.]

**Trial schema:** {{trial_schema_summary}} [INSTRUCTION: brief textual or diagrammatic summary of periods — screening, treatment, follow-up.]

#### 4. Trial Population
{{population}}

- **Planned sample size:** {{planned_enrollment}} participants at {{number_of_sites}} site(s).
- **Key inclusion criteria:** {{key_inclusion_criteria}} [INSTRUCTION: the 3–5 most decisive criteria, not the full list.]
- **Key exclusion criteria:** {{key_exclusion_criteria}}

#### 5. Investigational Product, Dose, and Route
{{intervention_summary}}
[INSTRUCTION: IP name, dose/regimen, route, and comparator (if any). State the maximum planned dose and duration of exposure. This must be consistent with full protocol Section 6.]

#### 6. Safety Assessments and Monitoring
{{safety_summary}}
[INSTRUCTION: Summarize the safety monitoring approach and the principal AE/SAE handling. AEs and SAEs are defined and reported per 21 CFR 312.32; the investigator reports SAEs to the sponsor-investigator per 21 CFR 312.64(b). Reference any DSMB/safety review committee and stopping rules.]

#### 7. Statistical Considerations
{{statistical_summary}}
[INSTRUCTION: Sample-size basis (formal power or practical basis for Phase 1), analysis populations, and the primary analysis method. The full Statistical Analysis Plan ([[03-documents/statistical-analysis-plan-ich-e9]]) elaborates and may not contradict this.]

#### 8. Trial Duration and Milestones
{{duration_milestones}} [INSTRUCTION: e.g., estimated enrollment period, per-subject duration, and end-of-trial definition.]

---

[INSTRUCTION: The synopsis inherits the confidentiality status of the full protocol and is not separately signed; approval attaches to the parent protocol's signature page. Do not circulate externally without the confidentiality statement of the parent protocol.]

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{title}} | study.protocol.title | ICH M11 §1.1 |
| {{protocol_number}} | study.protocol.number | ICH M11 §1.1 |
| {{protocol_version}} | study.protocol.version | ICH M11 §1.1 |
| {{protocol_date}} | study.protocol.date | ICH M11 §1.1 |
| {{drug_name}} | study.ip.name | ICH M11 §1.1 |
| {{ind_number}} | study.ind.number | ICH M11 §1.1 |
| {{sponsor_investigator_name}} | study.sponsor_investigator.name | ICH M11 §1.1 |
| {{phase}} | study.phase | ICH M11 §1.1 |
| {{nct_number}} | study.registration.nct_number | ICH M11 §1.1 |
| {{background_rationale}} | study.protocol.introduction.rationale | ICH M11 §2.1 |
| {{primary_objective}} | study.protocol.objectives.primary.objective | ICH M11 §3.1 |
| {{primary_endpoint}} | study.protocol.objectives.primary.endpoint | ICH M11 §3.1 |
| {{secondary_objective}} | study.protocol.objectives.secondary[].objective | ICH M11 §3.2 |
| {{secondary_endpoint}} | study.protocol.objectives.secondary[].endpoint | ICH M11 §3.2 |
| {{exploratory_objective}} | study.protocol.objectives.exploratory[].objective | ICH M11 §3.3 |
| {{exploratory_endpoint}} | study.protocol.objectives.exploratory[].endpoint | ICH M11 §3.3 |
| {{design}} | study.protocol.design.description | ICH M11 §4.1 |
| {{trial_schema_summary}} | study.protocol.schema | ICH M11 §1.2 |
| {{population}} | study.protocol.population.summary | ICH M11 §5 |
| {{planned_enrollment}} | study.protocol.population.planned_enrollment | ICH M11 §5 |
| {{number_of_sites}} | study.sites.count | ICH M11 §5 |
| {{key_inclusion_criteria}} | study.protocol.population.inclusion[] | ICH M11 §5.1 |
| {{key_exclusion_criteria}} | study.protocol.population.exclusion[] | ICH M11 §5.2 |
| {{intervention_summary}} | study.protocol.intervention.summary | ICH M11 §6 |
| {{safety_summary}} | study.protocol.assessments.safety_summary | ICH M11 §8.2 |
| {{statistical_summary}} | study.protocol.statistics.summary | ICH M11 §9; ICH E9 |
| {{duration_milestones}} | study.protocol.design.milestones | ICH M11 §4.4 |

## Related

- [[03-documents/protocol-synopsis]]
- [[03-documents/clinical-protocol-ich-m11-ceshharp]]
- [[03-documents/statistical-analysis-plan-ich-e9]]
- [[03-documents/site-feasibility-questionnaire]]
- [[02-lifecycle/pre-ind-and-ind-preparation]]
- [[02-lifecycle/feasibility-and-patient-matching]]
