---
title: "Matching as Eligibility Adjudication (retrieve → adjudicate)"
section: "05-ossicro-system"
status: mixed
governing_authority:
  - "45 CFR 164.512(i)(1)(ii) (review preparatory to research)"
  - "45 CFR 164.502(b) (minimum necessary)"
  - "21 CFR 312.60 (investigator responsibilities; protocol adherence)"
  - "21 CFR 50.20, 50.25 (informed consent)"
  - "FDA Draft Guidance on AI to Support Regulatory Decision-Making (Jan 2025, FDA-2024-D-4689)"
tags: [ossicro/matching, ossicro/gating, ossicro/ai-credibility, cfr/312, cfr/50, lifecycle/feasibility, status/interpretive]
aliases: ["Eligibility Adjudication", "Retrieve-Adjudicate Matching", "Three-Valued Matching"]
updated: 2026-07-09
---

# Matching as Eligibility Adjudication (retrieve → adjudicate)

> [!authority] Governing authority
> Matching operates under the HIPAA [45 CFR 164.512(i)(1)(ii)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.512#p-164.512(i)(1)(ii)) "review preparatory to research" basis (no PHI egress; see [[privacy-state-machine]], [[hipaa-and-privacy-gating]]), with chart reads bounded by the minimum-necessary standard ([45 CFR 164.502(b)](https://www.law.cornell.edu/cfr/text/45/164.502)). The output is a candidate list with per-criterion rationale — never an enrollment decision. The eligibility determination is reserved to the investigator under [21 CFR 312.60](https://www.law.cornell.edu/cfr/text/21/312.60), and enrollment is gated on consent ([21 CFR 50.20](https://www.law.cornell.edu/cfr/text/21/50.20)) and IRB approval. Status: **Mixed** — the regulatory boundaries and the published informatics prior art are confirmed; the retrieve→adjudicate architecture and the three-valued verdict contract are interpretive OSSICRO positions.

Semantic similarity ranks trials; it does not adjudicate whether *this patient* meets *this criterion*. That gap is the difference between "another keyword matcher" and matching a clinician can act on. OSSICRO splits matching into two mechanically distinct stages — **retrieve** (cast a wide, recall-first net over the trial space) then **adjudicate** (evaluate each eligibility criterion against structured patient data and emit a per-criterion verdict) — and refuses to collapse them. The adjudication stage produces a **three-valued verdict per criterion** with citations on both sides: to the patient datum that satisfied or failed it, and to the exact criterion text in the trial record. The investigator reads the adjudication and makes the call; the machine never returns a bare "eligible / ineligible."

## Why two stages, and why in this order

A single-stage ranker optimizes a similarity score and surfaces the top-k. Two failure modes follow. First, a genuinely eligible trial whose eligibility prose is worded unusually ranks low and never surfaces — a **false exclusion**, which in this domain means a patient silently loses access. Second, a high-ranking trial the patient plainly fails (wrong line of therapy, an excluded comorbidity) still appears, wasting the scarcest resource in the loop — clinician attention. Separating retrieval from adjudication lets each stage be tuned for its own objective and evaluated independently ([[matching-evaluation-and-benchmarks]]).

- **Retrieve — recall-first.** The retrieval stage is deliberately over-inclusive. It queries the [[data-integrations-ctgov-pubmed|ClinicalTrials.gov v2 API]] on structured facets (condition, phase, recruitment status, geography, age/sex) and a semantic layer over the free-text summary, and it expands the candidate set through the [[matching-mechanism-graph]] so that mechanism-matched basket/umbrella trials surface even when the patient's stated condition is not the trial's indexed condition. Retrieval tuning targets **high recall at the cost of precision** — it is cheaper to adjudicate a false positive away than to never see a true positive.
- **Adjudicate — per-criterion, three-valued.** Each candidate's inclusion and exclusion criteria are parsed into computable predicates and evaluated against the patient's structured chart data ([[smart-on-fhir-integration]], mapped to OMOP/US Core/mCODE). Each criterion resolves to one of three values, and the trial-level result is a *ledger of criteria*, not a single verdict.

### Retrieval is inside the recall contract

The three-valued protection at adjudication is worthless if a trial is silently dropped one stage earlier: a candidate excluded by a retrieval filter never reaches adjudication, generates no ledger entry, and routes no question to the clinician — the exact "patient silently loses access" failure this page exists to prevent. The recall-first commitment therefore binds retrieval, not only adjudication, through three rules:

1. **Facet discipline — hard filters only on non-judgment facts.** A retrieval facet may hard-exclude a trial only when the underlying datum is neither a patient preference nor a chart-derived value that may be stale at a future enrollment date. In practice that limits hard exclusion to trial-side facts such as a completed/terminated/withdrawn recruitment status. **Geography is a soft facet**: distance ranks a candidate down, it never drops it — willingness to travel is the patient's decision, not a database predicate. **Age and sex are soft at the boundary**: age is evaluated against the projected enrollment window, and boundary cases (including chart data that may be stale) rank down and pass to adjudication as indeterminate rather than being filtered. Condition facets are protected against narrow indexing by the [[matching-mechanism-graph]] expansion.
2. **Retrieval-coverage transparency.** The clinician-facing output carries a coverage line stating what retrieval suppressed and why — e.g., "N trials matched the condition/mechanism facets but were rank-suppressed by geography (nearest site > X km)" — so a retrieval-stage exclusion is visible and reversible by a human, never silent.
3. **A minimum recall floor as a release gate.** OSSICRO commits, as a contract of this page and not merely a property of the eval harness, that the retrieval stage must meet a pre-registered minimum recall floor on the reference benchmark set of known patient–trial pairs before any matching release ships. The floor's current value and measurement protocol are maintained in [[matching-evaluation-and-benchmarks]]; a release that regresses below the floor does not ship.

## The three-valued verdict

Binary eligibility logic forces a premature commitment: an unknown datum must be guessed as either met or not-met, and either guess can silently exclude a patient. OSSICRO uses three values, matching the epistemic reality of an incomplete chart.

| Verdict | Meaning | Machine behavior | Who resolves |
|---|---|---|---|
| **met** | The criterion is satisfied by cited patient data | Show the satisfying datum + criterion citation | Investigator confirms |
| **not-met** | The criterion is contradicted by cited patient data | Show the contradicting datum + criterion citation | Investigator confirms |
| **indeterminate — needs data** | The datum required to evaluate the criterion is absent, ambiguous, or not computable from structured fields | Emit the **exact resolving question** (e.g., "ECOG performance status not in chart — required by inclusion #4") | Investigator supplies datum or judges |

The load-bearing rule: **indeterminate is never silently coerced to not-met.** A trial is excluded from a patient's candidate view only on an explicit, cited **not-met**; indeterminate criteria keep the trial visible and route a specific question to the clinician. This is the recall-first principle made concrete at the criterion level — the system's default when it does not know is to *ask*, not to reject. The same principle applied at the retrieval stage is the facet discipline above: no silent drop on a preference-laden or staleness-prone facet.

> [!interpretive] OSSICRO position
> The three-valued contract, the soft-facet retrieval discipline, and the recall-floor release gate are interpretive design choices, defended on two grounds. (1) **Safety asymmetry:** in a matching-for-access setting, a false exclusion (a real option a patient never learns about) is a worse error than a false inclusion (a candidate the clinician dismisses in seconds). Recall-first tuning, the no-silent-not-met rule, and the no-silent-drop retrieval rule encode that asymmetry end-to-end. (2) **COU honesty:** matching that can gate access is a *higher-influence* context of use than document drafting (see [[matching-evaluation-and-benchmarks]] and [[part-11-and-ai-credibility]]); a system in a higher-influence COU must expose its uncertainty rather than launder it into a confident binary.

## Computable eligibility — parsing criteria into predicates

Free-text eligibility criteria are converted into structured, checkable predicates. OSSICRO reimplements, independently, a well-published pattern from clinical-research informatics rather than inventing one:

- **EliIE** (Weng lab, Columbia) — an open information-extraction pipeline that parses eligibility criteria into structured entities, attributes, and relations ([Kang et al., JAMIA 2017;24(6):1062–1071](https://doi.org/10.1093/jamia/ocx019), [PMID 28379377](https://pubmed.ncbi.nlm.nih.gov/28379377/)).
- **Criteria2Query** — turns free-text criteria into executable cohort queries against a structured (OMOP) database, the closest published analogue to OSSICRO's parse-then-evaluate flow ([Yuan et al., JAMIA 2019;26(4):294–305](https://doi.org/10.1093/jamia/ocy178), [PMID 30753493](https://pubmed.ncbi.nlm.nih.gov/30753493/)).
- **OHDSI / OMOP Common Data Model** — the normalization target so a parsed predicate ("absolute neutrophil count ≥ 1.5 × 10⁹/L") evaluates against standardized concepts rather than site-local codes ([ohdsi.org](https://www.ohdsi.org/data-standardization/)).
- **HL7 CQL (Clinical Quality Language)** and **FHIR** — the interoperable expression layer for the predicates themselves, so a computable-eligibility rule is portable and human-auditable ([cql.hl7.org](https://cql.hl7.org/)).
- **CHIA** — the large annotated eligibility-criteria corpus used to train and evaluate the parser ([Kury et al., Sci Data 2020;7:281](https://doi.org/10.1038/s41597-020-00620-0)).

Criteria that resist reliable computable parsing — subjective judgments ("in the investigator's opinion, life expectancy > 3 months"), criteria requiring an examination not in the chart — are **not** force-fit into a predicate. They are surfaced verbatim to the clinician as an *indeterminate* item with the criterion text and its source citation. Guessing on an unparseable criterion is exactly the failure the three-valued contract exists to prevent.

## Citations on both sides — the match rationale

Every criterion verdict carries two provenance links, so the output is auditable rather than a black-box score:

1. **Criterion citation** — the exact eligibility clause in the trial record (ClinicalTrials.gov NCT ID + the inclusion/exclusion item), so the clinician sees the source-of-truth wording, not a paraphrase.
2. **Patient-datum citation** — the chart element (FHIR resource / OMOP record) that drove a *met* or *not-met*, honoring the [[draft-provenance-model]]: (source datum → provenance → citation). Under the [[privacy-state-machine]], these reads are local and no PHI leaves the covered-entity boundary during matching.

**Minimum-necessary is operationalized, not asserted.** The minimum-necessary standard ([45 CFR 164.502(b)](https://www.law.cornell.edu/cfr/text/45/164.502)) is a "reasonable efforts" obligation, and adjudicating hundreds of criteria over a recall-first candidate set can approach whole-chart access in practice — particularly since SMART-on-FHIR deployments commonly grant broad resource scopes at the authorization layer. OSSICRO therefore enforces the limit at the query layer, beneath whatever scope the EHR grants: each FHIR read request is **derived from the parsed predicate set** (resource types and terminology codes the active criteria actually reference — a lab predicate reads the matching `Observation` codes, not the chart), and the per-read audit log records **which criterion justified which read** (NCT ID + criterion index → FHIR query issued). The claim is thereby verifiable from the audit trail rather than a design intention: an auditor can reconcile every chart read against a specific eligibility predicate ([[hipaa-and-privacy-gating]]).

The rationale is the product. A ranked list with no rationale is unactionable in a regulated setting; a per-criterion ledger with citations is something an investigator can verify, correct, and stand behind.

## The non-delegable boundary

> [!warning] Non-delegable
> **The eligibility determination is the investigator's medical judgment**, not the matcher's output ([21 CFR 312.60](https://www.law.cornell.edu/cfr/text/21/312.60) — the investigator conducts the study per protocol and protects subjects). OSSICRO *retrieves, adjudicates per criterion, cites, and asks*; it never returns "enroll this patient." A trial appearing in a patient's candidate view is an invitation for the clinician to evaluate, never a clearance to enroll. Enrollment additionally requires the non-delegable **informed-consent event** ([21 CFR 50.20](https://www.law.cornell.edu/cfr/text/21/50.20); [[informed-consent-document-vs-event]]) and documented **IRB approval** ([21 CFR 56.111](https://www.law.cornell.edu/cfr/text/21/56.111)), and it triggers the HIPAA state transition from preparatory-review to authorization/waiver ([[privacy-state-machine]]). Matching sits entirely on the preparatory side of that line.

The HARD PRINCIPLE applies without exception here: OSSICRO drafts complete, cited decision *support* — a criterion-by-criterion ledger a qualified clinician reviews in one pass ([[single-pass-review-ux]]) — and never substitutes for the clinician's eligibility judgment, the IRB's approval, or the consent conversation.

## Interface to the rest of the system

- Indeterminate verdicts become **amber** open-items in the package [[completeness-ledger]] once a candidate progresses to activation; the "exact resolving question" is the ledger entry.
- Confirmed *met* criteria and their patient-datum citations pre-populate screening/eligibility worksheets as **drafts** for the [[generate-check-validate-engine]] — always behind the investigator's sign-off.
- Mechanism-driven candidate expansion is specified in [[matching-mechanism-graph]]; measured recall/precision behavior, the recall-floor value and measurement protocol, and the COU classification are specified in [[matching-evaluation-and-benchmarks]].

## Related

- [[matching-mechanism-graph]]
- [[matching-evaluation-and-benchmarks]]
- [[matching-engine]]
- [[patient-trial-matching]]
- [[feasibility-and-patient-matching]]
- [[privacy-state-machine]]
- [[hipaa-and-privacy-gating]]
- [[smart-on-fhir-integration]]
- [[draft-provenance-model]]
- [[completeness-ledger]]
- [[single-pass-review-ux]]
- [[non-delegable-functions-and-gates]]
- [[part-11-and-ai-credibility]]
- [[informed-consent-document-vs-event]]

## Sources

- [45 CFR 164.512(i) — Uses and disclosures for research; review preparatory to research](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.512)
- [45 CFR 164.502(b) — Standard: Minimum necessary](https://www.law.cornell.edu/cfr/text/45/164.502)
- [21 CFR 312.60 — General responsibilities of investigators](https://www.law.cornell.edu/cfr/text/21/312.60)
- [21 CFR 50.20 — General requirements for informed consent](https://www.law.cornell.edu/cfr/text/21/50.20)
- [21 CFR 50.25 — Elements of informed consent](https://www.law.cornell.edu/cfr/text/21/50.25)
- Kang T, Zhang S, Tang Y, et al. "EliIE: An open-source information extraction system for clinical trial eligibility criteria." JAMIA 2017;24(6):1062–1071. [DOI 10.1093/jamia/ocx019](https://doi.org/10.1093/jamia/ocx019) · [PMID 28379377](https://pubmed.ncbi.nlm.nih.gov/28379377/)
- Yuan C, Ryan PB, Ta C, et al. "Criteria2Query: a natural language interface to clinical databases for cohort definition." JAMIA 2019;26(4):294–305. [DOI 10.1093/jamia/ocy178](https://doi.org/10.1093/jamia/ocy178) · [PMID 30753493](https://pubmed.ncbi.nlm.nih.gov/30753493/)
- Kury F, Butler A, Yuan C, et al. "Chia, a large annotated corpus of clinical trial eligibility criteria." Sci Data 2020;7:281. [DOI 10.1038/s41597-020-00620-0](https://doi.org/10.1038/s41597-020-00620-0)
- [OHDSI — OMOP Common Data Model](https://www.ohdsi.org/data-standardization/)
- [HL7 Clinical Quality Language (CQL)](https://cql.hl7.org/)
- [ClinicalTrials.gov API v2](https://clinicaltrials.gov/data-api/api)
- [FDA Draft Guidance — Considerations for the Use of AI to Support Regulatory Decision-Making (Jan 2025, FDA-2024-D-4689)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-use-artificial-intelligence-support-regulatory-decision-making-drug-and-biological)