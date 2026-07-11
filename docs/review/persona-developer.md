# OSSICRO Review — Persona: Developer / Maintainer

**Reviewer role:** an engineer inheriting this codebase, responsible for correctness, security, and upkeep.
**Method:** static read of `engine/ossicro/*`, `app/server.py`, `app/static/index.html`, `engine/registry/*`, `docs/*` and the five wave-review memos; one read-only test run.
**Test run:** `python -m pytest engine/tests/ app/tests/ -q` → **336 passed in 2.00s** (matches the claim).
**Hard-line verdict:** No drafts-only / no-PHI-egress / auto-decision violation found in the shipped code. Live egress is doubly disabled (`_LIVE_EGRESS_ENABLED=False` plus an unimplemented live branch that raises), every deliverable path is fail-closed behind `require_committed`, gates raise `GateViolation` and no config flag bypasses them, and no endpoint sends/signs/submits. The risks below are tech-debt and a standing deployment precondition, not breaches.

---

## 1. INVENTORY — what the codebase actually is

**Shape.** ~11.5k LOC. A pure-stdlib engine (`engine/ossicro/`, 24 modules) + a stdlib `http.server` backend (`app/server.py`, 2092 lines) + a single 3366-line inlined SPA (`app/static/index.html`) + JSON registries (`engine/registry/`: rules, documents, gates, routes) + synthetic fixtures (`engine/fixtures/`).

**Engine modules I read and what they own:**
- `profile.py` — INV-3 committed-profile: canonicalization, domain-separated SHA-256 field/profile hashes, pending-field derivation, commit/confirm gate (blank actor → `GateViolation`), `require_committed` (fail-closed).
- `egress.py` — INV-4 gateway: closed `DeidentifiedPredicates` frozen dataclass, allow-list, query decomposition + ICD-10 roll-up, greenlight flag off, audit on every call.
- `audit.py` — append-only, hash-chained trail (`prev_hash`/`rec_hash`, `verify_chain`), flat value-free detail shape enforced, frozen read views.
- `matching.py` — registry-search organizer: matched/unmatched/unverifiable criteria, no score/rank, absence framing, v1-kind filter.
- `pipeline.py` — cheapest-first, escalate-only check composition; a reviewer exception escalates to red, never clears.
- `clocks.py` — working-day/calendar arithmetic on given anchors, never `now`.
- `gates.py` — record-only human sign-offs, role-vs-gate enforced, `finalize` refuses ungated advance.
- `pdf_3926.py` — hand-assembled watermarked PDF + FDF (field map flagged UNVERIFIED); `generate.py`, `ea_generators.py`, `assemble.py`, `check.py`, `rules.py`, `validate.py`, `review_port.py`/`review_claude.py`, `fhir_ingest.py`.

**Backend API surface:** case CRUD, `/intake` (schema-validated), `/generate` + `/package` + `/form3926.{pdf,fdf}` + `/match` (all INV-3 gated), `/profile/commit|confirm`, `/signoff`, `/fhir/import` (maps only), `/release` + `/manufacturer/inbox` (opaque `release_id`), `/patient-link` + `/api/patient/{token}` (opaque token, no enumeration), `/promote` (INV-5), `/cro/board`, `/audit`. Case store is disk-backed JSON with atomic tmp+fsync+replace writes and a corruption-skipping loader.

**Guarantees actually enforced in code (not just documented):** fail-closed generation gate; append-only tamper-evident audit; closed egress vocabulary with construction-time shape refusal; schema-only intake ingress; escalate-only review coupling; localhost-only bind.

## 2. ASSESSMENT — what serves the maintainer, and where it is weak

**Genuinely strong.** This is unusually disciplined code for a prototype. The hard lines are enforced structurally, not by convention: `GateViolation` fails closed, `require_committed` is the single chokepoint on every deliverable, the egress struct rejects bad shapes at construction, and the audit chain is verifiable. The wave-review memos are real adversarial reviews with mutation testing, and the fixes landed and are tested (I re-derived several). Comments explain *why*, and the INV-8/HMAC/residual-risk limits are documented honestly rather than hidden. A maintainer can trust the stated invariants.

