---
title: "Matching Evaluation and Benchmarks (recall/precision by phase)"
section: "05-ossicro-system"
status: mixed
governing_authority:
  - "FDA Draft Guidance on AI to Support Regulatory Decision-Making (Jan 2025, FDA-2024-D-4689)"
  - "21 CFR 312.60 (investigator responsibilities; eligibility determination)"
  - "45 CFR 164.512(i)(1)(ii) (review preparatory to research)"
tags: [ossicro/matching, ossicro/ai-credibility, ossicro/engine, cfr/312, status/interpretive]
aliases: ["Matching Eval Harness", "Matching Benchmarks", "Near-Perfect as a Measured Claim"]
updated: 2026-07-09
---

# Matching Evaluation and Benchmarks (recall/precision by phase)

> [!authority] Governing authority
> This page makes "near-perfect matching" a **measured** claim rather than a marketing one, and classifies matching's **context of use (COU)** under the FDA Draft Guidance on AI to support regulatory decision-making (Jan 2025, [FDA-2024-D-4689](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-use-artificial-intelligence-support-regulatory-decision-making-drug-and-biological); **still draft**). No benchmark score licenses OSSICRO to make the eligibility determination — that remains the investigator's non-delegable call ([21 CFR 312.60](https://www.law.cornell.edu/cfr/text/21/312.60)). Status: **Mixed** — the public benchmarks and metric definitions are established; the two-phase evaluation design, the COU classification, and the acceptance criteria are interpretive OSSICRO positions.

Matching that can return "no eligible trial" and thereby gate a patient's access is a **higher-influence context of use** than drafting a document for human review. A higher-influence COU obligates a measured, pre-registered evaluation — the system's quality must be a number with a denominator, evaluated on held-out public data, reported by phase, and honest about its failure modes. This page defines the harness: the benchmarks, the metrics, the by-phase reporting, the recall-first objective, and the acceptance criteria that "near-perfect" has to actually clear.

## Two phases, evaluated separately

Matching decomposes into **retrieve** then **adjudicate** ([[matching-eligibility-adjudication]]); each phase has a different job and therefore a different metric profile. Collapsing them into one end-to-end accuracy number hides exactly the errors that matter.

| Phase | Question it answers | Primary metric | Objective |
|---|---|---|---|
| **Retrieve** | Did the relevant trial appear in the candidate set at all? | **Recall@k**, false-exclusion rate | Maximize recall; a missed eligible trial is unrecoverable downstream |
| **Adjudicate** | For each criterion, is the met / not-met / indeterminate verdict correct? | Per-criterion accuracy; precision on *not-met*; indeterminate rate | Precise *not-met* (the only value that excludes); never mislabel unknown as not-met |

The decomposition means a retrieval miss and an adjudication miss are counted, attributed, and tuned independently — and the safety-critical error (a real option the patient never sees) is measured directly rather than buried in an aggregate.

## Benchmarks — held-out public data

OSSICRO evaluates on established, publicly documented benchmarks so results are comparable to the literature and not self-graded:

- **CHIA** — a large annotated corpus of clinical-trial eligibility criteria; the reference dataset for **criterion parsing / computable-eligibility extraction** (entities, relations, negation, temporality). [Kury et al., Sci Data 2020;7:281](https://doi.org/10.1038/s41597-020-00620-0).
- **n2c2 2018 Track 1 — Cohort Selection for Clinical Trials** — patient longitudinal records labeled met/not-met against 13 selection criteria; the reference task for **patient-against-criteria adjudication**, directly analogous to OSSICRO's per-criterion verdict. [Stubbs et al., JAMIA 2019;26(11):1163–1171](https://doi.org/10.1093/jamia/ocz163) · [PMID 31562516](https://pubmed.ncbi.nlm.nih.gov/31562516/).
- **TREC Clinical Trials Track (2021–2022)** — topics are synthetic patient case descriptions; the task is ranking trials by eligibility; the reference benchmark for the **retrieval / ranking** phase, scored with `NDCG@10`, `P@10`, and recall. [TREC-CT overview](https://www.trec-cds.org/).

Parser-level performance is graded on CHIA, adjudication on n2c2 2018, and retrieval/ranking on TREC-CT, each on its own held-out split. This keeps the evaluation honest — no phase is graded on the data it was tuned on.

## Metrics — and why recall leads

- **Recall (sensitivity)** — the fraction of truly relevant/eligible trials the system surfaces. **The lead metric.** In matching-for-access, a false negative is a patient who never learns an option existed; it is silent and unrecoverable. Recall is reported at the retrieval phase (Recall@k) and, at the criterion level, as the **false-exclusion rate**: how often a truly *met/indeterminate* criterion was wrongly called *not-met*.
- **Precision** — the fraction of surfaced candidates that are genuinely relevant. Precision protects **clinician attention**, not patient access; a precision miss costs seconds of review, so it is the *secondary* objective, deliberately traded for recall at the retrieval stage.
- **Per-criterion accuracy (three-valued)** — accuracy over the {met, not-met, indeterminate} labels, reported as a full confusion matrix, not a single number. The **indeterminate → not-met cell is a distinguished, tracked error** — it is the failure the three-valued contract exists to prevent, and it is reported explicitly.
- **Indeterminate rate** — the fraction of criteria the system routes back to the clinician as "needs data." Not an error; a calibrated indeterminate rate is *correct behavior* (the alternative is guessing). It is reported so reviewer workload is visible and so a rising rate signals a data-ingestion gap ([[smart-on-fhir-integration]]).
- **Ranking quality** — `NDCG@k` and `P@k` for the retrieval ordering (TREC-CT convention).

> [!interpretive] OSSICRO position
> **"Near-perfect" is defined operationally, not rhetorically.** The acceptance target is *near-perfect recall with an honest indeterminate rate* — i.e., the system almost never silently excludes an eligible trial, and when it cannot decide it says so. High precision is desirable but explicitly subordinate: OSSICRO would rather show a clinician three extra candidates to dismiss than hide one real option. A precision-optimized matcher that quietly drops borderline-eligible trials is the failure mode this metric hierarchy is designed to forbid. Concrete pre-registered gates (illustrative, to be fixed before any access-affecting deployment): retrieval Recall@k ≥ a high threshold with the false-exclusion rate the *binding* acceptance metric; on n2c2-style adjudication, the indeterminate→not-met misclassification rate held to near-zero. These thresholds are set and version-controlled with the [[regulatory-change-log]] discipline, and a release that regresses on false-exclusion does not ship regardless of aggregate accuracy.

## COU classification and its consequences

Under the FDA draft AI-credibility framework (a 7-step assessment scaled to model influence × decision consequence), OSSICRO classifies matching *above* document drafting:

- **Document drafting** — low influence, low consequence: the model proposes, a named human reviews and signs every span ([[generate-check-validate-engine]], [[part-11-and-ai-credibility]]).
- **Matching** — **higher influence**: a candidate list that omits a trial can, in practice, gate access before any human sees the omission. The higher COU is *why* matching gets this dedicated measured harness, recall-first tuning, the three-valued contract, and pre-registered acceptance gates — a heavier credibility burden that drafting does not carry.

This is the honest concession made in the strategy review: matching cannot be waved through on the same low-COU argument as drafting. It earns its credibility by measurement.

## The non-delegable boundary

> [!warning] Non-delegable
> **Benchmark performance never substitutes for the investigator's eligibility determination** ([21 CFR 312.60](https://www.law.cornell.edu/cfr/text/21/312.60)). A 0.99 recall does not make the system's output an enrollment clearance; it makes the *candidate list* more trustworthy as decision support that a qualified clinician still adjudicates and owns. Evaluation quantifies how good the draft is; it does not move the gate. Enrollment remains gated on the clinician's judgment, the informed-consent event ([[informed-consent-document-vs-event]]), and IRB approval, with the HIPAA transition off the preparatory-review basis ([[privacy-state-machine]]).

## Evaluation as living infrastructure

The harness is not a one-time validation. It runs as a regression suite: every change to the parser, the retrieval layer, the [[matching-mechanism-graph]], or the criterion library is re-scored on all three benchmarks before release, and a regression on the binding false-exclusion metric blocks the release. Benchmark versions, splits, metric definitions, and acceptance thresholds are tracked under the [[regulatory-change-log]] and surfaced in [[compliance-mapping]] so the quality claim is auditable over time. Consistent with the open-source thesis, OSSICRO intends to publish its computable-eligibility parses as an open dataset ([[matching-eligibility-adjudication]]) — a network-effect asset and an external check on its own numbers.

## Related

- [[matching-eligibility-adjudication]]
- [[matching-mechanism-graph]]
- [[matching-engine]]
- [[patient-trial-matching]]
- [[generate-check-validate-engine]]
- [[part-11-and-ai-credibility]]
- [[smart-on-fhir-integration]]
- [[compliance-mapping]]
- [[regulatory-change-log]]
- [[completeness-ledger]]
- [[non-delegable-functions-and-gates]]

## Sources

- Kury F, Butler A, Yuan C, et al. "Chia, a large annotated corpus of clinical trial eligibility criteria." Sci Data 2020;7:281. [DOI 10.1038/s41597-020-00620-0](https://doi.org/10.1038/s41597-020-00620-0)
- Stubbs A, Filannino M, Soysal E, Henry S, Uzuner Ö. "Cohort selection for clinical trials: n2c2 2018 shared task Track 1." JAMIA 2019;26(11):1163–1171. [DOI 10.1093/jamia/ocz163](https://doi.org/10.1093/jamia/ocz163) · [PMID 31562516](https://pubmed.ncbi.nlm.nih.gov/31562516/)
- [TREC Clinical Trials Track — overview and qrels](https://www.trec-cds.org/)
- Yuan C, Ryan PB, Ta C, et al. "Criteria2Query." JAMIA 2019;26(4):294–305. [DOI 10.1093/jamia/ocy178](https://doi.org/10.1093/jamia/ocy178)
- Kang T, et al. "EliIE." JAMIA 2017;24(6):1062–1071. [DOI 10.1093/jamia/ocx019](https://doi.org/10.1093/jamia/ocx019)
- [FDA Draft Guidance — Considerations for the Use of AI to Support Regulatory Decision-Making (Jan 2025, FDA-2024-D-4689)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-use-artificial-intelligence-support-regulatory-decision-making-drug-and-biological)
- [21 CFR 312.60 — General responsibilities of investigators](https://www.law.cornell.edu/cfr/text/21/312.60)
- [45 CFR 164.512(i) — Review preparatory to research](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.512)
