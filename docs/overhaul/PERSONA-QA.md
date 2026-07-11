# Persona QA re-check of the overhaul (P1–P9)

**Method:** each persona's MAJOR findings from `docs/review/INVENTORY.md` re-checked against the
post-overhaul working tree — `app/static/index.html` user strings, `app/server.py`,
`engine/ossicro/` (ea_generators, clocks, check, assemble, citations, pdf_3926, profile),
`engine/registry/*.json` — judged **from that persona's point of view**, not the implementer's.
**Suite at re-check: 582 passed** (pre-overhaul baseline 337).
**Date:** 2026-07-11. Quotes are verbatim from the tree.

A recurring pattern below: three items are **code-resolved but carry an honest
`PENDING-HUMAN-VERIFICATION` marker** (M8 citation map, M6 form numbering, P6 consent
language). For every persona that raised them, the *defect they named* (silent wrongness) is
gone; what remains is a scheduled human act that the artifact itself discloses.

---

## 1. Patient

### Consent / voluntariness thread — RESOLVED
Every stage's "what still has to happen" list now carries the choice sentence, and it survives
enrollment (the exact gap the patient review flagged):

- Draft/committed/released (server.py:407–409): *"Before any treatment, you will be asked for
  your written permission (informed consent). Saying yes or no is always your choice."*
- Enrolled (server.py:489–496), consent-status-agnostic per HC1 plus the new m10 line:
  *"If you have not already given your written permission (informed consent), you will be asked
  before treatment starts, and it is still your choice."* and *"Even after treatment starts,
  continuing is your choice. You can stop at any time — tell your doctor first so stopping can
  be planned safely."*
- Emergency-route variants (m9, server.py:416–429 etc.) are honest about the §50.23 reality
  instead of promising consent-first: *"...unless the emergency makes that impossible under the
  rules doctors follow. Saying yes or no is always your choice whenever you are able to make it."*

### No false "draft" at the enrolled stage — RESOLVED, with a recurrence tripwire
- `patient_notice_enrolled` (server.py:394–397) makes no submission claim: *"This page only
  shows status. For anything about your treatment or where things stand, your doctor's office is
  the right place to ask."*
- The payload flag is stage-aware: `"draft": stage != "enrolled"` (server.py:1837, commented
  *"not a draft once enrolled (patient review #4)"*).
- Patient mode hides the standing draft bar (index.html:474–477,
  `body.patient-mode .draftbar{display:none}`).
- **New since the patient review:** the "nothing submitted" sentence is now a registered claim
  (PT-3, `engine/registry/claims.json`) composed once — server.py:384–389 — and a grep test
  fails if the claim text is hardcoded anywhere else. This is the structural fix for how the
  third hardcoded "Still in draft." slipped past three reviewers.

