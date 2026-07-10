# Privacy State Machine — EHR Ingestion (Explore, Phase 1)

**Version 1.0 — 2026-07-09.** The code-enforceable privacy design for OSSICRO's FHIR ingestion. Everything here is written to be implemented directly: named states, named transitions, named invariants, and the concrete guarantees the backend must satisfy before the Build phase can claim FRAME success criterion 4. Legal anchors: 45 CFR 164.508, 164.512(i), 164.506, 164.502(b), 164.514(b); Constitution HC1 (humans decide) and HC2 (privacy / no PHI externalization). Companion: `fhir-intake-mapping.md` (what is extracted) and its §1.3 never-extract list.

## 1. Design stance

**Local-first, deny-by-default egress, human-confirmed intake.** The FHIR bundle is the most identifier-dense object OSSICRO will ever touch — a chart carries name, MRN, birthDate, address, telecom. The design treats the bundle as radioactive: it is parsed and mapped entirely in-process, it never crosses the network, it never lands in a log, and nothing extracted from it acquires any authority until a named human confirms it field by field. There is exactly one door to the network and it is too narrow for an identifier to fit through.

## 2. States and transitions

```
IDLE
  │  load_bundle(source ∈ {file-upload, paste, mocked-SMART-launch, bulk-$export file})
  │  [log: case_id, actor, source-kind, bundle SHA-256 — never bundle content]
  ▼
BUNDLE_LOADED                          mode = PREPARATORY_REVIEW (entered + logged)
  │  parse_map()   — pure local function, no I/O (INV-1)
  ▼
MAPPED             ExtractionProposal[] built: {field_id, proposed_value,
  │                provenance{resource_type, fhirpath, coding_system, source_ref},
  │                confidence ∈ {high, medium}} ; absent/ambiguous → unattested
  │                (never guessed — mapping spec §1.2)
  ▼
CONFIRMING         field-by-field UI: value + source + confidence shown
  │  confirm(field_id, actor)  |  correct(field_id, new_value, actor)  |  reject(field_id, actor)
  │  [each is an audit event: ts, named actor, field_id, action, provenance, confidence]
  ▼
PROFILE_COMMITTED  commit_profile(actor):
  │                • confirmed values written to Study.raw (the ONLY write path — INV-2)
  │                • canonicalized profile hashed (SHA-256) = generation input-of-record (INV-3)
  │                • raw bundle purged from memory/disk unless the physician explicitly
  │                  elects local encrypted retention (INV-8)
  ▼
GENERATE → CHECK → PACKAGE   (existing engine flow, unchanged; consumes ONLY the
                              committed profile; drafts only; gates fail closed)

Orthogonal mode axis (any state):
PREPARATORY_REVIEW ──promote(actor, legal_basis)──▶ ENROLLMENT
  legal_basis ∈ {authorization-164.508 on file, waiver-164.512(i)(1)(i) documented,
                 treatment-disclosure determination}   [logged; one-way unless
                 demoted with a logged reason]
```

**Illegal transitions the code must make unrepresentable:** `MAPPED → GENERATE` (proposals can never reach the generator), `BUNDLE_LOADED → egress` (bundle content in any outbound payload), any write to `Study.raw` from the mapper (only `commit_profile` writes, and only confirmed values).

## 3. The legal boundary: preparatory review vs enrollment

- **Preparatory review — 45 CFR 164.512(i)(1)(ii).** The default mode from `load_bundle`. The physician (a covered-entity workforce member) reviews identified data to assess whether an expanded-access request is warranted and feasible. Under the preparatory-to-research provision, this review is permissible **only if the PHI is not removed from the covered entity** — which is exactly what local-first enforces: identified data stays inside the local process/machine; nothing identified is recorded outward or transmitted. Every external lookup in this mode (candidate trials, literature, safety data) carries only de-identified predicates (§4, INV-4).
- **Enrollment — §164.508 / §164.512(i)(1)(i).** When the case moves from "considering" to "doing" — assembling the package that will name the patient to FDA, the manufacturer, and the IRB — the disclosure basis changes: a signed **§164.508 authorization** from the patient (the operational default; it travels naturally with Part 50 informed consent), or a documented **IRB/privacy-board waiver under §164.512(i)(1)(i)**. The `promote()` transition requires one recorded basis and logs actor, timestamp, and basis. No enrollment artifact containing identified data may be *finalized* in PREPARATORY_REVIEW mode.
- **Honest nuance, recorded not blurred:** single-patient expanded access is *treatment, not research* (21 CFR 312.305(a); submission spec §0), so §164.506 treatment/operations disclosures may independently permit some of this flow. OSSICRO enforces the stricter research-style boundary anyway — it is the conservative floor, it costs one click, and the FRAME names it as the design. The `treatment-disclosure` basis exists in the enum so the record states the true basis rather than laundering everything through a research provision. Minimum necessary (§164.502(b)) applies throughout except to treatment disclosures.
- Regardless of mode: **OSSICRO never transmits the package.** Enrollment artifacts are drafts the physician sends (HC1; submission spec — OSSICRO never files). The mode boundary governs what may be *prepared and finalized*, not who sends; sending is always human.

## 4. Hard invariants (enforced in code, each with a test)

