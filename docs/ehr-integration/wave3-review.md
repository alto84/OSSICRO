# Wave 3 adversarial review — Form-3926 PDF/FDF export + Pharma persona / RELEASE gate

Standalone reviewer (not the builder). 2026-07-10.
Scope: `engine/ossicro/pdf_3926.py`, `app/server.py` (form3926.pdf/.fdf, /release,
/manufacturer/inbox), `app/static/index.html` (download + release + pharma view),
`engine/tests/test_pdf_3926.py`, `app/tests/test_wave3_pdf_release.py`, BUILD-PLAN Wave 3.

**VERDICT: FIRE-after-patching** — the send gate, the DRAFT watermark, the audit chain, and the
de-identified inbox all hold under attack (four live mutants of the gates were each caught by an
existing test), and the hand-written PDF is structurally valid in three independent parsers. One
MAJOR must be patched or explicitly accepted-and-documented before Wave 3 is called done: the
inbox hands the manufacturer persona the `case_id`, which is a full-access capability on every
other unauthenticated endpoint.

## How it was attacked

- `python -m pytest engine/tests/ app/tests/ -q` → **310 passed, 1.81s**.
- Mutation tests (in-process monkeypatch, then the shipped tests re-run):
  gate removed from PDF/FDF/release → 3/3 tests fail; inbox made to serve un-released cases →
  caught; release audit record skipped → caught; watermark op deleted → caught.
- PDF validated beyond the header: every xref offset points at its `N 0 obj`; every stream
  `/Length` is byte-exact; opens and extracts text in pypdf 6.10.2, PyPDF2 3.0.1, and PyMuPDF
  (2 pages, watermark text extractable on page 1).
- Injection: `drug.name = 'X) /V (pwn) >> ] >> >>'` — correctly paren-escaped in both PDF and
  FDF (`_pdf_escape`, pdf_3926.py:207); no object/trailer breakout.
- Fabrication: `render_3926_pdf({})` contains none of the sample's values; missing fields render
  as empty `(Label: )` — never `[[MISSING`, never a default. No wall-clock date in the PDF.
- Released-view grep: `Female`, `58`, `patient.age`, prior-therapies text, `no_alternative_basis`
  all ABSENT from the release snapshot; present are only coded id (`PT-3926-014`), drug,
  diagnosis summary, physician contact, and the LOA-request text. The route schema itself carries
  no name/DOB/MRN/patient-address field, so those identifiers cannot exist to leak.
- Un-released case in the inbox: unreachable — `_manufacturer_inbox` (server.py:816) skips any
  case whose `released` record is absent or not targeted at `manufacturer`; the view served is
  the release-time snapshot (server.py:795-804), verified immune to post-release intake edits.
- Release without a named human: blank/whitespace actor → 400 (server.py:767); uncommitted
  profile → 409 via `require_committed`; committed-but-never-generated → 409
  (`generated_hash != committed_hash`, server.py:780); generated-then-drifted → 409; repeat
  release for the same committed hash → 409. Exactly one hash-chained `release` audit record per
  act; `audit.verify_chain` returns intact in the tests and the chain binds prev-hash correctly
  (audit.py:87-115).