### Still open (patient-adjacent)
The EA consent form the patient would eventually *sign* (P6's `gen_icf_ea`) ships with
*"PENDING-HUMAN-VERIFICATION — consent language not yet reviewed by a qualified human"* in its
draft banner. Correct and honest, but a real patient must not sign it until that review happens.

**Patient verdict: SATISFIED.** The status page is honest at every stage and never drops
voluntariness.

---

## 2. Physician (sponsor-investigator)

### M5 — undatable routine case — RESOLVED
`routes.json:48` now has the field the engine was already consuming:
*"submission.date" — "Preparation / planned submission date" ... "Dates the cover letter, Form
3926, and LOA request. Enter the date you prepare or submit the package; never guessed by
OSSICRO."* It is in the sample fixture (`ea_sample_case.json:47`), so the span→field harvest
makes `[[MISSING: cover_date]]` fix-loop reachable. A non-emergency pre-submission case can now
be dated without inventing an FDA receipt date.

### M7 — permanent drug-accountability red — RESOLVED
`documents.json:480`: `"required_fields": ["drug_name"]` — `lot_numbers` and
`dispensing_entries` removed, per the explicit shell-at-dispensing decision (P2). The ledger row
is green-with-note when the drug name is present; the template still renders the columns as
honestly `[[MISSING]]` at submission time. The physician no longer stares at a red no action can
clear.

### Also closed for this persona
- **M1 (engine remainder):** `clocks.py` now has single-anchor
  `written_3926_deadline(authorization_date=...)` (:146) and
  `irb_emergency_notification_deadline(first_treatment_date=...)` (:161); the combined
  wrong-anchor function is gone, keyword-only args make a swapped anchor a TypeError, and
  `_sponsor_obligations` arms 56.104(c) from first treatment (server.py:1949–1953: *"NOT the
  authorization date"*). Reconciliation tests exist (`test_reconciliation.py`).
- **M4:** non-emergency promote now **refuses (409)** without valid consent/IRB sign-offs unless
  the physician types `acknowledge_unsigned_gates` *"in your own words"* (server.py:630–638);
  advisories persist in the enrollment record and render escalate-only in the check ledger.
- **M10/M11:** the checklist appears as soon as any anchoring fact exists (server.py:1933–1936),
  the 312.310(c)(2) end-of-treatment summary row is always present (server.py:1992–2009), and
  the tracked-subset line is on the checklist (server.py:605).
- **m2:** physician-facing strings say "treatment start", supplying the 56.104(c) trigger at the
  moment it happens.

### Still open (marked, not silent)
**M6** — the 3926 item numbering is unified in one `FORM_3926_ITEMS` table (pdf_3926.py:143)
from which the text template, PDF layout, and FDF map all derive, and every rendered surface now
carries *"[PENDING-HUMAN-VERIFICATION] Item numbering pending verification"* (pdf_3926.py:120).
The internal inconsistency the physician caught is structurally impossible now; the human pass
against the official OMB 0910-0814 form has not happened. The physician can no longer
*unknowingly* transcribe unverified numbering — the artifact says so.

**Physician verdict: SATISFIED** on M5/M7/M1/M4 (fully closed); M6 correctly downgraded from
"silent risk" to "disclosed pending human act."

---

## 3. Manufacturer (Medical Affairs)

### M2 — green LOA without the manufacturer's act — RESOLVED
- Fourth ledger state (check.py:36): `AWAITING_EXTERNAL_PARTY = "awaiting-external-party"`, with
  the registry fact behind it — every document carries `author_party`, LOA = `"manufacturer"`
  (documents.json:100). Docstring: *"Intake completeness alone can never turn such a document
  green."*
- Receipt-fact contract (check.py:45–50): `manufacturer.loa_received_date` + `loa_signatory`
  (+ optional `loa_document_sha256`) turn the row green; the resolving question says *"the
  letter shown here is OSSICRO's draft for their review."*
- `submission_ready` consults the fact (assemble.py:149–156): *"Manufacturer LOA not yet
  received (recorded fact required; the no-IND division-contact branch is the alternative) ...
  the decision to issue it is the manufacturer's alone (FDCA 561A)."*
- Readiness is never a bare boolean: `human_acts_outstanding` enumerates unsigned gates and
  awaiting-external-party docs (assemble.py:178–212).
- Enclosure honesty (ea_generators.py:398): *"Letter of Authorization (enclosed upon receipt
  from the manufacturer)"*. A rushed clinician can no longer print a package asserting a letter
  the manufacturer never saw.

### M15 — triage-incomplete LOA request — RESOLVED
`gen_loa_request` (ea_generators.py:829–922) now renders: `URGENCY:` computed from
`submission.emergency` + `submission.needed_by_date` (*"drug needed by %s
(physician-entered)"*), medical license + state, quantity requested, patient age/sex
(coded-safe), shipping site, IRB status, and a charging/cost-recovery section — *"6. Charging /
cost recovery (...): {{cost_recovery_statement}}"* — the first 21 CFR 312.8 appearance in the
repo, routed through the citations table. Missing values render `[[MISSING]]` as always.

### Also closed
**m6/M15-badge:** the release snapshot and inbox carry `loa_request_sha256` and `emergency`
(server.py:1711–1712), so Medical Affairs can pin the exact artifact they acted on and see
urgency. **m4:** `gen_loa` now uses the reference letterhead structure and the previously dead
`manufacturer.address`. **m5:** template dotted paths normalized.

**Manufacturer verdict: SATISFIED.** Their decision is now a first-class recorded fact, and the
request they receive is answerable without a call-back questionnaire.

---

## 4. FDA reviewer (regulator)

### M8 — systematic off-by-one 312.305(b)(2) pinpoints — RESOLVED in code; human initial pending, disclosed
- The corrected map lives once, in the new single-source table `engine/ossicro/citations.py`
  (:64–88): rationale → **(b)(2)(ii)**, patient description → **(iii)**, dose/route/duration →
  **(iv)**, facility → **(v)**, CMC → **(vi)**, pharm/tox → **(vii)**, monitoring →
  **(viii)** — each row annotated *"M8 remap: was (b)(2)(n)"*, monitoring's row carrying
  *"JUDGMENT CALL for the human verifier"* exactly as the plan required.
- Generators and `routes.json` consume the table by content key; no pinpoint is string-literal'd
  twice; tests pin the corrected values.
- `docs/regulatory/CITATION-INVENTORY.md` renders the table (24 pending markers); documents
  using pending citations carry the footer *"[PENDING-HUMAN-VERIFICATION] Citation pinpoints
  marked pending verification..."* (citations.py:39).

From this persona's POV the finding was "citations are guessed and wrong, presented as
computed." They are now computed from one auditable table, corrected to the reviewer's own map,
and any residual uncertainty is stamped on the artifact itself. The remaining act — a qualified
human initialing the rows against eCFR — is exactly the discipline this reviewer would demand.

### Adjacent: M6
Same status as under Physician: one item-map source, pending marker on the rendered 3926 text
and PDF footer, heading softened to *"draft layout"*. The reviewer never receives an artifact
that overstates its verification status.

**FDA reviewer verdict: SATISFIED with the mechanism; formally open until a human initials the
citation inventory and the 3926 map** (both artifacts say so on their face).

---

## 5. IRB / ethics

### M13 — evidence-free, server-synthesized IRB concurrence — RESOLVED
For `informed-consent` and `irb-approval` (`_SIGNOFF_EVIDENCE_KEYS`, server.py:2027–2029):
- The attestation `statement` *"must be TYPED BY THE SIGNER in their own words"*
  (server.py:2281) — minimum length enforced, placeholder/synthesized text rejected
  (server.py:663–672: *"type what you are attesting in your own words. OSSICRO does not..."*).
  Server synthesis remains only for the non-ethics gates.
- An `evidence` object is persisted with the record — irb-approval:
  `{concurrence_date, concurring_member, irb_reference}`; informed-consent: `{consent_date}` —
  keys always asked, honestly blank allowed (server.py:2330–2333).
- m13b: re-signing **supersedes, never overwrites** — the old record stays with
  `superseded_at`/`superseded_by`; validity checks consider only non-superseded records
  (server.py:1352–1353, 2351–2356). The cover letter's "IRB concurrence evidence" promise now
  has something behind it.

### M14 — unconditional "consent will be obtained before treatment begins" — RESOLVED
The fixed sentence is gone. `gen_irb_request` computes the literal from route emergency +
`consent.timing_attestation` (ea_generators.py:965–1040): non-emergency → future-tense;
emergency + `obtained-before-treatment` → past-tense; emergency + `exception-50.23-documented`
→ the §50.23 exception statement; attestation absent →
`[[MISSING: consent.timing_attestation]]` — *"never a fixed assertion that is false ... under
the 21 CFR 50.23 exception"*. Provenance-stamped; all four states tested. The board is never
told something the physician didn't attest.

### Also closed for this persona
- **M4 (silent enrollment):** now a 409 refusal on the non-emergency route without valid
  consent/IRB sign-offs, overridable only by a typed own-words acknowledgment persisted in the
  enrollment record and audit; emergency route gets persisted escalate-only advisories. The
  most ethics-laden transition is now the loudest.
- **M3 (research-framed ICF):** new `informed-consent-form-part50-ea` opens *"You are being
  asked to receive treatment with an investigational drug ... This is treatment, not a research
  study, but laws that protect research participants also protect you"* (ea_generators.py:1126–
  1128); 50.25(a)(6) is satisfiable via `consent.injury_compensation_statement`
  (routes.json:71); EA disclosures (supply-may-stop, cost/312.8(d), (b)(4)/(b)(5)) present; the
  eight verbatim-locked headings kept hash-verified. **Open, by design:** the qualified-human
  adequacy review — the draft banner says *"consent language not yet reviewed by a qualified
  human"* until it happens. An IRB should treat that review as the release gate; the document
  now says exactly that.
- **B1 (their BLOCKER):** one `ai_review` audit record per live review
  (server.py:1042–1053), disposition capture endpoint, and a never-silent check-screen
  disclosure from the claim registry — *"Reviewed by the offline built-in checker — nothing
  left this machine."* / *"...document text left this machine under the deployment's signed
  BAA."* (claims.json:34,41). "What leaves the machine, when, who consented?" now has a good
  answer.

**IRB/ethics verdict: SATISFIED** on M13/M14/M4/B1 (fully closed); M3 code-complete with the
consent-language human review correctly positioned as a disclosed release gate.

---

## 6. Compliance / legal

### B1 + M12 — egress attribution and Part-11 overclaim — RESOLVED
- Live reviewer double-gated (`OSSICRO_LIVE_CONCEPT_REVIEW` explicit affirmative; stub when
  unset even with `ANTHROPIC_API_KEY` — env-matrix tested); one flat, value-free `ai_review`
  audit record per review that actually left the machine (model, version, doc ids, input hash,
  destination); `ai_review_disposition` records the human's judgment on each finding (HC5's
  second half, previously unimplemented).
