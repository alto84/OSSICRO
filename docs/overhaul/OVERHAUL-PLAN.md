# OSSICRO Overhaul Plan — the 15 MAJORs, sequenced

**Reader:** the implementer of the next build phase (agent or human), and Alton approving it.
**Synthesized:** 2026-07-11, from `docs/review/INVENTORY.md`, the seven persona reviews, the
wave memos, and a fresh read of the code every MAJOR touches.
**Baseline verified this pass:** `python -m pytest engine/tests/ app/tests/ -q` → **337 passed**.
**Governed by:** `docs/OSSICRO-CONSTITUTION.md`. Nothing in this plan weakens a hard line.
Verification is pytest only. The app server on :8765 is never started or bound by this work.

**State of the tree relative to the reviews (verified in code, not assumed):**
- The SMALL-FIXES pass has landed (clocks.py docstring, routes.json help text, v-prefix, patient
  strings, etc.).
- B1 has an **interim** fix: `_LIVE_CONCEPT_REVIEW` (`app/server.py:583`) requires
  `OSSICRO_LIVE_CONCEPT_REVIEW` to be explicitly affirmative before the live Claude reviewer is
  selected. The fuller remediation (per-review audit record, UI disclosure, BAA precondition
  doc) is still open — Package 3.
- M1 is **half fixed**: `app/server.py:_enrollment_obligations` (lines 1273–1298) now arms the
  56.104(c) row from `submission.first_treatment_date`, and `obligation_irb_notify_q` names the
  right trigger. The engine function `clocks.expanded_access_emergency_deadlines` (clocks.py:137)
  still computes BOTH deadlines from one `authorization_date` and its docstring still says both
  clocks "start when FDA authorizes emergency use by phone." The reconciliation test does not
  exist yet. — Package 1.
- M8 is fully live: the off-by-one 312.305(b)(2) pinpoints are in `ea_generators.py`
  (565–569, 595–614, 637, 643–651, 781–783) and `routes.json` (lines 21–24, 64).
- Everything else in the MAJOR list is confirmed unfixed.

## How the packages are cut

Packages run **sequentially**, one at a time, each ending with a full green suite. Two packages
are pure foundation (P1 corrects what registries/engine already assert; P2 adds the fields and
registry facts every later package consumes). P3 closes the remaining hard-line-adjacent gap
early. P4–P7 are one concern each, end-to-end (schema consumer → engine → server → UI → tests).
P8 is the human-verification pass on the 3926 instrument. P9 is the wall that must exist before
any non-synthetic pilot. Process-tooling improvements from `PROCESS-ANALYSIS.md` that are
implementable as code/registry are folded in where marked **[PT-n]**.

Field names, states, and function names declared in a package are **contracts**: later packages
use them exactly as written here.

---

## Package 1 — Statutory-clock split + citation remap ("computed, not guessed" repairs)

**Closes:** M1 (engine remainder), M8, m16. Folds in **[PT-2] the single-source citation table**
and **[PT-6] cross-artifact clock reconciliation tests**.
**HITL: YES** — the M8 pinpoint map was verified against eCFR by the regulator persona, but a
statutory-citation change ships with a `PENDING-HUMAN-VERIFICATION` row in the citation
inventory until a qualified human initials it against eCFR. Never silently asserted final.

**Files:** `engine/ossicro/clocks.py`, `engine/ossicro/ea_generators.py`,
`engine/registry/routes.json`, `app/server.py`, new `engine/ossicro/citations.py`,
new `docs/regulatory/CITATION-INVENTORY.md`, `engine/tests/test_clocks.py`,
`engine/tests/test_ea_generators.py`, new `engine/tests/test_reconciliation.py`.

**Spec:**
1. **Split the emergency-deadline function.** Replace
   `expanded_access_emergency_deadlines(authorization_date)` with two single-anchor functions:
   - `written_3926_deadline(authorization_date: date) -> Deadline` — 15 working days,
     `21 CFR 312.310(d)(2)`.
   - `irb_emergency_notification_deadline(first_treatment_date: date) -> Deadline` — 5 working
     days, `21 CFR 56.104(c)`, anchored on the emergency use (first treatment).
   Delete the combined function (grep shows its only production caller is
   `ea_generators.py:423`, which uses `[0]` — switch it to `written_3926_deadline`). Update the
   module `__all__` and the misleading docstring at clocks.py:138.
2. **Move the 312.33 annual-report math into the engine (m16).** New
   `ind_annual_report_deadline(fda_receipt_date: date) -> Deadline` in `clocks.py`: effective =
   `ind_30_day_deadline(receipt).due`; anniversary = effective + 1 year (Feb 29 → Feb 28); due =
   anniversary + 60 calendar days. Replace the inline copy in
   `app/server.py:_enrollment_obligations` (lines 1299–1311) with a call to it. One engine owns
   all deadline arithmetic; the app never computes a date again.
