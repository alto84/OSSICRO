# Wave 1 Audit-Log + Persistence Hardening — Standalone Adversarial Review

**Reviewer:** standalone adversarial agent (not the builder) · **Date:** 2026-07-10
**Scope:** `engine/ossicro/audit.py`, `app/server.py` (audit wiring + case store),
`engine/tests/test_audit.py`, `app/tests/test_wave1_hardening.py`, BUILD-PLAN Wave 1.
**Test run:** `python -m pytest engine/tests/ app/tests/ -q` → **233 passed in 1.52s**.

## VERDICT: FIRE-after-patching — patch MAJOR-1 (and preferably MINOR-2/3) before commit; everything else is small.

---

## Answers to the six pressed questions

1. **Append-only?** Yes, at the API surface. `audit.append` is the sole write op; it never
   reads back into or reorders prior entries; stored details are deep-copied
   (`audit.py:113`); `read`/`append` return frozen dataclass views (mappingproxy, tuples).
   Verified by test *and* by inspection: no other writer touches `case["audit"]`
   (the only call sites are `server.py:661, 714, 750, 818`, all `audit_mod.append`).
   Caveats: enforcement is convention + module surface — any in-process code or a direct
   file edit can still rewrite history (no hash chain, MINOR-7), and a corrupt *entry*
   inside a valid list slips past the loader guard (MINOR-2).
2. **Value leak?** None found. I ran the real sample flow (intake → commit → drift →
   reconfirm → signoff → FHIR sample import → generate → save) with a distinctive actor
   name, then grepped the produced audit trail *and* privacy_log for every sample-intake
   value and every string in the sample FHIR bundle. Zero chart values. (All apparent hits
   were substring false positives: `'initial'` inside the field id
   `submission.initial_or_followup`, `'phone'/'email'` inside `contacts.phone/email` ids,
   `'proposal'` inside the `proposals` count key.) BUT the guard is shape-based, not
   content-based, and intake **keys** are client-controlled free text — see MAJOR-1.
3. **Every act logged exactly once?** Yes for the Wave-1 scope (commit / reconfirm /
   signoff / bundle_loaded): each handler appends exactly one record on success with the
   correct actor and input_hash (commit → new committed hash; reconfirm → the commit
   object's current hash, new hash on auto-recommit; signoff → committed hash in force,
   `""` pre-commit; import → `sha256:<bundle>` with honestly-blank actor), and every
   failure path (400/409) appends nothing — all under `_LOCK`. Auto-recommit inside
   `/profile/confirm` intentionally emits one `reconfirm` (not a second `commit`) carrying
   the NEW hash + actor; attribution holds. Named **intake** confirmations (HC5) land only
   in the mutable `confirmations[]` list, not the audit trail — in-scope-consistent with
   the plan's list but see MINOR-6.
4. **Corruption tolerance?** Good. `_load_cases` skips unparseable JSON, non-dict JSON,
   and non-list audit trails with a stderr warning; good cases still load; corrupt files
   are preserved on disk (forensics), never deleted or coerced to `[]`. All tested.
   Gap: a corrupt entry *inside* a valid audit list is accepted and later crashes
   GET /audit (MINOR-2).
5. **m6 regression?** No. The intake response is strictly additive
   (`{ok, intake_rev}` + `stale` + `profile`); the frontend consumes `res.profile` with a
   `refreshProfile()` fallback (`index.html:1408-1409`), so old-client/new-server and
   new-client/old-server both work. Two nits: the response's `stale`/`profile` are
   computed after `_LOCK` is released (MINOR-4) and the server docstring still documents
   the old shape (MINOR-5).
6. **Test quality?** Strong for the claims made. Mutation analysis: deleting the
   `_normalize_case` audit-list guard fails `test_normalize_rejects_unrecoverable_shapes`;
   making `append` mutate priors fails `test_append_never_alters_existing_records`;
   removing the deep-copy fails `test_callers_later_mutation...`; dropping ANY of the four
   audit writes fails its exactly-one test; deleting the 409 mapping fails the socketless
   HTTP tests (nice: they drive the real `Handler` without binding 8765). Gaps: no test
   for corrupt-entry trails, none for PHI-shaped intake keys, none for the `_save_case`
   failure path at the HTTP layer.

