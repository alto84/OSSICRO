# Adversarial Review — EHR/SMART-on-FHIR Ingestion (Phase 13)

**Reviewer stance:** standalone adversarial review; clinical-informatics physician + HIPAA privacy officer persona. No stake in the build.
**Artifacts reviewed:** `engine/ossicro/fhir_ingest.py`, `app/server.py` (`/fhir/import`), `app/static/index.html` (import/confirm surface), `engine/tests/test_fhir_ingest.py`, `docs/ehr-integration/fhir-intake-mapping.md`, `docs/ehr-integration/privacy-state-machine.md`, `engine/fixtures/fhir_sample_bundle.json`, `docs/OSSICRO-CONSTITUTION.md` (HC1–HC6).
**Method:** full code read + 97-test suite run (all pass) + 12 hostile bundles fed to `extract_proposals` directly. Every finding below marked **[confirmed]** was reproduced by executing code, not inferred from reading.

## Verdict

Not shippable, even as a governed DRAFT-only prototype, until BLOCKER-1 through BLOCKER-3 are fixed. The good news is real and worth stating precisely: the auto-extraction→intake gate narrowly holds (the import endpoint provably never writes intake; proposal inputs live outside the intake form and cannot be POSTed untouched; structured Patient identifiers are structurally excluded; birthDate → age-only works; there is no network egress anywhere, so the HC2 outer boundary is intact by absence). But three things an FDA reviewer, IRB, or breach auditor would seize on are demonstrably broken: (1) the never-extract/leak-guard claim is **false for free text** — I extracted a patient's name, MRN, and DOB into proposal values with trivially realistic bundles, and the guard has zero direct test coverage; (2) an ordinary active home-medication order becomes the investigational agent at **high** confidence, and the "Confirm all high-confidence" button will write it into a Form 3926 draft in one click — a patient-safety-class bug; (3) the privacy-state-machine document claims eight invariants "enforced in code, each with a test" while INV-3, INV-4, and INV-5 have neither code nor test, and HC1's *named*-human confirmation and HC5's attribution substrate do not exist — confirmation is an anonymous browser checkbox whose record evaporates on page reload. The gaps are fixable in scope; the overclaiming in the docs is the part that would do lasting credibility damage in front of an auditor, because it reads as the system asserting protections it does not have.

---

## BLOCKER findings

### B1. Free-text PHI passes the never-extract line; the leak-guard is a sieve — **[confirmed]** — real hole

**Vulnerability.** Mapping spec §1.3 hard-excludes "any … free-text note body," and the module docstring claims "a final leak-guard drops any proposal whose value would carry a patient identifier string." Neither is true in code. The mapper extracts free text verbatim into proposal values via `_cc_display` on `Condition.code.text` (`engine/ossicro/fhir_ingest.py:300`, via 139–148), `dosageInstruction.text` as the dose fallback (`fhir_ingest.py:572–573`), `medicationCodeableConcept.text` (547–558), and `Observation.valueCodeableConcept` text (329–336). The leak-guard (`fhir_ingest.py:718–732`) then matches **exact-case substrings** of strings harvested only from top-level `Patient` resources (688–715). It is defeated by:

- **No Patient resource in the bundle** (patient held by external reference — common in problem-oriented exports): forbidden list is empty, guard is a no-op, and the "Deliberately never extracted" UI panel renders empty, giving false comfort.
- **Case mismatch**: EHRs routinely store `QUIMBY, HARRIET` in `Patient.name` while note text says "Harriet Quimby". `f in value` at line 725 is case-sensitive.
- **Format mismatch**: `birthDate` `1968-03-14` does not match "dob 3/14/1968" in a note.
- **Contained resources**: `_entries` (96–102) never descends into `contained`, so a Patient contained inside a Condition contributes nothing to the forbidden list.
- **Anything not on the list**: family-member names, addresses appearing only in narrative, patient nicknames.