3. **Citation remap (M8).** Apply the regulator's corrected 312.305(b)(2) map in one pass:

   | Content | Was | Becomes |
   |---|---|---|
   | rationale for treatment use | (b)(2)(i) | **(b)(2)(ii)** |
   | patient description / diagnosis / prior therapies / coded id | (b)(2)(ii) | **(b)(2)(iii)** |
   | dose / route / duration / treatment-plan summary / dosing_plan | (b)(2)(iii) | **(b)(2)(iv)** |
   | facility / site.name | (b)(2)(iv) | **(b)(2)(v)** |
   | CMC | (b)(2)(v) | **(b)(2)(vi)** |
   | pharmacology / toxicology | (b)(2)(vi) | **(b)(2)(vii)** |
   | monitoring plan | (b)(2)(vii) | **(b)(2)(viii)** |

   Sites: `ea_generators.py` 565–569 (gen_form_3926 sources), 595/598/603/607/610/614
   (`_TREATMENT_PLAN_TEMPLATE` headers), 637 (`dosing_plan`), 643–651 (gen_treatment_plan
   sources), 781–783 (gen_loa_request); `routes.json` lines 21–23 (`drug.dose/route/duration` →
   (b)(2)(iv)), line 24 (`treatment.monitoring_plan` → (b)(2)(viii)), line 64 (`site.name` →
   (b)(2)(v)). Monitoring goes to (viii) — the treatment plan's §6 is clinical monitoring to
   evaluate effects and minimize risk, not the (iv) administration-adjacent procedures; record
   that judgment call in the inventory row for the human verifier.
4. **[PT-2] Single-source citation table.** New module `engine/ossicro/citations.py`: a
   `CITATIONS: Dict[str, Citation]` table where `Citation = (pinpoint: str, status:
   "HUMAN-VERIFIED" | "PENDING-HUMAN-VERIFICATION", verified_by: str, verified_date: str)`.
   Every pinpoint the generators/templates emit is looked up by content key
   (e.g. `"ea.treatment_plan.monitoring"`), never string-literal'd twice. A stdlib script
   (`python -m ossicro.citations > docs/regulatory/CITATION-INVENTORY.md`) renders the table
   with its statuses; the 312.305(b)(2) rows start `PENDING-HUMAN-VERIFICATION`. A human flips
   a row only by editing the table with their name and date. Migrating every existing citation
   into the table in this package is required for the 312.305(b)(2) family and the clock
   citations; the rest may migrate opportunistically in later packages, but no NEW pinpoint may
   bypass the table from this package on.
5. **Rendered-artifact marker.** While any citation used by a document has status
   `PENDING-HUMAN-VERIFICATION`, the document footer gains one line:
   `Citation pinpoints marked pending verification against eCFR — see CITATION-INVENTORY.`