---

## Findings

### MAJOR-1 — Unvalidated client-supplied intake keys flow into the *unremovable* audit trail (INV-8 hole)
- **Where:** `app/server.py:964-969` (POST /intake stores any non-empty key, never checked
  against `SCHEMA_FIELDS`) → `app/server.py:717` (commit audit `detail.field_ids` =
  every intake key, via `committed_profile.field_hashes`). Same vector reaches
  `reconfirm` field_ids (validated only against the pending set, i.e. the same
  arbitrary keys).
- **Repro (verified):**
  ```python
  case["intake"]["Patient John Q. Smith DOB 1980-01-01 dx pancreatic ca"] = "yes"
  server._profile_commit(case, {"actor": "Dr. Probe"})   # 200
  # "John Q. Smith" is now in case["audit"] — and append-only means no API can remove it
  ```
- **Why it matters:** the INV-8 guard (`audit._check_detail`) checks value *shape*, not
  key *content*. A direct API caller, a future persona client, or a client bug that swaps
  key/value bakes PHI-shaped text permanently into the one structure designed never to be
  mutated or deleted. The append-only property turns a transient leak into a durable one.
  Contained today (synthetic-only, the shipped frontend sends only schema ids) — hence
  MAJOR, not BLOCKER.
- **Fix:** reject unknown field ids at the POST /intake ingress
  (`if key not in SCHEMA_FIELDS: 400`), which is the single chokepoint; or, defensively,
  filter/replace non-schema ids at the audit call sites (`field_ids = sorted(k for k in
  ... if k in SCHEMA_FIELDS)` + an `unrecognized: N` count). Add a regression test.

### MINOR-2 — Corrupt audit *entry* passes the loader guard; GET /audit then dies with no HTTP response
- **Where:** `app/server.py:147` (`_normalize_case` checks only `isinstance(case["audit"], list)`),
  `app/server.py:913` (`dict(r)` on a non-dict entry raises), and the `_CASE_AUDIT` GET
  branch has no try/except (unlike /check and /package) — the exception propagates out of
  `do_GET`, the connection resets, the client gets nothing.
- **Repro (verified):** a case file with `"audit": [{...ok...}, "GARBAGE-ENTRY"]` loads
  fine; `GET /api/case/{id}/audit` → `ValueError: dictionary update sequence...`,
  unhandled. (`audit.append` itself survives — `last_seq` falls back to `len(trail)`.)
- **Fix:** in `_normalize_case`, require every trail entry to be a dict (raise ValueError
  → file skipped with the existing warning, forensics preserved); and/or wrap the audit
  GET branch in the same `except Exception → 500 JSON` used by /check.

### MINOR-3 — `_save_case` failures are unhandled on the commit / confirm / signoff / intake branches
- **Where:** `app/server.py:990, 1046-1047, 1064-1065, 1079-1080` (no try/except; contrast
  /generate at 1003-1016).
- **Failure mode:** disk-full or permission error after a successful commit mutates the
  in-memory case (including its new audit record) but raises out of `do_POST` — no HTTP
  response, and a later restart silently drops the record (memory/disk divergence). The
  atomic-write itself is correct (tmp + fsync + replace, tested); it's the *caller* that
  neither reports nor logs the failure.
- **Fix:** wrap those branches like /generate (`except Exception → 500 {error}`), ideally
  noting the divergence honestly in the response.

