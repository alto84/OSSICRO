# Persona review — Pharma Medical Affairs (manufacturer receiving a single-patient EA request)

Reviewer stance: I sit at the manufacturer's Medical Affairs / expanded-access intake. A physician
has asked us to (1) supply an investigational drug for one patient and (2) issue a Letter of
Authorization so FDA can cross-reference our IND/DMF (21 CFR 312.23(b), 312.305(b)(1); FDCA §561A).
I decide whether the request as OSSICRO presents it is complete and actionable, whether my
company's decision and signature stay unambiguously ours, and where the system leaves me exposed.

Reviewed: `engine/ossicro/ea_generators.py` (gen_loa_request, gen_loa), `engine/ossicro/assemble.py`
(_manufacturer_packet, submission_ready/blocking), `engine/ossicro/check.py` (ledger), `app/server.py`
(_release, _manufacturer_inbox, STRINGS), `app/static/index.html` (release card, pharma persona view,
STRINGS.pharma/release), `engine/registry/{routes,documents,gates}.json`,
`docs/route-3926-submission-spec.md` (§0, §4, §8.4, §9), `docs/OSSICRO-CONSTITUTION.md` (HC1),
`templates/expanded-access/manufacturer-letter-of-authorization.md`, `wiki/06-personas/pharma.md`,
wave-3 review memo, live `GET /api/manufacturer/inbox`. Test suite run read-only: **336 passed**.

---

## 1. INVENTORY — what OSSICRO offers the manufacturer today

**Documents drafted for/about me:**
- **LOA request** (`manufacturer-loa-request`, `gen_loa_request`, ea_generators.py:724-786): a
  physician→manufacturer letter asking for supply + an LOA, with coded patient id, diagnosis,
  drug, dose/route/duration summary, physician contact block, and an explicit statement that FDA
  authorization does NOT obligate supply and that the supply decision, LOA signature, and any
  FMV/anti-kickback judgment are the manufacturer's alone. Marked `[DRAFT]`, with "OSSICRO never
  auto-sends (Constitution HC1)" in the header.
- **Draft LOA** (`manufacturer-letter-of-authorization`, `gen_loa`, ea_generators.py:662-717): a
  courtesy draft of *my* letter, headed "Draft for the manufacturer's review — issued on
  {{manufacturer_name}} letterhead and signed by an official authorized to bind the company" and
  footed "[EXTERNAL-PARTY ACT — the manufacturer signs this LOA. OSSICRO records the returned LOA
  as a fact; it never signs or supplies (FDCA 561A).]"
- **Manufacturer packet** (`assemble._manufacturer_packet`): the LOA request + a one-paragraph
  transmittal cover note including "Supply commitment on file: YES / not yet recorded."

**Flows:**
- **Release** (`POST /api/case/{id}/release`, server.py:974-1035): cross-persona visibility is a
  SEND — a *named clinician* must explicitly release; requires a committed profile AND documents
  generated from exactly that committed hash; snapshot taken at release time (immune to later
  intake edits); one immutable audit record per release; re-release refused until re-commit.
