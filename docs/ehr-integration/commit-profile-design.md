# INV-3 Design — Committed Profile + Per-Field Re-Confirmation Gate

**Status: DESIGN ONLY (Phase 14 milestone). Nothing in this document is implemented.**
Version 1.0 — 2026-07-10. Companion to `privacy-state-machine.md` (§2 `PROFILE_COMMITTED`,
§4 INV-3 row, §5 guarantees 4–5) and `review.md` B3 ("`commit_profile` does not exist").
Constitution anchors: HC1 (nothing auto drives generation before a named human confirms it),
HC5 (identity and disposition of the human reviewer recorded), INV-8 (no chart values in
logs — this design stores value *hashes*, never values, in the commit object).

Everything below is grounded in the code as read on 2026-07-10:
`engine/ossicro/models.py`, `gates.py`, `pipeline.py`, `generate.py`,
`ea_generators.py`, and `app/server.py`.

---

## 0. What exists today (the substrate this design builds on)

| Fact | Where |
|---|---|
| Case store is a flat dict: `{intake, route_id, signoffs, intake_rev, generated_rev, confirmations, field_provenance}` (+ optional `privacy_log`) | `app/server.py:93-100` (`_new_case`) |
| `intake` is a **flat dotted-key → scalar** map; empty values are never stored ("blanks stay honestly absent") | `server.py:674-679` |
| `intake_rev` increments on any effective intake change; `generated_rev` is set to `intake_rev` at generate time; staleness = `generated_rev is not None and generated_rev != intake_rev` | `server.py:698-699, 347, 336-337` |
| **Documents are never persisted.** Every `/generate`, `/check`, `/package` call regenerates from current intake via `_study_and_docs` → `build_study(case["intake"], route)` → `generate_route_documents` | `server.py:189-194` |
| Every filled span emits `ProvenanceRecord(span, source, citation)` — three fields, no hash slot | `models.py:42-48`; stamped at `generate.py:306-313, 321-329` and `ea_generators.py:285, 295, 309` |
| `confirmations` trail: `{actor, field_ids, from_chart, at}` appended **only when an actor is named**; `field_provenance` per-field `chart-confirmed`/`manual`. Actor is optional on `POST /intake` — anonymous writes are legal today | `server.py:667-697` |
| Sign-offs are a separate axis: `_record_signoff` validates gate/role/named-human and persists; `_apply_signoffs` re-applies them to freshly regenerated docs through `gates.record_signoff` on every request | `server.py:458-492, 163-186` |
| The pipeline is escalate-only; nothing in check can clear a gate; `_normalize_case` back-fills missing keys on load (the existing lazy-migration pattern) | `pipeline.py:132-250`; `server.py:103-107` |
| `TriggerDateError` shows the established pattern for a structured, user-fixable refusal (caught and returned as 400 with `field_id`) | `server.py:715-716` |
| On-disk legacy shape exists with only 6 keys (pre-confirmations): e.g. `app/data/cases/125ca025f7ee.json` = `{generated_rev, intake, intake_rev, route_id, signoffs}` | disk, verified |

Design consequence of the "documents are never persisted" fact: the input-of-record hash
cannot be attached at some one-time "generation event" — it must be recomputable and
re-stamped on **every** regeneration, and the gate must be a comparison between the
*current* intake's hash and the *committed* hash.

---

## 1. Design overview

One new engine module (`engine/ossicro/profile.py`, pure stdlib: `hashlib`, `json`,
`unicodedata`, `dataclasses`), one new case key (`committed_profile`), two new endpoints,
one new field on `ProvenanceRecord`, and a fail-closed check in `_generate_payload` /
`_package_payload`.

Per-case profile state machine (derived, never stored as a string — unrepresentable-drift
principle):

```
UNCOMMITTED        committed_profile is None (every legacy + new case)
   │  POST /profile/commit {actor}      ← the named human act (HC1/HC5)
   ▼
COMMITTED          committed_profile set AND pending_fields() == []
   │  any effective POST /intake write  ← automatic re-entry, no ceremony
   ▼
CONFIRMING         committed_profile set AND pending_fields() != []
   │  POST /profile/confirm {actor, field_ids}  — per changed field, not whole form
   │  (confirming the last pending field auto-recommits → NEW profile_hash)
   ▼
COMMITTED (new hash)
```

- `/generate` and `/package` are allowed **only** in COMMITTED and only when the current
  intake's hash equals the committed hash. Refusal is structured (409), names the pending
  fields, and never generates (fail closed — state-machine guarantee 5).
