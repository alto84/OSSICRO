# Persona review — the Enrolling Physician (sponsor-investigator)

Reviewer stance: a busy treating clinician with a dying patient, no regulatory-affairs
department, using OSSICRO end-to-end to assemble a single-patient expanded-access
(Form FDA 3926 / 21 CFR 312.310) package and carry the sponsor-investigator duties.
Method: static review of `engine/ossicro/*`, `app/server.py`, `app/static/index.html`,
`engine/registry/*.json`, docs and wiki; verification by running the test suite
(336 passed) and simulating the UI-driven sample case through the engine.
Date: 2026-07-11.

---

## 1. INVENTORY — what the system offers this persona today

**Workflow (5-step wizard, physician workspace):**

1. **Start a case** — in-memory + disk-persisted draft case (`app/data/cases/{id}.json`),
   coded identifiers only, resumable via URL hash; standing draft banner on every screen.
2. **Intake** — 55 fields in 7 sections (patient-coded, physician, drug/plan, manufacturer,
   IRB, submission control, consent), every field labeled with its governing citation and
   help text; tri-state attestations (Unattested/Yes/No) that are never defaulted; blanks
   recorded as unanswered, never guessed; a "Load example case" synthetic patient;
   localStorage mirror + server persistence; required-field counters per section.
3. **Chart import (SMART on FHIR, optional)** — drop/paste a FHIR R4 bundle; server maps it
   to PROPOSALS ONLY (17 auto, 3 derived, 35 manual by design); per-proposal provenance
   (resource + FHIRPath + coding) and confidence badge; field-by-field confirmation under a
   named confirming clinician — deliberately no accept-all; identifiers (name/MRN/address/
   DOB) structurally never extracted, free text taint-guarded; unconfirmed proposals
   discarded; single-subject bundles only.
4. **Commit → generate → ledger** — a named clinician commits the profile (hash-only
   input-of-record, INV-3); generate/package/match/PDF all 409 fail-closed unless
   committed; any later edit re-opens per-field named re-confirmation; 8 documents
   generated (cover letter, Form 3926 text render, treatment plan, LOA draft, LOA request,
   IRB concurrence request, Part-50 ICF, drug-accountability shell), each span
   provenance-stamped with citation and the consumed-input hash; `[[MISSING: field]]`
   markers instead of invented values; completeness ledger (green/amber/red) with exact
   resolving questions and "Fix in intake →" deep links; cross-document consistency
   findings; statutory clocks computed from physician-entered trigger dates only (unarmed
   with a resolving question otherwise); escalate-only voice/concept review (advisory,
   never clears a gate); "Who must act" gate table; sign-off recorder (records that the
   named human performed the act outside OSSICRO — role must match the gate).
5. **Package** — FDA-reviewer view (eCTD module map with honest "not mandatory for a 3926"
   caveat, draft cover letter, SHA-256 manifest with explicit ABSENT rows, package digest);
   manufacturer view (LOA request + transmittal cover); DRAFT-watermarked filled Form 3926
   PDF + FDF field map (map explicitly flagged UNVERIFIED); export JSON; standalone offline
   verifier (`verify.html`); printable view with DRAFT stamp; stale-draft guard freezing
   assembly/export when intake drifts from the generated revision.

**Post-drafting acts (all named-human, all audited):** release-to-manufacturer (snapshot
visibility, opaque release_id, no send); patient status link (opaque token, read-only
plain-language page, stage-correct notices); enrollment/promote (records one HIPAA legal
basis + named physician; arms the post-enrollment obligations checklist — 312.32(c)(1)/(2)
safety clocks per-event-unarmed, 312.310(d)(2) + 56.104(c) emergency clocks, 312.33 annual
report); read-only coordinator board across cases. Append-only hash-chained audit trail
(`/api/case/{id}/audit`) with chain verification.

**Matching** — registry-search organizer from the committed profile's de-identified
predicates (closed struct: rolled-up condition codes + drug token outbound; age band, sex,
route compared locally, never sent); matched/unmatched/unverifiable criteria, no scores,
no ranking; honest absence framing; mock registry only (live egress code-disabled).

**Guarantees that hold on inspection:** drafts-only (every gate fails closed in the engine;
sign-offs only record; DRAFT watermark unremovable by flag); no PHI egress (live egress
raises `EgressDisabled`; the closed predicate struct rejects non-code-shaped values);
nothing auto-decided (no defaulted attestation, no auto-commit, no accept-all, no score,
no auto-send anywhere I could find).

