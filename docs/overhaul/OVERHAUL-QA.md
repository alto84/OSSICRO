# OSSICRO Overhaul — standalone adversarial QA

**QA role:** independent adversarial verifier (not the builder). **Date:** 2026-07-11.
**Method:** read `OVERHAUL-PLAN.md` + `docs/review/INVENTORY.md`, then verified every claimed
closure against the code — static reads, targeted greps, and **live adversarial probes**
(ledger state machine, promote refusal matrix, bind-guard matrix, obligations anchors,
rendered-document markers). The server was never started; :8765 was never bound
(probes call `_bind_refusal`, `_promote`, `_sponsor_obligations` in-process).
**Suite:** `python -m pytest engine/tests/ app/tests/ -q` → **582 passed** (baseline was 337).

**Overall verdict (one line):** All nine packages VERIFIED — every MAJOR the plan claims to
close is closed in code with tests, no hard line was breached, no gate weakened, no egress
path opened; two minor internal inconsistencies found (readiness-vs-ledger LOA fact split,
stale HITL worksheet pinpoints), neither blocking.

---

## Per-package verdicts

### Package 1 — Clock split + citation remap (M1, M8, m16, PT-2, PT-6) — **VERIFIED**

- **M1 split:** `engine/ossicro/clocks.py:146` `written_3926_deadline(*, authorization_date)`
  and `clocks.py:161` `irb_emergency_notification_deadline(*, first_treatment_date)` —
  keyword-only anchors named for their statutory events, so a swapped anchor is a TypeError.
  The combined function is deleted; `engine/tests/test_clocks.py:78` and
  `test_ea_features.py:103-104` assert its absence. No production caller remains
  (repo-wide grep: only historical review memos mention it).
- **m16:** `clocks.py:186` `ind_annual_report_deadline` owns the 312.33 arithmetic
  (Feb-29 → Feb-28 documented); `app/server.py:1976-1991` calls it — the app computes no date.
- **M8 remap:** applied via the single-source table `engine/ossicro/citations.py:61-91`
  (rationale→(ii), patient→(iii), dosing→(iv), facility→(v), CMC→(vi), pharm/tox→(vii),
  monitoring→(viii) with the judgment-call note for the human verifier). `routes.json:21-23`
  (dose/route/duration → (iv)), `:25` (monitoring_plan → (viii)), `:76` (site.name → (v)).
  Rendered probe: treatment plan §6 header reads `MONITORING PLAN — 21 CFR 312.305(b)(2)(viii)`;
  `test_ea_generators.py:112-128` pins all eight headers and asserts the old values absent.
- **HITL marker present:** every 312.305(b)(2) row ships `PENDING-HUMAN-VERIFICATION`
  (`citations.py:52-53,66-91`); a row flips only by a human editing the table with name+date
  (`citations.py:9-18`). Rendered documents auto-carry the pending footer
  (`ea_generators.py:343-344`, probe: footer present on the rendered treatment plan).
  `docs/regulatory/CITATION-INVENTORY.md` is the generated inventory; a test keeps it in sync.
- **PT-6:** `engine/tests/test_reconciliation.py` (7 tests) reconciles routes.json clock,
  generator paragraph, `_sponsor_obligations` row, and the engine helper on ONE fact set with
  three deliberately different anchor dates — the tripwire M1 lacked.

### Package 2 — Registry/schema foundations (M5, M7, m7, PT-3, PT-4) — **VERIFIED**

- **M5:** `submission.date` exists (`routes.json:48`), optional, help text says
  "never guessed by OSSICRO"; `derive_as_of` (`ea_generators.py:183`) returns None → MISSING
  markers, never wall-clock (fabrication check passed).
- **M7:** `documents.json` drug-accountability `required_fields` is now `["drug_name"]` only
  (verified by loading the registry).
- **PT-4:** every one of the document entries carries `author_party`; the loader fails closed
  on missing/unknown values (`registry.py:44-53`, `RegistryError`).
- **PT-3:** `engine/registry/claims.json` — six claims each with `tripwire` literal and
  `true_when` conditions; server injects, SPA renders; duplication-grep test in
  `app/tests/test_p2_claims_schema.py`.
- **m7:** `irb-concurrence-request` now in Module 1 of both routes' `ectd_map` (verified by
  loading routes.json).

### Package 3 — AI-review attribution + whole-app egress boundary (B1-full, M12, PT-5) — **VERIFIED**