- `/check` runs in **any** state (its resolving questions are how the user gets back to
  COMMITTED) but reports the profile state honestly and stamps the *true* hash of what it
  consumed (§6).
- `POST /intake` is mechanically unchanged: it writes values and bumps `intake_rev`.
  Writing a field after commit *is* the CONFIRMING transition; no new blocking there.
- FHIR import is untouched: proposals only (INV-2), applied via `/intake`, which lands the
  fields in pending, which requires named re-confirmation. INV-2 and INV-3 compose with
  no new coupling.

Commit is **attribution, not a gate sign-off**. It deliberately does not use
`models.HumanSignoff`/`gates.record_signoff` — those are the non-delegable regulatory acts
(1571 signature, consent, IRB) with role enforcement (`gates.py:63-106`). Commit is the
same species as the existing `confirmations` trail (`server.py:689-697`): a named-actor
attribution record. Conflating them would let a "profile commit" look like a Part-11 act,
which review B3 explicitly warns against.

---

## 2. Canonicalization + hash spec (the input-of-record)

Hashed object: **`case["intake"]` exactly as stored** — the flat dotted-key map. Not the
unflattened `Study.raw` (`ea_generators.unflatten` at `ea_generators.py:43-56` plus
`build_study`'s derived defaults at `:67-82` inject `title`, `ind_number`,
`protocol_number`, `required_documents` — those are *derived*, and hashing derived values
would make the hash depend on generator code, not on what the human confirmed). The flat
intake is the exact thing the named human confirms and the only thing `build_study`
consumes, so it is the input-of-record. The route is a function of
`submission.emergency` (`server.py:158-160`), which is itself an intake field, so the
hash covers route selection for free.

Canonical form, versioned:

1. **Keys**: taken verbatim (schema ids from `routes_mod.intake_fields()`; no case-folding,
   no normalization — a wrong key is a different field, and the server already rejects
   nothing here, so the hash must not paper over key typos).
2. **Values**: drop entries that are `None` or whitespace-only (mirrors the store rule at
   `server.py:675-677`, so the hash can never differ from stored intake on emptiness).
   Then per value:
   - non-string scalar / list / dict → `json.dumps(v, sort_keys=True, ensure_ascii=True)`
     first (uniform text form; avoids Python `str(True)` = `"True"` vs JSON `true` drift);
   - strings used as-is;
   - then `unicodedata.normalize("NFC", text)` and whitespace normalization:
     `" ".join(text.split())` (collapses runs, strips ends, folds newlines/tabs).
     Normalization is **hash-only** — stored intake and generated documents keep the
     user's original text; only the equivalence class for "did the input change" is
     whitespace-insensitive, per the INV-3 wording "canonicalize (sorted keys, normalized
     whitespace)".
   - if normalization empties the value, drop the entry (same honesty rule).
3. **Serialization / preimage** (domain-separated and versioned so a future change can
   never silently collide):

   ```
   preimage = "ossicro-profile-v1\n"
            + json.dumps(canon_map, sort_keys=True,
                         separators=(",", ":"), ensure_ascii=True)
   profile_hash = "sha256:" + hashlib.sha256(preimage.encode("utf-8")).hexdigest()
   ```

4. **Per-field value hash** (for pending detection and INV-8-clean storage):
   `field_value_hash(v) = "sha256:" + sha256("ossicro-field-v1\n" + canonical_value)`.
   The commit object stores these hashes, **never the values** — a committed_profile
   block leaks nothing from the chart even if a case JSON escapes.

Explicit exclusions from the hash: `signoffs` (separate gate axis; §7 handles the
interaction), `confirmations` / `field_provenance` (attribution about the input, not the
input), `privacy_log`, `route_id` (derived), the rev counters.

---

## 3. The committed-profile object (case schema)

New key on the case dict, persisted by the existing atomic `_save_case`
(`server.py:114-122`); `None` means UNCOMMITTED:

```json
"committed_profile": {
  "canon_version": 1,
  "profile_hash": "sha256:…",
  "field_hashes": {"patient.coded_id": "sha256:…", "drug.name": "sha256:…", …},
  "committed_by": "Jordan A. Rivera, MD",
  "committed_at": "2026-07-10T14:03:22Z",
  "intake_rev_at_commit": 7,
  "staged": {},
  "history": [
    {"profile_hash": "sha256:…", "committed_by": "…", "committed_at": "…",
     "intake_rev_at_commit": 3, "reconfirmed_fields": ["patient.diagnosis"]}
  ]
}
```