| # | Invariant | Enforcement |
|---|---|---|
| **INV-1** | **Locality of parse/map.** The ingestion module (`fhir_ingest`) performs no I/O: pure stdlib `json` parsing, no HTTP client imported, no socket use, no file writes. Bundle bytes and parsed resources exist only in process memory (plus optional encrypted local case store per INV-8). | Module imports audited in test (`fhir_ingest` must not import `urllib`, `socket`, `http`, `requests`); parse/map are pure functions `bytes → proposals`. |
| **INV-2** | **No auto-intake (HC1).** Extracted values live in `ExtractionProposal` objects — a distinct type from intake. The **only** function that moves a proposal into `Study.raw` requires a `HumanConfirmation{field_id, value, named_actor, ts}`. The generator's entry point type-checks that it received a committed profile, not proposals. | Type separation + single write path; test: invoking generate with unconfirmed proposals raises `GateViolation`. |
| **INV-3** | **Input-of-record hash.** `commit_profile` canonicalizes (sorted keys, normalized whitespace) and SHA-256-hashes the confirmed profile; generation records the hash in every `ProvenanceRecord`. Any later field change re-enters CONFIRMING and produces a new hash. | Test: mutate one confirmed field → generation blocked until re-confirmation; hash changes. |
| **INV-4** | **Egress gateway (HC2).** Exactly one function may construct outbound requests. Its argument is a `DeidentifiedPredicates` struct whose fields are a closed whitelist: condition codes (SNOMED/ICD-10-CM), drug names/RxNorm codes, `age_band` (5-year bands, top band "90+" per §164.514(b)(2)(i)(C)), administrative sex, and coded route-of-care facts. It structurally cannot carry names, dates, identifiers, geography, coded_id, case ids, or free text lifted from the chart. Every call is audit-logged with full predicate payload + destination. | Constructor validation + closed struct (no dict passthrough); test: any attempt to smuggle an identifier field fails at construction. Destination allowlist: `clinicaltrials.gov`, `pubmed.ncbi.nlm.nih.gov` / NCBI eutils, `api.fda.gov`. Deny-by-default for everything else. |
| **INV-5** | **Mode transitions logged.** PREPARATORY_REVIEW → ENROLLMENT requires `legal_basis` and named actor; demotion requires a logged reason. Finalizing an identified enrollment artifact in PREPARATORY_REVIEW raises `GateViolation`. | State machine + test on both directions. |
| **INV-6** | **Unattested honesty.** Absent/ambiguous chart data → field marked unattested; generated documents render the existing honest placeholders; no default, no population prior, no guess (existing `StudyFact` behavior extended to imports). | Test: bundle lacking an element yields unattested, never a fabricated value. |
| **INV-7** | **Read-only toward the EHR.** The ingestion module contains no code path that constructs FHIR write/update/transaction requests. SMART scopes (when the real launch lands) are requested read-only (`patient/*.read`-class); this pass mocks the launch and accepts bundles only. | Code review gate + scope assertion at token exchange (future). |
| **INV-8** | **No PHI at rest or in logs.** Logs carry field ids, resource types, FHIRPaths, confidence, hashes, actors, timestamps — never values from the chart. The raw bundle is purged at `commit_profile`; retention only by explicit physician election, encrypted at rest, purged at case close. `Patient.birthDate` is consumed inside the age computation and never stored (mapping spec §1.3). | Log-schema test: audit records validated against a schema with no free-value field for chart data; retention test: post-commit, bundle absent unless election flag set. |

## 5. Concrete backend guarantees (the build checklist)

1. `fhir_ingest.parse_bundle(bundle_bytes) -> list[ExtractionProposal]` — pure, stdlib-only, no I/O (INV-1). Malformed input → structured error, never a partial guess.
2. `ExtractionProposal` carries `field_id`, `proposed_value`, `provenance` (resource type, FHIRPath, coding system, in-bundle source ref), `confidence` — and is **not** accepted anywhere `Study.raw` values are accepted (INV-2).
3. The never-extract list (mapping spec §1.3) is a code-level filter applied before proposals are built; `Patient.name`/`identifier`/`address`/`telecom`/`birthDate` values cannot appear in any proposal, log, or error message.
4. `confirm / correct / reject` each write one audit record `{ts, actor, case_id, field_id, action, provenance, confidence}`; `commit_profile` writes confirmed values to `Study.raw`, computes the SHA-256 input-of-record, and purges the bundle (INV-3, INV-8).
5. Generation refuses any input that is not a committed, hashed profile; unconfirmed anything → `GateViolation` (fail closed, HC1).
6. All outbound matching/generation-support queries route through the single egress gateway taking `DeidentifiedPredicates` only; destination allowlist enforced; every egress audit-logged (INV-4). Small-cell caution: predicates are limited to condition + drug + age_band + sex — no geography, no dates — so a rare-disease query cannot be sharpened into a re-identification key by the query string itself.
7. Mode is a persisted, logged property of the case; `promote()` demands a recorded legal basis (§164.508 authorization / §164.512(i)(1)(i) waiver / treatment-disclosure determination) (INV-5).
8. No EHR write-back exists in the codebase (INV-7). No external CDN, no telemetry, no analytics beacon in the import/confirmation UI (FRAME constraint: no external CDNs — which here is also a privacy property).
9. Every invariant above ships with its named test in the engine suite; the existing tests stay green (FRAME constraint).

## 6. What this machine deliberately does not do

It does not de-identify for export (no §164.514 expert-determination tooling — out of scope); it does not manage the patient's §164.508 authorization document beyond recording that one exists and where; it does not decide the legal basis — it demands that a named human record one. The machine's whole job is narrower and harder: make the safe path the only path that compiles.
