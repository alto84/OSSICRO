# Wave 2 adversarial review — INV-4 egress gateway + matching engine

**Reviewer:** standalone adversarial review (not the builder). **Date:** 2026-07-10.
**Scope:** `engine/ossicro/egress.py`, `engine/ossicro/matching.py`, fixtures
(`registry_sample.json`, `match_eval.json`), `app/server.py` (/match), the match UI in
`app/static/index.html`, `engine/tests/test_egress.py`, `engine/tests/test_matching.py`,
`app/tests/test_match_endpoint.py`, `TestEngineEgressBoundary` (test_fhir_ingest.py), and
BUILD-PLAN Wave 2 incl. the Fable amendments. Full suite run: **280 passed** (`python -m
pytest engine/tests/ app/tests/ -q`). Every finding below was reproduced by executing code,
not by reading it.

## VERDICT: FIRE-after-patching

No hard line is violated in the shipped build: live egress is structurally off (two
independent walls — the flag raises `EgressDisabled`, and even a flipped flag hits a live
branch that raises because no client exists, egress.py:394–402), the only product
construction path is the closed-vocabulary `from_profile`, /match is hard-gated on a
committed profile and mutates nothing, and the organizer emits criteria — never a score.
But the marquee safety claim ("free text is structurally unrepresentable") is **overstated
in three specific, demonstrated ways**, and the boundary test that the BUILD-PLAN says
*enforces* the egress perimeter has a trivial evasion. These must be patched before the
struct is treated as the thing the future live-egress greenlight leans on.

---

## MAJOR-1 — `_CODE_RE` accepts single-token names, coded patient ids, and 8-digit dates as "condition codes"

**Where:** `engine/ossicro/egress.py:105` (`_CODE_RE = ^[A-Za-z0-9][A-Za-z0-9.]{0,17}$`),
enforced at `egress.py:126–132`; the claim it fails to back is at egress.py:12–14 and 24–25.

**Repro (all pass construction and flow to the adapter un-rolled):**
```python
DeidentifiedPredicates(condition_codes=("Rivera",))       # a surname
DeidentifiedPredicates(condition_codes=("19680314",))     # a DOB, YYYYMMDD (no separators -> _looks_like_date misses it)
DeidentifiedPredicates(condition_codes=("PT3926.014",))   # a coded patient id
decompose_query(...)  ->  outbound condition_codes == ['Rivera']
```
`test_free_text_rejected` only probes multi-word strings ("metastatic disease"); no test
probes a single-token identifier, so the suite rubber-stamps the docstring's claim.

**Why it matters:** the struct is the wall the greenlight will rely on. Today `from_profile`
is the only product path and it emits codes solely from the closed term table, so this is
defense-in-depth, not an active leak — but the wall itself is advertised as closed and is
not.

**Fix:** replace the one permissive regex with the two real shapes it claims to accept —
SNOMED CT (`^\d{6,18}$`) OR ICD-10-CM (`^[A-Za-z]\d{2}(\.[A-Za-z0-9]{1,4})?$`) — which
rejects all three probes above (no all-alpha tokens; 8-digit dates fail the ICD shape and
are implausible SNOMED but if desired add an explicit YYYYMMDD/8-digit-date refusal).
Add the three probes as tests.

## MAJOR-2 — `from_profile` DOES copy one raw intake value outbound: the first token of `drug.name`

**Where:** `engine/ossicro/egress.py:205` + `_drug_token` at egress.py:266–271;
sent outbound at egress.py:337/409.

**Repro:**
```python
p = DeidentifiedPredicates.from_profile({"drug.name": "Rivera investigational compound"})
p.drug_name == "Rivera"           # a surname, derived from raw intake text
# egress_query(...) -> adapter receives drug_name='Rivera'
```
Condition codes and route codes pass through closed local tables; `drug_name` is the **one
field where raw intake text crosses the boundary** validated only by shape (single token,
letters/digits/hyphens). A patient or investigator name mis-typed into the drug field — a
realistic intake error — egresses. The module's otherwise honest residual-risk statement
(egress.py:40–51) does not mention this at all, and the answer to "does from_profile ever
copy a raw value?" is currently *yes, this one*.

**Fix (any of, in preference order):** (a) a closed drug vocabulary / RxNorm table like the
condition and route tables — unrecognized drug ⇒ `drug_name=None`, honest absence; (b) keep
the token but add it explicitly to the residual-risk statement AND surface the derived
predicates to the physician **before** the query fires (the UI shows `predicates_used` only
*after* the response, index.html:2160–2163 — fine while the adapter is a mock, wrong order
once live). (b) is the minimum; (a) is what the rest of the module's design says it wants.

