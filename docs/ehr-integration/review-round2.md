# Re-Review (Round 2) — EHR/SMART-on-FHIR Ingestion (Phase 13)

**Reviewer stance:** same standalone adversarial persona as round 1 (clinical-informatics physician + HIPAA privacy officer), fresh context. Charge: verify claimed fixes, catch revision-introduced defects, render a verdict.
**Method:** full re-read of `engine/ossicro/fhir_ingest.py`, `engine/tests/test_fhir_ingest.py`, `app/server.py`, `app/static/index.html`, `docs/ehr-integration/privacy-state-machine.md`; test suite run (**120 passed**); 14 fresh hostile bundles executed against `extract_proposals`; live-server round-trip on 127.0.0.1:8765 (multi-patient refusal, no-actor backward compat, named-actor confirmation persistence, provenance spoof, and the full non-EHR generate/check/package flow — 8 documents, check and package green). Every finding below marked **[confirmed]** was reproduced by executing code.

## VERDICT: FIRE after small patching

Patches 1 and 2 below are **blocking-mechanical** — each is a one-condition code change with a deterministic test, but each closes a real reproduced hole and must land (with its test) before fire. Patches 3–6 are non-blocking mechanical cleanups. The revision's architecture (taint + fail-closed guard, staged-candidate restriction, named durable confirmation, honest Status column) is sound; nothing here requires design rework.

---

## Round-1 findings — verification status

| # | Claimed fix | Status |
|---|---|---|
| B1 | Free-text taint + hardened fail-closed leak-guard | **Verified real.** Guard fires on name-in-`Condition.text`, case mismatch, `dob 3/14/1968`, contained-Patient and RelatedPerson names; no-Patient tainted values fail closed; clean coded diagnosis survives (`TestLeakGuardHostile`, re-reproduced by hand). One taint-propagation site was missed — **NEW-1** (blocking). |
| B2 | Drug candidates restricted to staged orders; RxNorm inversion; multi-candidate cap | **Verified real.** `active`+`order` excluded; lisinopril-before-draft yields the draft; active-only bundle yields no drug; `drug.name` medium always; multi-candidate caps route. The new predicate admits dead-status plan-intent orders — **NEW-2** (blocking). |
| B3 | Named confirming clinician + durable `confirmations`/`field_provenance`; doc overclaim corrected | **Verified real.** Frontend requires a name before Apply (`index.html:1123–1128`, `1236–1253`); server persists actor + per-field provenance, values never copied into the record; survives round-trip and restart (`_save_case`/`_normalize_case`); PHI-free (checked live). Doc §4/§4a honestly marks INV-3/4/5 DEFERRED. Residuals: no test covers the substrate (**NEW-4**), provenance is client-spoofable (**note N-2**). |
| M1 | Multi-patient bundle refused | **Verified real** (engine `BundleError` + live 400). Residual: a single-Patient bundle whose Condition `subject` references an *external* patient is still mapped — **NEW-5** (minor, tracked). |
| M2 | first_treatment emergency-gated, drug-scoped, whole-word | **Verified real** (`TestFirstTreatmentGating`, re-reproduced). Residual: token-set *intersection* still single-token false-matches, and can grant HIGH — **NEW-3** (minor). |
| M3 | Recency sort + date disclosed | **Verified real** (`TestObservationRecency`; stale ECOG 0 loses to current ECOG 3, dated). |
| M4 | Condition status filtering both branches | **Verified real** (`_condition_ok` applied before the mCODE/active split; `TestConditionStatusFiltering`). |
| M5 | Bulk confirm-all removed | **Verified real.** Button gone; copy states "deliberately no bulk-accept"; per-field checkboxes + named-clinician gate remain. |
| M6 | Provenance stamps branch-accurate | **Verified real** (`TestProvenanceAccuracy`: expectedSupplyDuration named; Practitioner fallback labeled Practitioner; multi-condition note generic). |
| M7 | Egress boundary test in lieu of gateway; INV-4 re-documented deferred-but-guarded | **Verified real.** `TestEngineEgressBoundary` sweeps all engine modules; `review_claude.py` is the sole sanctioned egress and provably never imports `fhir_ingest`. No `commit_profile`/`promote`/`DeidentifiedPredicates` anywhere in code — doc's DEFERRED claims are exact. |
| MIN1 | coded_id 3→8 hex | **Verified real** (code + test regex `[0-9A-F]{8}`). |
| MIN2 | RxNorm de-dup (partial) | **Verified real**; problem-list preference honestly deferred. |
| MIN3 | `gender="unknown"` unattested | **Verified real** (`TestSexUnattested`). |
| MIN4/NIT | Deferred as disclosed | **Verified** — acceptable-for-prototype per round 1. |
| T1 | Hostile-bundle battery | **Verified real.** 23 new tests across 9 hostile classes; deleting `_apply_leak_guard` would now fail multiple tests. |

