---
title: "Matching Engine: Multi-Directional Trial / Condition / Medication Matching"
section: "05-ossicro-system"
status: mixed
governing_authority:
  - "ClinicalTrials.gov API v2 (trial discovery, eligibility text, sites/contacts)"
  - "PubMed / NCBI E-utilities (supporting and safety evidence)"
  - "openFDA (drug labels, FAERS)"
  - "HIPAA Privacy Rule — 45 CFR 164.512(i)(1)(ii) (preparatory review; local-first, min-necessary, no PHI egress)"
  - "21 CFR 312.60 (eligibility determination is the investigator's non-delegable call)"
  - "FDA Draft Guidance — AI to Support Regulatory Decision-Making (2025-01-07, FDA-2024-D-4689)"
tags: [ossicro/matching, ossicro/engine, ossicro/gating, usc/hipaa, cfr/312, status/mixed]
aliases: ["Matching Engine", "Multi-Directional Matching", "Trial Matcher"]
updated: 2026-07-09
---

# Matching Engine: Multi-Directional Trial / Condition / Medication Matching

> [!authority] Governing authority
> Data sources: [ClinicalTrials.gov API v2](https://clinicaltrials.gov/data-api/api), [PubMed / NCBI E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/), [openFDA](https://open.fda.gov/apis/). Privacy floor: [45 CFR 164.512(i)(1)(ii)](https://www.ecfr.gov/current/title-45/section-164.512). Non-delegable floor: [21 CFR 312.60](https://www.ecfr.gov/current/title-21/section-312.60) (eligibility determination). AI-COU frame: [FDA-2024-D-4689](https://www.federalregister.gov/documents/2025/01/07/2024-31542/considerations-for-the-use-of-artificial-intelligence-to-support-regulatory-decision-making-for-drug) (draft). Status: **Mixed** — the data sources and the privacy/eligibility floors are confirmed; the retrieve→adjudicate architecture, the mechanism graph, and the recall-first design are interpretive positions, marked inline.

The matching engine is the mechanical core beneath [[patient-trial-matching]]. Where that page states *what matching is and where the privacy line sits*, this page specifies *how the engine discovers candidates and renders a cited, auditable rationale* across three directions of query. Every operation on this page runs inside the covered-entity boundary enforced by the [[privacy-state-machine]]; nothing here moves PHI, and nothing here determines eligibility.

## Three directions of matching

The native [ClinicalTrials.gov v2 API](https://clinicaltrials.gov/data-api/api) supports structured filters (condition, intervention, phase, status, location) but returns eligibility as **free text** and offers no synonym expansion and no biomarker-to-trial reasoning. OSSICRO's engine adds a semantic + mechanism-aware layer and supports matching from any of three entry vectors, resolving each onto the same candidate space.

1. **Patient profile → trials.** Given a de-identified clinical picture (diagnosis, phase-of-illness, prior lines, biomarker/variant profile, geography, key labs), return candidate trials and accessible investigational therapies, each with a per-criterion eligibility read. This is the classic "does a trial fit this patient?" direction and the primary path for the [[patient|Patient]] and [[hcp-physician|HCP]] entry points.
2. **Condition / diagnosis → trials & therapies.** Given a condition (with synonym and ontology expansion), return the landscape: open interventional trials by phase, plus marketed and investigational therapies for that indication drawn from [openFDA drug labels](https://open.fda.gov/apis/drug/label/). Supports the "what exists for this disease?" survey a clinician runs before a specific patient is in view.
3. **Medication / mechanism → trials, labels, evidence.** Given a drug or a molecular target/pathway, return trials of that agent or mechanism (including basket/umbrella trials that recruit by biomarker across stated conditions via the [[matching-mechanism-graph]]), its [openFDA label](https://open.fda.gov/apis/drug/label/) and [FAERS](https://open.fda.gov/apis/drug/event/) safety profile, and supporting [PubMed](https://www.ncbi.nlm.nih.gov/books/NBK25501/) evidence. Supports mechanism-first discovery — the case where the patient's actionable biomarker, not the histology, is the match key.

All three directions feed one candidate list with a uniform, cited rationale, so downstream triage ([[the-three-pathways-triage]]) and document generation ([[generate-check-validate-engine]]) consume a single shape regardless of how the query started.

## Retrieve → adjudicate (interpretive)

> [!interpretive] OSSICRO position
> Semantic-similarity ranking is necessary but **not sufficient**: ranking a trial highly is not the same as adjudicating a patient against its eligibility criteria, and a similarity score alone hits the free-text-eligibility recall/precision ceiling that separates "another keyword matcher" from useful matching. The engine therefore runs two stages: **retrieve** (broad, recall-first candidate generation via structured filters + semantic + mechanism expansion) then **adjudicate** (per-criterion evaluation of the patient against each candidate's parsed eligibility criteria). Adjudication is detailed in [[matching-eligibility-adjudication]]; independent prior art reimplemented includes Criteria2Query and EliIE (Weng, Columbia), OHDSI/OMOP, and CQL.

### Computable-eligibility parsing

Free-text inclusion/exclusion criteria are parsed into checkable predicates (concept + comparator + value + temporality), each retaining a pointer back to the exact source sentence in the registry record. A criterion that cannot be reduced to a computable predicate is **not discarded** — it is carried forward as a human-review item, because silently dropping a criterion is a silent exclusion risk.

### Three-valued per-criterion verdict

Each parsed criterion resolves to one of three states, never a bare boolean:

| Verdict | Meaning | Engine behavior |
|---------|---------|-----------------|
| **met** | Chart data satisfies the predicate | Cite chart datum + criterion; contribute to candidacy |
| **not-met** | Chart data contradicts the predicate | Cite the contradicting datum + criterion; flag, do not silently drop |
| **indeterminate-needs-data** | Data absent or ambiguous | Name the exact missing datum and the resolving question |

The candidate is presented with its verdict vector, not collapsed to a single score. An "indeterminate" is an invitation to gather data, not a denial. This is the mechanism that makes the [[completeness-ledger]]'s amber/red items concrete at the matching stage.

### Recall-first objective

> [!interpretive] OSSICRO position
> Because a false "not eligible" can **gate a patient's access to care**, the engine optimizes **recall first** (do not miss a candidate the patient could plausibly enter), accepting lower precision and pushing precision work onto the human review of a slightly larger candidate set. This objective is a design commitment, and it is a **measured** claim: the engine is evaluated on public benchmarks (CHIA, TREC Clinical Trials, n2c2) with recall and precision reported by trial phase in [[matching-evaluation-and-benchmarks]]. "Near-perfect matching" is only ever a benchmarked number, never marketing.

## Cited match rationale (provenance)

Every candidate carries a transparent rationale a human can audit: for each criterion, the verdict, the **chart citation** (which patient datum), and the **criterion citation** (which registry sentence). This is the same (source datum → provenance → citation) triple used across OSSICRO drafts ([[draft-provenance-model]]); for matching it is the difference between a defensible decision-support output and an opaque score. The rationale is written to the [[privacy-state-machine]] audit trail as part of the preparatory-review record.

## Privacy and non-delegable floors

> [!warning] Non-delegable
> The engine runs under [45 CFR 164.512(i)(1)(ii)](https://www.ecfr.gov/current/title-45/section-164.512): **local-first, minimum-necessary, no PHI egress, ephemeral audited reads**. No candidate list, and no criterion verdict, may leave the covered-entity boundary as PHI without a recorded [45 CFR 164.508](https://www.ecfr.gov/current/title-45/section-164.508) authorization or [45 CFR 164.512(i)(1)(i)](https://www.ecfr.gov/current/title-45/section-164.512) waiver. See [[hipaa-and-privacy-gating]].

> [!warning] Non-delegable
> **Eligibility determination is the investigator's judgment** ([21 CFR 312.60](https://www.ecfr.gov/current/title-21/section-312.60)). The engine surfaces candidates and adjudicates *criteria*; it does not adjudicate *enrollment*. A "met" vector is a recommendation to review, not an eligibility ruling, and the investigator may override any verdict with recorded reasoning.

## Interfaces

- **Upstream feeds:** [[data-integrations-ctgov-pubmed]] (CT.gov v2, PubMed E-utilities, openFDA) and, for chart data, [[smart-on-fhir-integration]] (US Core / mCODE / FHIR Genomics) behind the [[privacy-state-machine]].
- **Mechanism expansion:** [[matching-mechanism-graph]] (biomarker → pathway → target → trials).
- **Adjudication detail:** [[matching-eligibility-adjudication]].
- **Evaluation:** [[matching-evaluation-and-benchmarks]].
- **Downstream:** [[the-three-pathways-triage]] → Mode A/B/expanded access; candidate + rationale packaged for [[generate-check-validate-engine]] document auto-population and routed by the [[communication-hub]] after gating.

## Related
- [[patient-trial-matching]]
- [[matching-eligibility-adjudication]]
- [[matching-mechanism-graph]]
- [[matching-evaluation-and-benchmarks]]
- [[data-integrations-ctgov-pubmed]]
- [[smart-on-fhir-integration]]
- [[privacy-state-machine]]
- [[draft-provenance-model]]
- [[completeness-ledger]]
- [[the-three-pathways-triage]]
- [[communication-hub]]

## Sources
- [ClinicalTrials.gov API v2 documentation](https://clinicaltrials.gov/data-api/api)
- [NCBI E-utilities (Entrez Programming Utilities) — reference](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
- [openFDA APIs — drug labels and FAERS](https://open.fda.gov/apis/)
- [45 CFR 164.512 — preparatory-to-research and waiver (eCFR)](https://www.ecfr.gov/current/title-45/section-164.512)
- [21 CFR 312.60 — General responsibilities of investigators (eCFR)](https://www.ecfr.gov/current/title-21/section-312.60)
- [FDA Draft Guidance — AI to Support Regulatory Decision-Making (Federal Register, 2025-01-07)](https://www.federalregister.gov/documents/2025/01/07/2024-31542/considerations-for-the-use-of-artificial-intelligence-to-support-regulatory-decision-making-for-drug)
- Criteria2Query: Yuan C, et al. *J Am Med Inform Assoc.* 2019;26(4):294–305. [DOI:10.1093/jamia/ocy178](https://doi.org/10.1093/jamia/ocy178)
- EliIE (eligibility criteria information extraction): Kang T, et al. *J Am Med Inform Assoc.* 2017;24(6):1062–1071. [DOI:10.1093/jamia/ocx019](https://doi.org/10.1093/jamia/ocx019)