## MAJOR-3 — `TestEngineEgressBoundary` is evaded by `from urllib import request`

**Where:** `engine/tests/test_fhir_ingest.py:1078–1080`.

**Repro:** the forbidden regex
`^\s*(?:import|from)\s+(urllib\.request|socket|requests|httpx|httplib2|aiohttp|http\.client)\b`
does not match `from urllib import request` (nor `import urllib` + attribute access, nor
`importlib.import_module("urllib.request")`). Verified: `rx.search("from urllib import
request\n")` ⇒ None. A future module using the plausible alternate spelling passes the test
the BUILD-PLAN names as the *enforcement* of the perimeter ("`TestEngineEgressBoundary`
extended to *enforce* it", BUILD-PLAN.md:54).

**Fix:** forbid the parent packages, not just the submodule paths:
`(urllib|socket|requests|httpx|httplib2|aiohttp|http\.client|http$)` — i.e. any
`import urllib`/`from urllib import ...` spelling — and add `importlib` to the swept list
or document dynamic import as an accepted residual of a source-level check. (Confirmed
otherwise clean: a repo grep shows `urllib`/socket/requests imports in exactly one engine
module — egress.py:63; `review_claude.py` lazily imports only `anthropic` inside
`from_anthropic`, and neither sanctioned module contains the string `fhir_ingest` —
enforced at test_fhir_ingest.py:1099–1105 and passing.)

## MINOR-4 — matching.py claims route is "compared LOCALLY in this module"; it never is

**Where:** claim at `engine/ossicro/matching.py:26–27`; `_criteria`
(matching.py:113–191) reads condition/age/sex/drug_name/unstructured and **never**
`route_code` (grep: zero occurrences of `route_code` in matching.py). `route_code` is
correctly *withheld* from egress (good) but then dropped on the floor.

**Repro:** add `"route": "oral"`-style structured eligibility to a fixture record — it
renders with no trace: not matched, not unmatched, not unverifiable. Same for **any**
unrecognized structured eligibility key (e.g. `"pregnancy_excluded": true`) — silently
ignored, contra the module's own "honest unverifiable, never silently ignored" principle
(matching.py:185–189, applied only to the `unstructured` list).

**Fix:** either compare route (records carry none today, so the honest v1 move is:) emit
`"not evaluated from structured data: <key>"` unverifiable entries for every structured
eligibility key `_criteria` does not recognize, and correct the docstring to "age / sex /
drug compared locally; route withheld from egress and not yet compared."

## MINOR-5 — egress audit records carry `drug_name` + condition codes while tests/docs call them "value-free"

**Where:** detail written at `engine/ossicro/egress.py:382–392`; called "value-free" at
`engine/tests/test_egress.py:13` and returned verbatim by `/audit` under the comment "the
trail carries no chart values (INV-8)" (`app/server.py:955–957`).

`"Cytoravir"` is an intake value (`drug.name`) and it sits in the persisted, verbatim-served
audit trail; the app test's `INTAKE_ONLY_STRINGS` list simply omits it. Recording the exact
outbound facts is the *right* design (accountability for what left the machine) — but it is
a deliberate, bounded exception to INV-8's no-values rule and should be named as such, not
papered over with "value-free." **Fix:** wording only — "identifier-free; carries exactly
the de-identified outbound facts" in both places, and add `Cytoravir` awareness to the test
comment so the next reviewer doesn't read it as a hole.

## MINOR-6 — mini-eval: real, but its recall/precision arithmetic is decorative and it benchmarks retrieval only

**Where:** `engine/fixtures/match_eval.json`, `engine/tests/test_matching.py:172–198`.

The eval is **not a rubber stamp** on retrieval: I verified it would catch the three
realistic regressions — silent filtering of unmatched candidates (NCT90000004, male-only,
is *expected* for a female patient), a v1-scope leak (`DRUG-90000001` in `must_not_return`),
and false absence (case 3 asserts `absence` true). But (a) the recall/precision computation
sits on top of `assertEqual(returned, expected)` which already forces both to 1.0 — the
metrics can never say anything the assertion didn't; (b) no eval case labels expected
*criteria* outcomes, so a `_criteria` regression (e.g. age-straddle wrongly called matched)
passes the eval and is caught only by unit tests. **Fix:** add per-candidate expected
`matched/unmatched/unverifiable` labels to at least one eval case; either drop the
metric arithmetic or compute it before asserting.

---

## Pressed questions the build survives (verified, not assumed)

- **Live path:** `_LIVE_EGRESS_ENABLED=False`; `live=True` raises before the adapter is
  touched (test_egress.py:181–188); even a flipped flag raises at the GREENLIGHT MARKER
  (egress.py:394–402). No test binds a port or opens a socket; the app tests drive the real
  Handler over a fake socket.
- **Decomposition:** age band / sex / route provably never reach the adapter
  (test_egress.py:251–260) and never appear in the outbound dict (egress.py:336–345); the
  audit records name the withheld fields without their values. ICD-10 roll-up works;
  SNOMED pass-through + clinic-source/timing/linkability residuals are documented honestly
  (egress.py:40–51) — the missing item is MAJOR-2's drug token.
- **Organizer, not recommender:** no score/confidence/rank key anywhere (asserted over the
  serialized response, both suites); candidates in registry order; unmatched criteria are
  shown, not filtered; absence renders the exact "in the queried registries as of <date>"
  framing verbatim in the UI with an explicit "not a statement that no options exist" note
  (index.html:2165–2173); v1 kinds filter drops `drug_listing` structurally (matching.py:54,
  216–218).
- **/match:** gated by the same `require_committed` as /generate (server.py:654–656; 409
  UNCOMMITTED and 409 CONFIRMING both tested); mutates nothing but the append-only audit
  trail (intake/rev/hash byte-stable, tested); error payloads carry the exception type only.
- **No auto-action anywhere:** the UI's only affordance per candidate is a link to the
  source registry; "OSSICRO ranks nothing, scores nothing, and contacts no one"
  (index.html:2133–2134) is true of the code.

## Reply from the team

Revision by the orchestrator. Suite 280 → **282**. Verdict accepted (no hard line breached;
the overstated-wall findings patched before the struct becomes the greenlight's foundation):

**MAJOR-1 (permissive code regex) — CONCEDED, fixed.** `_CODE_RE` replaced by two real shapes —
SNOMED CT (`^\d{6,18}$`) OR ICD-10-CM (`^[A-Za-z]\d{2}(\.[A-Za-z0-9]{1,4})?$`) — plus an explicit
YYYYMMDD refusal. The three probes ("Rivera", "19680314", "PT3926.014") now fail construction;
real codes still pass. Test `test_single_token_identifiers_rejected_as_codes`.

**MAJOR-2 (raw `drug.name` token egressed) — CONCEDED, fixed.** `from_profile` now derives the drug
through a CLOSED table (`_DRUG_TERM_TOKENS`), exactly like conditions and routes — a known agent
resolves to its canonical token, an investigational/unrecognized agent (or a name mistyped into the
drug field) resolves to `None`. Raw drug text can no longer leave. The sample's investigational
"Cytoravir" → `None` (honest absence; matching proceeds on the condition axis). Test
`test_drug_derived_from_closed_table_only` includes the "Rivera investigational compound" repro.

**MAJOR-3 (boundary test evaded by `from urllib import request`) — CONCEDED, fixed.**
`TestEngineEgressBoundary` now forbids the PARENT packages (`urllib|socket|requests|httpx|httplib2|
aiohttp|http|importlib`), catching every import spelling and dynamic import; verified no legit
engine module trips it (only the sanctioned `egress.py` imports urllib).

**MINOR-4 (unrecognized eligibility keys silently dropped) — CONCEDED, fixed.** `_criteria` now
surfaces any structured eligibility key it does not evaluate (route, pregnancy exclusions, ...) as
`"not evaluated from structured data: <key>"` unverifiable, and the docstring is corrected. Test
`test_unevaluated_keys_are_unverifiable`.

**MINOR-5 ("value-free" overstates the egress records) — CONCEDED, fixed.** Wording corrected in
`test_egress.py` and the `/audit` handler: the trail is "identifier-free" and egress records carry
"the de-identified outbound facts (codes/bands/tokens), never raw chart text" — a bounded, named
exception to INV-8's no-values rule (accountability for exactly what left the machine).

**MINOR-6 (eval arithmetic decorative; retrieval-only) — ACKNOWLEDGED, deferred.** The reviewer
confirmed the eval already catches the three realistic regressions (silent unmatched-filtering, v1
scope leak, false absence). Per-candidate expected-criteria labels are a worthwhile enhancement for
the next matching iteration (when the criteria logic grows); tracked, not blocking.