### MINOR-4 — m6 computes `stale`/`profile` outside `_LOCK`
- **Where:** `app/server.py:993-995` — evaluated after the `with _LOCK:` block closes.
  Under `ThreadingHTTPServer`, a concurrent write can make the returned profile block
  reflect a different state than the write just performed. Move both computations inside
  the lock (they're cheap).

### MINOR-5 — Stale contract docstring
- **Where:** `app/server.py:14` still documents `POST .../intake -> {ok, intake_rev}`;
  the response now also carries `stale` and `profile`. Update the docstring.

### MINOR-6 — Attributable intake confirmations (HC5) live outside the append-only surface
- **Where:** `app/server.py:979-987` (named intake confirmation → `confirmations[]`),
  `app/server.py:805-814` (`privacy_log`). Both are plain mutable lists with none of
  I-AUDIT's guarantees. Wave-1's scope line ("every commit / signoff / import / release /
  egress") makes this consistent, not a violation — but the dual-trail split means the
  "who confirmed which fields" record is mutable while the commit record is not. Consider
  mirroring named intake confirmations into the audit trail (field ids only) in Wave 2,
  when egress starts writing there anyway.

### MINOR-7 — Append-only is API-surface-only: no tamper evidence
- **Where:** `engine/ossicro/audit.py` (design), `app/server.py:157-178` (the whole case
  JSON, trail included, is rewritten wholesale on every save). A direct file edit or any
  future in-process bug rewrites history invisibly. Not a Wave-1 claim violation, but the
  wiki's Part-11 ambitions will eventually want a per-record hash chain
  (`prev_record_hash`) — cheap to add now, expensive to retrofit after real trails exist.

### Positive findings (verified, not just read)
- Frozen views, deep-copy detachment, strictly-increasing seq, JSON round-trip, and the
  no-mutator API surface all hold under test and probe.
- The PHI probe over the real sample flow (including the persisted on-disk form) is clean.
- Failure paths (blank actor, empty intake, pending-field commit, wrong-role signoff,
  bad bundle) all append nothing — tested.
- Corrupt files are skipped loudly, preserved for forensics, and never coerced; startup
  never crashes on them — tested.
- The socketless in-process Handler tests are a genuinely good pattern: the 409 contract
  and the /audit endpoint are exercised through the real routing without touching the
  live 8765 server.

## Reply from the team

Revision by the orchestrator. Suite 233 → **239** (+6). Verdict accepted; patches landed:

**MAJOR-1 (unvalidated intake keys → unremovable trail) — CONCEDED, fixed.** POST /intake now
rejects any key not in `SCHEMA_FIELDS` with a 400 at the ingress chokepoint (verified all 55
legitimate fields, incl. the derived `coded_id`/`plan_id`/`plan_version`, are in the schema, so
the confirm-apply flow is unaffected). Test `test_unknown_intake_key_rejected_and_never_audited`
proves a PHI-shaped key is rejected and never reaches intake or the audit trail.

**MINOR-2 (corrupt entry crashes /audit) — CONCEDED, fixed.** `_normalize_case` now rejects a
trail with any non-dict entry (file skipped-with-warning on load, preserved for forensics — never
serves a corrupt trail), and the `/audit` GET branch is wrapped in the same try/except → 500 the
other read paths use.

**MINOR-7 (append-only was convention-only) — CONCEDED, upgraded to a tamper-evident hash chain.**
Each record now carries `prev_hash` + `rec_hash` (sha256 over its content bound to the predecessor);
`audit.verify_chain()` returns the seqs of any altered/reordered/deleted records, and GET /audit
reports `chain_ok`. Tests prove an edited or dropped record is detected. This is the Part-11
substrate the reviewer flagged as cheap-now/expensive-later — done now.

**MINOR-4 (state computed outside lock) — CONCEDED, fixed.** The intake response's `stale`/`profile`
are now computed inside `_LOCK`.

**MINOR-5 (stale docstring) — CONCEDED, fixed.** The intake/GET-case contract lines updated.

**MINOR-3 (unhandled `_save_case` failure on commit/confirm/signoff/intake) — ACKNOWLEDGED, deferred.**
The atomic write itself is correct (tmp+fsync+replace, tested); the gap is a disk-full/permission
edge that leaves memory ahead of disk with no HTTP response. Real but low-severity on a
single-user synthetic prototype; folded into the next persistence pass alongside a uniform
handler-level `except → 500 {error}` wrapper. **MINOR-6** (named intake confirmations live in the
mutable `confirmations[]`, not the append-only trail) — deferred to Wave 2 as the reviewer
suggested, when egress starts writing to the trail anyway; the named-confirmation record will be
mirrored there (field ids only).
