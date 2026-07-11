# Wave 4 adversarial review — Patient persona (F), Micro-CRO board (G), INV-5 promote() (H)

Standalone outside review (not the build team). 2026-07-10.
Scope: `app/server.py` (patient-link, `/api/patient/{token}`, `/promote`, `/cro/board`),
`app/static/index.html` (patient view, enroll card, CRO board), `app/tests/test_wave4_patient_cro_promote.py`,
BUILD-PLAN Wave 4. Method: full read + live probes through the real Handler (leak-grep of serialized
payloads against the sample fixture's identifiers, enumeration probes, malformed-payload probes) +
7 targeted mutations run against the Wave-4 test module.

**VERDICT: FIRE-after-patching** — the access model, the INV-5 gates, the HC3 clock honesty, and the
test suite all held under attack. Two MAJORs are content/coverage defects with small, local fixes;
nothing architectural. Patch MAJOR-1 and MAJOR-2 (and ideally MINOR-1/MINOR-6) before closing the wave.

Baseline: `python -m pytest engine/tests/ app/tests/ -q` → **334 passed**.

---

## MAJOR-1 — Emergency enrollment checklist silently drops the 21 CFR 56.104(c) IRB-notification duty (the shortest deadline of all)

- **Where:** `app/server.py:1225` — `followup = expanded_access_emergency_deadlines(auth_date)[0]`.
- **What:** The canonical clock function (`engine/ossicro/clocks.py:137`) returns **two** deadlines for an
  FDA emergency phone authorization: the 15-working-day written 3926 (312.310(d)(2)) **and the
  5-working-day IRB notification (56.104(c))**. `_enrollment_obligations` indexes `[0]` and discards `[1]`.
- **Repro (probe, confirmed):** commit a sample case with `submission.emergency=true`,
  `submission.emergency_auth_datetime=2026-06-26`, promote → `obligations_checklist` citations are
  `312.32(c)(1), 312.32(c)(2), 312.310(d)(2), 312.33` — no 56.104(c), even though it is the shortest
  clock the enrollment arms.
- **Why it matters:** the wave's own acceptance line (BUILD-PLAN SERIOUS-7) is *"the system must not walk
  a physician into duties it then ignores."* The promote card says "the obligation clocks are armed —
  OSSICRO tracks the deadlines," presenting the checklist as authoritative. The duty does appear in the
  CHECK screen's route clocks (`irb-notify-5-working-day`), so the system isn't wholly blind — but the
  one artifact promote() emits as "the duties the enrollment creates" omits it.
- **Fix:** append `expanded_access_emergency_deadlines(auth_date)[1]` as a fifth obligation (armed from
  the same recorded anchor; unarmed-with-resolving-question when the auth date is absent/unreadable,
  exactly like the 312.310(d)(2) row). Add a test asserting 56.104(c) is present and armed on the
  emergency path — none of the current tests would catch this regression.

## MAJOR-2 — The patient notice becomes factually false at the `enrolled` stage

- **Where:** `app/server.py:221-225` (`patient_notice`, unconditional) + `app/server.py:1131-1139`
  (`_patient_view` attaches it at every stage); `app/static/index.html:3226` (patient-mode draft bar
  hardcodes "Nothing has been sent to the FDA yet" before the fetch even returns).
- **What:** the enrolled-stage status honestly says *"your doctor has recorded that you are enrolled…
  responsible for watching your safety and sending required reports"* — while the standing notice on the
  same page still says *"Everything described here is a DRAFT that your doctor is preparing. Nothing has
  been submitted to the FDA, and no decision has been made."* Real enrollment follows FDA allowance
  (emergency path: FDA **has** decided, by phone) plus IRB and consent. Both sentences cannot be true.
- **Repro (probe, confirmed):** promote a case, GET `/api/patient/{token}` → `stage: "enrolled"` with the
  contradictory notice verbatim.
- **Why it matters:** the entire justification for the patient surface is 21 CFR Part 50 plain-language
  *honesty*. A notice that is false at exactly the stage where the stakes become real is the one defect
  this persona cannot carry. Note `test_stage_tracks_lifecycle` (test file :278-280) **enshrines** the
  defect by asserting the draft notice "never leaves."
- **Fix:** make the notice stage-conditional in STRINGS (draft/committed/released keep the current text;
  `enrolled` gets e.g. "This page only shows status. Your doctor's office can tell you exactly where
  things stand — they are the right people for every question."); have `enterPatientMode` re-render the
  top bar from the server's stage instead of hardcoding it; fix the test to assert the *stage-correct*
  notice.

## MAJOR-3 — Standing deploy condition, restated so it can't be lost: the token model is sound at the API, but the surrounding surface is unauthenticated

- **Where:** `app/server.py:1767-1786` (GET `/api/case/{id}` returns `patient_token`),
  `:1313-1369` (`/api/cro/board` lists every `case_id`), `HOST = "127.0.0.1"` (:163);
  `index.html` patient-mode is CSS/JS-only over the same origin that serves the full physician app.
- **What:** anyone who can reach the socket can walk board → case_id → full intake + patient_token. And
  because the server binds localhost only, the "share this link with the patient" URL
  (`#patient=<token>`) only actually opens on the physician's own machine — the patient surface is
  pilot scaffolding, not yet a shareable artifact.
- **Assessment:** this is the *documented* INV-7 deferral (BUILD-PLAN Wave 4 F; `cro_board_note` says the
  board "must not be exposed beyond the physician pilot"), and the localhost bind makes it safe today.
  Not a code change for this wave — but it is a hard precondition: **no bind change, port-forward, or
  tunnel until INV-7 auth lands**, or the token gate (which is real and tested) is moot.

## MINOR-1 — A non-string `actor` is stringified into the append-only record

- **Where:** `app/server.py:1265` (`_promote`), same pattern at `:1109` (`_patient_link`), `:957`
  (`_release`), `:1446` (`_profile_commit`).
- **Repro (probe, confirmed):** `POST /promote {"actor": {"name":"hax"}, ...}` → 200; the enrollment and
  the immutable audit record carry `actor = "{'name': 'hax'}"`. `{"actor": ["a"]}` → actor `"['a']"`.
  The named-human requirement is satisfied by `str()` of arbitrary JSON.
- **Fix:** `if not isinstance(actor, str)` → 400 across the four act endpoints (one shared helper).

## MINOR-2 — The patient token rides in a GET path: server log + browser history exposure

- **Where:** `app/server.py:1629-1630` (`log_message` writes every request line, token included, to
  stderr); the trailing-slash miss (`/api/patient/<tok>/`) falls to the generic 404 that echoes the path
  (`:1791`) — echo-to-sender only, no info gain, but the stderr log line is a durable capability copy.
- **Fix (cheap):** mask `/api/patient/...` paths in `log_message`. Accepted tradeoff otherwise —
  capability-URL is the design.

## MINOR-3 — Token lookup is a linear disk-loading scan with non-constant-time compare

- **Where:** `app/server.py:1074-1086` — every patient-view request re-lists the cases dir and `==`-compares
  per case. At 128 random bits a timing oracle is impractical, and case counts are tiny in the pilot;
  still, a `{token: case_id}` index plus `hmac.compare_digest` is a five-line hardening.

## MINOR-4 — The 312.33 annual-report arithmetic lives in server.py, not the canonical clocks

- **Where:** `app/server.py:1239-1247` — anniversary + 60 days computed inline (the Feb-29 fallback
  hardcodes `(year+1, 2, 28)`, correct only because `.replace(year+1)` can only fail on Feb 29). It is
  HC3-honest (anchored on the recorded receipt date via `ind_30_day_deadline`), so this is placement,
  not fabrication: move it into `ossicro.clocks` beside its siblings so one engine owns all deadline math.

## MINOR-5 — `_cro_board` / `_patient_view` read live case dicts outside `_LOCK`

- **Where:** `app/server.py:1319` (`dict(case["intake"])` before the try), `:1131`. A concurrent intake
  POST during the copy can raise `RuntimeError: dict changed size` → the whole board 500s (per-case
  rollup_error handling doesn't cover it). Single-user pilot makes this theoretical; snapshot under
  `_LOCK` when convenient.

## MINOR-6 — No leak-grep test over the CRO board payload

- **Where:** `app/tests/test_wave4_patient_cro_promote.py` — the patient view gets a serialized-payload
  PHI grep (`:236-261`); the board does not. A mutation adding `patient_token` or `patient.diagnosis` to
  a board row would survive the suite. The board is clean today (probe: no token, no diagnosis, no
  physician identifiers — coded id + drug only). Add the same raw-text assertion the patient view has.

---

## What was attacked and held

- **Token opacity/unguessability:** `uuid.uuid4().hex` (128-bit, `os.urandom`), minted server-side, never
  derived from the case; stable across re-shares, each share audit-logged with chain verified.
- **No enumeration:** bad token, the case_id itself, the case-flipped token, and a well-formed miss all
  return the identical bare `404 {"error": "not found"}`; the token is never echoed; there is no
  not-found vs not-authorized distinction to probe. No patient view exists until a named human mints the
  link (`patient_token: None` → unreachable).
- **Patient-view leak-grep (live probe):** none of case_id, physician name/phone/email/address/license,
  diagnosis, prior therapies, age, or sex appear in the serialized payload — coded id + drug name only.
  Jargon grep (CFR/IND/LOA/312.) clean; the vocabulary is genuinely plain, authored in STRINGS now, not
  deferred to Wave 5.
- **INV-5 gates (probes + mutations):** no promote without a named actor (400), a recognized
  `legal_basis` (400 + allowed list), and a committed, non-drifted profile (409 UNCOMMITTED / 409
  CONFIRMING with pending list). Repeat promote → 409 with the standing record; refusals mutate nothing
  (persist only on 200). Exactly one `promote` audit record; `verify_chain` intact.
- **HC3 clock honesty:** safety 15-day / 7-day clocks are per-event and always emitted `armed:false` with
  the correct per-event resolving question; 312.310(d)(2) arms only from the recorded phone-auth date via
  the canonical working-day engine (2026-06-26 → 2026-07-20, July-4 observance skipped); 312.33 arms only
  from the recorded FDA receipt date via `ind_30_day_deadline`; an unreadable date yields
  `armed:false, due:null` + a "could not be read" question — never a guessed date. Every obligation
  carries a real citation and `owner: "physician-sponsor"`.
- **No regulated act anywhere:** patient-link mints a token and explicitly sends nothing (the physician
  copies the URL); promote records a decision already made; the board is GET-only (POST → 404) and its
  rows render no buttons; release/LOA stay DRAFT with named-human framing. No send, sign, or submission
  path was found in server or frontend.
- **Test quality (mutation run, all CAUGHT):** token-check removed → caught; legal_basis check removed →
  caught; actor check removed → caught; committed-profile gate removed → caught; fabricated safety-clock
  date → caught; promote audit record dropped → caught; board POST route added → caught. 23/23 wave-4
  tests green at baseline. The two coverage holes that *would* survive mutation are named in MAJOR-1
  (56.104(c) absence) and MINOR-6 (board leak-grep).

## Reply from the team

Revision by the orchestrator. Suite 334 → **336**. Verdict accepted; the access model, INV-5
gates, and HC3 clock honesty were confirmed to hold under mutation.

**MAJOR-1 (emergency checklist drops the 56.104(c) IRB-notification duty) — CONCEDED, fixed.** The
enrollment obligations now emit BOTH deadlines `expanded_access_emergency_deadlines` returns: the
15-working-day written 3926 and the 5-working-day IRB notification (56.104(c)), the shortest of all.
Both list unarmed with a resolving question when no phone-authorization date is recorded, and both
arm from it. `test_emergency_followup_arms_from_recorded_authorization` now asserts 56.104(c) armed
to 2026-07-06 (five working days, the July-3 observance skipped); the citation-set and count tests
include it.

**MAJOR-2 (patient notice false at the enrolled stage) — CONCEDED, fixed.** The patient notice is
now stage-conditional. Draft, committed, and released keep the "nothing submitted to the FDA"
notice, which is true there. The enrolled stage gets a notice that makes no submission claim and
points to the doctor's office. The frontend's standing draft bar is hidden in patient mode, so the
server-driven card notice is the single source and is always stage-correct. The test that enshrined
the old behavior now asserts the stage-correct notice.

**MINOR-1 (non-string actor stringified into the immutable record) — CONCEDED, fixed.** A shared
`_actor_str` helper returns "" for any non-string actor, so a dict or list is rejected by the
existing "actor required" check across all six act endpoints. Test:
`test_non_string_actor_rejected_and_not_recorded`.

**MINOR-6 (no leak-grep over the CRO board) — CONCEDED, fixed.** `test_board_carries_no_token_or_clinical_phi`
asserts the board payload contains no patient_token and no diagnosis/age/sex.

**MAJOR-3, MINOR-2/3/4/5 — ACKNOWLEDGED.** MAJOR-3 is the documented INV-7 deferral (localhost bind
makes it safe; the standing rule holds: no bind change or tunnel until auth lands). MINOR-2 (mask the
token in request logs), MINOR-3 (constant-time token compare + index), MINOR-4 (move the 312.33
arithmetic into `clocks`), and MINOR-5 (snapshot under `_LOCK`) are real but low-severity on a
single-user synthetic pilot; folded into the persistence-and-security hardening pass.
