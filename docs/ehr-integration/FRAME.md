# EHR / SMART-on-FHIR Integration + UI Uplift — Frame (Phase 0)

**Problem.** The 55-field manual intake is the enrolling physician's single biggest burden and the first thing that makes OSSICRO feel like work rather than help. A physician's EHR already holds most of it — diagnosis, stage, labs, medications, demographics. EHR / SMART-on-FHIR integration lets the clinician pull the structured chart and auto-populate the intake, turning an hour of typing into minutes of confirming. The catch that makes this hard and worth doing carefully: nothing auto-extracted may drive document generation until a named human has confirmed it, and PHI must not leave the covered-entity boundary.

**Success criteria.**
1. A FHIR R4 **Bundle** (from a SMART App Launch, a Bulk Data `$export`, or an uploaded/pasted bundle) is parsed and mapped to the intake profile, each field carrying **provenance** (source FHIR resource type + path + coding system) and a **confidence**. Unmapped or low-confidence data is left explicitly **unattested** — never guessed.
2. A **field-by-field confirmation UI**: the physician sees each extracted value with its source and confidence and confirms or corrects it. Only confirmed values become intake. The confirmed profile is hashed as the generation input-of-record.
3. The confirmed profile drives the existing generate → check → package flow unchanged.
4. **Privacy state machine** enforced: local-first; matching/generation queries carry only de-identified predicates; a logged boundary between *preparatory review* (identified data stays local, 45 CFR 164.512(i)(1)(ii)) and *enrollment* (authorization/waiver). **No PHI egress.**
5. **UI uplift**: an import flow, the confirmation surface, and navigation/design polish that make the app materially more usable.

**Scope — in.** FHIR R4 Bundle ingestion; US Core + mCODE resource→field mapping; provenance + confidence; the confirmation UI; the privacy gate; a synthetic (Synthea-style) demo bundle; UI polish.

**Scope — out (this pass).** A live production-EHR connection (use a synthetic bundle / sandbox); a real SMART OAuth handshake against a live server (accept a bundle; mock the launch); any write-back to the EHR (read-only, always).

**Constraints.** Pure-stdlib backend (FHIR parsing in `json`, no pip deps); frontend no external CDNs; keep all engine tests green; the hard line holds — drafts only, gates fail closed, nothing auto-populated drives generation before a named human confirms it (Constitution HC1/HC2).

## Phase log
| Phase | Status | Artifact |
|-------|--------|----------|
| 0 Frame | done | this file |
| 1 Explore (FHIR→intake mapping + privacy design) | done | `fhir-intake-mapping.md` (17 auto / 3 derived / 35 manual), `engine/fixtures/fhir_sample_bundle.json`, `privacy-state-machine.md` |
| 2 Plan | folded into Explore spec | the mapping + privacy invariants are the build spec |
| 3 Build (backend FHIR ingest + confirmation UI + polish) | done | `engine/ossicro/fhir_ingest.py` (+23 tests, 97 green), `app/server.py` (POST `/fhir/import`), `app/static/index.html` (import + confirmation UI + uplift). HTTP-verified: import returns 19 proposals, does NOT mutate intake, no patient PHI in proposals, planted-PHI bundle leaks nothing, confirm→`/intake` works. |
| 4 Adversarial review (clinical-informatics + privacy skeptic) | done | `docs/ehr-integration/review.md` — 3 BLOCKER, 7 MAJOR, 4 MINOR + T1 test-gap; all reproduced by executing code |
| 5 Revise (orchestrator, not builders) | done | fixes B1/B2/B3/M1-M7/MIN1-3 + hostile-bundle test battery (97→120 tests); doc-honesty pass on `privacy-state-machine.md`; per-charge reply in review.md |
| 6 Re-review (fresh reviewer) | in progress | round-2 memo |