---

## 2. ASSESSMENT — what serves this persona, and where it fails them

**Genuinely serves the physician.** The commit → generate → ledger → gate loop is the
strongest part of the product: the resolving-question ledger with deep links back to the
exact intake field is exactly how a clinician without regulatory staff repairs a package.
The clock discipline (unarmed until a physician-entered date, working-day vs calendar-day
calendars, federal holidays) is better than what most clinicians do with a calendar. The
sponsor-investigator duties are named at the moment they attach (the promote card's
"OSSICRO tracks the deadlines; you perform the acts" + obligations checklist) — the system
does not walk the physician into duties it then ignores. The four-decisions/four-owners
framing on screen 1 and the gate table make the non-delegable line unusually clear. The
FHIR confirm-per-field flow honestly trades speed for attribution.

**Where it is weak or misleading for them:**

- **A green that isn't earned (LOA).** The ledger's color semantics ("Green = complete")
  are the physician's dashboard, and the OSSICRO-drafted Manufacturer LOA goes green with
  no recorded fact that the manufacturer ever issued or signed it (verified by simulation:
  the UI-loaded sample yields GREEN for `manufacturer-letter-of-authorization`). A rushed
  clinician can print a package containing a letter purporting to be from the manufacturer
  that the manufacturer never saw. (Finding 8.)
- **A red that can't be fixed (drug accountability).** `drug-accountability-log` requires
  `lot_numbers`/`dispensing_entries`, which have no intake fields — the server rejects
  unknown ids, the fix-loop link is absent, and the doc's own template says these values
  are "honestly absent at submission time." Every UI-driven case carries a permanent red
  the physician cannot resolve. (Finding 9.)
- **No way to date the submission.** The engine anchors document dates on
  `submission.date` first (`_AS_OF_FIELDS`) and falls back the 30-day clock to it — but no
  such intake field exists in the schema. A routine non-emergency case renders
  `[[MISSING: cover_date]]` and a blank Form 3926 "DATE OF SUBMISSION" with no fix link;
  the only workaround is entering `submission.fda_receipt_date`, a date the physician
  cannot know before submitting. (Finding 10.)
- **One statutory clock is anchored on the wrong trigger in one of its two homes.** The
  route clock correctly arms the 56.104(c) 5-working-day IRB notification from
  `submission.first_treatment_date`; the post-enrollment obligations checklist arms the
  same duty from the FDA telephone-authorization date and instructs the physician to enter
  that (wrong) date. Two screens can show two different deadlines for the same legal duty.
  Practical direction is conservative (auth precedes treatment), but it is a computed
  statutory deadline from the wrong anchor (HC3-adjacent). (Finding 11.)
- **The ICF is research-framed for a treatment request.** Screen 1 says "Treatment, not
  research (21 CFR 312.305(a))"; the drafted consent opens "You are being asked to take
  part in a research study" with Study/Protocol framing. (Finding 12.)
- **The Form 3926 item numbering is unverified and internally inconsistent** (template puts
  qualification at 7 and skips 9; the route spec says qualification is Field 6 and the
  rationale is Field 9). The FDF map is flagged TODO(HUMAN-VERIFY); the text template, PDF
  layout, and spec are not, and a clinician transcribing onto the official form could
  misplace content. (Finding 13.)
- **Enrollment is recordable while everything upstream is still amber.** The promote card
  sits in the linear flow with no advisory that consent, IRB, LOA, and FDA
  allow-to-proceed should precede treatment; a busy clinician can read the next button as
  the next step. Nothing is auto-decided — but the wizard's shape gives implicit
  permission. (Finding 14.)
- **Burden honestly reduced, but the ceiling is visible:** 35 of 55 fields are manual by
  design and several (consent risk language, benefit-risk rationale) are blank-textarea
  authoring tasks with no drafting help; the safety-report shells and annual-report draft
  the spec (§7) promises are not among the 8 generated documents; matching's closed
  vocabulary (5 conditions, 7 drugs) makes the feature demo-only beyond the sample
  registry (the mock caption does disclose this). The system reduces assembly and deadline
  burden substantially; it does not yet reduce the writing burden of the clinical
  narratives, which is where this persona's hours actually go.

