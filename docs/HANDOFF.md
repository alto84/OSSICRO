# OSSICRO — Reviewer Handoff

Reader: someone opening this project for the first time to evaluate it. This
page tells you what OSSICRO is, how to run it, what is proven to work, who it
serves, how its governance is enforced, and what is deliberately not finished.

Date of this snapshot: 2026-07-11. Branch: `main`.

## 1. What this is, and the one hard rule

OSSICRO is a governed, drafts-only assistant that helps a physician assemble the
regulatory documentation for single-patient expanded access to an investigational
drug (21 CFR 312.310; FDA Form 3926). The backend is pure Python standard library
(`app/server.py` on `http.server`). The dashboard is one page
(`app/static/index.html`). The rules engine is in `engine/`.

The one hard rule, enforced in code and not just written down: **OSSICRO never
performs a non-delegable act.** It never obtains consent, never approves for an
IRB, never determines causality, never signs, and never submits to FDA. Each of
those is a gate owned by a named human. Everything the software produces is a
draft for that human to review. See Section 6 for where this is enforced.

## 2. Run it, and verify it

No dependencies. Python 3 standard library only.

```bash
cd OSSICRO
python app/server.py            # serves http://127.0.0.1:8765
```

Open `http://127.0.0.1:8765/` in a browser. Start a case, load the sample
intake, commit the profile under a name, generate the documents, read the
completeness ledger, then open the package view. The server binds to loopback
only and refuses any non-loopback host by design (see Section 7).

Two commands prove the system end to end:

```bash
python -m pytest engine/tests app/tests -q     # 582 tests, ~4.5s
python tools/smoke_e2e.py                       # drives all 19 API endpoints (server must be running)
```

`tools/smoke_e2e.py` creates a fresh synthetic case and exercises every persona
path: intake, profile commit, generate, ledger, package, Form-3926 PDF, registry
match, release, manufacturer inbox, patient link and view, audited export,
enrollment promote, coordinator board, and a role-checked IRB gate sign-off. It
exits non-zero if any step fails.

## 3. What works — verified on this snapshot

Every item below was run, not assumed.

- **Tests: 582 passed** (`engine/tests` + `app/tests`, ~4.5s), zero failures.
- **End-to-end flow: 19/19 endpoints pass** via `tools/smoke_e2e.py`. Generation
  produced 8 expanded-access documents; the ledger returned 4 green / 4 amber /
  0 red on the sample; the Form-3926 endpoint returned a real 8.8 KB PDF; the
  registry match returned 5 organized candidates; release, manufacturer inbox,
  patient token view (with a bare 404 on an unknown token), export, promote, and
  the coordinator board all responded correctly.
- **Dashboard click-through: no broken pieces.** An independent frontend review
  read the full 3,826-line page and confirmed every button, view, fetch path,
  and payload shape matches the server contract, with no null-deref, dead
  handler, or leftover debug code on any persona path. Zero blocker, zero major
  findings.
- **Governance is enforced in code, not just documented** (Section 6).
- **Prose discipline holds on the reader-facing surfaces.** The Constitution and
  README sit well under the project's own drift baselines (`tools/prose_lint.py`);
  drift is concentrated in internal planning docs, not the outputs or UI copy.

## 4. Repo map

| Path | What it is |
|---|---|
| `app/server.py` | Backend, 3,184 lines. Serves the SPA and the JSON API. Loopback-only. |
| `app/static/index.html` | The dashboard, one page, 3,826 lines, vanilla JS. |
| `engine/ossicro/*.py` | Rules engine, 25 modules (~8,000 lines): models, rules, validate, routes, pipeline, check, assemble, generate, ea_generators, pdf_3926, clocks, citations, matching, egress, fhir_ingest, profile, audit, review_port, review_claude, registry, gates, compliance, register_linter, cli. |
| `engine/registry/*.json` | 6 registries: documents (64 entries), rules, gates, routes, claims, banned-constructions. |
| `engine/tests`, `app/tests` | 582 tests. |
| `templates/` | 61 regulatory document templates in 17 categories (IND, safety, monitoring, IRB, consent, contracts, expanded-access, and more). |
| `wiki/` | 131-page knowledge base: roles, lifecycle, documents, personas, and the OSSICRO system model. |
| `docs/` | Constitution, submission spec, deployment-compliance, the six-persona QA punch list, and design/plan history. |
| `tools/` | `smoke_e2e.py` (end-to-end check), `prose_lint.py` (drift detector), `attestation_worksheet.py` (HITL citation worksheet). |
| `app/data/cases/` | Runtime case store (gitignored; synthetic only; coded identifiers, no real PHI). |
| `frontend/index.html` | A separate marketing landing page. NOT the running dashboard and NOT served by the app. Keep or remove is your call. |

## 5. Who it serves — party-coverage

Verified against the code, not just the persona docs.