**Tests:** pin every corrected pinpoint (a test that renders the treatment plan and asserts the
eight section headers' sub-citations); `test_reconciliation.py` — **[PT-6]** given one intake
fact set, the `routes.json` clock, the generator's computed deadline paragraph, and the
`_enrollment_obligations` row must produce the SAME due date for the same duty (56.104(c) from
first-treatment; 312.310(d)(2) from authorization; 312.33 from receipt); a test that
`written_3926_deadline`/`irb_emergency_notification_deadline` refuse to be called with the
other's anchor semantics (distinct names make the type system social, the test makes it real);
Feb-29 annual-report case moved from app tests into engine tests.

---

## Package 2 — Registry + intake-schema foundations (fields and facts later packages consume)

**Closes:** M5, M7, m7. Folds in **[PT-4] the author/signer model on every registry document**
and **[PT-3] the single-source claim registry**. Declares every new field contract.
**HITL: no** (M7 is a semantics decision, made here explicitly: the accountability log is a
shell filled at dispensing).

**Files:** `engine/registry/routes.json`, `engine/registry/documents.json`, new
`engine/registry/claims.json`, `engine/ossicro/ea_generators.py` (only the `_AS_OF_FIELDS`
comment + drug-accountability note span), `engine/fixtures/ea_sample_case.json`,
`app/server.py` (claims consumption), `app/static/index.html` (claims consumption),
`engine/tests/`, `app/tests/`.

**Spec:**
1. **`submission.date` (M5).** New intake field in `routes.json`:
   `{"id": "submission.date", "label": "Preparation / planned submission date", "citation":
   "Form FDA 3926 field 1", "type": "date", "required": false, "section": "Submission control",
   "help": "Dates the cover letter, Form 3926, and LOA request. Enter the date you prepare or
   submit the package; never guessed by OSSICRO."}`. The engine already consumes it
   (`ea_generators._AS_OF_FIELDS[0]` at :157 and the 30-day-clock fallback at :212), so adding
   the field makes the dead anchors live and the fix-loop can reach `[[MISSING: cover_date]]`
   (the span→field harvest in `_build_span_to_field` picks it up automatically once the sample
   fixture carries it). Add it to the sample fixture.
2. **Drug-accountability semantics (M7) — decide, don't leave half-wired.** Decision: the log is
   a **shell to be filled at dispensing**. Remove `lot_numbers` and `dispensing_entries` from
   `documents.json:428` `required_fields` (keep `drug_name`); leave the template columns
   rendering `[[MISSING: ...]]` with the existing "honestly absent at submission time" note;
   the ledger row for the document becomes green-with-note (its resolving question, if the
   drug name is present, is none). Do NOT add post-supply intake fields in this pass (that is
   post-enrollment record-keeping, out of the drafting product's scope; documented in the
   document's registry `description`). Re-baseline the ledger tests.
3. **[PT-4] `author_party` on every document.** Every entry in `documents.json` gains
   `"author_party": "physician" | "manufacturer" | "irb" | "fda"` — who authors/signs the
   real-world instrument this draft stands in for. Assignments: LOA → `manufacturer`; IRB
   concurrence (the concurrence itself, distinct from the request) → `irb`; everything currently
   drafted for the physician's own hand → `physician`. Loader (`registry.py`) validates the
   enum and fails closed on a missing value. This field is inert data in this package;
   Package 4 gives it ledger behavior. (This is the durable fix for "a manufacturer letter goes
   green on physician-typed data": authorship is now a registry fact, not an inference.)
4. **External-party receipt facts (contract for Package 4).** New intake fields:
   - `manufacturer.loa_received_date` (date) — "Date the signed LOA was received. Records a
     fact; the decision is the manufacturer's alone."
   - `manufacturer.loa_signatory` (text) — name/title on the received LOA.
   - `manufacturer.loa_document_sha256` (text, optional) — hash of the received letter file.
5. **Anchor + attestation fields (contracts for Packages 5, 6, 7).**
   - `submission.fda_authorization_date` (date) — FDA allow-to-proceed/authorization fact
     (M4's record-carrying fact; distinct from the emergency phone-auth field).
   - `treatment.conclusion_date` (date) — arms the 312.310(c)(2) end-of-treatment summary row
     (M10).
   - `consent.timing_attestation` (select: `obtained-before-treatment` |
     `exception-50.23-documented` | `not-yet-obtained`) — physician attestation, never
     defaulted, feeds M14's computed consent sentence.
   - `consent.injury_compensation_statement` (textarea, 21 CFR 50.25(a)(6)) — the
     whether-compensation/whether-treatment statement.
   - `consent.cost_statement` (textarea, 21 CFR 50.25(b)(3); 312.8(d)) — whether the patient
     may be charged.
   - `drug.quantity_requested` (text), `submission.needed_by_date` (date),
     `submission.cost_recovery_statement` (textarea, 21 CFR 312.8) — M15's triage facts.
   All fields carry citation + help in the house style; all flow through the existing
   schema-validated intake automatically (the SPA renders from `/schema`).
6. **m7:** move `irb-concurrence-request` from Module 5 to Module 1 in both routes' `ectd_map`.
7. **[PT-3] Claim registry.** New `engine/registry/claims.json`: the cross-cutting user-facing
   claims that have already burned us, each with an id, canonical text, and the stage/config
   conditions under which it is true — starting set: `nothing-submitted-to-fda`,
   `chart-data-stays-local`, `drafts-only-banner`, `no-direct-identifiers-in-view`. Server
   STRINGS and index.html render these claims from the registry (server injects them into the
   boot payload; the SPA reads `S.claims`), so each claim has exactly one authored copy. A test
   greps `app/` for the claim literals and fails if a registered claim's distinctive text
   appears outside the registry/render path (this is the tripwire that would have caught the
   third hardcoded "Still in draft.").

**Tests:** schema round-trip for every new field (accepted by `/intake`, reachable by fix-loop);
ledger re-baseline for the accountability log; loader validation of `author_party`; claim-
duplication grep test; ectd_map placement test.

---

## Package 3 — AI-review attribution + whole-app egress boundary (B1 full remediation, M12)

**Closes:** B1 (remaining scope: audit record, UI disclosure, BAA precondition, disposition
capture), M12. Folds in **[PT-5] extending the egress-boundary test to the whole app**.
**HITL: no** (no regulatory-content assertion changes; the BAA precondition doc states
requirements, it does not certify them).

**Files:** `app/server.py`, `engine/ossicro/review_claude.py`, `app/static/index.html`,
`wiki/05-ossicro-system/part-11-and-ai-credibility.md`, new
`docs/deployment/AI-REVIEW-PRECONDITIONS.md`, `app/tests/`, `engine/tests/test_fhir_ingest.py`
(boundary test relocation/extension).

**Spec:**
1. **One audit record per live concept review (HC5).** In `_check_payload` and
   `_package_payload`, when the selected reviewer is the live one, append an `ai_review` audit
   record before returning: `actor="system:concept-reviewer"`, `action="ai_review"`,
   `input_hash=` the committed-profile hash, `detail={"model": <model id>, "model_version":
   <version>, "doc_ids": [...], "finding_count": n, "destination": "anthropic-api"}` — flat,
   value-free (INV-8). The stub reviewer writes nothing (no egress happened).
   `review_claude.ClaudeConceptReviewer` exposes `model_id`/`model_version` for this.
2. **Reviewer disposition capture (the HC5 "disposition of the human reviewer" half).** New
   endpoint `POST /api/case/{id}/review-disposition` `{actor, finding_id, disposition:
   "accepted"|"dismissed", note?}` → appends an `ai_review_disposition` audit record. The check
   UI renders accept/dismiss buttons beside each concept finding (escalate-only is untouched —
   a disposition never changes ledger state; it records the human's judgment). HC5's text is
   left exactly as written; the mechanism now exists to satisfy it.
3. **UI disclosure.** The check screen states, from the server payload, one of:
   "These drafts were reviewed by an external AI model (<model>) — document text left this
   machine under the deployment's signed BAA." / "Reviewed by the offline built-in checker —
   nothing left this machine." Never silent either way. The claim joins `claims.json`.
4. **BAA/zero-retention precondition doc.** `docs/deployment/AI-REVIEW-PRECONDITIONS.md`:
   setting `OSSICRO_LIVE_CONCEPT_REVIEW` is a deployment decision requiring (a) a BAA with the
   model provider or a documented de-identified projection, (b) zero-retention configuration,
   (c) the named human who flipped it recorded in the deployment log. Referenced from the flag's
   code comment and README.
5. **Part-11 truth (M12).** Add a `Status: BUILT / NOT-YET-BUILT / PARTIAL` column to the wiki
   clause table; mark role-scoped access NOT-YET-BUILT (INV-7), e-signature ceremony
   NOT-YET-BUILT, `ai_review` logging BUILT (as of this package).
6. **[PT-5] Whole-app egress boundary test.** Extend `TestEngineEgressBoundary` (currently
   engine-only, sanctioning `review_claude.py`) with an app-side sweep: import-walk
   `app/server.py` and every module it loads; assert no outbound HTTP client
   (`urllib.request`, `http.client`, `socket.create_connection`, `requests`) is imported outside
   the two sanctioned modules (`egress.py` gateway, `review_claude.py`), and assert
   `_select_reviewer()` returns the stub when `OSSICRO_LIVE_CONCEPT_REVIEW` is unset even with
   `ANTHROPIC_API_KEY` present. The boundary claim becomes a tested property of the whole
   program, not just the engine.

**Tests:** ai_review record written on live path (monkeypatched reviewer), absent on stub path;
disposition endpoint round-trip + audit record; env-matrix test on `_select_reviewer`; the
boundary sweep itself.

---

## Package 4 — External-party document model: the manufacturer concern end-to-end

**Closes:** M2, M15, m4, m5, m6. Consumes Package 2's `author_party` +
`manufacturer.loa_received_date/loa_signatory/loa_document_sha256` and
`drug.quantity_requested`/`submission.needed_by_date`/`submission.cost_recovery_statement`.
**HITL: no.**

**Files:** `engine/ossicro/check.py`, `engine/ossicro/assemble.py`,
`engine/ossicro/ea_generators.py`, `app/server.py`, `app/static/index.html`,
`templates/expanded-access/*.md` (path normalization), `engine/tests/`, `app/tests/`.

**Spec:**
1. **New ledger state `awaiting-external-party` (M2).** In `check.build_ledger`: a document
   whose registry `author_party != "physician"` can never be `green` on intake completeness
   alone. For the LOA: required fields filled + `manufacturer.loa_received_date` absent →
   status `awaiting-external-party` (rendered as a distinct badge, amber-family), resolving
   question: "Record the received, signed LOA (date + signatory) when the manufacturer issues
   it — the letter shown here is OSSICRO's draft for their review." With
   `loa_received_date` + `loa_signatory` recorded → `green`, note carrying the recorded
   signatory/date (+ document hash if entered). Ledger totals gain the fourth bucket.
2. **`submission_ready` consults the external fact (M2).** In `assemble.assemble_submission`,
   the existing LOA-reference-or-division-contact rule (assemble.py:130–144) additionally
   requires, on the LOA branch, `manufacturer.loa_received_date` present — otherwise a blocking
   entry "Manufacturer LOA not yet received (recorded fact required; the no-IND
   division-contact branch is the alternative)." The payload gains
   `human_acts_outstanding: [...]` (unsigned gates + awaiting-external-party docs), and the UI
   readiness banner renders "Documentation ready — N human acts outstanding" instead of a bare
   boolean (ethics 9).
3. **Enclosure honesty.** Cover-letter enclosure line: "manufacturer Letter of Authorization
   (enclosed upon receipt from the manufacturer)".
4. **LOA request triage completeness (M15).** Extend `gen_loa_request`: an URGENCY literal
   computed from `submission.emergency` + `submission.needed_by_date` (reuse the cover-letter
   computation); optional lines for `drug.quantity_requested`, `patient.age`/`patient.sex`
   (already coded-safe), `investigator.license_number`/`license_state`, `site.name` (shipping
   destination), IRB status (irb.name + pathway), and a charging statement from
   `submission.cost_recovery_statement` citing 21 CFR 312.8 (first appearance of 312.8 in the
   repo — route it through the Package 1 citations table). Missing values render
   `[[MISSING: ...]]` as always.
5. **Release snapshot/inbox (m6 + M15 badge).** Add `loa_request_sha256` (SHA-256 of the exact
   LOA-request text released) and `emergency: bool` to the release snapshot and inbox items;
   the manufacturer view badges urgent requests and shows the hash so the manufacturer can pin
   the artifact they acted on.
6. **m4:** fold the reference template's structure into `gen_loa` — letterhead block using
   `manufacturer.address` (currently a dead field), sections-expressly-excluded, effective
   date/expiration-or-revocation terms, signatory name/title block — values honestly MISSING
   where only the manufacturer can supply them. **m5:** normalize the dotted paths in
   `templates/expanded-access/*.md` field tables to the routes.json vocabulary (or add a
   legacy-paths note at the top of each).

**Tests:** ledger state machine for the LOA (draft → awaiting-external-party → green on
recorded fact); `submission_ready` blocked/unblocked matrix (LOA branch vs division-contact
branch); snapshot hash stability; urgency badge; gen_loa_request literal assertions.

---

## Package 5 — Ethics-gate honesty: promote, sign-off evidence, pathway-true statements

**Closes:** M4, M13, M14, m8, m13, m1. Consumes Package 2's `consent.timing_attestation` and
`submission.fda_authorization_date`.
**HITL: no** (statements become computed-from-attestation; no new regulatory assertion).

**Files:** `app/server.py`, `engine/ossicro/gates.py`, `engine/ossicro/models.py`,
`engine/ossicro/ea_generators.py`, `engine/registry/gates.json`, `app/static/index.html`,
`engine/tests/`, `app/tests/`.

**Spec:**
1. **Promote advisory — loud, persisted, escalate-only (M4).** `_promote` gains a gate sweep:
   for each of `informed-consent`, `irb-approval` without a currently-valid sign-off, and for
   each absent external fact (`manufacturer.loa_received_date`,
   `submission.fda_authorization_date` or emergency-auth), build an advisory string naming the
   citation (312.60 / Part 50 / Part 56 / FDCA 561A). Behavior:
   - **Non-emergency route:** refuse (409) when `informed-consent` or `irb-approval` lacks a
     valid sign-off, UNLESS the payload carries
     `acknowledge_unsigned_gates: "<typed sentence in the actor's own words>"` — a named-human
     override, persisted in `case["enrollment"]["advisories"]` and in the promote audit
     record's detail. Nothing is auto-decided; the skip is now a recorded human act instead of
     a silence.
   - **Emergency route:** advisory only (a §50.23/56.104(c) reality), same persistence.
   The advisories render in the promote response, on the promote card, and as an escalate-only
   line in the check ledger. The patient page is untouched (it already handles enrolled
   honestly post-SMALL-FIXES).
2. **Sign-off evidence (M13).** For gates `informed-consent` and `irb-approval`,
   `_record_signoff` requires: `statement` typed by the signer **in their own words** (the
   server stops synthesizing it — the synthesized text remains only for the other gates, and
   a minimum-length/not-equal-to-placeholder check applies), plus an `evidence` object persisted
   in the sign-off record: for irb-approval `{concurrence_date, concurring_member,
   irb_reference}` (each may be honestly blank but the keys are asked); for informed-consent
   `{consent_date}`. `gates.record_signoff` accepts and stores the extra kwargs (it already
   passes `**kwargs` through). The sign-off modal grows the fields; the role field stays
   read-only.
3. **Supersede, never overwrite (m13b, 11.10(e)).** A re-recorded sign-off for the same
   (gate_id, doc_id) no longer replaces the prior record: the old record gains
   `superseded_at`/`superseded_by` and stays in `case["signoffs"]`; validity checks consider
   only non-superseded records.
4. **Pathway-true consent sentence in the IRB request (M14).** Replace the fixed line at
   `ea_generators.py:809` with a computed literal keyed to route emergency +
   `consent.timing_attestation`: non-emergency → "Informed consent per 21 CFR Part 50 will be
   obtained before treatment begins."; emergency + `obtained-before-treatment` → past-tense
   statement; emergency + `exception-50.23-documented` → the §50.23 exception statement;
   attestation absent → "[[MISSING: consent.timing_attestation]]" (HC2: never assert what was
   not entered). Provenance-stamped like `pathway_statement`.
5. **m8:** `Document.advance("final")` (`models.py:200`) refuses `final` outright for gated
   documents — `finalize()` becomes the only path, by code instead of by convention.
6. **m1:** `gates.json` `sae-causality.responsible_role` label →
   `"physician-sponsor / medical monitor"` (display label; role-matching key unchanged or
   remapped with its tests).
7. **Point-of-use 312.52 line (m13a):** one sentence on the sign-off modal and the promote
   card: "You remain the sponsor-investigator; OSSICRO is not and cannot be a 21 CFR 312.52
   transferee — recording this act transfers nothing to software."

**Tests:** promote refusal/override/advisory matrix across both routes; advisory persistence +
audit content; own-words statement enforcement; evidence persistence; supersede chain;
advance("final") refusal; IRB-request sentence for all four attestation states.

---

## Package 6 — EA-profiled informed-consent form

**Closes:** M3, m10, m9, m12. Consumes Package 2's `consent.injury_compensation_statement`
and `consent.cost_statement`.
**HITL: YES** — consent language a real patient would sign requires review by a qualified
human (IRB-experienced). The template ships to the best-known target (FDA individual-patient
EA guidance) with a `PENDING-HUMAN-VERIFICATION — consent language not yet reviewed by a
qualified human` line in the document's draft banner, removed only by that review.

**Files:** `engine/ossicro/ea_generators.py` (new `gen_icf_ea` + template),
`engine/ossicro/generate.py` (generic template untouched for non-EA routes),
`engine/registry/documents.json` (new doc id), `engine/registry/routes.json` (route doc lists),
`engine/registry/rules.json` + `engine/registry/banned-constructions.json`,
`app/server.py`, `engine/tests/`, `app/tests/`.

**Spec:**
1. **New document `informed-consent-form-part50-ea`** generated by `gen_icf_ea` in
   `ea_generators.py`; both 3926 routes swap it in for the generic ICF (`routes.json`
   `documents`/`fda_package`/`ectd_map`). The generic `informed-consent-form-part50` remains in
   the registry for non-EA routes.
2. **Framing:** opens with treatment-use framing per FDA's individual-patient EA guidance —
   "You are being asked to receive treatment with an investigational drug under the FDA's
   expanded access ('compassionate use') program. This is treatment, not a research study,
   but laws that protect research participants also protect you." — resolving the
   both-directions therapeutic misconception explicitly. Keep the eight verbatim-locked
   50.25(a) element headings byte-identical (R-ICF-50.25 verifies by hash; if the EA doc id
   needs its own rule row, add `R-ICF-50.25-EA` pointing at the same verbatim spans).
3. **50.25(a)(6) becomes satisfiable:** element 6 renders `consent.injury_compensation_statement`
   (the whether-compensation / whether-medical-treatment statement) plus the injury contact;
   absent → `[[MISSING]]`, and the ledger question directs to the new intake field.
4. **EA-specific disclosures**, each its own paragraph: not FDA-approved for this condition and
   FDA permission is not evidence it works; the manufacturer may decline or stop supplying at
   any time; costs/charging from `consent.cost_statement` (50.25(b)(3); 312.8(d));
   significant-new-findings (50.25(b)(5)); consequences and procedure of stopping treatment
   (50.25(b)(4)); voluntariness restated (50.25(a)(8)).
5. **Adequacy is a named release gate, not a deferred rule:** the document's draft banner
   carries the PENDING-HUMAN-VERIFICATION line (see HITL above); `R-ICF-50.25-ADEQ` stays
   deferred but the doc's registry `description` states plainly that heading-completeness is
   NOT adequacy and a qualified human review is the release precondition for real-patient use.
6. **m12:** grow banned-constructions tier-A from the FDA exculpatory-language guidance
   examples (hold-harmless, cost-shifting-as-waiver, affirmative no-fault phrasings); reword
   the HC6 note in `banned-constructions.json` metadata to "the deterministic tier hard-fails
   the enumerated constructions; judgment owns the class" (the Constitution's own text is not
   edited by this package — propose the HC6 justification reword to Alton separately, since
   the Constitution changes only by its own amendment path).
7. **m10:** add the voluntariness line to `patient_remaining_enrolled`. **m9:** emergency
   variants of the three `patient_remaining_*` lists keyed on the route (the server knows
   `submission.emergency`), keeping the plain-language register.

**Tests:** EA ICF renders all 8 verbatim headings (hash check) + all EA disclosures; a(6)
missing → MISSING + ledger question; tier-A tripwires fire on the new guidance examples;
patient remaining-lists per route; regression: generic ICF unchanged for non-EA routes.

---

## Package 7 — Obligations lifecycle: complete, decoupled from promote, treatment-vocabulary

**Closes:** M10, M11, m2. Consumes Package 2's `treatment.conclusion_date` and Package 1's
clock helpers.
**HITL: no.**

**Files:** `app/server.py` (`_enrollment_obligations` → renamed `_sponsor_obligations`,
STRINGS), `engine/ossicro/clocks.py` (only if a helper is wanted; the conclusion-summary row
uses `treatment.conclusion_date` directly), `app/static/index.html`, `app/tests/`.

**Spec:**
1. **Decouple from promote (M11).** `_sponsor_obligations(case)` returns rows as soon as ANY
   anchoring fact exists — `submission.emergency_auth_datetime`,
   `submission.first_treatment_date`, `submission.fda_receipt_date`, or an enrollment record —
   not only after promote. Promote remains the HIPAA-basis transition it actually is; the
   checklist is surfaced on the check screen pre-promote when armed-or-armable. Reword the UI:
   "duties this treatment use creates — shown from the moment the anchoring facts are
   recorded" (replacing "duties the enrollment creates").
2. **312.310(c)(2) end-of-treatment summary row (M10).** Always-present row: "Written summary
   of the expanded access use, including adverse effects, at the conclusion of treatment —
   21 CFR 312.310(c)(2)"; armed from `treatment.conclusion_date` (honestly UNARMED with the
   resolving question "Record the treatment-conclusion date to arm this deadline" until then;
   the due-date convention — the summary is due "at the conclusion" — renders the date itself,
   not date+N). The generated treatment plan's promise (ea_generators.py:617–621) and the
   tracker now agree.
3. **Tracked-subset disclosure:** one line on the checklist: "This list is the tracked subset
   of sponsor-investigator duties, not the entirety (recordkeeping under 312.57/312.62 and
   other duties are yours untracked)."
4. **m2 vocabulary:** physician-facing strings rename "Record enrollment" → "Record start of
   treatment (legal basis)" and "enrollment" → "treatment start" in the physician workspace
   only (INV-5 machinery, endpoints, patient-page strings, and audit action names unchanged).
   The promote card asks for `submission.first_treatment_date` right there — the act that
   naturally supplies M1's 56.104(c) trigger at the moment it happens.

**Tests:** obligations visible pre-promote once an anchor exists; 312.310(c)(2) row
armed/unarmed; checklist text assertions; rename does not touch patient strings or audit
actions.

---

## Package 8 — Form 3926 fidelity pass (against OMB 0910-0814)

**Closes:** M6.
**HITL: YES — this package IS the human-verification pass.** The agent implements to the
best-known target (reconciling against the local
`sources/fda-guidance/FDA_Expanded-Access-Form-3926-Instructions.pdf`); the item numbering and
AcroForm names are only final when a human has opened the official fillable form and initialed
the map. Until then every rendered surface carries the pending marker.

**Files:** `engine/ossicro/pdf_3926.py` (`_PDF_LAYOUT`, `FDF_3926_FIELD_MAP`),
`engine/ossicro/ea_generators.py` (`_FORM_3926_TEMPLATE`, `gen_form_3926`),
`docs/route-3926-submission-spec.md` (§1.1 field references), `engine/tests/test_pdf_3926.py`,
`engine/tests/test_ea_generators.py`.

**Spec:**
1. Reconcile the three renderers and the spec to ONE item-number map (today the template/PDF
   say LOA=6, qualification=7, IRB=8, no 9; the spec says qualification=6, rationale=9 — at
   least one is wrong). Best-known target derives from the instructions PDF; where its
   font-encoded text resists extraction, the agent transcribes what it can and marks the rest
   UNRESOLVED for the human pass.
2. **Surface the caveat on the artifacts themselves (not just the FDF):** the text template
   header and the PDF draft footer gain "Item numbering pending verification against the
   official Form FDA 3926 (OMB 0910-0814)" — `PENDING-HUMAN-VERIFICATION`, removed only by the
   human pass; heading softened to "Form FDA 3926 (draft layout)".
3. A single `FORM_3926_ITEMS` table in `pdf_3926.py` becomes the one source both the text
   template section order and `_PDF_LAYOUT` consume, so the two renders cannot disagree again;
   the spec cites the table.
4. **Human checklist (blocks marker removal, nothing else):** open the official fillable 3926
   in a forms inspector; verify/correct all ~30 `FDF_3926_FIELD_MAP` names; verify item
   numbers/labels including whatever the real item 9 is; initial the map header with name+date.

**Tests:** template/PDF/FDF item-order consistency test off `FORM_3926_ITEMS`; pending-marker
present until the map header carries a verifier; existing structural PDF tests re-baselined.

---

## Package 9 — Deployment guardrails and store hardening (the pre-non-synthetic wall)

**Closes:** M9, m14, m15, m17, m18, m20. **[PT-7] deferral tripwires** implemented here.
**HITL: no** (engineering hardening; the deployment-compliance page is documentation a human
reviews before any real-PHI decision, which is itself a standing Alton gate).

**Files:** `app/server.py`, `engine/ossicro/profile.py`, `engine/ossicro/egress.py`,
`engine/registry/routes.json` (coded-id help), `app/static/index.html`, new
`docs/deployment/DEPLOYMENT-COMPLIANCE.md`, `README.md` + `app/README.md` (links),
`engine/tests/`, `app/tests/`.

**Spec:**
1. **Bind guard (M9a).** `main()` refuses to start on a non-loopback `HOST` unless BOTH
   `OSSICRO_ALLOW_NONLOCAL_BIND=1` AND an auth backend are configured (today none exists, so
   the override cannot succeed — the guard prints the INV-7 reason and exits non-zero). The
   standing no-bind-change rule becomes program-enforced. (Test constructs the server object
   with a patched HOST and asserts the refusal; the suite never binds 8765.)
2. **HMAC field hashes (m14).** `profile.py` hashing keyed with HMAC-SHA256 under a
   server-side secret loaded from `app/data/secret.key` (created on first run, 0600, never in
   a case JSON, gitignored). Pending-detection and revert-equality semantics unchanged;
   existing committed profiles re-verify under a versioned hash-scheme tag so old synthetic
   cases fail loud, not wrong. Update the honest docstring.
3. **Token hygiene (m17).** `log_message` masks `/api/patient/<token>` paths; patient-token
   lookup via a `{token: case_id}` index compared with `hmac.compare_digest`.
4. **POST durability (m15).** Uniform handler-level wrapper: any `_save_case` failure on
   commit/confirm/signoff/intake/promote/release returns 500 with an honest
   memory-disk-divergence message instead of raising out of `do_POST`.
5. **Export act (m18).** Model PDF/FDF export as an explicit `POST /api/case/{id}/export`
   `{actor, format}` that writes one `export` audit record and returns the bytes; the GET
   endpoints remain for the browser but the UI download buttons go through the POST. (Decision
   made: track it — "one email from a submission" deserves a record.)
6. **Identifier lint (m20).** A naive deterministic lint (SSN/date-like/DOB patterns,
   "name:"-adjacent capitalized pairs) over free-text fields at release and egress time —
   escalate-only warning naming the field, never a block, never a rewrite.
7. **Scope statements (M9b-e).** `DEPLOYMENT-COMPLIANCE.md`: covered-entity boundary; the case
   store is PHI the moment a real case exists; encryption-at-rest expectation; BAA inventory
   (model API, host); retention/deletion; INV-7 persona auth and m14 HMAC as PRECONDITIONS for
   any non-synthetic pilot (not deferrals). Coded-id help text (`routes.json:4`) reworded to
   prefer a study-assigned code over initials. One pilot-scope line in the physician UI footer:
   "Single-user local pilot — do not expose this server or share case URLs."

**Tests:** bind-guard refusal matrix; HMAC keying (hash changes under a different key; equality
semantics preserved); token masked in log output; 500-wrapper on injected save failure; export
audit record; lint fires on seeded identifier text and stays silent on the sample case.

---

## Sequencing summary

| # | Package | Closes | Depends on | HITL |
|---|---|---|---|---|
| 1 | Clock split + citation remap | M1, M8, m16 (+PT-2, PT-6) | — | **YES** (M8 map) |
| 2 | Registry/schema foundations | M5, M7, m7 (+PT-3, PT-4) | — | no |
| 3 | AI-review attribution + app egress boundary | B1-full, M12 (+PT-5) | — | no |
| 4 | External-party model (manufacturer) | M2, M15, m4, m5, m6 | P2 | no |
| 5 | Ethics-gate honesty | M4, M13, M14, m8, m13, m1 | P2 | no |
| 6 | EA-profiled ICF | M3, m9, m10, m12 | P2 | **YES** (consent language) |
| 7 | Obligations lifecycle | M10, M11, m2 | P1, P2 | no |
| 8 | Form 3926 fidelity | M6 | — | **YES** (this is the pass) |
| 9 | Deployment guardrails | M9, m14, m15, m17, m18, m20 (+PT-7) | — | no |

Every package: implement → full suite green (`python -m pytest engine/tests/ app/tests/ -q`,
baseline 337 + the package's new tests) → commit → next. MINORs not packaged (m3, m11, m19,
m21) stay on the INVENTORY backlog; m21 is a scoping fact, not a defect.

All three HITL packages ship working code at the best-known target with a visible
`PENDING-HUMAN-VERIFICATION` marker on the affected artifact; the human act removes the marker,
never gates the merge.
