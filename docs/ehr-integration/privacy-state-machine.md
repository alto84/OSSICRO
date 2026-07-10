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
  │                • raw bundle is never written to disk: it is mapped in memory and
  │                  discarded once proposals are produced (no retention feature exists — INV-8)
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

## 4. Hard invariants — target design and Phase-1 status

> **Read this first (honesty note, added in the Phase-13 adversarial-review
> revision).** The table below is the *target* design. Not all of it is built
> yet. The `commit_profile` / `promote()` / `DeidentifiedPredicates` machinery
> (INV-3, INV-4, INV-5) is **design, not code** in Phase 1. The **Status**
> column states exactly what is implemented-and-tested versus deferred, so this
> document cannot be read as asserting a protection that does not exist. The
> Phase-1 substrate that *is* built is summarized in §4a.

| # | Invariant | Enforcement | Status (Phase 1) |
|---|---|---|---|
| **INV-1** | **Locality of parse/map.** The ingestion module (`fhir_ingest`) performs no I/O: pure stdlib `json` parsing, no HTTP client imported, no socket use, no file writes. Bundle bytes and parsed resources exist only in process memory; the local case store holds coded identifiers and confirmed intake only — never raw chart data (INV-8). | Module imports audited in test (`fhir_ingest` must not import `urllib`, `socket`, `http`, `requests`); parse/map are pure functions `bytes → proposals`. | **Implemented + tested.** `TestParsePurity`, `TestEngineEgressBoundary` (engine-wide network-free except the one sanctioned reviewer). |
| **INV-2** | **No auto-intake (HC1).** Extracted values live in `ExtractionProposal` objects — a distinct type from intake. The **only** path that writes the input-of-record is the confirm step. | Import endpoint provably never writes intake; the confirmation subset flows through the existing `POST /intake`; test asserts intake stays `{}`/rev 0 after import. | **Implemented + tested.** `test_import_returns_proposals_and_never_mutates_intake`. (The typed `HumanConfirmation`/committed-profile object is deferred — see INV-3.) |
| **INV-3** | **Input-of-record hash.** `commit_profile` canonicalizes (sorted keys, normalized whitespace) and SHA-256-hashes the confirmed profile; generation records the hash in every `ProvenanceRecord`. Any later field change re-enters CONFIRMING and produces a new hash. | Test: mutate one confirmed field → generation blocked until re-confirmation; hash changes. | **DEFERRED.** No `commit_profile`, no profile hash, no re-confirmation-on-change gate. Staleness today is the coarse `intake_rev`/`generated_rev` counter, which flags "regenerate," not per-field re-confirmation. Tracked. |
| **INV-4** | **Egress gateway (HC2).** Exactly one function may construct outbound requests. Its argument is a `DeidentifiedPredicates` struct whose fields are a closed whitelist: condition codes (SNOMED/ICD-10-CM), drug names/RxNorm codes, `age_band` (5-year bands, top band "90+" per §164.514(b)(2)(i)(C)), administrative sex, and coded route-of-care facts. It structurally cannot carry names, dates, identifiers, geography, coded_id, case ids, or free text lifted from the chart. Every call is audit-logged with full predicate payload + destination. | Constructor validation + closed struct (no dict passthrough); test: any attempt to smuggle an identifier field fails at construction. Destination allowlist: `clinicaltrials.gov`, `pubmed.ncbi.nlm.nih.gov` / NCBI eutils, `api.fda.gov`. Deny-by-default for everything else. | **DEFERRED — vacuously safe today.** No outbound request is constructed anywhere in the ingestion/app path (HC2 holds by absence). Meanwhile `TestEngineEgressBoundary` asserts no engine module except the single sanctioned concept-reviewer imports an outbound client, and that reviewer never imports the PHI path — so the *next* feature cannot quietly egress. The typed `DeidentifiedPredicates` gateway is built when the trial-matcher lands. |
| **INV-5** | **Mode transitions logged.** PREPARATORY_REVIEW → ENROLLMENT requires `legal_basis` and named actor; demotion requires a logged reason. Finalizing an identified enrollment artifact in PREPARATORY_REVIEW raises `GateViolation`. | State machine + test on both directions. | **DEFERRED.** `PREPARATORY_REVIEW` is recorded on the load event but there is no `promote()`; no enrollment path exists yet to gate. Tracked. |
| **INV-6** | **Unattested honesty.** Absent/ambiguous chart data → field marked unattested; generated documents render the existing honest placeholders; no default, no population prior, no guess (existing `StudyFact` behavior extended to imports). | Test: bundle lacking an element yields unattested, never a fabricated value. | **Implemented + tested.** `test_absent_elements_yield_no_proposal_never_a_guess`, `TestSexUnattested`. |
| **INV-7** | **Read-only toward the EHR.** The ingestion module contains no code path that constructs FHIR write/update/transaction requests. SMART scopes (when the real launch lands) are requested read-only (`patient/*.read`-class); this pass mocks the launch and accepts bundles only. | Code review gate + scope assertion at token exchange (future). | **True by absence** (no write path exists). Scope assertion deferred with the real SMART launch. |
| **INV-8** | **No PHI at rest or in logs.** Logs carry field ids, resource types, FHIRPaths, confidence, hashes, actors, timestamps — never values from the chart. Structured `Patient.name`/`identifier`/`address`/`telecom` are excluded and `birthDate` is consumed into age then discarded; **free-text** values are treated as tainted and pass a hardened, fail-closed leak-guard (B1). **No raw chart bundle is retained on disk** — it is mapped in memory and discarded; the case store persists only coded identifiers + confirmed intake. | Never-extract tests; `TestLeakGuardHostile` (guard must fire on PHI in `Condition.code.text` / `dosageInstruction.text`, case/format variants, contained + RelatedPerson names, and fail closed when no Patient basis exists); privacy-log test asserts no chart value recorded. | **Implemented + tested** (structured **and** free-text). *Encrypted-at-rest is not a current gap: nothing retains the raw bundle, so there is no chart-at-rest to encrypt. If a bundle-retention feature is ever built, encryption-at-rest ships with it — see the note below.* |