- `field_hashes`: one entry per intake field at commit time. This is what makes pending
  detection **computed, not bookkept** (§4) — the intake handler needs zero new logic.
- `staged`: the partial-re-confirmation ledger, `{field_id: value_hash_confirmed}`.
  Present so a user can re-confirm 2 of 5 pending fields, leave, and come back; and so a
  field edited *again after* being re-confirmed correctly re-enters pending (its current
  value hash no longer matches its staged hash).
- `history`: prior commits, appended on every recommit. Each entry is ~200 bytes of
  hashes and attribution; unbounded is fine at this scale (open question Q7).
- `intake_rev_at_commit`: the bridge to the existing counter (§6).

---

## 4. Pending-field computation (the re-confirmation gate)

Pure function in `profile.py`, computed on every read — never stored, so it can never
drift from intake:

```python
def pending_fields(intake: dict, committed: dict) -> list[str]:
    # committed is the committed_profile dict; caller handles None (UNCOMMITTED).
    current = {k: field_value_hash(v) for k, v in canonical_items(intake)}
    baseline = dict(committed["field_hashes"])
    baseline.update(committed.get("staged", {}))     # staged re-confirmations count
    changed  = [k for k, h in current.items() if baseline.get(k) != h]   # added/edited
    removed  = [k for k in baseline if k not in current]                 # deleted fields
    return sorted(set(changed) | set(removed))
```

Properties, all deliberate:

- **Edit → pending.** Any effective change to a committed field (or a new field, or a
  deletion) puts exactly that field in pending. The whole form never re-confirms.
- **Revert → clears.** Changing a field and changing it back yields an empty pending set
  and the *same* profile hash — the input equals what the named human already confirmed,
  so no ceremony is owed. (`intake_rev` still incremented twice; that is why the hash,
  not the counter, is the authority — §6.)
- **Whitespace-only edits don't trigger re-confirmation** (canonicalization equivalence).
  Flagged as open question Q5 — it is the INV-3 wording, but it means reflowing a
  clinical-narrative field is hash-invisible.
- **Deletion requires re-confirmation too.** Removing a confirmed fact changes the input
  of record; the removed field id appears in pending and must be confirmed away by a
  named actor before a new commit exists.

---

## 5. Engine module and endpoints

### 5.1 `engine/ossicro/profile.py` (new; pure stdlib; no I/O — extends the
`TestEngineEgressBoundary` surface)

```python
canonicalize_intake(flat: dict) -> str            # canonical JSON text (§2 step 3, sans prefix)
profile_hash(flat: dict) -> str                   # "sha256:…"
field_value_hash(value) -> str                    # "sha256:…"
pending_fields(flat: dict, committed: dict) -> list[str]
commit_profile(flat: dict, actor: str, prior: dict | None) -> dict
    # returns a new committed_profile dict; raises GateViolation if actor is
    # blank (a nameless commit is software executing a human act — models.py:30-35
    # says that refusal is correct behavior) or if prior exists and
    # pending_fields(flat, prior) is non-empty and not fully staged.
confirm_fields(flat: dict, committed: dict, actor: str, field_ids: list[str]) -> dict
    # stages value-hashes for the named pending fields; raises ValueError on a
    # field_id not currently pending (fail loud, no silent no-op); if staging
    # empties pending, returns commit_profile(flat, actor, prior=committed)
    # (auto-recommit → NEW profile_hash, prior pushed to history with
    # reconfirmed_fields); else returns committed with updated "staged".
require_committed(flat: dict, committed: dict | None) -> str
    # returns the committed profile_hash iff committed is not None and
    # profile_hash(flat) == committed["profile_hash"]; else raises
    # ProfileNotCommitted(pending=…) — a structured exception carrying the
    # pending field ids (or "never committed"), mirroring TriggerDateError's
    # field-carrying pattern (ea_generators.py:114; server.py:715-716).
stamp_input_hash(documents: dict[str, Document], input_hash: str) -> None
    # single post-pass setting rec.input_hash on every ProvenanceRecord and
    # doc.input_hash on every Document (§6) — one stamping site instead of
    # threading a parameter through generate.py:306/321 and
    # ea_generators.py:285/295/309 and every future generator.
```

`ProfileNotCommitted` is its own exception (mapped to HTTP 409), **not** a
`GateViolation` subclass: an uncommitted profile is a user-fixable workflow state, not an
attempted non-delegable act. `commit_profile` with a blank actor *is* `GateViolation`.

### 5.2 Model change (backward compatible — keeps all 128 tests green)