**Where it is weak for me as maintainer:**

1. **The whole security model rests on one module constant with no code guard.** `HOST = "127.0.0.1"` (server.py:163) is the *entire* thing standing between "safe synthetic pilot" and "full unauthenticated PHI-class surface exposed to the network." Every review memo restates the standing rule ("no bind change / port-forward / tunnel until INV-7 auth"), but nothing in the code enforces it — a one-token edit to `"0.0.0.0"`, or an env override a future contributor adds, silently exposes `GET /api/case/{id}` (full intake), `/cro/board` (enumerates every `case_id`), and every patient token. This is the single highest-risk gap for a maintainer because it is a one-line regression away and there is no tripwire. (See FINDING 1.)

2. **Field hashes are unkeyed; the commit object is not PHI-safe at rest.** Documented candidly in `profile.py:10-22`, but a real integrator who flips this to real PHI before the HMAC/INV-7 work inherits an offline-enumerable store. The honesty is good; the trap is real.

3. **A registry document requires intake fields that the intake schema cannot supply.** `drug-accountability-log` is a route-3926 document and its generator consumes `drug.lot_numbers` / `drug.dispensing_entries`, but neither is in the routes.json intake schema — so the sample fixture carries them (and `/intake` *rejects* them, 400), yet no real user flow can ever populate them. The doc renders permanently blank on those spans. (See FINDING 2.)

4. **Deferred backlog is real and mostly MINOR, but scattered.** No single tracked list; it lives across five memos as "ACKNOWLEDGED, deferred." Consolidated in FINDINGS 5-10.

5. **Docs drift.** The top-level `README.md` still describes an earlier system (60-doc registry, "9/9 tests pass," no mention of the app/personas/INV-3) — actively misleading to someone onboarding. (See FINDING 4.)

6. **Self-acknowledged rubber-stamp risk in tests.** The reviewers themselves flagged the match mini-eval's recall/precision arithmetic as "decorative" (sits on top of an `assertEqual` that already forces 1.0) and retrieval-only. Not dangerous, but it is the one place a green number means less than it looks. (See FINDING 9.)

## 3. FINDINGS