## 4a. Phase-1 substrate (what is actually built)

Implemented and covered by the engine suite (120 tests):

- **Import returns proposals only; intake is never auto-written** (INV-2 / HC1).
- **Single-subject enforcement**: a bundle with more than one `Patient` is refused.
- **Never-extract + free-text taint** (INV-8, B1): structured identifiers excluded; any value drawn from free text passes a hardened, fail-closed leak-guard.
- **Clinical-safety filters**: an active home-med order can never become the investigational agent (B2); refuted / entered-in-error / inactive diagnoses are dropped (M4); performance status is the most recent observation, dated, not bundle-order (M3); `first_treatment_date` is emergency-route-only and drug-scoped (M2).
- **Named, durable confirmation trail** (partial INV-2/HC5, B3): the confirm step carries a confirming-clinician name and a per-field `chart-confirmed` vs `manual` provenance; both persist on the case (`confirmations`, `field_provenance`) and survive reload. This is **not** a Part-11 signature and executes no gate — it is an attribution record, and the frontend requires a name before applying chart values.
- **Engine egress boundary** (partial INV-4): no engine module except the single sanctioned concept-reviewer imports an outbound client, and that reviewer never imports the ingestion path (asserted by test).

Deferred (tracked, not claimed as present): the `DeidentifiedPredicates` egress gateway (INV-4); `promote()` mode transitions and the enrollment path (INV-5); the real SMART OAuth launch with read-only scope assertion (INV-7 tail). (The typed `commit_profile` / per-field re-confirmation gate, INV-3, is being implemented this session — see `commit-profile-design.md`.)

**On "encrypted at rest" (INV-8 tail — re-scoped 2026-07-10, honestly).** An earlier draft promised optional encrypted local retention of the raw chart bundle. That promise is re-scoped rather than built, because it describes a protection for data the system does not hold: the FHIR bundle is parsed in memory and discarded after proposals are produced; the on-disk case store contains only coded identifiers and the physician-confirmed intake, never raw chart values. Building encryption-at-rest now — the only pure-stdlib option being Windows-only DPAPI via `ctypes` — would be effort spent guarding a file that is never written. If a bundle-retention feature is ever added (e.g. to support re-review of the source chart), encryption-at-rest is built and tested **together with it**, against real retained data. Claiming it now would repeat the exact claims-vs-code credibility gap the Phase-13 review flagged.

## 5. Concrete backend guarantees (the build checklist)

1. `fhir_ingest.parse_bundle(bundle_bytes) -> list[ExtractionProposal]` — pure, stdlib-only, no I/O (INV-1). Malformed input → structured error, never a partial guess.
2. `ExtractionProposal` carries `field_id`, `proposed_value`, `provenance` (resource type, FHIRPath, coding system, in-bundle source ref), `confidence` — and is **not** accepted anywhere `Study.raw` values are accepted (INV-2).
3. The never-extract list (mapping spec §1.3) is a code-level filter applied before proposals are built; `Patient.name`/`identifier`/`address`/`telecom`/`birthDate` values cannot appear in any proposal, log, or error message.
4. Chart-confirmation writes an attribution record `{actor, field_ids, from_chart, at}` (the `confirmations` trail); `commit_profile` computes the SHA-256 of the canonicalized confirmed intake as the input-of-record and stores per-field value **hashes** (never values — INV-8), stamped onto every ProvenanceRecord and Document at generation (INV-3). No bundle purge step exists because no raw bundle is retained (INV-8, re-scoped §4a).
5. Generation refuses any input that is not a committed, hashed profile; unconfirmed anything → `GateViolation` (fail closed, HC1).
6. All outbound matching/generation-support queries route through the single egress gateway taking `DeidentifiedPredicates` only; destination allowlist enforced; every egress audit-logged (INV-4). Small-cell caution: predicates are limited to condition + drug + age_band + sex — no geography, no dates — so a rare-disease query cannot be sharpened into a re-identification key by the query string itself.
7. Mode is a persisted, logged property of the case; `promote()` demands a recorded legal basis (§164.508 authorization / §164.512(i)(1)(i) waiver / treatment-disclosure determination) (INV-5).
8. No EHR write-back exists in the codebase (INV-7). No external CDN, no telemetry, no analytics beacon in the import/confirmation UI (FRAME constraint: no external CDNs — which here is also a privacy property).
9. Every **implemented** invariant (§4a) ships with its named test in the engine suite (120 tests green). Guarantees 4, 6, and 7 describe deferred design (`commit_profile`, the egress gateway, `promote()`) — see the Status column in §4; they are not asserted as present.

## 6. What this machine deliberately does not do

It does not de-identify for export (no §164.514 expert-determination tooling — out of scope); it does not manage the patient's §164.508 authorization document beyond recording that one exists and where; it does not decide the legal basis — it demands that a named human record one. The machine's whole job is narrower and harder: make the safe path the only path that compiles.
