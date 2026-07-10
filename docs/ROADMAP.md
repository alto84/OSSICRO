# OSSICRO Roadmap

**Status:** Synthesized 2026-07-10 from the round-3 map, the INV-3 design pass, and the two improvement batches landed this round.
**Governing doc:** [OSSICRO-CONSTITUTION.md](OSSICRO-CONSTITUTION.md). Hard lines assumed throughout: synthetic data only, no PHI egress (HC2), nothing auto drives generation before a named human confirms it (HC1), statutory clocks are computed never judged (HC3).
**Live constraint (until UI QA ends):** the app server on port 8765 is held by a live UI QA session — everything below lands as code + pytest verification; no restart/rebind of the app.
**Test suite:** 147 green (`python -m pytest engine/tests/ -q`). Baseline was 128; +13 from the fhir_ingest tail work, +6 from the clock-canonicalization pins. "Keep the suite green" now means 147.

---

## 1. Just landed this round

Nothing in this section needs action; it is the new floor.

### 1.1 fhir_ingest tail improvements (code, 13 new tests)
Files: `engine/ossicro/fhir_ingest.py`, `engine/tests/test_fhir_ingest.py`.

- **NEW-5 — subject-reference filtering.** `_subject_ok`/`_scoped` now gate Condition / Observation / MedicationRequest / MedicationAdministration: a subject that resolves to (or is Patient-shaped and names) a Patient other than the single target patient excludes the resource. Absent/opaque subjects and non-Patient subjects keep prior behavior. Closes the external-reference side door (patient B's facts on patient A's 3926 draft — simultaneously a correctness and an HC2/INV-8 bug). 6 hostile-bundle tests.
- **MIN2 — diagnosis candidate preference.** Non-mCODE fallback now prefers `problem-list-item` Conditions with a cancer-adjacent code system (SNOMED/ICD-10-CM) before dumping the full active problem list; narrowing disclosed in the provenance path. Attacks the habituation risk (noisy medium-confidence proposals train physicians to skim). 4 tests.
- **MIN4 — practitioner selection.** `_select_practitioner` prefers Encounter.participant.individual, then Condition.asserter (subject-scoped), over `practitioners[0]`; selection basis disclosed in the investigator.name provenance path. 3 tests.

### 1.2 Clock reconciliation proven + README debt flag cleared (DEBT-1)
Files: `engine/tests/test_ea_features.py`, `app/README.md`.

The inline-clock debt was already paid in committed history (ea_generators re-exports the canonical `clocks.py` arithmetic). This round added `ComputeClocksCanonicalTests` (6 tests) pinning route-declared clocks to the canonical constructors date-for-date, the HC3 unarmed guarantee (no trigger date → armed:false, never a fabricated date), `TriggerDateError` on garbled triggers, and the 312.310(d)(2) deadline in the rendered emergency cover letter. README's stale "Known cleanup" flag replaced with the honest single-sourced statement. **DEBT-1 is closed.**

### 1.3 INV-3 committed-profile design (design-only)
Doc: [ehr-integration/commit-profile-design.md](ehr-integration/commit-profile-design.md).

Complete design for `commit_profile`: hash the flat stored intake (dotted keys, not `Study.raw`), canonicalization spec (`ossicro-profile-v1` domain-separated preimage → `sha256:<hex>`), per-field value hashes so `committed_profile` never stores plaintext (INV-8 clean), computed-not-bookkept pending_fields, named-actor requirement on commit, `input_hash` stamped onto ProvenanceRecord/Document via a single post-pass, rev-counter subsumption, lazy additive migration with **no auto-commit ever**, and a 16-item test plan that never binds port 8765. Nine open questions (Q1–Q9) recorded in its §10 — three of them are the Alton decisions at the bottom of this roadmap.

---

## 2. Load-bearing next

Ranked. These are the items where the system's central guarantees currently rest on prose or absence rather than code.