- **Opt-in is real:** `_live_concept_review_enabled()` reads the env at CALL time
  (`app/server.py:996-1001`); `_select_reviewer` (`:1004-1012`) requires affirmative
  `OSSICRO_LIVE_CONCEPT_REVIEW` AND a key. `test_fhir_ingest.py:1184+` asserts a key alone,
  and every non-affirmative flag spelling, still selects the offline stub.
- **HC5 audit:** `_append_ai_review_audit` fires on the live path in both `_check_payload`
  (`server.py:1464-1465`) and `_package_payload` (`:1504-1506`); stub path writes nothing.
  `review_claude.py` exposes `model_id`/`model_version` (never blank).
- **Disclosure:** `ai-review-offline` / `ai-review-live` claims in `claims.json:34-41`,
  rendered from the server payload on the check screen — never silent either way; the
  `chart-data-stays-local` claim's `true_when` explicitly ties itself to the live-reviewer
  disclosure so it cannot render unqualified while text can leave the machine.
- **PT-5 whole-app sweep:** `test_fhir_ingest.py:1151-1182` exec-loads `app/server.py`,
  walks every repo module it loads, and forbids outbound clients outside the two sanctioned
  modules — with an anti-vacuity assertion that the sweep covered `server.py` and
  `pipeline.py`. Independent grep confirms no outbound import outside
  `egress.py`/`review_claude.py`.
- **M12:** the wiki Part-11 clause table carries the Status column; role-scoped access and the
  e-signature ceremony marked NOT-YET-BUILT; `ai_review`/`ai_review_disposition` logging BUILT
  (`wiki/05-ossicro-system/part-11-and-ai-credibility.md:30-46`).
- `docs/deployment/AI-REVIEW-PRECONDITIONS.md` exists (BAA / zero-retention / named human).

### Package 4 — External-party document model (M2, M15, m4, m5, m6) — **VERIFIED** (one minor inconsistency, F1 below)

- **M2 answer to the QA question — NO, an external-party document does NOT go green on
  physician-entered drafting data alone.** Live probe on the full sample intake with receipt
  facts removed: LOA ledger row = `awaiting-external-party`, `submission_ready=False`, the
  LOA-receipt blocking entry present, and the doc listed in `human_acts_outstanding`.
  With `loa_received_date` + `loa_signatory` recorded → green with the recorded
  signatory/date in the note (`check.py:236-273`; `EXTERNAL_RECEIPT_FACTS` at `check.py:45`).
  LOA registry entry is `author_party: "manufacturer"`, `gate: null` — the green path
  requires the recorded receipt facts, structurally.
- The IRB concurrence path: the request doc is physician-authored but gated by `irb-approval`,
  whose sign-off now demands own-words statement + evidence (Package 5) — the concurrence
  cannot be recorded in 5 keystrokes anymore.
- **submission_ready:** `assemble.py:145-163` blocks the LOA branch without
  `loa_received_date`; the no-IND division-contact branch is the alternative.
  `human_acts_outstanding` enumerated on every payload (`assemble.py:173-195`).
- **Enclosure honesty** (probe): cover letter renders
  "Letter of Authorization (enclosed upon receipt from the manufacturer);".
- Ledger has the fourth bucket everywhere (`check.py:297-302`, `server.py:1360`).
- m5: templates carry the legacy-paths note pointing at `citations.py` as canonical.

### Package 5 — Ethics-gate honesty (M4, M13, M14, m8, m13, m1) — **VERIFIED**

- **M4 answer to the QA question — YES, promote now warns, and on the non-emergency route it
  REFUSES.** Live probe matrix: no ack → **409** with 3 advisories
  (informed-consent, irb-approval, external facts); ack under 20 chars → **400**;
  valid own-words ack → 200 with advisories persisted in
  `case["enrollment"]["advisories"]` and advisory ids in the promote audit detail;
  emergency route → 200 advisory-only (a §50.23/56.104(c) reality). Repeat promote → 409
  (append-only). Code: `_promote_advisories` `server.py:2072`, refusal/override
  `server.py:2156-2172`, persistence `:2174-2196`; ledger surfacing `:1384-1392`.
- **M13:** `_record_signoff` (`server.py:2277-2352`) requires an own-words statement
  (min-length + placeholder check) and asks the evidence keys (stored honestly blank, never
  invented) for the two ethics gates; role-vs-gate matching enforced.