**14 of 14 round-1 code findings verified fixed or honestly re-scoped; none regressed.** Non-EHR flow (generate → check → package) exercised live: no regression from the `_new_case` keys or the intake-handler change; old persisted cases are backfilled by `_normalize_case`.

---

## NEW findings (introduced or exposed by the revision)

### NEW-1. **MAJOR — stage-observation taint is discarded; PHI in stage free text leaks past fail-closed** — [confirmed]

`engine/ossicro/fhir_ingest.py:371`: `stage, stage_dt, _ = _latest_observation(bundle, LOINC_STAGE_GROUP)` — the third return value (the taint flag) is thrown away, while the ECOG line right below it (`:372`) and the disease-status line in prior-therapies (`:447–449`) both propagate it. The stage text is composed verbatim into `patient.diagnosis`.

**Repro (executed):** bundle with a Patient carrying *no* name/identifier/birthDate (so `has_basis` is False — exactly the population fail-closed exists for), a coded Condition, and a stage Observation whose `valueCodeableConcept.text` = "Stage IV - per note, Harriet Quimby MRN 88-1234" → proposal value `"Cholangiocarcinoma (SNOMED CT 70179006). Stage: Stage IV - per note, Harriet Quimby MRN 88-1234 (as of 2026-06-01)."` — name and MRN in the output. The identical bundle with the PHI in an *ECOG* text is correctly dropped (control, executed). With a normal identifier-bearing Patient the word-guard still catches the name, so the exposure is narrow — but it is precisely the B1 fail-closed corner the revision claims to have sealed.

**Fix (one line + one test):** capture and propagate — `stage, stage_dt, stage_tainted = _latest_observation(...)` then `tainted = tainted or stage_tainted`. Add the repro above to `TestLeakGuardHostile`.

### NEW-2. **MAJOR — `_candidate_drug_requests` resurrects dead orders: `cancelled`/`entered-in-error`/`completed` + `intent=plan|proposal` qualify as the EA candidate** — [confirmed]

`engine/ossicro/fhir_ingest.py:597–604`: the predicate is `status in ("draft","on-hold") OR intent in ("proposal","plan")` — the intent arm ignores status entirely. Round 1's own fix language ("restrict to `intent in (proposal, plan)` or `status in (draft, on-hold)`") was implemented literally, but the pre-revision code at least required a not-closed status; the revision dropped that guard, so a *dead* staged order now qualifies where it previously did not. This is the M4 bug (resurrecting quarantined records) re-created in the drug section.

**Repro (executed):** (a) `status=cancelled, intent=plan` "Abandoned-Agent" as the only MR → `drug.name = "Abandoned-Agent"` and its SNOMED route at **high** (single candidate, no cap). An abandoned EA idea becomes the investigational agent. (b) `status=entered-in-error, intent=plan` → proposed. (c) cancelled plan listed before the real draft → `drug.name = "Abandoned-Agent"` wins the first-candidate slot (medium + ambiguity note — mitigated but still wrong-first).

