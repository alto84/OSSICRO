# INV-3 commit_profile — Adversarial Review

**Reviewer:** standalone adversarial pass (regulatory-software + HIPAA-privacy lens), 2026-07-10.
**Scope:** `engine/ossicro/profile.py`, `engine/ossicro/models.py`, `app/server.py`, `engine/tests/test_profile.py`, `app/tests/test_commit_profile.py`, `app/static/index.html`, against `docs/ehr-integration/commit-profile-design.md`.
**Test run:** `python -m pytest engine/tests/ app/tests/ -q` → **198 passed in 1.39s** (128 pre-existing + 70 new, zero edits to old tests as the design promised).

## VERDICT: FIRE-after-patching — the hard gate is real and the tests would catch its removal, but one race can breach it, one reachable state deadlocks the UI, and the INV-8 "leaks nothing" claim is demonstrably false for low-entropy fields. All three are localized patches, not redesigns.

What I confirmed holds before the findings: the fail-closed line is genuinely enforced in the single-threaded path — `require_committed` runs first in both `_generate_payload` (server.py:401) and `_package_payload` (server.py:559), before any document is built, and nothing is persisted on refusal. Commit/edit/regenerate refuses with a 409 naming exactly the edited field (repro'd; also the named test `test_inv3_commit_then_mutate_then_reconfirm`). Canonicalization is sound: key-order independence, whitespace/NFC equivalence, `True` == `"true"` != `"True"`, revert-to-committed yields the identical hash and empty pending — all tested and verified. Commit is correctly *not* a gate sign-off: no role enforcement (an RN re-confirms in `test_commit_and_reconfirm_append_actioned_confirmations`), nothing touches `gates.record_signoff`/`HumanSignoff`, and `ProfileNotCommitted` is asserted not to be a `GateViolation`. Migration does no auto-commit and the legacy staleness branch is tested against the literal 6-key on-disk shape. The frontend gates generate client-side *and* folds the server 409 back into the commit panel on both `/generate` (index.html:1640) and `/package` (index.html:1891) — a stale button lands on a handled 409, not a bypass.

---

## BLOCKER

### B1. GET /package runs the hard gate without the lock — a concurrent intake write lets a package assemble from a drifted, unconfirmed input
**Where:** app/server.py:810-824 (the `_CASE_PACKAGE` GET branch calls `_package_payload(case)` with no `_LOCK`); contrast app/server.py:912 where `/generate` correctly holds `_LOCK`.
**Repro (by inspection; `ThreadingHTTPServer`, server.py:1008, gives real per-request threads):**
1. Thread A: `GET /api/case/X/package` → `require_committed(case["intake"], …)` passes on the committed intake (server.py:559).
2. Thread B: `POST /api/case/X/intake` mutates `case["intake"]` under `_LOCK` (which thread A never took).
3. Thread A continues: `_study_and_docs(case)` (server.py:560) re-reads the **now-mutated** shared dict and assembles a package from an input no named human confirmed — then `stamp_input_hash(documents, committed_hash)` stamps the *old committed hash* onto provenance records that did not consume it. That is the exact double violation the design forbids (fail-closed guarantee 5 + the §6 honesty rule), and it is silent.

Same pattern, lower stakes: `GET /check` (server.py:798-808) can stamp a hash that doesn't match what it consumed under the same race — the honesty rule, not the gate.
**Fix (3 lines):** snapshot once and use the snapshot everywhere in the payload builder — `intake = dict(case["intake"])` at the top of `_package_payload` (and `_generate_payload`/`_check_payload` for uniformity), pass it to `require_committed`, `build_study`, and `profile_hash`. Or wrap the GET package/check handlers in `with _LOCK:`. Snapshot is better: it also removes the dict-mutated-during-iteration crash mode. Add a regression test that monkeypatches `_study_and_docs` to mutate `case["intake"]` mid-call and asserts the package still reflects the gated snapshot.
**Real hole vs prototype limit:** real hole. Single-user localhost makes it unlikely, but the UI itself can race it (autosave/mirror + a package refresh), and the whole point of INV-3 is that the deliverable path *cannot* run on an unconfirmed input — "cannot unless two requests overlap" is not that.

---

## MAJOR

### M1. Reachable CONFIRMING state with `pending == []` — the 409 names nothing and the commit panel renders no action, dead-ending the user
**Where:** engine/ossicro/profile.py:287-290 (`require_committed` raises with `pending_fields(...)` which is empty here; message renders "(none listed)"); app/server.py:377-390 (`_profile_block` reports `state=CONFIRMING, pending=[]`); app/static/index.html:1501-1519 (the CONFIRMING branch renders only per-pending-field rows — zero rows — and **no commit button**, which exists only in the UNCOMMITTED branch at index.html:1529).
**Repro (executed, confirmed):** commit {a,b,c} → edit `a` and `b` → `POST /profile/confirm` on `a` only (staged) → revert `b` to its committed value. Now `pending_fields` = `[]` (the staged hash for `a` sits in the baseline, profile.py:172-176) but `profile_hash(intake) != committed hash` (the *commit* still reflects old `a`). Result: generate/package correctly refuse (fail-closed holds — good direction), but the exception carries `pending=[]`, `_profile_block` shows "0 fields have changed", and the panel offers no re-confirm rows and no commit button. Server-side `POST /profile/commit` *does* rescue (verified: returns 200 COMMITTED, folding the staged value in) — the UI just never offers it.
**Fix:** two halves. (1) In `_profile_block` / `require_committed`, when the hash differs but pending is empty, surface the staged field ids (or an explicit `"recommit_needed": true`) instead of an empty list — the refusal must always name a next action. (2) In the CONFIRMING branch of `renderCommitPanel`, when `pending.length === 0`, render a "Recommit profile" button wired to `commitProfile()`. Add a test for the exact repro sequence.
**Real hole vs prototype limit:** real hole in the *contract* ("refusal names the pending fields") and in the UX, though not in the gate — the failure direction is closed, which is the safe one.

### M2. INV-8 overclaim: unsalted field hashes are dictionary-reversible — I recovered `patient.sex` and `patient.age` from the commit object alone
**Where:** engine/ossicro/profile.py:143-155 (`field_value_hash` — deterministic, domain-separated but unkeyed and unsalted); the claim at profile.py:7-9 and design §2 step 4: "a committed_profile block leaks nothing from the chart even if a case JSON escapes."
**Repro (executed):** committed `{"patient.sex": "female", "patient.age": "44"}`; enumerated ≤124 candidate values offline against `field_hashes`; recovered both plaintexts exactly. The same works for any low-entropy PHI: sex, age, dates (~40k candidates), drug names (finite formulary), coded diagnoses (ICD vocabulary). Under the HIPAA lens this is the classic error — a hash of a value from an enumerable space is *not* de-identified. `profile_hash` is safer (whole-map preimage) but `field_hashes` and `staged` are per-field oracles, and `history` retains every superseded one.
**Fix:** minimum honest fix — delete/correct the "leaks nothing" claim in profile.py's docstring and the design, and state the real property ("field ids + value fingerprints; low-entropy values are recoverable by enumeration"). Better fix, still small: HMAC-SHA256 with a server-side key that lives *outside* the case JSON (`field_value_hash(value, key)`); pending detection and revert-equality all still work since only the server computes hashes. A per-commit random salt stored in the object defeats rainbow tables but not targeted enumeration — not sufficient alone.
**Real hole vs prototype limit:** borderline. All current data is synthetic fixture ("no real PHI", server.py:7), so nothing has leaked — acceptable prototype *behavior*. The written claim is not acceptable: it's exactly the sentence a later integrator will rely on. At minimum the claim must be corrected in the same patch; the HMAC fix can ride Q3's auth work.

---

## MINOR

### m1. The HTTP 409 contract is untested — deleting the `except ProfileNotCommitted` handlers keeps all 198 tests green
**Where:** app/server.py:817-820 and 916-920 (the handler-level mappings to `409 {error, pending, state}`); app/tests/test_commit_profile.py exercises the payload builders directly and asserts the *exception*, never the status/shape.
**Repro:** remove the two `except ProfileNotCommitted` clauses → suite passes → the generic `except Exception` returns **500** `{"error": "ProfileNotCommitted", …}` → the frontend's `e.status === 409` branch (index.html:1640, 1891) misses and the user gets a raw toast instead of being routed to the commit panel. Still fail-closed, but the documented contract dies silently.
**Fix:** one test that drives `Handler` via a socketless in-process request (or extract the two regex branches into testable functions like the payload builders) asserting status 409 and the `{error, pending, state}` keys for both `/generate` and `/package`.

### m2. Idempotent recommits pile duplicate history entries
**Where:** engine/ossicro/profile.py:212-228 (`commit_profile` unconditionally appends `prior` to history); app/server.py:643-649 only blocks recommit when pending is non-empty.
**Repro (executed):** commit → click Commit twice more with nothing changed → `history` holds 3 entries, all the same hash. Audit-trail noise that makes the real supersessions harder to read.
**Fix:** in `_profile_commit`, short-circuit 200 (or 409 "already committed at this hash") when `profile_hash(intake) == cp["profile_hash"]` and nothing is staged; or skip the history append when the new hash equals the prior's.

### m3. `_write_intake` mirrors the intake handler instead of exercising it
**Where:** app/tests/test_commit_profile.py:28-38 duplicates the store rule from app/server.py:874-900. If the handler's blank-drop / rev-bump logic ever drifts from the mirror, every profile test keeps passing against the stale copy. Acceptable for a socketless suite, but worth one integration-shaped test through the real POST body path (pairs with m1's fix).

