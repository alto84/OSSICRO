---
title: "Mechanism-Aware Candidate Expansion (biomarker → pathway → target → trials)"
section: "05-ossicro-system"
status: mixed
governing_authority:
  - "45 CFR 164.512(i)(1)(ii) (review preparatory to research)"
  - "21 CFR 312.60 (investigator responsibilities)"
  - "FDA Draft Guidance on AI to Support Regulatory Decision-Making (Jan 2025, FDA-2024-D-4689)"
tags: [ossicro/matching, ossicro/ai-credibility, cfr/312, lifecycle/feasibility, status/interpretive]
aliases: ["Mechanism Graph", "Biomarker Expansion", "Mechanism-Aware Matching"]
updated: 2026-07-09
---

# Mechanism-Aware Candidate Expansion (biomarker → pathway → target → trials)

> [!authority] Governing authority
> Mechanism-aware expansion is a **retrieval-stage** function of [[matching-eligibility-adjudication]], operating on the [45 CFR 164.512(i)(1)(ii)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.512) preparatory-review basis. It surfaces *candidate* trials for adjudication and clinician review; it makes no therapeutic recommendation and no eligibility determination ([21 CFR 312.60](https://www.law.cornell.edu/cfr/text/21/312.60)). Status: **Mixed** — the biological knowledge sources and the trial designs (basket/umbrella) are established; the graph-expansion architecture and its use in matching are interpretive OSSICRO positions.

A patient described by their **stated condition** ("metastatic colorectal cancer") is invisible to a trial indexed by its **molecular target** ("BRAF V600E–mutant solid tumors") when matching keys on condition strings alone. The clinically relevant fact — a shared actionable mechanism — is exactly what a string match misses. Mechanism-aware expansion closes that gap: it walks a knowledge graph from the patient's **biomarker or variant**, to the **pathway** it perturbs, to the **druggable target**, to **trials** recruiting against that target or mechanism, so mutation-matched **basket** (one mechanism, many histologies) and **umbrella** (one histology, many mechanisms) trials surface across the patient's stated condition boundary. The output feeds the recall-first retrieval net; every expanded candidate is still adjudicated criterion-by-criterion and read by the clinician.

## The expansion graph

The graph is a typed, cited knowledge structure. Each edge carries its source so the resulting **match rationale is auditable** and the clinician can inspect why a trial surfaced ([[draft-provenance-model]]).

```
biomarker / variant  →  gene / protein  →  pathway  →  drug target / MoA  →  trial
   (e.g., BRAF V600E)    (BRAF, MAPK)      (RAS/RAF/    (BRAF inhibitor,     (NCT… basket
                                            MEK/ERK)     class effect)         trial)
```

- **biomarker / variant → gene / protein.** Normalize the patient's molecular finding to a canonical gene/variant using [HGNC](https://www.genenames.org/) nomenclature and variant standards (HGVS); ingest via [[smart-on-fhir-integration]] FHIR Genomics + [mCODE](https://hl7.org/fhir/us/mcode/) so the finding is structured, not free text.
- **gene → pathway.** Map to canonical pathways ([Reactome](https://reactome.org/), KEGG) to reach *mechanistically adjacent* targets — a downstream node in the same pathway can be the actionable one even when the patient's own variant is not directly druggable.
- **variant / gene → clinical actionability.** Grade the variant's therapeutic relevance against curated oncology knowledge bases — [OncoKB](https://www.oncokb.org/) (FDA-recognized precision-oncology levels of evidence) and [CIViC](https://civicdb.org/) (open, community-curated clinical interpretations) — so expansion is anchored to evidence tiers, not mere biological plausibility.
- **target → drug / mechanism.** Resolve targets to drug classes and mechanisms of action via [Open Targets](https://www.opentargets.org/), [DrugBank](https://go.drugbank.com/), and [ChEMBL](https://www.ebi.ac.uk/chembl/); pharmacogenomic relationships via [PharmGKB](https://www.pharmgkb.org/).
- **mechanism → trials.** Query the [[data-integrations-ctgov-pubmed|ClinicalTrials.gov v2 API]] for trials whose eligibility is keyed on the biomarker, gene, or drug class rather than the histology, and pull supporting evidence from PubMed ([[data-integrations-ctgov-pubmed]]).

## Why basket and umbrella trials are the target

Mechanism-agnostic matching structurally under-serves exactly the modern trial designs that a mechanism graph is built to find:

- **Basket trials** enroll multiple tumor histologies sharing one molecular alteration (the design behind [NCI-MATCH / EAY131](https://www.cancer.gov/about-cancer/treatment/clinical-trials/nci-supported/nci-match) and [ASCO TAPUR](https://www.tapur.org/)). A colorectal patient with a *BRAF* V600E variant belongs in a *BRAF*-mutant basket that is not indexed under "colorectal."
- **Umbrella trials** enroll one histology and route sub-arms by mechanism; the patient's variant determines the arm, so matching must reason about the variant, not just the histology.

These are precisely the early-phase, precision-medicine programs OSSICRO's guiding scenario is about — a clinician with a patient and a candidate mechanism-matched therapy. Surfacing them is the recall win that a condition-string matcher cannot deliver.

## Provenance and the recall-first discipline

Every expansion edge is retained as provenance, so a surfaced trial arrives with its reasoning chain: *variant X (OncoKB level Y) → pathway P → target T → this trial's inclusion criterion*. Two disciplines govern it:

1. **Expansion widens; it never decides.** A mechanistic link is a *hypothesis worth a clinician's look*, surfaced for adjudication — not a conclusion that the drug will work or that the patient is eligible. The strength of the biological link (e.g., direct target vs. downstream-pathway inference vs. class effect) is labeled so the clinician can weight it.
2. **Recall-first, then adjudicate.** Expansion deliberately over-generates candidates; the criterion-level three-valued adjudication in [[matching-eligibility-adjudication]] and the clinician's review are what narrow the set. A weak-but-plausible mechanistic link surfaces as a low-confidence candidate rather than being silently dropped — consistent with the safety asymmetry (a false exclusion costs a patient an option).

> [!interpretive] OSSICRO position
> Using a mechanism graph for *candidate expansion* is defensible under the low-to-moderate-influence framing only because expansion is bounded by two downstream human-controlled stages: per-criterion adjudication and investigator review. The graph never asserts a treatment is indicated; it asserts a trial is *worth adjudicating*. This keeps mechanism expansion inside the retrieval COU rather than turning it into a molecular-tumor-board recommendation — a line OSSICRO does not cross. Flagged interpretive; the biological knowledge bases are curated third-party evidence sources, and their evidence grades (e.g., OncoKB levels) are surfaced, not overridden.

## The non-delegable boundary

> [!warning] Non-delegable
> Interpreting a genomic result for therapeutic action is **the practice of medicine** — the molecular-tumor-board / treating-physician judgment, informed where appropriate by qualified genomic expertise. OSSICRO surfaces mechanism-matched trial *candidates* with cited evidence links; it does not recommend a therapy, does not assert the variant is actionable in this patient, and does not determine eligibility ([21 CFR 312.60](https://www.law.cornell.edu/cfr/text/21/312.60)). The clinician evaluates the mechanistic rationale and owns every clinical conclusion drawn from it. Enrollment remains gated on consent and IRB approval; matching stays on the preparatory-review side of the [[privacy-state-machine]].

## Interface to the rest of the system

- Feeds the **retrieve** stage of [[matching-eligibility-adjudication]]; expanded candidates enter the same three-valued adjudication as condition-matched candidates.
- Expansion recall and false-exclusion behavior are measured in [[matching-evaluation-and-benchmarks]] (mechanism-matched recall is reported separately, since it is where a naive matcher fails hardest).
- Structured molecular inputs arrive via [[smart-on-fhir-integration]] (FHIR Genomics + mCODE), under [[hipaa-and-privacy-gating]].

## Related

- [[matching-eligibility-adjudication]]
- [[matching-evaluation-and-benchmarks]]
- [[matching-engine]]
- [[patient-trial-matching]]
- [[smart-on-fhir-integration]]
- [[data-integrations-ctgov-pubmed]]
- [[draft-provenance-model]]
- [[privacy-state-machine]]
- [[hipaa-and-privacy-gating]]
- [[non-delegable-functions-and-gates]]

## Sources

- [ClinicalTrials.gov API v2](https://clinicaltrials.gov/data-api/api)
- [OncoKB — Precision Oncology Knowledge Base (FDA-recognized)](https://www.oncokb.org/)
- [CIViC — Clinical Interpretation of Variants in Cancer](https://civicdb.org/)
- [Open Targets Platform](https://www.opentargets.org/)
- [Reactome Pathway Knowledgebase](https://reactome.org/)
- [PharmGKB](https://www.pharmgkb.org/)
- [DrugBank](https://go.drugbank.com/) · [ChEMBL](https://www.ebi.ac.uk/chembl/)
- [HL7 FHIR — mCODE (minimal Common Oncology Data Elements) Implementation Guide](https://hl7.org/fhir/us/mcode/)
- [NCI-MATCH (EAY131) — molecularly targeted basket trial](https://www.cancer.gov/about-cancer/treatment/clinical-trials/nci-supported/nci-match)
- [ASCO TAPUR Study](https://www.tapur.org/)
- [21 CFR 312.60 — General responsibilities of investigators](https://www.law.cornell.edu/cfr/text/21/312.60)
- [45 CFR 164.512(i) — Review preparatory to research](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.512)