- Forbidden acts: no endpoint or UI affordance sends, authorizes, supplies, or signs. The pharma
  view renders NO decision control (index.html pharma section; "supply/authorize decision …
  manufacturer's alone" note); release copy says "Nothing was sent"; signature blocks in the PDF
  and LOA are blank notices flagged NON-DELEGABLE HUMAN ACT / EXTERNAL-PARTY ACT.
- Pure stdlib: `pdf_3926.py` imports `textwrap` + `typing` only, and it sits inside the
  glob-based `TestEngineEgressBoundary` sweep (test_fhir_ingest.py:1068), so adding a network
  import would fail the suite.
- FDF honesty: all 30 right-hand AcroForm names carry `TODO(HUMAN-VERIFY)` (pdf_3926.py:75-113),
  the FDF file itself opens with an UNVERIFIED-placeholders comment AND carries an in-data
  `ossicro_draft_notice` field, and the endpoint docstring repeats it. Honest three times over.

## Findings

### MAJOR-1 — Inbox exposes `case_id`, a full-access capability that bypasses the release snapshot
- **Where:** server.py:837 (`"case_id": case_id` in the inbox item) + server.py:1217-1232
  (unauthenticated `GET /api/case/{id}` returns the ENTIRE intake) — likewise `/check`,
  `/audit`, `/package`, `/form3926.pdf`.
- **Repro:** `GET /api/manufacturer/inbox` → take any `case_id` → `GET /api/case/{case_id}` →
  age 58, sex Female, full prior-therapies history, clinical rationale, consent narratives.
  Demonstrated live during review.
- **Why it matters:** the release view is carefully minimized to coded-id + clinical summary,
  but the same response hands over the key that unlocks everything the minimization excluded.
  BUILD-PLAN Wave 4 already rules case-id-as-capability unacceptable for the patient persona
  ("a patient surface cannot ship with case-id-as-capability"); the pharma persona is the same
  class of surface. BLOCKER-2's intent ("nothing the physician produced becomes visible in any
  other persona without a release act") is enforced at one endpoint and voidable at five others.
- **Bounding:** localhost-only, synthetic-only pilot, and NO persona auth exists anywhere by
  design (INV-7 deferred) — so this is MAJOR, not BLOCKER.
- **Fix (small):** mint an opaque `release_id` (uuid) into the `released` record at release time
  and key inbox items by it instead of `case_id`; or, if deferral is chosen, state in
  BUILD-PLAN/README that persona separation is UI-only until INV-7 and add a test asserting the
  inbox item set contains no `case_id` key.

### MINOR-2 — FDF gate lacks a drift-state test
- **Where:** app/tests/test_wave3_pdf_release.py:151 (`test_fdf_409_pre_commit`).
- **Repro:** the PDF has `test_pdf_409_after_drift` (CONFIRMING → 409); the FDF is only tested
  UNCOMMITTED. A regression that gates `_form3926_fdf_bytes` on "a commit exists" rather than
  `require_committed` would pass every shipped test.
- **Fix:** clone `test_pdf_409_after_drift` for `.fdf` (4 lines).

### MINOR-3 — PDF/FDF export writes no audit record
- **Where:** server.py:723-745; audit actions exist for commit / reconfirm / signoff /
  bundle_loaded / egress_query / release — but not for exporting the filled 3926, the artifact
  the plan itself calls "one email from a submission".
- **Fix:** append an `export` audit record (target = `form3926.pdf`/`.fdf`, input_hash =
  committed hash, actor honestly blank — a GET has no named actor) under `_LOCK` in the two
  handlers. Not strictly required by BUILD-PLAN Wave 1's list; consistency argues for it.

### MINOR-4 — Free-text de-identification in the released view is honor-system
- **Where:** server.py:795-801 — `indication` passes `patient.diagnosis` verbatim; the LOA
  request embeds the same free text (ea_generators.py:741).
- **Repro:** a physician who types "Jane Doe, DOB 1/2/1968" into the diagnosis field releases it.
- **Bounding:** the schema is coded-only (no identifier fields exist), the pilot is synthetic,
  and the intake UI labels the coded-id rule. Fix later: a naive identifier lint at release time,
  or accept as documented residual (mirroring the INV-4 residual-risk pattern).

### MINOR-5 — `_manufacturer_inbox` snapshots `CASES` outside `_LOCK`
- **Where:** server.py:823-827 under `ThreadingHTTPServer`.
- **Repro:** `set(CASES)` racing a concurrent `POST /api/case` can raise
  `RuntimeError: dictionary changed size during iteration` (CPython-version dependent; reads of
  the `released` dict itself are safe — single reference assignment under lock).
- **Fix:** take `_LOCK` around the id-snapshot two-liner.

## Verified-good (explicit, so the team doesn't re-litigate)

- Send gate unbypassable at the inbox endpoint itself; mutation-verified.
- Release = named human + committed profile + docs generated from exactly that commit + LOA
  present; single audit record; chain intact; re-release only after recommit+regenerate.
- Inbox item key set is closed and tested (`test_released_case_appears_with_coded_id_only`
  asserts the exact key set — a leaked extra key fails the test).
- PDF structurally valid (3 parsers), watermark + human-review footer on every page including
  page 2+, no unwatermarked render path exists in code, nothing fabricated, injection-safe.
- FDF field map flagged unverified in map, file, and docs; synthetic-only stated.
- No send/auto-decision/signature anywhere; UI renders no decision affordance in pharma view.
- Pure stdlib; module swept by the egress boundary test automatically.
- 310/310 tests green; the new tests are load-bearing, not decorative.

## Reply from the team

Revision by the orchestrator. Suite 310 → **311**. Verdict accepted; the send gate, watermark,
audit chain, and de-identified inbox were all confirmed to hold under mutation.

**MAJOR-1 (inbox leaks `case_id`, a full-access capability) — CONCEDED, fixed.** Release now mints
an opaque `release_id` (uuid) into the `released` record, and the manufacturer inbox keys on it —
the `case_id` is never sent. Persona separation is now real, not just UI. Tests updated:
`test_released_case_appears_with_coded_id_only` asserts the item's exact key set contains
`release_id`, **no** `case_id`, and that the case_id string never appears in the serialized item;
the frontend renders the coded/opaque ids only. (An idempotent re-release reuses the prior
`release_id`.)

**MINOR-2 (FDF drift untested) — CONCEDED, fixed.** `test_fdf_409_after_drift` mirrors the PDF
drift test, so a regression that gated the FDF on "a commit exists" rather than `require_committed`
now fails.

**MINOR-5 (inbox snapshots `CASES` outside `_LOCK`) — CONCEDED, fixed.** The id-snapshot is taken
under `_LOCK`.

**MINOR-3 (export writes no audit record) — ACKNOWLEDGED, deferred deliberately.** Adding a side
effect (audit append + `_save_case`) to a GET is a design smell, and a re-download would spam the
trail. If export-tracking is wanted, it belongs as an explicit POSTed "export" act or a dedup'd
record — folded into the Wave-5 hardening decision, not bolted onto a GET now.

**MINOR-4 (free-text de-id in the released view is honor-system) — ACKNOWLEDGED, documented
residual.** The route schema is coded-only (no name/DOB/MRN/address field exists to leak), the
pilot is synthetic, and the intake UI labels the coded-id rule; `indication` is the physician's
own `patient.diagnosis` free text. This is the same class as the INV-4 documented residual: a
release-time identifier lint is a reasonable Wave-5 defense-in-depth item, tracked, not blocking a
synthetic-only build.
