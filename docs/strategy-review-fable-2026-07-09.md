# OSSICRO — Fable Strategist Review (2026-07-09)

_Model self-report: the standalone Fable strategist did not emit the requested MODEL line; treat model as unconfirmed-Fable. Reasoning quality consistent with Fable 5._

Seven high-leverage improvements, ranked, plus a second tier. All adopted into the master strategy (see `detailed-plan.md`) and reflected as new `05-ossicro-system/` and `references/` wiki pages.

## Three framing critiques
1. **Semantic-similarity matching hits the free-text-eligibility recall/precision ceiling.** Ranking ≠ adjudicating eligibility. That gap is "another keyword matcher" vs. near-perfect matching.
2. **Matching risk is under-classified.** Drafting is low-influence COU; matching that can return "no eligible trial" and gate a patient's access is a HIGHER-influence context of use and must be designed/evaluated as one.
3. **AI-in-the-loop is generic ("drafts behind gates").** Single-pass HITL demands a specific provenance + attention-triage architecture.

## Ranked improvements
1. **SMART-on-FHIR chart ingestion behind a code-enforced privacy state machine** (highest leverage). App Launch (point-of-care) + Backend Services/Bulk `$export` (panel screening). US Core + mCODE + FHIR Genomics. Feeds BOTH matching and drafting. HIPAA 45 CFR 164.512(i)(1)(ii) "review preparatory to research" enforced in code (local-first, minimum-necessary, no PHI egress, ephemeral audited reads); hard logged state transition preparatory→enrollment (§164.508 auth or §164.512(i)(1)(i) waiver). Read-mostly. → `smart-on-fhir-integration.md`, `privacy-state-machine.md`.
2. **Eligibility-adjudication matching engine** — retrieve→adjudicate; mechanism-aware candidate expansion (biomarker→pathway→target→trials); three-valued per-criterion verdict (met / not-met / indeterminate-needs-data) with chart + criterion citations; recall-first, never silently exclude; eligibility determination stays the investigator's non-delegable call. Prior art to reimplement: Criteria2Query, EliIE (Weng, Columbia), OHDSI/OMOP, CQL. Eval harness on CHIA + TREC Clinical Trials + n2c2. → `matching-eligibility-adjudication.md`, `matching-mechanism-graph.md`, `matching-evaluation-and-benchmarks.md`.
3. **Provenance-linked drafts + attention-triaged review UX** (single-pass HITL core). Every span carries (source datum → provenance → citation). Three review lanes: deterministic (collapsed), boilerplate (collapsed), inferred/interpretive (foregrounded). Provenance == ALCOA++/Part-11 audit trail rendered as UX. → `single-pass-review-ux.md`, `draft-provenance-model.md`.
4. **Adversarial machine pre-review + cross-document consistency engine.** Independent QC agent (structurally separate from drafting) red-teams the package and checks cross-document consistency (PI/name/address/dates/IND#/protocol version identical across 1572, delegation log, protocol). Human receives draft + critique. → elevated "check" pass in `generate-check-validate-engine.md`.
5. **Completeness ledger (open-items contract).** Every package ships a machine-checked ledger: green (validated) / amber (needs human judgment = the gate) / red (missing data + the exact resolving question). Operating definition of "COMPLETE documentation"; closes the loop with matching's indeterminate outputs. → `completeness-ledger.md`.
6. **Verifiable site-qualification dossier** (pharma trust wedge + Micro-CRO moat). Cryptographically verifiable, citation-complete manifest: requirement → artifact → citation → responsible-human signature, hash-chained into the Part-11 audit trail, verifiable without trusting OSSICRO. → `verifiable-site-qualification-dossier.md`.
7. **Living-compliance regulatory-change watch** (durable moat / anti-rot). Diffs FDA/ICH/eCFR on a cadence and flags every affected page/template/rule via the citation-dependency graph; human curator confirms. E6(R3)/M11/DCT/AI-credibility are all in motion. → `references/regulatory-change-log.md`.

## Second tier (adopted)
- **Offline / single-container local deployment** (privacy + low-resource-site adoption). → `offline-local-deployment.md`.
- **Safety-clock engine** — dedicated 7/15-day IND safety-report (312.32) deadline computation + escalation; computes/escalates but never files and never makes causality call (medical monitor owns causality). → `safety-clock-engine.md`.
- **Publish computable eligibility as an open dataset** (network-effect asset consistent with MIT/open-source thesis).

**Through-line:** items 2–3 are the product differentiators; items 6–7 are the moat; item 1 is the data spine that makes 2 and 3 achievable.