- **m13b:** supersede-never-overwrite; validity checks use `_active_signoffs`
  (`server.py:2059-2069`).
- **M14:** the IRB-request consent sentence is computed from route emergency +
  `consent.timing_attestation` (`ea_generators.py:965-1040`), rendering
  `[[MISSING: consent.timing_attestation]]` when absent — all four states tested.
- **m8:** `Document.advance("final")` on gated documents refuses without the capability token
  held only by `gates.finalize` (`models.py:_GATED_FINAL_TOKEN`) — final-by-code, not
  convention. Gates were strengthened, not weakened.

### Package 6 — EA-profiled ICF (M3, m9, m10, m12) — **VERIFIED**

- **M3 answer to the QA question — YES, the ICF is now expanded-access-framed.** Rendered
  probe: opens "You are being asked to receive treatment with an investigational drug under
  the FDA's expanded access ('compassionate use') program. This is treatment, not a research
  study…" (`ea_generators.py:1125-1129`); the old "asked to take part in a research study"
  opener is absent from the rendered EA ICF. Both 3926 routes swap in
  `informed-consent-form-part50-ea`; the generic form stays registered for non-EA routes.
- Eight 50.25(a) headings byte-identical via `R-ICF-50.25-EA` hashing against the SAME
  registered hashes (`rules.json:93-99`); adequacy explicitly NOT heading-completeness
  (`R-ICF-50.25-ADEQ-EA`, deferred, `rules.json:140-146`).
- 50.25(a)(6) satisfiable: renders `consent.injury_compensation_statement`
  (`ea_generators.py:1251`); EA disclosures A–F (not-approved, supply-may-stop,
  costs 50.25(b)(3);312.8(d), stopping (b)(4), new findings (b)(5), voluntariness restated).
- **HITL marker present:** `ICF_EA_PENDING_BANNER` rendered in the document
  (`ea_generators.py:1116-1118`, probe confirmed), removable only by the qualified human
  review.

### Package 7 — Obligations lifecycle (M10, M11, m2) — **VERIFIED**

- **M10/M11 answer to the QA question — YES, each clock is on its own trigger and the list is
  present without promote.** Live probe, un-promoted case with ONLY
  `submission.first_treatment_date=2026-07-01`: 6 rows returned; 56.104(c) armed
  due **2026-07-09** (5 working days, correctly skipping the observed July-3 holiday and the
  weekend) from `first_treatment_date`; 312.310(d)(2) separately UNARMED on its own trigger
  `emergency_auth_datetime`; 312.33 unarmed on `fda_receipt_date`; 312.310(c)(2) always
  present, armed from `treatment.conclusion_date` with due = the conclusion date itself
  (never date+N; probe: conclusion 2026-08-15 → due 2026-08-15). Empty case → 0 rows.
  Code: `_OBLIGATION_ANCHOR_FIELDS` + `_sponsor_obligations`, `app/server.py:1892-2010`.
- Tracked-subset disclosure rides every checklist payload (`server.py:2201-2202`).
- The reconciliation suite pins these against the generator paragraphs and engine helpers.

### Package 8 — Form 3926 fidelity (M6) — **VERIFIED as shipped-pending (HITL by design)**

- `FORM_3926_ITEMS` in `pdf_3926.py:143` is the ONE item map all three renderers consume;
  consistency tests in `test_pdf_3926.py`. Rendered probe: the 3926 text carries
  "Item numbering pending verification…" (`PENDING_NUMBERING_NOTE`, `pdf_3926.py:119`),
  removable only by filling `FORM_3926_MAP_VERIFIED_BY` (`pdf_3926.py:237`). The human pass
  itself is, correctly, still open — the plan says the human act removes the marker, never
  gates the merge.

### Package 9 — Deployment guardrails (M9, m14, m15, m17, m18, m20) — **VERIFIED**

- **M9 answer to the QA question — YES, a non-loopback bind is refused without auth.** Live
  probe matrix on `_bind_refusal` (`server.py:3148-3162`): `127.0.0.1`/`localhost`/`::1`
  allowed; `""` (INADDR_ANY!), `0.0.0.0`, `::`, `192.168.1.5` all refused; with
  `OSSICRO_ALLOW_NONLOCAL_BIND=1` still refused because `_auth_backend_configured()` is
  hard-coded False (`server.py:3145`) — the override structurally cannot succeed until an
  auth backend exists. `main()` exits 2 on refusal (`server.py:3165-3169`). The suite never
  binds 8765 (reconciliation test imports the module only).