```python
@dataclass
class ProvenanceRecord:
    span: str
    source: str
    citation: str
    input_hash: str = ""     # NEW: sha256 of the canonicalized intake consumed
                             # by the generation that produced this record.
                             # "" = pre-INV-3 record or engine-only test path.

@dataclass
class Document:
    ...existing fields...
    input_hash: str = ""     # NEW: same hash at document grain (package manifest)
```

Defaulted trailing fields mean every existing positional/keyword construction site
(`generate.py`, `ea_generators.py`, `import_existing_documents`, all tests) compiles
unchanged.

### 5.3 API surface (additive; existing contract untouched)

```
POST /api/case/{id}/profile/commit    {actor}
  → 200 {ok, profile: {state:"COMMITTED", profile_hash, committed_by, committed_at}}
  → 400 blank actor / empty intake; 409 pending fields exist (must go through /confirm)

POST /api/case/{id}/profile/confirm   {actor, field_ids:[…]}
  → 200 {ok, profile: {state, profile_hash?, pending:[…]}}   # recommitted iff pending drained
  → 400 blank actor, or a field_id that is not pending

GET /api/case/{id}          → adds "profile": {state, profile_hash, pending, committed_by, committed_at}
GET /api/case/{id}/check    → adds the same "profile" block; "stale" redefined (§6)
POST /api/case/{id}/generate, GET /api/case/{id}/package
  → 409 {"error":"profile not committed", "pending":[field_ids], "state":…} unless
    require_committed passes (fail closed — the deliverable paths never run on an
    unconfirmed input; HC1 / state-machine guarantee 5)
```

Both new POSTs also append to the **existing** `confirmations` trail
(`{actor, field_ids, from_chart, at}`, `server.py:689-697`) with an added
`"action": "commit" | "reconfirm"` key — one attribution trail, not two (B3's durable
named trail is subsumed, not duplicated). Server-side, all mutation happens under the
existing `_LOCK` + `_save_case` discipline.

---

## 6. Subsuming `intake_rev` / `generated_rev` (bridge, don't duplicate)

The counters stay — they are cheap, the frontend contract exposes them, and
`intake_rev_at_commit` gives the commit object a human-legible anchor. But **authority
inverts**: the hash comparison becomes the definition of staleness and the counters
become display/diagnostic metadata.

- `generated_rev` (`server.py:347`) is joined by `generated_hash`: `_generate_payload`
  sets both after `require_committed` passes. `generated_hash` is by construction equal
  to the committed hash at that moment.
- `_is_stale` (`server.py:336-337`) becomes:

  ```python
  def _is_stale(case):
      cp = case.get("committed_profile")
      if case.get("generated_hash"):                     # post-INV-3 generation
          return (cp is None
                  or case["generated_hash"] != cp["profile_hash"]
                  or profile_hash(case["intake"]) != cp["profile_hash"])
      return (case.get("generated_rev") is not None      # legacy fallback, verbatim
              and case["generated_rev"] != case["intake_rev"])
  ```

  This *subsumes* the counter: every case the old rule called stale, the hash rule also
  calls stale (an effective intake change moves the hash), and the hash rule additionally
  un-stales the revert-to-committed-value case and additionally stales the
  never-committed / drifted-from-commit cases. The legacy branch keeps the live UI QA's
  behavior byte-identical for cases that predate the feature.
- `/check` keeps running in every state, because its resolving questions are the repair
  loop. Honesty rule for stamping: `stamp_input_hash` always stamps the hash of the
  intake **actually consumed** (recomputed per request), never the committed hash — so a
  check run in CONFIRMING carries the drifted input's true hash plus
  `profile.state = "CONFIRMING"`, and a provenance record can never claim a committed
  input it did not have. On the `/generate` and `/package` paths the two are equal by the
  `require_committed` gate, so "generation records the committed hash in every
  provenance record" (INV-3) holds exactly where it matters.