| Party | What they get | Endpoint / view | Status |
|---|---|---|---|
| Treating physician (sponsor-investigator) | 55-field intake, 8 generated EA docs, completeness ledger, clocks, obligations checklist, draft 3926 PDF/FDF | SPA at `/`; case endpoints | Full |
| FDA reviewer | eCTD module map, cover letter, per-doc SHA-256 manifest + package digest, `submission_ready`/`blocking`, `human_acts_outstanding` | `GET /api/case/{id}/package` | Full (consumes the physician's package; no separate reviewer login — INV-7 deferred) |
| Drug manufacturer | Release-time snapshot: LOA-request text, drug/indication, coded id, LOA-request hash, emergency badge | `POST /release`, `GET /api/manufacturer/inbox` | Full (supply/LOA decision correctly not modeled as an OSSICRO act) |
| Patient | Read-only plain-language status page, coded id + drug only, opaque token entry | `POST /patient-link`, `GET /api/patient/{token}` | Full (constant-time token compare; unknown token → bare 404) |
| IRB | Generated concurrence-request document + an `irb-approval` gate to record the board's determination | Doc in route set; gate via `POST /signoff` | Partial — outbound artifact + gate only; no interactive IRB view |
| Coordinating physician | Read-only board: per-case stage, mode, profile state, gate counts, ledger rollup, clocks | `GET /api/cro/board` | Full (read-only by design) |
| Pharma partner | Same surface as the manufacturer inbox | Manufacturer inbox | Full |
| Micro-CRO legal entity (312.52 TORO holder) | — | — | **Gap** — described in the wiki persona but has no functional surface: no TORO generator, no obligation-transfer endpoint, no entity onboarding |

## 6. Governance — enforced in code

An independent audit mapped each constraint to its enforcement point. Summary of
that audit (file:line references verified in the source):

| Constraint | Enforced | Where |
|---|---|---|
| HC1 — non-delegable acts never performed | Yes | `gates.py:105-144`, `models.py:240-246`, `server.py:2163-2167` (no submit/consent/IRB-approval endpoint exists; recording a gate act needs role + named human + statement) |
| HC2 — no fabrication | Yes | `ea_generators.py` (missing data → visible `[[MISSING]]` marker + red ledger item, never an invented value); citations single-sourced via `citations.py` |
| HC3 — computed clocks, honestly unarmed | Yes | `clocks.py` (calendar math on recorded anchors only, never `today()`; keyword-only anchors); absent trigger → `armed:false` + the exact resolving question |
| HC4 — provenance + hash manifest | Yes | `models.py:50-56` (per-span provenance), `assemble.py:85-110` (per-doc SHA-256 + package digest) |
| HC5 — Part-11 AI attribution | Yes | `server.py:1042-1060` (`ai_review` audit record: model, version, doc ids, count, destination — never text), `server.py:1089` (named human's disposition) |
| HC6 — no exculpatory consent language | Yes | `banned-constructions.json` + `register_linter.py` (deterministic hard-fail, scoped to consent docs) |
| HC7 — no drafting-process leakage | Yes | `banned-constructions.json` + `register_linter.py` (chat/AI-self-reference residue hard-fails) |
| INV-3 — commit-profile hard gate (409) | Yes | `profile.py:348-366`; every deliverable path fails closed to 409 unless a named human committed and the intake still matches the committed hash |
| INV-8 — no PHI egress (hashes only) | Yes | `audit.py`, `egress.py` (frozen de-identified predicate struct), `profile.py` (value hashes only), intake rejects unknown keys |
| Egress gateway live-disabled | Yes | `egress.py:92` (`_LIVE_EGRESS_ENABLED=False`); only the mock adapter answers |
| Loopback-only bind guard | Yes | `server.py:3148-3169`; override needs both an env var and an auth backend that does not exist, so it cannot currently succeed |
| Append-only hash-chained audit log | Yes (tamper-evident) | `audit.py:133-164` (append is the only writer; chained hashes; `verify_chain`). Honest caveat: plain-JSON persistence, so a direct file edit is possible but detectable via the chain |
| Concept (AI) layer is escalate-only | Yes | `pipeline.py:132-299` (a clean review can never clear a gate or turn red green; a broken reviewer escalates to red) |

Verdict from the audit: the governance framework is genuinely enforced, well past
"semi-functional." No path lets OSSICRO perform a reserved act.

## 7. Known limitations and backlog — read this before judging scope

This is deliberately honest. None of these lets the software perform a gated act.

**Structural, by design (not defects):**
- **Single-user loopback pilot; no authentication (INV-7 deferred).** The server
  refuses to bind to the network. There is no login. Do not expose it.
- **Synthetic data only.** No real PHI. The case store holds coded identifiers.
  Everything a real deployment must satisfy first is in
  `docs/deployment/DEPLOYMENT-COMPLIANCE.md`.
- **Drafts only.** The gated acts are human acts; the system stops and waits.

**Coverage gaps (documented in the wiki, no functional surface yet):**
- **Micro-CRO legal entity** — no TORO generator or obligation-transfer surface.
- **IRB** — served by an outbound artifact and a gate, not an interactive view.

**Pending human verification (carry visible markers in the code/docs):**
- The regulatory citation set has items marked `PENDING-HUMAN-VERIFICATION`;
  see `docs/regulatory/CITATION-INVENTORY.md` and the attestation worksheet.
- The Form-3926 field numbering and the FDF field-name map are unverified
  against the official OMB form (`ossicro.pdf_3926`).

**Open QA backlog (`qa/PUNCH-LIST.md`, six-persona review, 2026-07-09):**
- 56 findings (18 high, 23 medium, 15 low). A regulatory re-triage on this
  snapshot found that most were already remediated in the overhaul: of the 41
  high/medium findings, about 28 are fixed. Two concrete citation corrections
  remained. One is applied here (see below). The other, the Form FDA 1571 field
  numbers, is flagged for human verification rather than auto-changed, because
  correcting one regulatory number to another without primary-source
  confirmation would risk substituting a second wrong value (the no-fabrication
  rule, HC2).
- **Needs human verification (do not take the current wiki text as correct):**
  the transfer-of-obligations page (`wiki/03-documents/transfer-of-regulatory-
  obligations-toro.md`, and echoes in the legal-thesis and micro-cro pages)
  states the CRO transfer disclosure is "Field 16" of Form FDA 1571. A
  regulatory review indicates it is **Field 14** (with the monitoring and safety
  personnel fields at 15 and 16, not 17 and 18), and that the cited "03/23
  edition" of the form may not exist. Confirm against the current Form 1571 image
  before editing; the fix is then a small find-and-replace.
- The remaining ~11 open findings are structural design judgments (for example,
  therapeutic-misconception framing and pharma-side acceptance economics), not
  small edits.

**Before enabling the opt-in live AI reviewer (one real code fix, currently dormant):**
- The live concept reviewer is OFF by default. When a deployment turns it on
  (`OSSICRO_LIVE_CONCEPT_REVIEW`), `GET /check` and `GET /package` append an
  `ai_review` record to the audit trail from inside `_check_payload` /
  `_package_payload`, which run outside `server.py`'s `_LOCK`. Two concurrent
  requests on one case could then read the same previous hash and write
  duplicate-sequence records, breaking the append-only chain. Fix before
  enabling live review: make the `ai_review` append atomic under a lock (either
  around the append in `_append_ai_review_audit`, or by giving `audit.append`
  its own module lock). This sits alongside the BAA / de-identification
  preconditions that path already requires (`docs/deployment/AI-REVIEW-PRECONDITIONS.md`).

**Robustness backlog (independent backend review: 0 blocker, 1 dormant major, 18 minor, 6 tidy):**
- Fixed on this snapshot: a whitespace-only drug name crashing FHIR import;
  a title-less registry entry aborting the whole ledger; silent duplicate ids in
  the document and gate registries; an absent study fact misreported as a
  `None`-valued mismatch; an unused import; and the site-initiation-visit-report
  citation (`312.53(b)` → `312.56(a)`, matching its sibling entry).
- Deferred (defensive hardening on malformed or opt-in-path input, none of which
  breaks the default flow): FHIR list-shape guards, egress None-adapter ordering,
  a live-review request timeout, and several other edge cases enumerated in the
  review. Worth a hardening pass before any non-synthetic use.

**Frontend polish (independent review: 0 blocker, 0 major):**
- 8 minor and 3 tidy items, all cosmetic or edge-case. Fixed on this snapshot:
  keyboard operability of the "fix in intake" jump links, a clock null-guard, and
  an unused CSS rule. The rest (a stale package-panel message on re-load, a
  dropped identifier-lint advisory in the match view, double-submit guarding) are
  recorded for later.

**Two `index.html` files — a clarification, because it misled two reviewers:**
- The working clinician dashboard is `app/static/index.html`, served at `/`. It is
  the full flow and it works (Section 3). A separate `frontend/index.html` is a
  marketing landing page that the app does not serve; two reviewers opened it,
  did not realize the real dashboard existed, and wrongly concluded there was no
  clinician flow. Recommend removing or clearly labeling `frontend/index.html` so
  the next reader is not misled.

## 8. Where to look first

1. Run the two verification commands in Section 2.
2. Click through the dashboard as the physician: start a case, load the sample,
   commit, generate, read the ledger, open the package, download the 3926 draft.
3. Read `app/README.md` for the full API contract, then
   `docs/OSSICRO-CONSTITUTION.md` for the hard constraints.
4. The governance seams are the heart of the system: the gates (`engine/ossicro/
   gates.py`), the commit-profile hard gate (`engine/ossicro/profile.py`), and the
   egress boundary (`engine/ossicro/egress.py`).
5. `qa/PUNCH-LIST.md` is the honest backlog.