**Fix (one condition + tests):** `if status in ("draft", "on-hold") or (intent in ("proposal", "plan") and status not in ("cancelled", "completed", "stopped", "entered-in-error")):`. Add cases (a)–(c) to `TestDrugCandidateSafety`. (Note `active`+`plan` and `active`+`proposal` correctly remain candidates — verified by execution; the restriction did **not** over-narrow the legitimate staged cases, and the sample's `drug.route` stays high/single-candidate.)

### NEW-3. **MINOR — first_treatment token *intersection* is any-single-token; grants HIGH on a wrong date** — [confirmed]

`engine/ossicro/fhir_ingest.py:717–719`: `_norm_tokens(a) & _norm_tokens(b)` matches on one shared token, and `coded_match` is display-token overlap (not code equality) yet earns **high** (`:731`). Executed: drug "sodium bicarbonate (investigational protocol)" + completed admin "sodium chloride 0.9% injection" (RxNorm-coded) → `first_treatment_date = 2026-06-15` at **high**; drug "Cytoravir (investigational)" + admin text "investigational product, other study" → matched at medium on the token "investigational". Emergency-route-only and physician-confirmed, but a HIGH badge on a wrong statutory-trigger date is the exact badge-trust failure M5 was about.
**Fix:** require token containment (`drug_tokens <= admin_tokens or admin_tokens <= drug_tokens`) rather than intersection, and never grant high without RxNorm **code** equality (the candidate's code is available at the `_extract_drug` call site — return it alongside the name); otherwise cap medium.

### NEW-4. **MINOR — §4a overclaims test coverage for the confirmation substrate** — [confirmed by grep]

`docs/ehr-integration/privacy-state-machine.md` §4a opens "Implemented and covered by the engine suite (120 tests)" over five bullets, but no test in the suite exercises `actor`/`confirmations`/`field_provenance` (grep across `engine/tests/`: zero hits). I verified the behavior manually against the live server — it works — but round 1's central credibility complaint was claims-without-tests, and this is one, freshly minted.
**Fix:** add one test to `TestImportEndpoint` (POST intake with `actor` + `provenance`, assert the persisted `confirmations` record and `field_provenance` map, assert values absent from the record and no-actor POSTs still work), or reword the §4a preamble.

### NEW-5. **MINOR (tracked) — external-subject resources still chimera-map** — [confirmed]

`extract_proposals` refuses >1 top-level `Patient`, but a bundle with one Patient plus a Condition whose `subject` is `Patient/P2-external` (unresolvable, different patient) is still mapped into this patient's `patient.diagnosis` (executed). Round 1's M1 fix option named subject-filtering; the revision implemented refusal only — and the doc claims exactly that, so this is honest scope, not overclaim. Track subject-reference filtering (cap medium + disclose when `subject` is absent or unresolvable; drop when it resolves elsewhere).

### NEW-6. **MINOR — leak-guard over-drop: real but fail-safe; one pathological case** — [confirmed]

Charge-1 probes executed: patient surname **"Young"** kills a legitimate "Glioblastoma, young-adult onset variant" diagnosis; surname **"Case"** kills a dose text containing "in case of vomiting"; a practitioner sharing the patient's surname loses `investigator.name`. All drop *toward safety* with a disclosed reason in `never_extracted` — acceptable for a prototype, and the ≥3-char word threshold is reasonable. The pathological case: a **single-token 2-char family name** (e.g., "Ng", common Vietnamese/Cantonese surname, no given name in the resource) enters `subs` (≥2-char, *substring*-matched) and nukes every value containing the letters "ng" — including the fully **coded** display "Cholangiocarcinoma" (executed). Also: when a Patient exists but carries no harvestable identifiers, the fail-closed reason says "no Patient resource in the bundle" — inaccurate message.
**Fix:** only add a full-name string to `subs` when it is multi-token (contains a space); single tokens are already covered by `words` with the ≥3 whole-word rule. Reword the fail-closed reason to "no verifiable patient identifiers in the bundle". Optionally add a "Young"-style false-positive test documenting the intended conservative behavior.

### Notes (no patch demanded)

- **N-1.** A hostile `coding.display` carrying a name is untainted by design (controlled-terminology trust); with any identifier-bearing Patient present the word-guard still catches it. Residual only in no-basis bundles. Accepted tradeoff — worth one sentence in the mapping spec.
- **N-2.** `provenance` is client-asserted: a hand-typed value POSTed as `chart-confirmed` is recorded as `from_chart` (executed live). Single-user localhost prototype, attribution-not-signature is already the doc's framing — note it in §4a's wording, don't build server-side verification now.
- **N-3.** A 2-char *given* name alone in free text ("counseled Jo at home") is below the word threshold and not caught — inherent heuristic depth, matches the guard's documented scope.

---

## Mechanical patches (verdict rider)

Blocking (must land with tests before fire):
1. `fhir_ingest.py:371` — propagate `stage_tainted` into the diagnosis taint (NEW-1) + `TestLeakGuardHostile` case.
2. `fhir_ingest.py:597–604` — exclude dead statuses from the intent arm of `_candidate_drug_requests` (NEW-2) + three `TestDrugCandidateSafety` cases.

Non-blocking (same PR if cheap, else tracked):
3. First-treatment match: containment not intersection; high only on RxNorm code equality (NEW-3).
4. One `TestImportEndpoint` test for `actor`/`confirmations`/`field_provenance` round-trip, or soften §4a's "covered by the engine suite" (NEW-4).
5. Multi-token-only `subs` + corrected fail-closed message (NEW-6).
6. Track subject-reference filtering as the M1 tail (NEW-5).

## Reply from the team

All six patches applied by the orchestrator; engine suite **120 → 128 green**
(+8 round-2 regression tests). The two blocking findings were both real and both
fixed:

- **NEW-1 (stage taint dropped) — CONCEDED, fixed.** `stage, stage_dt, stage_tainted = _latest_observation(...)`; `tainted = tainted or stage_tainted or ecog_tainted`. Test `test_stage_observation_free_text_fails_closed` plants a name+MRN in a stage-observation text with a no-basis Patient and asserts the diagnosis is dropped and "Quimby" never appears.
- **NEW-2 (dead orders resurrect as EA candidate) — CONCEDED, fixed.** `_candidate_drug_requests` now excludes `_CLOSED_MR_STATUSES` (`cancelled`/`completed`/`stopped`/`entered-in-error`) from the intent arm. Tests: `test_cancelled_plan_is_not_candidate` (4 dead statuses), `test_dead_plan_does_not_win_first_slot`, and `test_active_plan_remains_candidate` (guards against over-narrowing — the legitimate `active`+`plan` case still maps).

Non-blocking, also fixed this pass:
- **NEW-3 — fixed.** first_treatment now matches by RxNorm **code equality** (the only path to high) or whole-token **containment** (`drug ⊆ admin` or `admin ⊆ drug`), not single-token intersection. `_extract_drug` returns `(name, code)`; the code threads to the matcher. Tests: `test_shared_single_token_does_not_match`, `test_high_only_on_rxnorm_code_equality`.
- **NEW-4 — fixed.** `test_named_confirmation_persists_and_is_phi_free` covers the actor/`confirmations`/`field_provenance` round-trip, value-freeness, and no-actor backward compat. §4a's "covered by the engine suite" is now true.
- **NEW-6 — fixed.** Only multi-token names enter `subs` (single tokens go to the ≥3-char whole-word set), so a 2-char surname ("Ng") can no longer substring-drop "Cholangiocarcinoma"; test `test_two_char_surname_does_not_nuke_coded_term`. Fail-closed message corrected to "no verifiable patient identifiers in the bundle."

Tracked (honest scope, not fixed this pass):
- **NEW-5** — subject-reference filtering (a Condition whose `subject` points at an external patient still maps). The revision implemented multi-patient *refusal*, which the doc claims exactly; subject-filtering is the M1 tail, tracked for the SMART-launch pass.
- **N-1 / N-2 / N-3** — accepted tradeoffs (coding.display trust; client-asserted provenance on a single-user localhost prototype; sub-3-char given names below heuristic depth), each already matching the doc's framing.

Verdict accepted: **FIRE after small patching** — patches landed, re-verified, no new regressions.