**Hard lines:** I found **no violation** of drafts-only, no-PHI-egress, or
nothing-auto-decided. The nearest approaches are (a) the FHIR privacy note's "never leaves
this machine" wording, which is true only while the server is localhost (Finding 5), and
(b) the match panel claiming age/sex/route were "sent" when the egress design deliberately
never sends them — an overclaim in the safe direction (Finding 2).

---

## 3. FINDINGS

### Small fixes

1. **[SMALL-FIX]** Misleading working-day parenthetical on the clocks panel.
   `app/static/index.html:657-658` — current:
   `counted in working` / `days or calendar days (weekends and observed federal holidays included).`
   As written it reads as if working-day clocks include weekends/holidays; the engine
   excludes them. Replace with:
   `counted in working` / `days (weekends and observed federal holidays excluded) or calendar days (included).`

2. **[SMALL-FIX]** Match panel overstates what left the machine.
   `app/static/index.html:2575-2576` — current:
   `<p class="muted small" style="margin:8px 0 0"><b>De-identified search terms sent.</b> Everything` /
   `      that left the case is shown below; it contains no names, dates, geography, or identifiers:</p>`
   `egress.decompose_query` sends only rolled-up condition codes + drug token; age band,
   sex, and route are compared locally and never sent. Replace with:
   `<p class="muted small" style="margin:8px 0 0"><b>De-identified search terms used.</b> The full set` /
   `      is shown below — only the condition codes and drug token are sent to registries; age band, sex,` /
   `      and route are compared locally and never sent. None of it contains names, dates, geography, or identifiers:</p>`

3. **[SMALL-FIX]** Help text describes a default that cannot happen from the UI.
   `engine/registry/routes.json:46` — current help:
   `"Arms the 30-calendar-day IND-effective clock. Defaults to the submission date if left blank."`
   The fallback reads `submission.date`, a field the intake schema does not contain (see
   Finding 10), so from the UI the clock simply stays unarmed. Replace with:
   `"Arms the 30-calendar-day IND-effective clock. If left blank, the clock stays unarmed until the date is entered."`

4. **[SMALL-FIX]** README understates the Constitution's hard-constraint list.
   `README.md:7` — current: `(HC1–HC5: no non-delegable act, no fabrication, computed statutory clocks, provenance/verbatim integrity, Part-11 attribution)`.
   The Constitution enumerates HC1–HC7. Replace with:
   `(HC1–HC7: no non-delegable act, no fabrication, computed statutory clocks, provenance/verbatim integrity, Part-11 attribution, no exculpatory consent language, no drafting-process leakage)`

5. **[SMALL-FIX]** Privacy claim on chart import is deployment-coupled.
   `app/static/index.html:585-586` — current:
   `Your chart data is parsed locally and never leaves this machine; nothing here becomes part of` /
   `        the submission until you confirm it — field by field, below.`
   The bundle is POSTed to the OSSICRO server; "never leaves this machine" is true only
   while that server is 127.0.0.1. Replace with:
   `Your chart data goes only to your local OSSICRO server on this machine and never beyond it; nothing here becomes part of` /
   `        the submission until you confirm it — field by field, below.`

6. **[SMALL-FIX]** Commit-card "values are never stored" is ambiguous.
   `app/static/index.html:638-639` — current:
   `The commit stores your name, the time, and a SHA-256 fingerprint of each confirmed value.` /
   `        The values themselves are never stored.`
   The intake values ARE stored in the case file; only the commit record is hash-only. A
   clinician could read this as a no-storage promise. Replace second line with:
   `        The commit record itself stores no values — the intake values remain in the case file as usual.`

7. **[SMALL-FIX]** The green readiness banner omits the third-party acts.
   `app/static/index.html:2430-2432` — current:
   `      <b>Package assembly complete.</b> Every draft is validated and internally consistent.` /
   `      What remains: the physician's review, the required signatures, and the physician's` /
   `      own act of submission to FDA. OSSICRO does not file.</div>\`;`
   "What remains" lists only physician acts, but the manufacturer LOA, IRB concurrence,
   and consent event also remain (they are amber, not blocking). Replace middle lines with:
   `      What remains: the physician's review and signatures, the third-party acts tracked in the` /
   `      ledger (manufacturer LOA, IRB concurrence, informed consent), and the physician's` /
   `      own act of submission to FDA. OSSICRO does not file.</div>\`;`