### m4. `str(key)` coercion collides distinct keys
**Where:** engine/ossicro/profile.py:126. `{1: "x"}` and `{"1": "x"}` hash identically (verified). Unreachable through the JSON HTTP boundary (object keys are always strings), so theoretical — but the design's own rule is "a wrong key is a different field"; either reject non-str keys loudly or note the coercion.

### m5. Legacy staleness branch calls a reverted-but-hash-matching case stale until the first post-INV-3 generate
**Where:** app/server.py:373-374. Committed profile + `generated_hash` still None → counter rule governs, so edit-then-revert shows the stale banner even though the hash authority would clear it. Conservative direction, display-only, matches design §6's byte-identical-legacy intent. Fine as-is; noting so nobody "fixes" it into the unsafe direction.

### m6. Dead branch: frontend expects `res.profile` from POST /intake, which the server never sends
**Where:** app/static/index.html:1406-1409 vs app/server.py:902 (`{ok, intake_rev, stale}` only). Always falls through to `refreshProfile()` — one wasted GET per save, and a comment that misdescribes the contract. Either add the (cheap, already-computed) `"profile": _profile_block(case)` to the intake response or drop the branch.

---

## Test-quality answers (question 8, direct)

- **Is the INV-3 named test real?** Yes. `test_inv3_commit_then_mutate_then_reconfirm` (app/tests/test_commit_profile.py:72-105) performs the full commit → generate → mutate → assert-409-names-the-field → confirm → assert-new-hash → generate → assert-new-hash-stamped-and-history cycle against the real payload builder. Emptying `require_committed`'s checks fails it and 8+ others.
- **Does deleting `require_committed`'s raise fail a test?** Yes, immediately: `TestRequireCommitted` (engine), `TestUncommittedRefusal`, `TestLegacyMigration.test_legacy_generate_refused_never_committed`, and the named test all `assertRaises(ProfileNotCommitted)`.
- **Invariants claimed but untested:** the HTTP 409 status/shape (m1); the B1 concurrency guarantee (no test, and it's actually false); the "refusal names the pending fields" contract in the M1 corner (false there); "no role enforcement on commit" is evidenced only implicitly (RN actor) — cheap to make explicit.

## Reply from the team

Revision by the orchestrator (not the builders). Suite 198 → **201** (+3 review-patch
tests). Verdict accepted (FIRE-after-patching); the gate was confirmed real and its
removal test-caught. Disposition:

**B1 (BLOCKER — unlocked gate race) — CONCEDED, fixed.** `_generate_payload`,
`_package_payload`, and `_check_payload` now snapshot `intake = dict(case["intake"])`
once and thread it through `require_committed` → `_study_and_docs(case, intake)` →
`stamp_input_hash`, so a concurrent `POST /intake` can never make the build consume an
input the gate did not approve, and the stamped hash always matches what was built. Test
`test_b1_package_uses_gated_snapshot_under_mutation` spies `build_study`, mutates
`case["intake"]` mid-build, and asserts the build saw the committed snapshot.

**M1 (MAJOR — CONFIRMING-with-empty-pending dead-end) — CONCEDED, fixed.** `_profile_block`
now returns `recommit_needed: true` when the hash has drifted but pending is empty; the
frontend CONFIRMING branch renders a "Recommit profile" button in that state instead of an
empty panel. Test `test_m1_recommit_needed_state_has_an_action` drives the exact repro
(stage one edit, revert another) and asserts the state names an action and a plain recommit
rescues. Fail-closed direction was already correct; this fixes the contract + UX.

**M2 (MAJOR — INV-8 overclaim) — CONCEDED (claim corrected now; HMAC deferred to auth).**
The "leaks nothing" language is removed from `profile.py` and the design doc and replaced
with the honest property: unkeyed field hashes are enumeration-reversible for low-entropy
values (sex, age, dates, coded diagnoses), so the commit object is **not** PHI-safe at rest —
acceptable only because all data is synthetic. The HMAC-under-a-server-side-key hardening is
documented as riding the authentication work (Q3 / INV-7 tail), where key management is built
once, properly — not half-built here.

**m2 (idempotent-recommit history noise) — CONCEDED, fixed.** `commit_profile` skips the
history append when the new hash equals the prior and nothing was re-confirmed; test
`test_m2_idempotent_recommit_does_not_grow_history`.

**m1 (409 contract untested) — ACKNOWLEDGED, deferred to the Wave-1 hardening.** The
exception is tested; the HTTP status/shape mapping will get a socketless handler test in the
persistence-hardening pass (it pairs with m3's real-POST integration test). **m4/m5/m6** —
m5 is correct-as-is (noted so nobody "fixes" it unsafely); m4 (non-str key coercion) is
unreachable through the JSON boundary; m6 (dead frontend branch) is a one-GET waste, folded
into the hardening pass. None are gate or privacy holes.