**Reproduced.** Bundle with no Patient resource, `dosageInstruction.text` = "240 mg BID; counseled patient Harriet Quimby and daughter Anne at 12 Elm St on 7/1" → proposed verbatim as `drug.dose`. Bundle with `Patient.name` = QUIMBY/HARRIET and `Condition.code.text` = "Metastatic cholangiocarcinoma — pt Harriet Quimby, MRN 88-1234, dob 3/14/1968" → proposed verbatim as `patient.diagnosis`, `never_extracted` reporting name/birthDate as "never extracted" in the same response.

**Failure scenario.** One rushed confirm click and the name/MRN/DOB persists into `app/data/cases/{id}.json` — a store whose own header comment says "no real PHI; coded identifiers only" (`app/server.py:7`, gitignored, but nothing else about it is controlled: unencrypted, no purge, no access control) — and flows into every generated document. A breach auditor finds an identifier-bearing "coded-identifiers-only" store; an FDA reviewer finds a patient name inside a field the mapping spec certifies cannot carry one.

**Fix.** Treat verbatim free text as tainted, not as a value source: (a) stop proposing `.text`/`dosageInstruction.text`/narrative content as values — show them as reference context beside the field (the spec already has this concept for labs, §9); or if text-derived values must stay, (b) make the guard honest: casefold + punctuation-normalize both sides, add date-format variants of birthDate, harvest names from `contained` resources and `subject.display`/`RelatedPerson`, and when no Patient resource is present **refuse to propose any text-derived value** (guard cannot run → fail closed, per the repo's own fail-closed doctrine). Either way, add tests where the guard must actually fire (see T1).

### B2. Any active medication order becomes "the investigational drug" at HIGH confidence — **[confirmed]** — real hole, patient-safety class

**Vulnerability.** `_candidate_drug_request` (`fhir_ingest.py:526–537`) returns the **first** MedicationRequest whose status is not closed and whose intent is in `proposal|plan|order|original-order`. Every active home-med order (`status=active, intent=order`) qualifies. Real charts carry dozens. The fixture only passes because its four prior chemo orders are `completed` and the only open MR is the Cytoravir draft — the happy path hides the bug. Worse, an RxNorm-coded hijacker earns **high** confidence (549–551), and its SNOMED route earns **high** too (583–586); the mapping spec itself says investigational agents *usually lack RxNorm codes* (§4) — so a high-confidence RxNorm-coded `drug.name` is precisely the suspicious case, yet the code rewards it. This also violates the spec's own §1.2 rule: "more than one plausible candidate (all candidates shown; confidence capped at medium)" — implemented nowhere for `drug.*` (nor practitioner, site, or observations; only diagnosis implements it).

**Reproduced.** Bundle with an active lisinopril order listed before the Cytoravir draft proposal → `drug.name = "lisinopril"` **high**, `drug.dose = "10 mg"` (lisinopril's), `drug.route = "Oral route"` **high**, `treatment.plan_id = "TP-LISINOPRIL-…"`. Two of these are then auto-selected by "Confirm all high-confidence."

**Failure scenario.** A rushed physician clicks the bulk button and Applies: the expanded-access request now names the patient's blood-pressure medication as the investigational agent, with a plan ID branded to match. If the physician catches it, trust in the tool dies; if not, a wrong 3926 draft heads toward FDA.

**Fix.** (a) Restrict candidates to `intent in (proposal, plan)` or `status in (draft, on-hold)`; treat `active+order` as an existing therapy, never the EA candidate. (b) Implement the §1.2 multi-candidate cap: >1 open candidate → all shown, medium. (c) Invert the RxNorm heuristic for this field: an RxNorm-coded candidate is *less* likely to be an investigational agent — cap at medium and say why in the path. (d) See B3/M5 on the bulk-confirm button.

### B3. HC1's "named human" and HC5's attribution do not exist; the privacy-state-machine doc claims enforcement that is not in the code — real hole (as claimed), partly acceptable-for-prototype (if re-documented)

**Vulnerability.** The state machine (privacy-state-machine.md §2, §4) specifies `confirm(field_id, actor)` audit events, `HumanConfirmation{field_id, value, named_actor, ts}` as the only path into `Study.raw` (INV-2), a canonicalized profile hash as the generation input-of-record (INV-3), and logged mode transitions with a legal basis (INV-5). In the build:

- Confirmation is an **anonymous checkbox** (`app/static/index.html:1094`). No actor, ever. `POST /api/case/{id}/intake` (`app/server.py:651–672`) accepts fields with no identity attached — contrast the signoff endpoint, which correctly demands `signer_name` (server.py:469–470).
- There are **no confirm/correct/reject audit records at all**. The only privacy-log event is `fhir_bundle_loaded` (server.py:533–544) — and even that omits the `actor` the state machine's own diagram requires.
- **`commit_profile` does not exist.** No profile hash, no re-confirmation on change (INV-3); staleness is an integer rev counter, and a changed field never forces re-confirmation of anything.
- **`promote()` does not exist.** "PREPARATORY_REVIEW" is a hardcoded string in one log line; INV-5 is prose.
- The confirmed-from-chart provenance is a **DOM span** (`index.html:1212–1223`). Reload the page and nothing in the persisted case distinguishes a chart-extracted physician-confirmed value from a hand-typed one — which also guts HC4/HC5 for any downstream document that would want to cite chart provenance, and makes the physician's confirmation act unreconstructable for a Part 11-style audit (HC5: "identity and disposition of the human reviewer" — neither is recorded).

Meanwhile privacy-state-machine.md §4 states each invariant is "enforced in code, each with a test," and §5.9 says "every invariant above ships with its named test." For INV-3, INV-4 (see M6), and INV-5 this is false. The narrow HC1 gate — unconfirmed proposals cannot reach intake through the shipped UI, and the import endpoint never writes intake — genuinely holds and is tested. What does not hold is *named*, *audited*, *durable* confirmation, which is the part HC1/HC5 and this review's charge actually name.

**Fix (choose one, honestly).** Either (a) implement the minimum substrate: the confirm flow POSTs `{actor, field_id, action, value, provenance, confidence, ts}` audit records persisted on the case, plus a committed-profile hash checked by generate; or (b) amend privacy-state-machine.md to state plainly that Phase-1 implements INV-1/2/6/7/8 and **defers** INV-3/4/5 and the named-actor audit trail — with a tracking item. Shipping the doc as-is against this code is the kind of claims-vs-reality gap that turns an audit finding into a credibility finding.

---

## MAJOR findings

### M1. No subject check anywhere → multi-patient bundles produce chimera proposals — **[confirmed]** — real hole

`_of_type` pulls every resource of a type regardless of `subject` (`fhir_ingest.py:105–106`); `_extract_patient` takes `patients[0]` (201); conditions, observations, MedicationRequests, and MedicationAdministrations are never matched to the patient. The state machine explicitly names **bulk-$export files** as a load source (§2) — those are multi-patient by construction. Reproduced: two Patients in one bundle → `patient.age`/`sex` from patient 1, `patient.diagnosis` = patient 2's NSCLC with patient 2's "ECOG 3"; a completed pembrolizumab order whose `subject` points at a different patient reported as this patient's prior therapy. This is simultaneously a correctness bug (wrong chart facts on a federal form) and a privacy bug (patient B's clinical facts in patient A's case).
**Fix.** Resolve the target Patient first; **refuse** bundles containing >1 Patient (or force an explicit selection), then filter every extracted resource by `subject` resolving to that Patient; resources without a subject reference get capped at medium with the ambiguity named in the path.

### M2. `submission.first_treatment_date` proposed from any unrelated completed administration; fires on the non-emergency route — **[confirmed]** — real hole

`_extract_first_treatment` (`fhir_ingest.py:607–635`): when no drug proposal exists, `drug_name` is None and the match filter at line 623 is skipped entirely — **any** completed MedicationAdministration's date is proposed. Reproduced: a bundle containing only a completed morphine administration → `submission.first_treatment_date = 2026-06-15` (medium), on the **non-emergency** route (the `route` argument scopes nothing, contradicting mapping spec §7's "Non-emergency: absent by definition"). Text matching is also first-token substring (`"gem" in "gemcitabine"` class of false positives), so a prior chemo administration can date the investigational agent's first treatment. This field documents the trigger for the §312.310(d) emergency pathway — a wrong date here misdocuments the event that arms a statutory clock (HC3-adjacent: the arithmetic is safe, but the proposed trigger fact is wrong).
**Fix.** No `drug_name` → no proposal, period. Gate the extractor on the emergency route flag. Require coded match or whole-word match; multiple candidate administrations → cap medium and show all dates.

### M3. Clinical facts selected by bundle order, not recency — stale ECOG/stage presented as current — **[confirmed]** — real hole (patient-safety adjacent)

`_observation_value_text` (`fhir_ingest.py:329–336`) returns the **first** status-eligible Observation matching the LOINC code. No `effectiveDateTime` ordering, no recency disclosure. Reproduced: a 2024 "ECOG 0" listed before a current "ECOG 3" → diagnosis narrative says "Performance status: ECOG 0." An EA request understating performance status misrepresents the clinical picture to FDA in either direction (an ECOG 0 patient may look like they don't need expanded access; a stale ECOG 4 could wrongly disqualify). Same code path serves stage group and disease status; disease status at least appends its date (369–371), stage and ECOG do not.
**Fix.** Sort candidates by `effective[x]` descending; always render the observation date into the composed value; >1 candidate → the §1.2 medium cap with all candidates shown.

### M4. `entered-in-error` / inactive mCODE condition becomes the diagnosis — **[confirmed]** — real hole

`_primary_conditions` (`fhir_ingest.py:280–291`): the mCODE-profile branch (282–284) returns profiled conditions with **no clinicalStatus or verificationStatus check**; `verificationStatus` is never read anywhere in the module. Reproduced: an mCODE-profiled condition with `clinicalStatus=inactive` and `verificationStatus=entered-in-error` → proposed as `patient.diagnosis`. Charting errors and refuted diagnoses are exactly what `entered-in-error`/`refuted` exist to quarantine; the mapper resurrects them. (The Observation path does check status at 331 — correctly excluding `entered-in-error`/`preliminary` — but has no test proving it; see T1.)
**Fix.** Exclude `verificationStatus in (refuted, entered-in-error)` in both branches; require `clinicalStatus=active` (or recurrence/relapse) in the mCODE branch too, or disclose the status in the composed value.

### M5. "Confirm all high-confidence" is an automation-complacency footgun — real hole in design, amplified by B2/M3

`index.html:1142, 1176–1181`. One click selects every "high" proposal for writing. The surrounding prose ("a high badge grants nothing…") is contradicted by a button whose entire purpose is to make the badge grant bulk selection. Field-by-field confirmation is the product's hard line; this button trains physicians out of it on day one — and B2 proves "high" is assignable to a wrong drug, M3 that a composed narrative can embed a stale fact. HC1's spirit (named human decides *each* input of record) survives the letter here only because the click count is two instead of one.
**Fix.** Remove it. If a bulk affordance must exist, make it "review next unconfirmed" navigation, not bulk selection — or require each bulk-selected row to be individually expanded before Apply enables.

### M6. Provenance stamps that don't match where the value came from (HC4) — **[confirmed]** — real hole, small fixes

- `drug.duration` from `dispenseRequest.expectedSupplyDuration` is stamped `…timing.repeat.boundsDuration (UCUM)` (`fhir_ingest.py:594–603` — the path literal never switches with the fallback). Reproduced: value "90 d" from expectedSupplyDuration, provenance claims boundsDuration.
- `investigator.address`: when the role's Organization resolves but has no address and the value falls back to `Practitioner.address`, the stamp is `resource="Organization"` with `path="Practitioner.address (fallback)"` (`fhir_ingest.py:449–451`) — self-contradictory. Reproduced.
- The multi-candidate diagnosis note hardcodes "multiple active **cancer** Conditions" (318–319) even when the candidates are HTN/DM/GERD (see MIN3).
HC4 makes wrong provenance on a regulatory artifact a constitutional violation, and these stamps are exactly what the confirming physician is told to trust.
**Fix.** Set the path string where the value is actually found (one variable, assigned per branch); label the address resource from the same branch that produced the value; make the note generic ("multiple active Conditions").

### M7. INV-4 egress gateway does not exist even as a stub — currently vacuous, structurally unprotected

There is no outbound network code anywhere in the app or engine today (verified: no HTTP client imports in `fhir_ingest`, no CDN/external URL in `index.html`, server binds 127.0.0.1) — so HC2 holds **by absence**. But INV-4 promises "exactly one function may construct outbound requests," a closed `DeidentifiedPredicates` struct, a destination allowlist, and egress audit logging. None exists, and nothing structural stops the next feature (the candidate-trial matcher the state machine anticipates) from calling `urllib` directly from anywhere. An invariant that is only true because the feature is missing is not "enforced in code."
**Fix.** Either build the gateway stub now (struct + allowlist + a repo-wide test asserting no other module imports an HTTP client — extending `TestParsePurity` from one module to the whole engine/app), or mark INV-4 "deferred, protected meanwhile by repo-wide no-network test" in the doc — and actually add that repo-wide test.

---

## MINOR findings

### MIN1. `patient.coded_id` collision space and instability — real limitation, borderline acceptable-for-prototype

Suffix = first 3 hex chars of the bundle SHA-256 (`fhir_ingest.py:666–667`): 4,096 values → ~50% chance of two patients sharing a pseudonym by ~75 cases (birthday bound). Cross-case pseudonym collision in an EA registry is a record-mixup vector. Also unstable: re-importing the same patient's *updated* chart yields a different coded_id — the pseudonym doesn't identify the patient, it identifies the byte-exact bundle. Not reversible (SHA-256 preimage on 3 chars is not a re-identification risk) — that part is fine.
**Fix.** Widen to 6–8 chars and/or make the app check collisions against existing cases; document that the pseudonym is per-import, or derive it once per case and persist.

### MIN2. Prior-therapy and diagnosis quality noise — acceptable-for-prototype, disclose it

Duplicated MedicationRequests (re-orders/refills) render twice ("gemcitabine (…); gemcitabine (…)" — confirmed); non-mCODE charts pipe the whole active problem list into `patient.diagnosis` (HTN | DM | GERD | cancer — confirmed; the spec's own fallback design). Both are visible, medium-confidence, editable — the physician can fix them. The risk is habituation: noisy proposals train skimming, which compounds M5.
**Fix.** De-duplicate agents by RxNorm code; prefer conditions with `category=problem-list-item` + a cancer-adjacent code system hit before dumping the full list.

### MIN3. `patient.sex` = "unknown" proposed at high confidence

`fhir_ingest.py:231–246`: `gender="unknown"` is proposed as the value "unknown" with **high** confidence. "Unknown" is the absence of a fact; per §1.2/INV-6 that should be unattested (no proposal), not a high-confidence assertion of the string "unknown" into an FDA form field.
**Fix.** Treat `unknown` as unattested; `other` stays proposable.

### MIN4. Arbitrary first-Practitioner as investigator; privacy_log gaps — acceptable-for-prototype, disclosed

`practitioners[0]` (`fhir_ingest.py:399`) — a bundle listing the referring physician first mis-fills all seven `investigator.*` fields. Mitigated: capped medium with the inference disclosed in every path (395–493), spec §3 documents it. Still violates the §1.2 multi-candidate rule when several Practitioners are present. Separately, the `fhir_bundle_loaded` log entry lacks the `actor` its own state-machine diagram specifies, and `privacy_log` grows unbounded across imports.
**Fix.** Multiple Practitioners → propose the one referenced by Encounter.participant/Condition.asserter; else all candidates, medium. Add actor to the log event when B3's actor exists.

## NIT

- `TestParsePurity` regex (`test_fhir_ingest.py:327–337`) won't catch `__import__("urllib")` or an indirect import through another module; the namespace check helps but only for the listed four names. Fine for a prototype; the repo-wide no-network test (M7) supersedes it.
- `Practitioner.qualification.identifier` license loop returns after the first non-NPI identifier (`fhir_ingest.py:477–493`) — a second, correct license is silently ignored; disclosed as "one license proposal" in a comment but not in the proposal path text.
- `codingText`/`esc` usage in the import panel looks XSS-clean (all interpolations escaped) — verified, no finding.

---

## Test-quality audit (dimension 7): which invariants have a test that would fail if the invariant broke?

| Claim | Enforced in code? | Test that would actually fail? |
|---|---|---|
| INV-1 no network/pure | Yes | Yes — weak (regex + namespace, one module only) |
| INV-2 import never writes intake | Yes | **Yes — the best test in the file** (`test_import_returns_proposals_and_never_mutates_intake`) |
| INV-2 named-actor confirmation | **No** (B3) | No |
| INV-3 profile hash / re-confirm | **No** (B3) | No |
| INV-4 egress gateway | **No** (M7, vacuous) | No |
| INV-5 mode transitions | **No** (B3) | No |
| INV-6 unattested honesty | Yes | Yes (`test_absent_elements_yield_no_proposal_never_a_guess`) |
| INV-7 read-only to EHR | True by absence | No test (acceptable — nothing to test yet) |
| INV-8 structured identifiers excluded | Yes | Partly — see T1 |
| §1.2 multi-candidate → medium | Only for diagnosis | No — and B2/M1/M3/M4 all live in the gap |

**T1 — the load-bearing gap:** the leak-guard (`_apply_leak_guard`) has **zero** tests in which it fires. Every never-extract test plants identifiers only in structured Patient fields the extractors already skip; no test puts a patient name into `Condition.code.text` or `dosageInstruction.text`. Delete the leak-guard and all 97 tests still pass. Likewise untested: Observation status filtering, multi-patient bundles, the active-order drug hijack, first-treatment-date with no drug name, provenance-path accuracy. The suite is a well-built happy-path harness around one synthetic bundle — it proves the sample works, not that the invariants hold. Add: a hostile-bundle test class where (a) the guard must drop a proposal, (b) case/format-variant names must be caught (after B1's fix), (c) a two-Patient bundle must be refused, (d) an active unrelated order must not become `drug.name`, (e) each provenance path is asserted against a fallback-source input.

## What is acceptable for a synthetic prototype (explicitly not held against the build)

Mocked SMART launch (INV-7 scope assertion deferred, as documented); no authentication on a 127.0.0.1 single-user server; the pasted bundle remaining in browser memory/textarea; sample-fixture import path; `use_sample` reading a repo fixture; DERIVED-LOCAL fields at "low" requiring confirmation (good design, works); the 90+ age aggregation (correct per §164.514(b)(2)(i)(C), tested); the honest-absence behavior for manual fields (all 35 verified never-proposable via the whitelist assert at `fhir_ingest.py:180–183` — sound structural idea).

## Reply from the team

Revision by the orchestrator (not the original builders, per the review
discipline). Engine suite: 97 → **120 tests**, all green. Every code finding
below was reproduced, fixed, and covered by a test that fails if the hole
reopens. Disposition per charge:

**B1 (free-text PHI / sieve leak-guard) — CONCEDED, fixed.** Free text is now
*tainted*: values from `.text` / `dosageInstruction.text` are marked and pass a
rewritten leak-guard that (a) casefold- and punctuation-normalizes both sides,
(b) harvests forbidden strings from every Patient **and** `contained` Patients
**and** `RelatedPerson`, (c) matches `birthDate` in six written forms, and
(d) **fails closed** — a tainted value with no Patient basis to check against is
dropped. Coded `coding.display` (controlled terminology) is not tainted.
`TestLeakGuardHostile` (7 cases) now fires the guard on name-in-`Condition.text`,
case-mismatch, `dob 3/14/1968`, contained- and RelatedPerson-names, and the
no-Patient fail-closed path; a clean coded diagnosis still survives. (A bug in
my *own* first cut — the basis walked `contained` from the bundle root and
missed the entries, fail-closing three good proposals — was caught by re-running
the sample before commit and fixed.)

**B2 (any active order → investigational drug at HIGH) — CONCEDED, fixed.**
Drug candidates are now restricted to `status in (draft, on-hold)` or
`intent in (proposal, plan)`; `active`+`order` is existing therapy and never a
candidate. `drug.name` is capped at **medium always** (RxNorm inversion: a coded
agent is *less* likely investigational). >1 staged candidate caps all `drug.*`
at medium and names the ambiguity in the provenance path. `TestDrugCandidateSafety`
proves lisinopril-before-draft yields the draft (not lisinopril), an active-only
bundle yields no drug, and multi-candidate caps route to medium.

**B3 (no named human / no durable audit; doc overclaim) — CONCEDED, both parts.**
Code: the confirm step now carries a **confirming-clinician name** (the frontend
requires it before applying chart values) and a per-field `chart-confirmed` vs
`manual` provenance; the server persists both (`confirmations`, `field_provenance`)
so they survive reload and stay value-free. Doc: `privacy-state-machine.md` §4
now carries a **Status** column and a §4a substrate summary — INV-3/4/5 and the
committed-profile object are marked **DEFERRED**, not claimed as present; the
"every invariant ships with a test" line is corrected. This is an attribution
record, not a Part-11 signature, and is labeled as such. (The full
`commit_profile` profile-hash + re-confirmation gate remains deferred and
tracked — it is a larger change than this revision should smuggle in.)

**M1 (chimera multi-patient) — CONCEDED, fixed.** A bundle with >1 `Patient` is
refused (`BundleError`); `TestMultiPatientRefusal`.

**M2 (first_treatment from any admin; fires non-emergency) — CONCEDED, fixed.**
Gated on `route.emergency`; no drug candidate → no proposal; whole-word/coded
match instead of first-token substring. `TestFirstTreatmentGating` (3 cases).

**M3 (stale ECOG by bundle order) — CONCEDED, fixed.** `_latest_observation`
sorts by effective date descending and renders the date into the value.
`TestObservationRecency`.

**M4 (entered-in-error diagnosis) — CONCEDED, fixed.** `_condition_ok` excludes
`verificationStatus in (refuted, entered-in-error)` and
`clinicalStatus in (inactive, resolved, remission)` in both branches; absent
status is permitted (the sample Condition carries none). `TestConditionStatusFiltering`.

**M5 ("Confirm all high-confidence" footgun) — CONCEDED, removed.** The bulk
button is gone; copy states there is deliberately no bulk-accept.

**M6 (wrong provenance stamps) — CONCEDED, fixed.** `drug.duration` names
`expectedSupplyDuration` vs `boundsDuration` per branch; the address fallback
labels `resource="Practitioner"`; the multi-condition note is generic
("Conditions", not "cancer"). `TestProvenanceAccuracy`.

**M7 (egress gateway vacuous/unprotected) — EXTENDED.** No gateway is built
(HC2 holds by absence, YAGNI until the trial-matcher exists), but the invariant
is no longer vacuous: `TestEngineEgressBoundary` asserts no engine module except
the single sanctioned concept-reviewer imports an outbound client, and that
reviewer never imports the PHI path. INV-4 re-documented as deferred-but-guarded.

**MIN1 — CONCEDED.** `coded_id` widened 3→8 hex (~4.3e9 space).
**MIN3 — CONCEDED.** `gender="unknown"` is now unattested (no proposal);
`TestSexUnattested`.
**MIN2 — CONCEDED (partial).** Prior therapies de-duplicated by RxNorm code.
Problem-list-item preference deferred.
**MIN4 / NIT (arbitrary first-practitioner; single-license) — ACKNOWLEDGED,
deferred.** Both are capped-medium and disclosed in the provenance path (review
marked them acceptable-for-prototype); Encounter/asserter-based practitioner
selection is tracked.

**Re-review requested** on: the leak-guard's normalization (false-negative risk
on exotic name encodings), the drug-candidate restriction (did it over-narrow
and drop a legitimate `active`+`plan` case?), and whether the doc's Status
column now matches the code exactly.