- **m14:** HMAC-SHA256 keyed profile hashes under `app/data/secret.key` (0600, gitignored via
  `app/data/`, never in a case JSON); versioned scheme tags (`sha256-v1` vs `hmac-sha256-v1`)
  with differing prefixes — probe confirmed a profile committed unkeyed FAILS LOUD
  (`require_committed` refuses) against the keyed server, exactly the promised
  fail-loud-not-wrong behavior.
- **m17:** patient token masked in `log_message` (`server.py:2591-2597`); token index +
  `hmac.compare_digest`.
- **m18:** `POST /api/case/{id}/export` writes one `export` audit record (`server.py:3011`).
- **m20:** identifier lint in `egress.py` is escalate-only and names the field + pattern KIND,
  never the matched text (no re-leak channel); never blocks, never rewrites.
- `docs/deployment/DEPLOYMENT-COMPLIANCE.md` exists; coded-id help prefers assigned code.

---

## Hard-line / regression sweep (tried to break each fix)

- **Fabricated values: none found.** `derive_as_of` returns None → MISSING markers;
  `submission.date` is physician-entered ("never guessed"); evidence keys stored honestly
  blank; obligation rows honestly UNARMED; the 312.310(c)(2) due date is the recorded date
  itself; `cite()` raises KeyError on an unregistered key rather than inventing a pinpoint.
- **Weakened gates: none.** Every gate change is a tightening (promote refusal, own-words +
  evidence sign-offs, supersede-not-overwrite, token-gated `final`, fail-closed
  `author_party` loader, four-bucket ledger).
- **Egress: no new path.** Only `egress.py` and `review_claude.py` import outbound clients
  (independent grep + the PT-5 sweep test with anti-vacuity assertions); the live reviewer
  needs an affirmative flag read at call time; the m20 lint is engineered not to re-leak.
- **HITL discipline: intact.** Three pending-marker families (citation footer, ICF-EA banner,
  3926 numbering note) all render on the artifacts and are removable only by a named human
  editing the source of truth.

## New findings (ranked)

**F1 — MINOR (M2 seam): `submission_ready` and the ledger disagree on what "LOA received"
means.** `assemble.py:149-150` unblocks on `manufacturer.loa_received_date` alone;
`check.py:241` requires date AND signatory for green. Probe: date-only intake →
`submission_ready=True` while the LOA row is still `awaiting-external-party` (it does remain
listed in `human_acts_outstanding`, so it is not silent). Follows the plan's literal spec, but
the two surfaces should agree — recommend `assemble` also require the signatory.

**F2 — MINOR (M8 residue): the HITL attestation worksheet is stale.**
`docs/hitl/citation-clock-attestation-worksheet.md:38-40` still lists the PRE-remap
312.305(b)(2) pinpoints ((iii) dose, (iv) site, (vii) monitoring). It is generated output
(`tools/attestation_worksheet.py` reads routes.json, which is corrected), so a regeneration
fixes it — but as committed, a human attesting from this file would initial the old map.
Regenerate before the Package-1 human pass. (Same class, docs-only:
`docs/ehr-integration/fhir-intake-mapping.md:78` still cites (vii) for monitoring.)

**F3 — INFO (M9 edge): `_bind_refusal` allows any HOST string starting `"127."`**
(`server.py:3156`), including a hostname like `127.0.0.1.evil.com` that DNS could resolve
elsewhere. HOST is a module constant, not runtime input, so this is theoretical; an
`ipaddress`-based check would close it for free.

**F4 — INFO (M4/M13 limit): "own words" is enforceable only as min-20-chars + 4 placeholder
fragments** (`server.py:2034-2044`) — a boilerplate sentence passes. Inherent to the problem;
the act is still named, persisted, and audited, which is the actual control.

**F5 — INFO (P7): the two emergency clocks render (unarmed) on non-emergency cases too.**
Pre-existing behavior, not a regression; a route-keyed row set would be cleaner.

## Bottom line

All 15 MAJORs + B1 claimed by the plan are closed in code, tested (582 passing), and none of
the fixes fabricates a value, weakens a gate, or opens an egress path. F1 and F2 are the only
items worth a follow-up commit; neither blocks the overhaul.