### Larger issues

8. **[LARGER-ISSUE] MAJOR — The drafted Manufacturer LOA turns GREEN ("complete") with no
   record the manufacturer ever issued it.**
   `engine/registry/documents.json` gives `manufacturer-letter-of-authorization` no gate;
   once `manufacturer_name` / `drug_master_file_reference` / `authorized_party` are filled,
   the ledger shows green (verified by simulation on the sample case). Green is the
   ledger's word for "complete," yet this document is legally the manufacturer's act
   (FDCA §561A; the template's own bracket note says so). A busy clinician can assemble
   and print a package containing an OSSICRO-drafted letter on the manufacturer's behalf
   that the manufacturer never saw, and nothing on the dashboard distinguishes it from a
   received LOA. Direction: give the LOA an external-party pending state — e.g. a recorded
   fact ("signed LOA received", like `manufacturer.supply_committed`) required before
   green, or an external-party gate row so it sits amber "awaiting manufacturer act."

9. **[LARGER-ISSUE] MAJOR — The drug-accountability log is a permanent, unfixable red in
   every UI-driven case.** Its registry entry requires `lot_numbers` and
   `dispensing_entries`, but no intake field exists for them (`POST /intake` rejects
   unknown ids; the sample fixture's `drug.lot_numbers`/`drug.dispensing_entries` are
   silently dropped by the UI), so the ledger question "Provide 'lot_numbers'…" has no fix
   link and no resolution path — while the document's own template says these values are
   "honestly absent at submission time." The physician stares at a red they can never
   clear. Direction: either drop the two fields from `required_fields` (it is a shell to
   be filled at dispensing — amber or green-with-note semantics fit better), or add
   post-supply intake fields; either way the ledger question must name a real next action.

10. **[LARGER-ISSUE] MAJOR — There is no "date of submission" intake field, so a routine
    case cannot be dated.** `ea_generators._AS_OF_FIELDS` anchors document dates on
    `submission.date` first and `compute_clocks` falls the 30-day clock back to it — but
    `routes.json` intake_fields never asks for it. In a non-emergency case the only
    available anchor is `submission.fda_receipt_date`, which the physician cannot know
    before submitting (circular); until then the cover letter renders
    `[[MISSING: cover_date]]` and the Form 3926 "1. DATE OF SUBMISSION" is blank, with no
    fix-loop link (the span maps to a non-schema path). Direction: add a
    `submission.date` ("Planned/actual submission date") field to the schema — the engine
    already consumes it — and let the fix-loop reach it.

11. **[LARGER-ISSUE] MAJOR — The 56.104(c) IRB-notification deadline is computed from the
    wrong trigger in the post-enrollment obligations checklist.** The regulation (and the
    route clock, `routes.json` `irb-notify-5-working-day`, trigger
    `submission.first_treatment_date`) anchor the 5-working-day notification on the
    emergency use (first treatment). But `clocks.expanded_access_emergency_deadlines()`
    anchors BOTH emergency deadlines on the FDA telephone-authorization date, and
    `app/server.py:_enrollment_obligations` arms the IRB-notification obligation from
    `submission.emergency_auth_datetime` — with `STRINGS["obligation_irb_notify_q"]`
    explicitly instructing the physician to enter the authorization date to arm it. The
    same duty can show two different deadlines on the check screen vs the obligations
    checklist. The error is conservative in practice (authorization precedes treatment),
    but a statutory clock computed from the wrong anchor is exactly what HC3 exists to
    prevent. Direction: give `expanded_access_emergency_deadlines` a separate
    treatment-date parameter (or split the function), arm the checklist's 56.104(c) row
    from `submission.first_treatment_date`, and fix the resolving-question string and the
    `clocks.py` docstring ("The two clocks that start when FDA authorizes emergency use by
    phone") to match.

12. **[LARGER-ISSUE] MAJOR — The informed-consent draft is research-framed for a
    treatment-use request.** `engine/ossicro/generate.py` ICF template: "You are being
    asked to take part in a research study", "Study: {{protocol_title}}",
    "Protocol: {{protocol_number}}" — while screen 1 of the same product says "Treatment,
    not research (21 CFR 312.305(a))". Part 50 elements are present, but describing
    expanded-access treatment to the patient as a research study misstates its purpose
    (and the required fields `protocol_number`/`protocol_version` lean on an optional
    treatment-plan-id workaround). Direction: an EA-profiled ICF variant that describes
    treatment use of an investigational drug (per FDA's individual-patient EA guidance),
    keeping the verbatim 50.25 spans.

13. **[LARGER-ISSUE] MAJOR — Form 3926 item numbering is unverified and internally
    inconsistent.** The text template and PDF layout number LOA=6, qualification=7,
    IRB=8, then jump to 10.a/10.b (no item 9, no item 1 in the PDF layout beyond the
    title); the route spec (`docs/route-3926-submission-spec.md` §1.1) says the physician
    qualification statement is "3926 Field 6" and the clinical rationale is "Field 9". At
    least one is wrong against the official OMB 0910-0814 form. Only the FDF map carries
    the TODO(HUMAN-VERIFY) flag; the rendered text the physician transcribes from carries
    none. A clinician copying OSSICRO's draft onto the official form could misplace
    content. Direction: extend the one human verification pass to cover the text template,
    `_PDF_LAYOUT`, and the spec's field references, and until then surface the
    "numbering unverified" caveat on the rendered 3926 itself, not just the FDF.

14. **[LARGER-ISSUE] MAJOR — Enrollment can be recorded while consent, IRB, LOA, and FDA
    authorization are all still outstanding, with no advisory.** `POST /promote` gates
    only on a committed profile + named actor + legal basis; the promote card sits in the
    package screen's linear flow ("Record enrollment") with nothing telling a hurried
    clinician that the informed-consent and irb-approval sign-offs are unrecorded, no
    supply commitment is on file, and no FDA allow-to-proceed fact exists anywhere in the
    schema. Nothing is auto-decided — but the wizard's shape reads as permission.
    Direction: an escalate-only advisory on the promote card listing the gates without
    recorded sign-offs and the absent external facts ("Recording enrollment now records
    YOUR decision; these acts have no record yet: …"), and consider an intake fact for
    FDA authorization (date/means) so the record can carry it.

15. **[LARGER-ISSUE] MINOR — The sae-causality gate names a "medical-monitor" this persona
    does not have.** `gates.json` responsible_role is `medical-monitor`; in single-patient
    EA the physician-sponsor is the medical monitor. The gate table tells the clinician a
    person they don't employ must act. Direction: role label
    `physician-sponsor / medical monitor` for the EA route, or per-route role overlays.

16. **[LARGER-ISSUE] MINOR — "Enrollment" is trial vocabulary for a treatment pathway.**
    The whole Wave-4 surface calls the treatment-start transition "enroll/enrollment"
    while screen 1 insists this is treatment, not research, and the patient page says
    "the formal treatment process has begun." For the physician the legally meaningful
    moments are IND-effective and first treatment. Direction: rename the act in physician-
    facing strings ("Record start of treatment (legal basis)") while keeping the INV-5
    machinery; it also naturally supplies the `submission.first_treatment_date` trigger
    that Finding 11 needs.

17. **[LARGER-ISSUE] MINOR — Matching is effectively demo-only and its ceiling is quiet.**
    The closed derivation tables cover 5 conditions and 7 drugs; any other diagnosis
    yields zero predicates and an empty search rendered as the registries' honest answer.
    The mock-registry caption is good, but nothing tells the physician that an
    unrecognized diagnosis produced no searchable predicates at all (the predicate chips
    just render empty). Direction: when `condition_codes` is empty, say so explicitly
    ("your diagnosis text matched no coded search term — the search ran on nothing") so an
    empty result is never mistaken for a searched result.

18. **[LARGER-ISSUE] MINOR — Everything is unauthenticated and the physician-facing UI
    never says so.** The case id in the URL hash is a full-access capability; the
    manufacturer/coordinator personas are header toggles in the same browser; persona auth
    is INV-7-deferred (documented in code/strings the physician never reads). Fine for a
    localhost synthetic pilot, but the physician workspace itself should carry the
    "single-user local pilot — do not expose this server or share case URLs" statement the
    CRO board note already makes internally. Direction: one pilot-scope line in the draft
    banner or footer, until INV-7 lands.

---

*No hard-line violation found: drafts-only, no-PHI-egress, and nothing-auto-decided all
hold on static review and simulation. Findings 2 and 5 are wording drifts near the
privacy line (both overclaim in different directions), not violations.*