**FINDING 1 — [LARGER-ISSUE] [MAJOR] The localhost-only guarantee has no code enforcement.**
`app/server.py:163` `HOST, PORT = "127.0.0.1", 8765`; `main()` binds it directly at :2080. The entire access-control posture (every review memo's "no bind change until INV-7") is a naked module constant. `GET /api/case/{id}` returns the full intake, `/api/cro/board` enumerates all `case_id`s, and `GET /api/case/{id}` leaks `patient_token` — all unauthenticated. Why it matters to me: this is the one regression that turns a safe pilot into an open PHI-class surface, it is a one-line edit or a future `os.environ.get("HOST")` convenience away, and nothing warns. Direction: add a code-level guard in `main()` — refuse to start on a non-loopback bind unless an explicit `OSSICRO_ALLOW_NONLOCAL_BIND=1` *and* an auth backend are present (fail closed, print the INV-7 reason), so the standing rule is enforced by the program rather than by memory. Cheap now, and it makes the deferral honest.

**FINDING 2 — [LARGER-ISSUE] [MINOR] `drug-accountability-log` requires intake fields absent from the schema.**
`engine/registry/routes.json` route-3926 includes `drug-accountability-log`; its generator (`ea_generators.py:883-884`) maps `drug.lot_numbers` and `drug.dispensing_entries`, and `documents.json:428` lists them as `required_fields`. But `routes.intake_fields()` has neither (verified: sample fields not in schema = `['drug.dispensing_entries', 'drug.lot_numbers']`), so `POST /intake` *rejects* them with a 400 (the MAJOR-1 schema-only guard), and the SPA's `applySampleFields` iterates only `S.schema` and silently skips them. Net effect: the two fields exist only in the fixture; a real physician flow can never fill them, so the drug-accountability log always renders those spans blank while claiming them required. Why it matters: it is a latent completeness bug in a generated regulatory document, masked because only the fixture (not the live flow) exercises them. Direction: either add both fields to `routes.json` `intake_fields` (making the fixture and the doc coherent — but re-baseline the ledger tests) or drop them from the generator + `documents.json` required set if the accountability log is out of route-3926 scope. Decide, don't leave the half-wired state.

**FINDING 3 — [LARGER-ISSUE] [MINOR] Unkeyed field hashes — commit store is enumerable, must not meet real PHI.**
`engine/ossicro/profile.py:150-168` — profile/field hashes are domain-separated but **unkeyed** SHA-256. As the module docstring states plainly (:10-22), a low-entropy value (sex, age, a date, a coded diagnosis) is recoverable by offline enumeration of `field_hashes`/`staged`/`history`. Acceptable for synthetic fixtures; a trap for the first integrator who points it at real PHI. Direction (already prescribed in-file): key with HMAC-SHA256 under a server-side secret held outside the case JSON, riding the INV-7/auth work; pending-detection and revert-equality are unchanged. Keep the honest docstring until then. Flagging so it stays on the maintainer's radar as a hard precondition, not a nice-to-have.

**FINDING 4 — [SMALL-FIX] Stale README misrepresents the built system.**
`README.md:14` states the engine is a "60-document registry + 8 gates … `python -m ossicro.cli demo`; **9/9 tests pass**." The shipped system is the route-3926 MVP with an HTTP backend, four personas, INV-3/4/5, and **336** passing tests; the README table (dated 2026-07-09) predates all of Waves 1-5 and never mentions `app/server.py`. At minimum correct the false test count: change `**9/9 tests pass**` to `**336/336 tests pass** (\`python -m pytest engine/tests/ app/tests/ -q\`)`. (The fuller table rewrite is a larger doc task — see note — but the "9/9" figure is a concrete, unambiguously-wrong string safe to fix now.)

**FINDING 5 — [LARGER-ISSUE] [MINOR] `_save_case` failure is unhandled on the commit/confirm/signoff/intake POST branches.**
`app/server.py` — the commit (:1988-1991), confirm (:2021-2024), signoff (:1970-1973) and intake (:1866-1896) branches persist inside `_LOCK` with no try/except, unlike `/generate` (:1910-1923). A disk-full or permission error after the in-memory mutation (including a freshly-appended audit record) raises out of `do_POST` with no HTTP response, and a later restart drops the un-persisted record → memory/disk divergence. Already ACKNOWLEDGED-deferred in wave1-audit-review MINOR-3. Direction: a uniform handler-level `except Exception → 500 {error}` wrapper that reports the divergence honestly; the atomic write itself is correct.

**FINDING 6 — [LARGER-ISSUE] [MINOR] Clock arithmetic split between the engine and the app.**
`app/server.py:1275-1293` computes the 21 CFR 312.33 annual-report window (anniversary + 60 days, with an inline Feb-29 fallback) inside `_enrollment_obligations` rather than in `engine/ossicro/clocks.py` beside its siblings (`ind_30_day_deadline`, `expanded_access_emergency_deadlines`). It is HC3-honest (anchored on the recorded receipt date), so this is placement, not fabrication — but one engine should own all deadline math, or the next clock change gets missed in the app copy. Direction: move it into `clocks.py` as e.g. `ind_annual_report_deadline(fda_receipt_date)` and call it from the server. (wave4-review MINOR-4.)

**FINDING 7 — [LARGER-ISSUE] [MINOR] Patient token leaks into stderr request logs; lookup is a linear non-constant-time scan.**
`app/server.py:1669-1670` (`log_message` writes every request line, `/api/patient/<token>` included, to stderr — a durable capability copy) and `:1100-1112` (`_case_for_patient_token` re-lists the cases dir every request and `==`-compares per case). At 128 bits a timing oracle is impractical and the pilot is tiny, but both are cheap hardenings: mask `/api/patient/...` in `log_message`, and build a `{token: case_id}` index with `hmac.compare_digest`. (wave4-review MINOR-2/3.)

**FINDING 8 — [LARGER-ISSUE] [MINOR] Deliverable export (PDF/FDF) writes no audit record.**
`app/server.py` `_form3926_pdf_bytes`/`_form3926_fdf_bytes` (:928-950) — the filled 3926 is "one email from a submission," yet commit/reconfirm/signoff/bundle_loaded/egress/release/promote all audit while export does not. The team deliberately deferred this because adding a side effect to a GET is a smell. Direction (as they noted): if export-tracking is wanted, model it as an explicit POSTed `export` act or a dedup'd record — a decision to make, not a bolt-on. Recording here for the maintainer's ledger.

**FINDING 9 — [LARGER-ISSUE] [MINOR] Match mini-eval metrics are decorative; no criteria-level labels.**
`engine/fixtures/match_eval.json` + `engine/tests/test_matching.py` — the recall/precision computation sits on top of `assertEqual(returned, expected)`, which already forces both to 1.0, so the metrics can never contradict the assertion, and no eval case labels expected per-candidate `matched/unmatched/unverifiable`, so a `_criteria` regression (e.g. an age-straddle wrongly called matched) passes the eval and is caught only by unit tests. Not a rubber stamp on *retrieval* (the reviewer verified it catches silent unmatched-filtering, a v1-scope leak, and false absence), but the arithmetic overstates what the eval proves. Direction: add per-candidate expected-criteria labels to at least one case; drop or compute-before-assert the metrics. (wave2 MINOR-6, deferred.)

**FINDING 10 — [LARGER-ISSUE] [MINOR] Free-text de-identification in two paths is honor-system.**
The released manufacturer view (`app/server.py:1011-1017`, `indication` = `patient.diagnosis` verbatim, also embedded in the LOA request) and the egress `patient.diagnosis` term-table lookup both pass physician free text. The route schema carries no name/DOB/MRN field, so structured identifiers cannot exist to leak, and the pilot is synthetic — but a physician who types "Jane Doe DOB 1/2/68" into the diagnosis field releases it. Documented residual, same class as the INV-4 residual-risk statement. Direction: a naive identifier lint at release/egress time, or accept as an explicitly-documented residual (it currently is, in wave3 MINOR-4). Named here so it is not forgotten when the pilot goes non-synthetic.

**FINDING 11 — [LARGER-ISSUE] [MINOR] INV-4 live egress branch is a stub — the marquee gateway is not actually built.**
`engine/ossicro/egress.py:421-429` — even with the greenlight flipped, `egress_query(live=True)` raises `EgressDisabled("no live registry client is implemented yet")`. This is correct and safe today (deliberate, doubly-guarded), but a maintainer should know the "de-identified egress gateway" advertised as done in BUILD-PLAN is the *validation wall* plus a mock adapter; the outbound HTTP client at the GREENLIGHT MARKER remains to be written, and that build (allow-listed registry APIs, real error handling, rate/volume mitigation for the documented linkability residual) is non-trivial. Not a defect — a scoping fact to carry.

---

### Summary of the non-negotiables (verified held)
- Drafts-only: every generated artifact is DRAFT-watermarked / gate-noticed; `finalize` and the gates refuse programmatic advance; no send/sign/submit endpoint exists.
- No-PHI-egress: `_LIVE_EGRESS_ENABLED=False` + unimplemented live branch; only the closed `DeidentifiedPredicates` struct crosses; `TestEngineEgressBoundary` sweeps every engine module for outbound imports.
- Nothing auto-decided: `require_committed` fail-closed on all deliverables; escalate-only pipeline can never clear a gate; every named-human act (commit, signoff, release, promote, patient-link) requires a non-empty string actor and is audit-logged.