- `/check` in UNCOMMITTED/CONFIRMING also injects one app-level ledger-shaped resolving
  question ("Profile not committed — a named clinician must commit it before
  generation"; with the pending field list in CONFIRMING). Injection happens in
  `_check_payload` (`server.py:381-443`), **not** in the engine pipeline — the engine's
  escalate-only layers (`pipeline.py:132-250`) stay untouched, and the question can only
  add, never clear, consistent with that philosophy.

### 6.1 Corollary: sign-offs recorded against a superseded profile

`_apply_signoffs` (`server.py:163-186`) re-applies persisted sign-offs to *freshly
regenerated* documents on every request. Once profiles are hashed, a sign-off recorded
when the profile was `H1` silently attaches to a document regenerated from `H2`. Design:
`_record_signoff` additionally stores `"input_hash": <committed hash at signoff time>`
on the record (empty for legacy records), and `_check_payload` appends an **advisory
note** (escalate-only: a note, not a demotion, and never a promotion) on any green/amber
gated item whose sign-off hash differs from the current committed hash: "sign-off
predates a profile change — confirm it still applies or re-execute the act." Whether a
mismatch should instead *invalidate* the sign-off (amber demotion via a new
`signoff_problems`-style read-time check, `gates.py:26-47`) is open question Q6 — it is
the stricter reading of HC5 but re-imposes ceremony on every recommit.

---

## 7. Migration for existing on-disk cases

Sixteen case files exist under `app/data/cases/`; the oldest have only
`{generated_rev, intake, intake_rev, route_id, signoffs}` (verified:
`125ca025f7ee.json`). Migration is **lazy and additive**, via the mechanism that already
performs exactly this job — `_normalize_case` (`server.py:103-107`):

1. Add `"committed_profile": None` and `"generated_hash": None` to `_new_case`'s
   defaults; `_normalize_case` back-fills every legacy case on load. No offline
   migration script, no file rewrite until the case next mutates (matching how
   `confirmations`/`field_provenance` were introduced).
2. **No auto-commit, ever.** A legacy case with populated intake — even one with a
   `confirmations` trail naming an actor — loads as UNCOMMITTED. Synthesizing a commit
   from historical records would be software performing the named-human act (HC1); the
   first `/generate` after upgrade returns the 409 with the one-click-away instruction,
   and a named human commits. This is a deliberate, visible behavior change for existing
   cases (open question Q1 covers the rollout).
3. Legacy staleness stays byte-identical through the fallback branch in `_is_stale`
   (§6), so an already-open CHECK screen on the live QA server renders the same until a
   commit exists.
4. Legacy sign-off records lack `input_hash`; they load as `""` and are exempt from the
   §6.1 advisory (can't compare what was never recorded — honest absence, not a guess).
5. No schema-version key is needed (`_normalize_case` is idempotent and shape-driven),
   but `canon_version` inside `committed_profile` future-proofs the hash itself.

Deployment note: the server currently running on 8765 (live UI QA) is **not** restarted
for this design; the migration lands whenever that process is next cycled by Alton.

---

## 8. Test plan

All pytest, run as a separate process (never binds 8765). Engine tests are pure; app
tests import `app/server.py` and drive the payload builders / handler helpers
**directly** (`_generate_payload`, `_check_payload`, `_record_signoff`,
`_normalize_case`, `profile` endpoints' core functions) with in-memory case dicts and a
`tmp_path`-patched `CASES_DIR` — no socket, matching how `_record_signoff` is already
structured for direct calls. The existing 128 engine tests must stay green with zero
edits (the dataclass defaults in §5.2 guarantee the constructors; a CI-visible way to
prove it is running the suite once before touching anything).

**New: `engine/tests/test_profile.py`**
1. Canonicalization: key-order independence; whitespace/newline/NFC equivalence →
   same hash; distinct value → distinct hash; empty-after-normalization dropped;
   non-string scalars (`True`, `3`) hash identically to their JSON text; preimage
   version prefix present (hash changes if bumped).
2. `commit_profile` blank/whitespace actor → `GateViolation`; empty intake → refused.
3. `pending_fields`: edit → exactly that field pending; add → pending; delete →
   pending; revert-to-committed → empty; whitespace-only edit → empty.
4. Staging: confirm 1 of 2 pending → still CONFIRMING, staged recorded; edit the staged
   field again → pending again; confirm last pending → auto-recommit, **new hash ≠ old
   hash**, prior pushed to `history` with `reconfirmed_fields`.
5. `confirm_fields` with a non-pending field id → `ValueError` (fail loud).
6. `require_committed`: None → raises with "never committed"; drifted intake → raises
   carrying the pending list; matching → returns the hash.
7. `stamp_input_hash`: after `generate_route_documents` on the sample fixture, **every**
   `ProvenanceRecord` (field spans, literal spans, verbatim spans) and every `Document`
   carries the hash; a default-constructed `ProvenanceRecord` still works (back-compat).
8. Egress boundary: `profile` added to the module list `TestEngineEgressBoundary`
   asserts imports no network client.

**New: app-level tests (e.g. `app/tests/test_commit_profile.py` or wherever the app
suite lands)**
9. **The INV-3 named test** (verbatim from privacy-state-machine.md §4 row INV-3):
   commit → generate OK; mutate one confirmed field → generate refused (409 payload
   names exactly that field) until re-confirmation; after `/profile/confirm` the new
   committed hash differs from the old and generate succeeds, stamping the new hash.
10. Generate/package refused on UNCOMMITTED (fresh case with intake, no commit).
11. Check runs in all three states; stamps the true consumed-input hash; in CONFIRMING
    the injected resolving question lists pending fields; engine ledger statuses are
    otherwise unchanged (escalate-only preserved).
12. Revert case: commit → edit → revert → generate allowed with the ORIGINAL hash, no
    re-confirmation demanded, `intake_rev` ≠ `intake_rev_at_commit` (proves hash
    authority over the counter).
13. Migration: load the literal 6-key legacy JSON shape through `_normalize_case` →
    `committed_profile is None`, `_is_stale` legacy branch matches today's values for
    (rev, generated_rev) combinations; generate → 409 "never committed".
14. Attribution: commit and reconfirm each append a `confirmations` record with
    `action` and named actor; `committed_profile` contains **no intake values** (INV-8
    check: assert no committed field's plaintext value appears anywhere in the
    serialized `committed_profile`).
15. §6.1 corollary: signoff recorded at hash H1, field edited + re-confirmed → H2;
    check payload carries the advisory note on that gated item; the gate itself is not
    cleared or invalidated (pending Q6's answer).
16. FHIR composition: import proposals → apply subset via `/intake` → those fields
    pending → named confirm → commit → generate; import itself still never touches
    intake (existing `test_import_returns_proposals_and_never_mutates_intake` stays
    green).

---

## 9. Explicitly unchanged

The gate system (`gates.py`) — commit is not a sign-off and touches no gate. The
escalate-only pipeline (`pipeline.py`) — no engine layer gains the ability to clear
anything. HC3 clocks — untouched. FHIR import (INV-2) — untouched. The intake POST
contract — untouched. The engine's generators — untouched except the two defaulted
dataclass fields; stamping is one external post-pass.

---

## 10. Open questions for Alton

- **Q1 — Hard gate from day one?** `require_committed` on `/generate`+`/package` breaks
  the current demo flow (sample-fill → generate immediately) and every existing case
  until a named human clicks Commit. Recommended: hard from day one (HC1, guarantee 5),
  with the commit UI shipping in the same change — but this is a visible behavior change
  on a live-QA'd surface and is Alton's call.
- **Q2 — Whole-profile initial commit vs per-field initial confirmation.** This design
  lets one named actor commit the entire profile in one act (per-field ceremony applies
  only to *re*-confirmation). The privacy-state-machine CONFIRMING diagram could be read
  as demanding per-field confirm events even initially. Recommended: whole-profile
  initial commit (the existing chart-apply flow already produces per-field
  `confirmations` records upstream), but confirm the reading.
- **Q3 — Actor identity strength.** Free-text name (matching `_record_signoff`'s
  `signer_name`) for now, with real authentication deferred alongside the SMART launch
  (INV-7 tail)?
- **Q4 — Should `/check` also be refused pre-commit?** Recommended no (it is the repair
  loop and drives users to commit), with the honest true-hash stamping of §6. Refusing
  would be stricter but makes the fix loop blind.
- **Q5 — Whitespace-insensitive change detection.** Per INV-3's own wording, a
  reflow/reformat of a narrative field does not re-enter CONFIRMING. Acceptable, or
  should string values hash verbatim (NFC only)?
- **Q6 — Sign-offs recorded against a superseded profile hash** (§6.1): advisory note
  (recommended, escalate-only, low ceremony) or hard invalidation (amber demotion until
  the human re-affirms)? The strict reading re-imposes gate ceremony on every recommit,
  including trivial ones.
- **Q7 — Commit history retention.** Unbounded `history` in the case JSON (~200 B/commit)
  — fine, or cap?
- **Q8 — `generated_rev` deprecation.** Keep the counter indefinitely as display
  metadata (recommended; the frontend reads it) or schedule removal once the UI reads
  `profile.state` + `generated_hash`?
- **Q9 — Bundle purge-on-commit (INV-8 tail).** The state machine bundles purge into
  `commit_profile`. Today no bundle is retained anywhere (import maps and discards), so
  this is vacuous. Recommended: keep deferred and note it here, rather than building a
  purge for a retention that does not exist.