- **Manufacturer inbox** (`GET /api/manufacturer/inbox`, server.py:1038-1073; UI "Manufacturer
  view"): released cases only; each item = opaque `release_id` (never the case_id capability),
  releasing clinician + timestamp, `released_hash`, coded patient id, drug, indication, physician,
  LOA-request text, `draft: true`. The UI renders **no approve/deny/reply control anywhere**
  (STRINGS.pharma.decisionNote) and says so out loud.

**Guarantees relevant to me:**
- HC1 (Constitution) + spec §0 four-party table: manufacturer supply + LOA signature are named as
  external-party acts OSSICRO "never performs... and only records their outcomes."
- The release view is minimized (wave-3 review verified: age/sex/prior-therapies absent from the
  snapshot; the schema itself is coded-only, so direct identifiers cannot exist to leak).
- Live registry egress disabled; the whole app is a localhost draft workspace; everything I see is
  stamped DRAFT and "synthetic-only pilot."

## 2. ASSESSMENT — through the manufacturer's eyes

**What genuinely serves me:** The decision-ownership line is the best-drilled message in the whole
system — the LOA request itself (item 5), the inbox note, the release card, the persona view, the
spec, and the Constitution all say the supply decision and LOA signature are mine alone, and the
pharma view deliberately renders no decision affordance. The release act being a named-human SEND
with an audited, hash-bound, snapshot semantics is exactly what my legal team would want to see:
I can tell *who* sent me *what*, *when*, generated from *which* committed input. The expectation-
setting sentence "FDA authorization does NOT obligate supply" (mirroring 561A's no-guarantee
posture) protects me from the most common escalation pattern in EA requests. No hard-line
violation found: nothing is auto-decided, auto-sent, or auto-signed anywhere in the manufacturer
path, and no PHI beyond the coded id + diagnosis reaches my view.

**Where it is weak for me:**
- **Triage-critical facts are missing from the request.** The LOA request carries no
  emergency/urgency flag (the cover letter computes one; my letter doesn't), no needed-by date, no
  drug quantity, no patient age/sex/weight (weight-based dosing makes "240 mg BID × duration"
  uncomputable for supply), no treating site/shipping destination, no physician license/credential
  detail (I must verify the prescriber), no IRB status, and no statement about charging vs. free
  supply (21 CFR 312.8 is uncited anywhere in the repo). My MA intake would open this letter and
  immediately send back a questionnaire.
- **The system can call the package "submission ready" on a LOA I never granted.** The drafted LOA
  goes GREEN in the ledger from physician-entered intake alone (gate: null), and `submission_ready`
  ignores `manufacturer.supply_committed`. That misstates *my* act as complete.
- **My decision has no first-class record.** `manufacturer.supply_committed` is a physician-set
  boolean; the spec (§4.1) promises an "LOA-acceptance record" that does not exist in the engine.
- **The request the manufacturer receives can be undated** — the as_of anchor derivation has no
  valid trigger at the pre-submission moment when the LOA request is actually sent.
- **Misleading claims/citations:** "No patient identifiers appear in this view" (a coded patient id
  is displayed); FMV/anti-kickback attributed to FDCA 561A (the corpus's own wiki correctly cites
  42 U.S.C. 1320a-7b + the 42 CFR 1001.952 safe harbor).

## 3. FINDINGS

1. **[SMALL-FIX]** Misleading persona-view claim: the inbox displays the coded patient id, so "No
   patient identifiers appear" is overbroad and would fail a privacy-review read at my company.
   `app/static/index.html:1013` — current:
   `"Synthetic cases only through the pilot. No patient identifiers appear in this view.",`
   replace with:
   `"Synthetic cases only through the pilot. No direct patient identifiers appear in this view — the patient is shown by coded ID only.",`

2. **[SMALL-FIX]** Wrong authority for the FMV/anti-kickback proposition: FDCA §561A (21 U.S.C.
   360bbb-0a) governs published EA policies and the no-guarantee-of-access posture; the FMV/AKS
   judgment rests on the Anti-Kickback Statute, which the wiki itself cites correctly
   (`wiki/06-personas/pharma.md` "Money: FMV, AKS, Sunshine": 42 USC 1320a-7b, 42 CFR 1001.952(d)).
   `engine/ossicro/ea_generators.py:753-755` — current:
   ```
   5. FDA authorization of expanded access does NOT obligate supply. The supply
      decision, the LOA signature, and any fair-market-value / anti-kickback
      judgment are the manufacturer's alone (FDCA 561A).
   ```
   replace with:
   ```
   5. FDA authorization of expanded access does NOT obligate supply. The supply
      decision, the LOA signature, and any fair-market-value / anti-kickback
      judgment (42 U.S.C. 1320a-7b) are the manufacturer's alone (FDCA 561A).
   ```
   (No test pins this template text; the package digest is computed dynamically.)

3. **[SMALL-FIX]** Same citation defect in the governing spec.
   `docs/route-3926-submission-spec.md:157` — current:
   `5. A statement that FDA authorization of expanded access does **not** obligate supply, and that the decision, LOA signature, and any FMV/anti-kickback judgment are the manufacturer's (FDCA §561A) — set expectations honestly (CP4).`
   replace with:
   `5. A statement that FDA authorization of expanded access does **not** obligate supply, and that the decision, LOA signature, and any FMV/anti-kickback judgment (42 U.S.C. §1320a-7b) are the manufacturer's (FDCA §561A) — set expectations honestly (CP4).`

4. **[SMALL-FIX]** Intake help text promises a default that cannot happen: the 30-day-clock
   fallback in `compute_clocks` resolves `submission.date`, which is **not** a schema field, and
   `POST /api/case/{id}/intake` rejects any non-schema key (server.py:1857-1862) — so "Defaults to
   the submission date" is false in the app; the clock simply stays unarmed.
   `engine/registry/routes.json:46` — current help string:
   `"Arms the 30-calendar-day IND-effective clock. Defaults to the submission date if left blank."`
   replace with:
   `"Arms the 30-calendar-day IND-effective clock. If left blank, the clock stays unarmed until this date is entered."`

5. **[LARGER-ISSUE] [MAJOR] The drafted LOA — my company's own letter — turns GREEN and counts
   toward `submission_ready` with no record that the manufacturer ever granted it.**
   `manufacturer-letter-of-authorization` has `"gate": null` (documents.json:649) and its three
   required fields (`manufacturer_name`, `drug_master_file_reference`, `authorized_party`) are all
   filled from *physician* intake, so `check.build_ledger` marks it green ("present; 3/3 required
   fields filled; validated") the moment the physician types my IND number. `assemble` blocks only
   on red FDA docs plus the LOA-*reference*-or-division-contact rule (assemble.py:129-144) and
   never consults `manufacturer.supply_committed` — despite spec §8.4 saying that field feeds
   "Package readiness." Meanwhile the cover letter's enclosure list (ea_generators.py:370-371)
   asserts "manufacturer Letter of Authorization" is enclosed. Net effect: a physician can see
   "submission ready," a green LOA row, and an enclosure list naming my letter when what actually
   exists is OSSICRO's own unsigned draft of it. This is not an HC1 violation (nothing is signed or
   sent by the system) but it misrepresents an external-party act as complete, and it is precisely
   the pattern that makes manufacturers distrust intermediary tooling — a package filed with a
   self-drafted "LOA" would implicate my company's right-of-reference without my consent.
   *Direction:* give external-party documents (owner = sponsor, gate = null) a third ledger state —
   amber "awaiting external party" — keyed to a recorded fact (see finding 6), and make
   `submission_ready` require the LOA-received fact (or the no-IND division-contact branch); reword
   the enclosure line to "manufacturer Letter of Authorization (upon receipt)".

6. **[LARGER-ISSUE] [MAJOR] No first-class record of the manufacturer's decision.** The only trace
   of my act in the whole data model is `manufacturer.supply_committed`, a boolean the *physician*
   sets in intake, surfaced in the transmittal cover as "Supply commitment on file: YES" with no
   who/when/what. Spec §4.1 explicitly promises "OSSICRO drafts the *request* to the manufacturer
   and the **LOA-acceptance record**" — no such record exists in the engine or registry. For my
   liability posture the difference matters: a returned LOA is a dated, signed instrument naming
   the referenced application and the authorized party; "true" in a physician's form is none of
   that. *Direction:* add intake fields for the returned LOA as recorded facts (e.g.
   `manufacturer.loa_received_date`, `manufacturer.loa_signatory`, optionally a document-hash of
   the returned letter), physician-entered on receipt, audit-logged like any intake write — the
   decision itself stays external and unmodeled, exactly as HC1 requires.

7. **[LARGER-ISSUE] [MAJOR] The LOA request is not triage-complete for a real Medical Affairs
   intake.** Missing from `gen_loa_request` (ea_generators.py:724-786) and from the release-view
   snapshot: (a) the **emergency flag / needed-by date** — `submission.emergency` is computed into
   the cover letter and Form 3926 but never into the manufacturer letter or inbox item, and EA
   intakes triage emergencies first (561A(b) even requires published anticipated response times);
   (b) **quantity of drug** — dose/route/duration without patient weight or cycle count leaves
   supply quantity uncomputable; (c) **patient age/sex** (already coded-safe, already in the 3926);
   (d) **physician license number/state** — I must verify the prescriber before shipping;
   (e) **site/shipping destination** (`site.name` exists in intake, unused here); (f) **IRB
   status**; (g) whether supply is requested **free of charge or under 21 CFR 312.8 cost
   recovery** — §312.8 appears nowhere in the repo, yet charging is a decision my company must
   make and FDA must authorize. *Direction:* extend the template with an emergency literal (reuse
   the cover-letter computation), optional quantity/weight/site/license lines, and a one-line
   charging statement; add the emergency flag to the release-view snapshot and inbox item so the
   manufacturer view can badge urgent requests.

8. **[LARGER-ISSUE] [MAJOR] The request the manufacturer receives is undated at exactly the moment
   it is sent.** `derive_as_of` (ea_generators.py:156-175) anchors on `submission.date` (not a
   schema field — unreachable via the app), else emergency-auth date, first-treatment date, or FDA
   receipt date. A *non-emergency, pre-submission* case — the normal state when the physician
   sends me the LOA request, since the LOA must exist before filing — has none of these, so
   `{{request_date}}` renders as `[[MISSING: request_date]]` in the letter I receive; the only way
   to date it is to enter an FDA receipt date that has not happened (a falsehood the sample case's
   pre-filled `submission.fda_receipt_date: 2026-06-15` conveniently masks). *Direction:* add a
   physician-entered preparation/request date to the schema (still never wall-clock, preserving
   the HC3/no-fabricated-today discipline) and put it first in `_AS_OF_FIELDS`; or drop the dead
   `submission.date` entries (ea_generators.py:157, 212) and document the honest gap.

9. **[LARGER-ISSUE] [MINOR] The engine's LOA draft is thinner than the corpus's own reference
   template, and drops a field intake collects for it.** `gen_loa`'s inline template omits:
   manufacturer address — although `manufacturer.address` is collected with help text "For the LOA
   letterhead block" (routes.json:32) and is filled in the sample case, it is consumed by no
   generator (dead field); sections expressly excluded; effective date / expiration-or-revocation
   terms; signatory name/title block; dosage form/strength. All of these are present in
   `templates/expanded-access/manufacturer-letter-of-authorization.md` (lines 36-76), which the
   engine does not use. Low harm — it is explicitly a draft for my review and my legal group would
   restyle it — but the divergence means the better letter exists in the repo and the worse one
   ships. *Direction:* fold the reference template's letterhead/signatory/terms structure into
   `gen_loa` (values honestly MISSING where the manufacturer alone can supply them), or mark the
   md template as the aspirational form in a comment.

10. **[LARGER-ISSUE] [MINOR] Template-corpus dotted paths diverge from the engine schema.** The md
    templates map `{{manufacturer_name}}` → `drug.manufacturer` and `{{manufacturer_address}}` →
    `drug.manufacturer_address` (manufacturer-letter-of-authorization.md:71-72; form-fda-3926 md:103),
    plus `physician.name`, `loa.*`, `fda.review_division` — none of which exist in the engine's
    intake schema (`manufacturer.name`, `manufacturer.address`, `investigator.name`,
    `submission.fda_division`). Anyone wiring the richer templates into the engine will silently
    resolve every field to None. *Direction:* one normalization pass over `templates/*/**.md`
    field tables to the routes.json dotted-path vocabulary, or an explicit legacy-paths note.

11. **[LARGER-ISSUE] [MINOR] The manufacturer inbox is unauthenticated (INV-7 deferred) and the
    manufacturer cannot independently verify what they received.** Anyone who can reach the server
    sees every released snapshot (coded id, diagnosis, physician contact, full LOA-request text);
    acceptable for the synthetic localhost pilot and documented as deferred, but persona auth must
    land before any pilot in which a real manufacturer contact uses this view. Relatedly, the
    inbox exposes `released_hash` (the committed-profile hash — values never stored, so nothing I
    can recompute) but no hash of the LOA-request text itself, while the standalone verifier
    (`/static/verify.html`) works only on the physician's exported package JSON. *Direction:* add
    `loa_request_sha256` to the release snapshot/inbox item so the manufacturer can pin the exact
    artifact they acted on, and keep INV-7 (persona auth) on the pre-pilot critical path.

**Hard-line check:** No violation found. Drafts-only holds (every manufacturer-facing artifact is
DRAFT-stamped and signature blocks are explicit non-delegable/external-party notices); no-PHI-egress
holds (coded-only schema, snapshot minimization verified, live egress disabled); nothing-auto-decided
holds (release is a named-human act, the pharma view has no decision affordance, and no endpoint
models supply, authorization, or signature as an OSSICRO action). Finding 5 is the closest approach
to the line — a green ledger row *describing* my unperformed act — and is reported as MAJOR, not
BLOCKER, because the system never performs or claims to have performed the act itself.