- `docs/deployment/AI-REVIEW-PRECONDITIONS.md` states the BAA / zero-retention / named-human
  deployment preconditions.
- The wiki Part-11 clause table now carries BUILT / NOT-YET-BUILT / PARTIAL statuses
  (part-11-and-ai-credibility.md) — the present-tense overclaim is gone.
- [PT-5] the egress boundary is a tested property of the whole app, not just the engine.

### M9 — bind/auth/real-PHI cluster — RESOLVED as a fail-closed wall
- `main()` refuses a non-loopback bind; the override *"OSSICRO_ALLOW_NONLOCAL_BIND=1 AND a
  configured authentication backend"* cannot currently succeed because *"no authentication
  backend"* exists (server.py:693–698, 3143–3158) — INV-7 is now a program-enforced
  precondition, not a deferral.
- `profile.py` hashing is HMAC-keyed under a first-run server secret (m14); patient tokens
  masked in logs, constant-time compare (m17); `_save_case` failures wrapped (m15); PDF/FDF
  export is an audited POST act (m18); identifier lint at release/egress (m20).
- `docs/deployment/DEPLOYMENT-COMPLIANCE.md` covers the covered-entity boundary, store-is-PHI,
  BAA inventory, retention; coded-id help now reads *"Prefer a study-assigned code (e.g.
  EA-001) over initials — in a rare-disease, small-community context initials can themselves
  identify the patient"* (routes.json:4); the UI footer carries *"Single-user local pilot — do
  not expose this server or share case URLs"* (index.html:948).