### #1 — INV-3: commit_profile (implement the design)
**Design doc:** [ehr-integration/commit-profile-design.md](ehr-integration/commit-profile-design.md)
**Where:** new `engine/ossicro/profile.py` (pure stdlib) + `app/server.py` `_generate_payload` / intake handler; new `POST /api/case/{id}/profile/commit` and `/profile/confirm`.
**Value:** This is the HC1 keystone. Today a changed field never forces re-confirmation — only a whole-case stale flag — and generation consumes whatever is in the intake dict with no hashed input-of-record. INV-3 makes generation consume only a committed, hashed, human-confirmed profile, and gives every ProvenanceRecord the Part-11-adjacent `input_hash` it should cite (HC5). review.md B3 called the doc-vs-code gap a credibility finding; §4 of the privacy state machine honestly marks it DEFERRED — this closes it.
**Effort:** M | **Risk:** medium | **Depends on:** B3 substrate (built). Design done; three open questions need Alton (see Decisions). Pytest-only verification; live 8765 untouched.
**Why first:** it unblocks the most downstream work of any single item — INV-8-TAIL (purge-on-commit has no trigger without it), INV-5 (finalize is only meaningful against a committed profile), the real N-2 fix (server-side provenance derivation becomes worth building when the profile is load-bearing), and GAP-5 (the confirmed-profile hash-of-record is P4a's central safeguard). Everything HC1-shaped converges here.

### #2 — GAP-1: wire the R-ICF-50.25-ADEQ concept rule into the pipeline
**Where:** `engine/registry/rules.json:92-103` (strategy "concept", check null) → `rules.py` concept_rules → pipeline stage 5. Review port + pipeline already exist.
**Value:** the canonical rule of the concept-over-rules doctrine — the ICF adequacy judgment the old string-match faked. Leaving it deferred means the ICF's substance is checked by nobody while the ledger implies otherwise. Escalate-only semantics already protect against the reviewer greening anything.
**Effort:** S | **Risk:** medium | **Depends on:** none — plumbing is present.

### #3 — GAP-7: app-layer case persistence (SQLite or JSON-file store, local only)
**Where:** `app/server.py` in-memory case dict; spec in EXECUTION-PLAN P3 task 7; boundary stated in `app/README.md`.
**Value:** any server restart loses every case mid-flow. Acceptable for a demo; disqualifying for the timed pilot (HITL-3) or any multi-session physician use.
**Effort:** S | **Risk:** medium | **Depends on:** none. Lands as code + tests now; the process restart that activates it waits for the UI QA session to release 8765. **Blocks HITL-3 in practice.**

### #4 — GAP-3: audit.py (Part 11 trail for reviewer calls + human dispositions)
**Where:** new `engine/ossicro/audit.py` per EXECUTION-PLAN D8 + §3.3 step 5 (`log_review`/`log_disposition`).
**Value:** accountability substrate for the judgment layer itself — model id, version, input hash, timestamp, reviewer identity, human disposition per finding. ClaudeReviewer runs whenever ANTHROPIC_API_KEY is set; today finding provenance lives only in the finding objects and dispositions are unrecorded. Matters more the moment a real (non-fixture) case is piloted. Pairs naturally with INV-3's `input_hash` (the audit record should cite the same hash).
**Effort:** M | **Risk:** medium | **Depends on:** benefits from INV-3 landing first (shared input_hash vocabulary), not blocked by it.

### #5 — GAP-4: Manufacturer Front-Door Registry (schema + human-confirmed seed data)
**Where:** new data file per EXECUTION-PLAN P5 task 1 (25–50 manufacturers, source URL + retrieval date + hash, freshness job).
**Value:** pure data work, no code dependency, explicitly parallelizable — and a public good. A stale intake contact spends a real patient's clock, so every record that could drive a real submission is human-confirmed before first use (HITL obligation baked in). Nothing else in P5 (front-door router, Say-Yes routing) can ship without it.
**Effort:** M | **Risk:** medium | **Depends on:** none. Can proceed in parallel with #1–#4.

### #6 — GAP-6: Lane 2 recall evaluation (slop corpus + eval/run_recall_lane.py)
**Where:** new `eval/` + `engine/fixtures/slop/` per EXECUTION-PLAN §5 Lane 2 + P1 task 7.
**Value:** the golden zero-FP lane shipped; without held-out seeded-defect fixtures there is no measurement of what the concept reviewer misses, no regression signal on model upgrade, no mechanized hindsight loop. Non-blocking by design (scheduled, not CI). Contamination rule from fixture one: slop never appears in prompts/exemplars.
**Effort:** M | **Risk:** low | **Depends on:** GAP-1 (worth measuring recall once the flagship concept rule actually runs).

---

## 3. Deferred privacy invariants — with their triggers

These are **deliberately not next**. Each is deferred on a stated principle (YAGNI, no consumer yet, or a prerequisite missing), and each has a concrete trigger that converts it to scheduled work. Building them early would violate the standing design restraint (no new automation without the incident/feature it serves).

| Invariant | What it is | Effort | Risk | Trigger that schedules it |
|---|---|---|---|---|
| **INV-4** egress gateway | `engine/ossicro/egress.py`: single sanctioned outbound-request constructor; closed DeidentifiedPredicates struct (condition codes, RxNorm, 5-yr age bands 90+ top, sex, coded route-of-care); destination allowlist (clinicaltrials.gov, NCBI eutils, api.fda.gov); egress audit log. Makes identifier egress *unrepresentable* — HC2 currently holds only by absence plus the `TestEngineEgressBoundary` interim guard. | M | low | **The candidate-trial-matcher feature** (first real outbound consumer) — build the gateway in the same pass. Also prerequisite-or-extended-by INV-7. |
| **INV-5** promote()/demote() mode transitions | Persisted case mode (today a hardcoded `PREPARATORY_REVIEW` string in `_fhir_import`); recorded legal basis ∈ {authorization-164.508, waiver-164.512(i)(1)(i), treatment-disclosure}; GateViolation on finalize-in-PREPARATORY_REVIEW. The 164.508/164.512(i) boundary is the legal moment PHI disclosure basis changes — the machine must demand a named actor + basis. | L | medium | **An enrollment path existing at all** — today no identified enrollment artifact can be finalized, so the gate has nothing to fire on. Sequence strictly after INV-3 (finalize is only meaningful against a committed profile). |
| **INV-7 tail** real SMART-on-FHIR launch | OAuth2 + read-only scope assertion (`patient/*.read`-class) at token exchange, entirely in the app layer (fhir_ingest stays pure per INV-1). Read-only-toward-the-EHR is currently true by absence; scope assertion makes it code. | L | high | **The decision to connect a live EHR.** Sequence with/after INV-4 (first real outbound network surface) — and note it is the first feature that collides with pure-stdlib (OAuth2 + TLS via stdlib only). NEW-5 subject filtering, tracked for this pass, already landed. |
| **INV-8 tail** bundle retention + purge-on-commit | Encrypted-at-rest retention for the imported bundle + raw-bundle purge when commit_profile fires. The bundle is the most identifier-dense object the system touches; its post-mapping lifetime is unmanaged. | M | medium | **INV-3 landing** gives purge-on-commit its trigger. But per design Q9: no bundle is currently retained anywhere, so purge is vacuous today — recommended keep deferred rather than build a purge for a retention that does not exist. The encrypted-at-rest half needs an Alton scoping decision (see Decisions: DPAPI-via-ctypes vs honest doc re-scope). |

---

## 4. HITL / human-owned items

Work where the scarce input is a qualified human's time and attestation, not code. These are the gate between "prototype" and "pilotable."

### HITL-2 — Route-scoped citation + clock verification pass ⟵ do this one first
**Where:** `docs/route-3926-submission-spec.md` (Confirmed/Interpretive labels, §3.3 clock table, §10 acceptance); `engine/registry/rules.json` + `routes.json`. No sign-off artifact exists anywhere in the repo.
**Value:** every draft, ledger entry, and clock inherits from these citations and day-counts, and they are **self-asserted by the build** — no named qualified human has attested them. A wrong citation or miscoded working-day rule propagates into a real patient's submission. Deliverable is a recorded, versioned attestation artifact (who, when, against which registry versions), consistent with HC1/CP4. Note: this round's clock-canonicalization tests reduce the *arithmetic* half of the risk (constants are now pinned to the canonical constructors); the *citation correctness* half is untouched and is precisely what needs the human.
**Effort:** M (human hours) | **Risk:** high | **Depends on:** nothing; blocks HITL-3.

### HITL-1 — Real fillable Form FDA 3926 PDF (deterministic AcroForm fill)
**Where:** `docs/rapid-access-vision-and-plan.md:53`; `app/server.py` package export + `engine/ossicro/ea_generators.py` (currently text-only); `app/static/index.html` document panes.
**Value:** the submission the FDA reviewer actually receives is the official OMB 0910-0814 form, not prose panes. Until it exists, every pilot ends in manual re-keying. No AI in this stage — deterministic field mapping only.
**Effort:** M | **Risk:** medium (field-mapping errors on a real federal form are consequential; the mapping is fixed/published) | **Depends on:** pure-stdlib constraint — the fill layer is stdlib raw AcroForm/FDF writing, or lives outside the engine boundary. Also feeds PERSONA-3's Say-Yes PDF export.

### HITL-3 — One timed end-to-end pilot case (Days-to-Drug instrumentation)
**Where:** `docs/EXECUTION-PLAN.md:370` (intake-to-green-ledger <24h acceptance) + cross-phase Days-to-Drug clock model.
**Value:** the product's central claim — time-to-drug collapse — is currently asserted, not measured. One timed synthetic-fixture run (physician-side intervals vs statutory clocks vs counterparty elapsed) converts claim to evidence and exposes real UX bottlenecks before any live case.
**Effort:** S | **Risk:** low | **Depends on:** **HITL-2** (verify the citations before timing a pilot on them) and **GAP-7** (a >1-session pilot cannot survive a restart). HITL-1 strengthens realism but is not blocking.

---

## 5. Breadth — the three un-built personas

Four entry points in the design (`docs/detailed-plan.md:83-90`); only HCP exists in software. Ordering below reflects readiness, not importance.

### PERSONA-3 — Pharma (LOA/Say-Yes receiving side + front-door router) — *closest to done*
**Where:** partially built — `app/static/verify.html` (standalone dossier verifier, the P5 trust wedge) + the LOA-request/manufacturer view in `app/server.py`. Missing: the front-door router (with the sales-contact hard rail as a validation error) and the signature-ready visible-PDF Say-Yes export (EXECUTION-PLAN P5 tasks 2–3).
**Value:** the manufacturer's yes is the real gate on drug supply; the remaining pieces make that yes an edit-and-sign instead of a drafting project.
**Effort:** M | **Risk:** medium | **Depends on:** GAP-4 (front-door registry data — hard prerequisite) and HITL-1 (PDF rendition machinery).

### PERSONA-1 — Patient entry point (discovery front door)
**Where:** docs only (`wiki/06-personas/patient.md`); no code.
**Value:** "is there a trial/therapy for me?" is one of the four doors. But full matching depends on the P4b research-grade program (ClinicalTrials.gov v2, computable eligibility), and building matching before P4b's eval harness exists would violate the no-unbenchmarked-quality-claims stance. **The honest scoped version is a thin patient-facing intake that routes to a physician — nothing more.**
**Effort:** L (thin version: M) | **Risk:** medium | **Depends on:** P4a extraction/route-classifier work (GAP-5); full matching deferred to P4b.

### PERSONA-2 — Micro-CRO entry point (accountable-layer workbench)
**Where:** docs only (`wiki/06-personas/micro-cro.md`, vision doc §4.5); no code.
**Value:** the workbench is what keeps the thin legally-accountable entity (holder of transferred 312.52 obligations) economically viable. But EXECUTION-PLAN deliberately defers entity formation + SDEA/TORO tooling until counsel review and a real counterparty; building the console before the entity exists is premature.
**Effort:** L | **Risk:** medium | **Depends on:** **a real counterparty materializing.** Correct disposition: keep as documented decision; do not schedule.

### Related large arc — GAP-5: P4a agentic intake
**Where:** EXECUTION-PLAN P4a tasks 1–6. Built today: fhir_ingest + the paste-a-Bundle box. Missing: free-text/PDF extraction agent, minimum-necessary gap loop, Mode A/B/312.310 route classifier with the four hard stops, Red-Resolver interview agent.
**Value:** the largest scheduled arc remaining (10–15 in-plan days) and the layer where HC1 is most easily violated — the extraction agent's indeterminate-never-guess contract and the confirmed-profile hash-of-record are the safeguards, and both must be adversarially tested, not asserted.
**Effort:** L | **Risk:** high | **Depends on:** INV-3 (its hash-of-record *is* the P4a confirmation substrate) and the Phase-13 EHR privacy work settling. Gate PERSONA-1's thin intake behind this.

---

## 6. Tech debt

Small, bounded items. None blocks the sequence; batch them opportunistically with adjacent work.

| Item | What / where | Value | Effort | Risk | Depends on / batch with |
|---|---|---|---|---|---|
| **GAP-2** two-tier registry split | Split `engine/registry/banned-constructions.json` into `hard-rules.json` + `slop-examples.json`; loader change in `register_linter.py`. Linter's two-tier logic already conforms. | File boundary mirrors the Constitution §III/§IV boundary; until it lands, tier drift is invisible in diffs and the conformance-test story is unenforceable. | S | low | None — data + loader only. |
| **MIN4-B** privacy_log hygiene | Add `actor` to the `fhir_bundle_loaded` event (`app/server.py` `_fhir_import`); bound privacy_log growth across repeated imports. | State machine §2 specifies actor on load_bundle — a documented-diagram-vs-code gap of exactly the round-1 credibility class. | S | low | Frontend already collects clinician name at Apply; collect at import too, or log "unattributed". Batch with INV-3's server work. |
| **NIT-LICENSE** single-license early return | `_extract_practitioner` qualification loop returns on the first non-NPI qualification identifier; a physician licensed in two states gets whichever the EHR listed first, no §1.2 multi-candidate disclosure. | investigator.license_number/state go on the federal form (HC4). | S | low | Same function/discipline as MIN4 — batch with any next `_extract_practitioner` touch. |
| **N-1** coding.display disclosure | One sentence in `docs/ehr-integration/fhir-intake-mapping.md`: coding.display bypasses the taint flag by design (controlled-terminology trust); residual is hostile display + no-basis bundle only. | Honesty-of-claims: the doc must state the boundary of the guarantee so it cannot be read as broader than it is. | S | low | Doc-only; do anytime. |
| **N-2** client-asserted provenance | Wording note in privacy-state-machine §4a now (attribution record, not a Part-11 signature). Real fix — server-side provenance derivation (server remembers which field_ids it proposed per import, validates the claim) — becomes load-bearing when INV-3 makes provenance feed a gate. | HC5: distinguishes chart-extracted from hand-typed in a future audit. Accepted on single-user localhost; a real gap the moment the app is multi-user. | S (note) / M (real fix) | low | Real fix rides the INV-3 implementation pass. |
| **DEBT-1** clock reconciliation | ~~Closed this round~~ — see §1.2. Residual judgment call blessed: `compute_clocks`/`compute_deadline` orchestration stays in ea_generators (equality with canonical constructors enforced by test, not relocation). | — | — | — | Done. |

---

## RECOMMENDED SEQUENCE

Two tracks run in parallel: a **code track** (agent-executable, pytest-verified, never touches 8765) and a **human track** (Alton / qualified-human hours). Items within a track are ordered; the tracks interleave freely.

**Code track:**
1. **INV-3 commit_profile** — implement the design doc (after the three Alton decisions below). Batch in MIN4-B (actor on import event) and the N-2 §4a wording note, which touch the same server surfaces.
2. **GAP-1** — wire R-ICF-50.25-ADEQ into pipeline stage 5 (small; can even precede INV-3 if its decisions stall).
3. **GAP-7** — case persistence, code + tests now; process restart deferred until UI QA releases 8765.
4. **GAP-3** — audit.py, citing INV-3's input_hash.
5. **HITL-1** — 3926 AcroForm fill layer (code half; the field-mapping verification is human).
6. **GAP-6** — Lane 2 recall eval, once GAP-1 makes the reviewer worth measuring.
7. **GAP-2 / NIT-LICENSE / N-1** — batch opportunistically.

**Human track (start immediately, in parallel):**
- **HITL-2** — citation + clock attestation pass (the highest-risk open item in the repo; pure human hours).
- **GAP-4** — front-door registry seed data, human-confirmed per record.

**Convergence point:** when HITL-2 + GAP-7 (+ ideally HITL-1) are done → **HITL-3, the timed pilot.** That run is the evidence gate for everything after it.

**After the pilot:** GAP-5 (P4a agentic intake) on the INV-3 substrate → PERSONA-3 completion (router + Say-Yes export, on GAP-4 + HITL-1) → thin PERSONA-1 intake. INV-4/INV-5/INV-7 fire on their triggers (trial-matcher / enrollment path / live-EHR decision), not on the calendar. PERSONA-2 stays parked until a counterparty exists.

---

## Decisions that need Alton

1. **INV-3 gating posture (design Q1):** hard-gate `/generate` + `/package` from day one — which breaks the current sample-fill→generate demo flow and every existing case until a named human commits — or soft-warn for one release? *Recommended: hard, per HC1/guarantee 5, with the commit UI shipping in the same change.* (Bundled sub-decisions from the same doc: Q5 whitespace-insensitive change detection, Q6 advisory-vs-hard invalidation of sign-offs recorded against a superseded profile hash — both recommended-as-written in the design's §10.)

2. **HITL-2 scheduling:** the citation/clock attestation is qualified-human hours that only Alton can commit (his time, or a named delegate's). It is the single highest-risk open item and it gates the timed pilot. When does it happen, and who is the named attester?

3. **INV-8 encrypted-at-rest scope:** pure-stdlib means no cryptography dep — so "encrypted local retention" is either OS-level DPAPI via ctypes (Windows-only answer) or an honest re-scoping of the doc's claim. Since no bundle is retained anywhere today (design Q9), the cheapest defensible answer is to re-scope the doc now and revisit if bundle retention is ever actually built. Which way?