### M10 + M11 — obligations checklist gaps — RESOLVED
The 312.310(c)(2) end-of-treatment summary row is always present, armed from
`treatment.conclusion_date`, due-date = the conclusion date itself, never date+N
(server.py:1992–2009); the checklist surfaces from the first anchoring fact, independent of
promote (server.py:1933–1936); the tracked-subset disclaimer is live (server.py:605). The
generated treatment plan's promise and the tracker now agree.

### Still open (compliance ledger)
- The three HITL acts (M8 citation initialing, M6 form-3926 pass, P6 consent-language review) —
  all disclosed on the artifacts themselves.
- INV-7 auth backend and the non-synthetic-pilot preconditions remain **unbuilt by design**;
  the difference from before is that the code now refuses rather than trusts a constant.
- Unpackaged MINORs m3, m11, m19, m21 stay on the INVENTORY backlog (m21 is a scoping fact).
- The HC6 justification reword in the Constitution itself still needs Alton's amendment path
  (the banned-constructions metadata reword landed; the Constitution text was correctly left
  alone).

**Compliance verdict: SATISFIED.** The falsifiable-privacy-claim exposure (B1) and the
overclaim pattern (M12) are closed; the remaining opens are correctly framed as disclosed
preconditions, not silent gaps.

---

## Bottom line

| Persona | Named MAJORs | Status from their POV |
|---|---|---|
| Patient | consent/voluntariness; false-draft-at-enrolled | **Resolved** (+ claim-registry tripwire) |
| Physician | M5, M7 (+M1, M4) | **Resolved**; M6 pending human pass, disclosed |
| Manufacturer | M2, M15 | **Resolved** |
| FDA reviewer | M8 (+M6) | **Resolved in code**; human initial pending, stamped on artifacts |
| IRB / ethics | M13, M14 (+M4, M3, B1) | **Resolved**; M3 consent-language human review is a disclosed release gate |
| Compliance | B1, M12, M9, M10, M11 | **Resolved**; INV-7 auth + HITL acts remain as fail-closed/disclosed preconditions |

No MAJOR remains in the state its persona originally objected to: every residual open item is
a **human act the system now discloses and refuses to pretend happened** — which is the
product's own design principle applied to itself.
