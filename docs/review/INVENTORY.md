# OSSICRO consolidated review — INVENTORY & prioritized backlog

Synthesized 2026-07-11 from the persona reviews in `docs/review/`: **physician, manufacturer,
regulator (FDA reviewer), ethics (IRB), compliance (legal), developer**.
**persona-patient.md had not been delivered at synthesis time** — this synthesis covers the
six delivered reviews; integrate the patient review when it lands (the patient-facing surface
is partially covered here via the ethics review's patient-page findings).

All six reviewers ran the suite read-only (336 passed) and reviewed the same tree.
Raw findings across the six files: **76** (26 [SMALL-FIX], 50 [LARGER-ISSUE]).
Consolidated below: **1 BLOCKER, 15 MAJOR, 21 MINOR** backlog items, plus **20 small-fix
items (26 edits)** in `SMALL-FIXES.md`.

---

## ⚠ HARD-LINE STATUS — read this first

**One conditional hard-line violation was flagged, independently, by two personas
(ethics finding 1; compliance L1) — item B1 below.** The live Claude concept reviewer
(`app/server.py:_select_reviewer` → `engine/ossicro/review_claude.py`) sends the **full
rendered documents** (diagnosis, age/sex, prior therapies, coded id, physician identity) to
the Anthropic API whenever `ANTHROPIC_API_KEY` is set in the server environment — silently,
with no named-human greenlight, no audit record, no BAA, no de-identification — while the UI
promises "never leaves this machine" and the system's own egress gateway (INV-4) demands an
explicit human greenlight to send even rolled-up condition codes.

It does **not** fire in the shipped default (no key set → stub reviewer; pilot is
synthetic-only), which is why it is *conditional/latent* rather than an active breach — but it
fires with zero code change the moment the documented "production" configuration meets a real
chart. **All six personas verified the other two hard lines — drafts-only and
nothing-auto-decided — HOLD everywhere they looked**, and no-PHI-egress holds in the shipped
default. B1 must be closed before any non-synthetic use.

---

## 1. SYSTEM INVENTORY — what OSSICRO offers each persona today

**Physician (sponsor-investigator).** A 5-step wizard for a single-patient 3926 package:
55-field cited intake with tri-state attestations never defaulted; optional SMART-on-FHIR
chart import that produces proposals only (per-field named confirmation, identifiers
structurally never extracted); commit → generate 8 documents (cover letter, 3926 text + DRAFT
PDF/FDF, treatment plan, LOA draft + LOA request, IRB request, Part-50 ICF, drug-accountability
shell), every span provenance-stamped, `[[MISSING]]` instead of invented values; a
green/amber/red completeness ledger with resolving questions and fix-in-intake deep links;
statutory clocks computed only from physician-entered trigger dates (federal-holiday-aware
working-day engine); escalate-only AI review that can never clear a gate; sign-off recorder;
post-enrollment obligations checklist; append-only hash-chained audit trail.

**Manufacturer (Medical Affairs).** A drafted LOA request and a courtesy LOA draft, both
explicit that supply, signature, and FMV/AKS judgment are the manufacturer's alone; a
named-human release act (hash-bound snapshot, immutable audit record, opaque release_id); a
read-only inbox with deliberately **no** approve/deny affordance; minimized snapshot (coded id,
diagnosis, drug, physician).

**FDA reviewer.** A facially complete individual-patient EA package in defensible order;
§312.305(a) criteria and §312.310(a) determination walked in the cover letter; an honest
"Interpretive, not mandatory" eCTD module map; SHA-256 manifest + package digest;
deterministic clocks (15wd/5wd/30cd/15cd/7cd/60d) from human-entered anchors; DRAFT watermark
on every PDF page with no removal flag.

**IRB / ethics.** A Part-50-structured ICF with verbatim-locked, hash-verified element
headings; deterministic HC6 exculpatory-language tripwires that hard-fail; the consent
*event* vs consent *form* distinction held everywhere; a three-pathway IRB concurrence
request with the computed 5-working-day emergency deadline; fail-closed gates verified
bypass-free (no config flag, no API path, invalid persisted sign-offs re-caught at read time);
a calibrated, non-promising, plain-language patient status page behind an opaque token.

**Compliance / legal.** A constitution with seven hard constraints and a correct, consistently
threaded 21 CFR 312.52 no-transferee line; a 19-row non-delegable gating matrix (8
code-enforced); Part-11 substrate (hash-chained audit, input-hash commit records, per-span
provenance); HIPAA preparatory-review/enrollment state machine with recorded legal basis;
closed de-identified egress struct with live egress hard-disabled; persona minimization;
an unusually good self-audit record (`qa/`, wave memos).

**Developer.** ~11.5k LOC, pure-stdlib engine (24 modules) + stdlib HTTP server + one-file
SPA + JSON registries; guarantees enforced structurally, not by convention (`GateViolation`
fail-closed, `require_committed` single chokepoint, construction-time egress shape refusal,
verifiable audit chain, atomic case writes); honest in-code documentation of known limits
(unkeyed hashes, INV-7 deferral, egress residual risk); real adversarial wave reviews with
landed, tested fixes.

---

## 2. BACKLOG — consolidated, de-duplicated, ranked

Issues raised by multiple personas are marked **[xN personas]** — those are the real ones.

### BLOCKER

**B1. Concept-reviewer egress is silent, un-gated, and un-audited — conditional no-PHI-egress
violation.** *[x2: ethics 1 (BLOCKER), compliance L1 (BLOCKER)]*
`_select_reviewer` auto-selects the live Claude reviewer on env-var presence; `/check` and
`/package` then ship full rendered documents off-machine with no greenlight act, no
`ai_review` audit record (also an HC5 gap — model/version/input-hash/reviewer-disposition are
never durably logged), no BAA anywhere in the repo, and a UI that promises the opposite.
For an n-of-1 rare-disease case this is realistically identifiable PHI (the project's own QA
says so). **Why it matters:** the flagship privacy claim is falsifiable by reading two files;
an IRB's first question ("what leaves the machine, when, who consented?") currently has a bad
answer. **Direction (both personas converge):** put the live reviewer behind the same
explicit, audited, named-human greenlight discipline as INV-4; write one audit record per
review (model, version, doc ids, input hash, timestamp); surface "documents were/were not
reviewed by an external model" in the check UI; document the BAA/zero-retention precondition;
reconcile the index.html:585 promise (SMALL-FIXES H2 is an interim improvement, not the fix).

### MAJOR

**M1. The 56.104(c) 5-working-day IRB clock is armed from the wrong statutory trigger in the
post-enrollment obligations checklist.** *[x4: physician 11, regulator F2, ethics 5,
compliance L2 — the most-corroborated finding in the whole review]*
The regulation, `routes.json` (`irb-notify-5-working-day` → `submission.first_treatment_date`),
the spec, and `gen_irb_request` all anchor on **first treatment**;
`clocks.expanded_access_emergency_deadlines` and `server._enrollment_obligations` anchor on
the **FDA telephone-authorization date**, and `obligation_irb_notify_q` instructs the
physician to enter that (wrong) date. The same duty can show two different deadlines on two
screens. Conservative in practice, but a computed statutory clock with the wrong anchor is
exactly what HC3 exists to prevent. **Direction:** split the two anchors in `clocks.py`
(15wd from authorization, 5wd from first treatment), arm the checklist row from
`first_treatment_date` (honestly UNARMED without it), fix `obligation_irb_notify_q` and the
function docstring, add a reconciliation test. (SMALL-FIXES C1 fixes only the module
docstring's separate mis-citation — it does not resolve this.)

**M2. The manufacturer's LOA turns GREEN ("complete") and feeds `submission_ready` with no
record the manufacturer ever issued it; the manufacturer's decision has no first-class
record.** *[x3: physician 8, manufacturer 5+6, ethics 9 (adjacent)]*
`manufacturer-letter-of-authorization` has `gate: null` and its required fields are all
physician-entered, so the ledger goes green the moment the physician types the IND number;
`submission_ready` never consults `manufacturer.supply_committed` (itself only a
physician-set boolean — the spec's promised "LOA-acceptance record" does not exist); the
cover letter's enclosure list asserts the LOA is enclosed. A rushed clinician can print a
package containing a letter purporting to be the manufacturer's that the manufacturer never
saw — the pattern that makes manufacturers distrust intermediary tooling. **Direction:** an
"awaiting external party" ledger state for external-party documents, keyed to recorded facts
(`manufacturer.loa_received_date`, `loa_signatory`, optional document hash); make
`submission_ready` require the LOA-received fact (or the no-IND division-contact branch);
reword the enclosure line ("upon receipt"); annotate `submission_ready` in the UI as
"documentation ready — N human acts outstanding" (ethics 9).

**M3. The informed-consent draft is a generic clinical-trial ICF, not an expanded-access
ICF.** *[x2: physician 12, ethics 3]*
It opens "You are being asked to take part in a research study" while screen 1 of the same
product says "Treatment, not research (312.305(a))" — both directions of the therapeutic
misconception live and unmanaged for a desperate patient. 50.25(a)(6) is structurally
unsatisfiable (no intake field for the compensation/medical-treatment whether-statement, yet
`R-ICF-50.25` shows green over it); EA-specific disclosures are absent (not FDA-approved,
supply may stop, cost/charging under 312.8, 50.25(b)(4)/(b)(5) elements); the adequacy rule
is deferred and nothing running evaluates whether the risks section informs. **Direction:**
an EA-profiled ICF variant per FDA's individual-patient EA guidance (keep the verbatim 50.25
spans), intake fields for injury-compensation and cost statements, and treat adequacy review
as a release gate for any real-patient use.

**M4. Enrollment can be recorded with consent, IRB, LOA, and FDA authorization all
outstanding — silently.** *[x2: physician 14, ethics 2]*
`POST /promote` gates only on committed profile + named actor + HIPAA basis; it never
consults the `informed-consent` or `irb-approval` gates; the promote card sits in the linear
flow reading as "the next step"; the patient page then flips to "enrolled." The system's
whole proposition is that skipped ethics steps are loud; its most ethics-laden transition is
silent. **Direction:** escalate-only advisory persisted on promote when either gate lacks a
sign-off (naming 312.60/Part 50/Part 56), surfaced in the promote response and check ledger;
consider fail-closed refusal on the non-emergency route; consider an intake fact for FDA
authorization so the record can carry it.

**M5. No "date of submission" intake field exists, so a routine case cannot be dated.**
*[x2: physician 10, manufacturer 8]*
`_AS_OF_FIELDS` and the 30-day-clock fallback anchor on `submission.date`, which the schema
never asks for and `/intake` rejects; a non-emergency pre-submission case renders
`[[MISSING: cover_date]]`, a blank 3926 "DATE OF SUBMISSION", and an undated LOA request at
exactly the moment it is sent — the only workaround is entering an FDA receipt date that
hasn't happened. **Direction:** add a physician-entered `submission.date`
(planned/actual submission or preparation date) to the schema — the engine already consumes
it — and let the fix-loop reach it; or drop the dead anchors and document the gap.
(SMALL-FIXES J2 fixes the false help-text promise meanwhile.)

**M6. Form 3926 item numbering is unverified against the official OMB 0910-0814 form and
internally inconsistent.** *[x2: physician 13, regulator F3]*
Template and PDF layout number LOA=6, qualification=7, IRB=8, skip 9; the route spec says
qualification is Field 6 and rationale Field 9 — at least one is wrong. Only the FDF map
carries TODO(HUMAN-VERIFY); the rendered text a clinician transcribes from carries no caveat.
**Direction:** one human verification pass against the official fillable form covering
`FDF_3926_FIELD_MAP`, `_PDF_LAYOUT`, `_FORM_3926_TEMPLATE`, and the spec's field references;
until then surface "item numbering pending verification" on the rendered 3926 itself.

**M7. The drug-accountability log is a permanent, unfixable red in every UI-driven case.**
*[x2: physician 9 (MAJOR), developer 2]*
Its `required_fields` (`drug.lot_numbers`, `drug.dispensing_entries`) exist in no intake
schema — `/intake` rejects them, the SPA silently skips them in the fixture, the ledger
question has no fix link. The physician stares at a red they can never clear, on a document
whose own template says the values are "honestly absent at submission time." **Direction:**
decide — either drop the two fields from `required_fields` (shell-to-be-filled-at-dispensing
semantics: amber or green-with-note), or add post-supply intake fields; either way the
ledger question must name a real next action. Don't leave the half-wired state.

**M8. Every 312.305(b)(2) roman-numeral pinpoint citation is systematically off by one.**
*[x1: regulator F1 — single persona, but verified against eCFR and spans ~20 sites]*
The enumeration omits (i) "cover sheet (Form 1571)" and starts substantive content at (i)
instead of (ii); the treatment plan's monitoring section is labeled (b)(2)(vii) — which is
pharmacology/toxicology, the one section the physician does NOT author. Undercuts the core
"citations are computed, not guessed" promise. **Direction:** apply the regulator's corrected
mapping table in one pass across `ea_generators.py` and `routes.json` (monitoring →
(b)(2)(viii), or (iv) if the intent is administration-adjacent monitoring); add tests
pinning the corrected pinpoints.

**M9. The entire access-control posture is one unenforced module constant, and the "no real
PHI" pilot assumption has no deployment guardrails.** *[x4: developer 1 (MAJOR),
compliance L6 (MAJOR), physician 18 (MINOR), manufacturer 11 (MINOR)]*
`HOST = "127.0.0.1"` is the only thing between "safe synthetic pilot" and a fully
unauthenticated PHI-class surface (`/api/case/{id}` returns full intake + patient token;
`/cro/board` enumerates case ids); nothing in code enforces the standing no-bind-change rule.
Meanwhile intake help invites **initials** into an unencrypted cleartext store, there is no
BAA inventory, no encryption-at-rest or retention note, and the physician-facing UI never
states the single-user-local-pilot scope. **Direction:** (a) code-level guard in `main()` —
refuse non-loopback bind unless an explicit override AND an auth backend exist; (b) a short
deployment-compliance page (covered-entity boundary, store-is-PHI, BAA inventory, retention);
(c) prefer study-assigned code over initials in the coded-id help; (d) make INV-7 persona
auth a precondition, not a deferral, for any non-synthetic pilot; (e) one pilot-scope line in
the physician UI.

**M10. The obligations checklist omits the 312.310(c)(2) end-of-treatment written summary —
a duty OSSICRO's own generated treatment plan promises FDA.** *[x1: compliance L3]*
The one obligation guaranteed to come due for a single-patient EA is drafted as a commitment
and then absent from the operative tracker, whose UI presents itself as the duty list.
**Direction:** an always-present, honestly-unarmed checklist row (trigger:
treatment-conclusion date, with intake support), plus a line stating the checklist is the
*tracked subset* of sponsor-investigator duties, not the entirety.

**M11. The obligations checklist is empty until the app-internal promote() event, but the
duties attach by operation of law.** *[x1: compliance L4]*
An emergency-use physician who records the authorization date, treats, and never clicks
"Record enrollment" sees no annual-report or safety-report duties anywhere. INV-5 is a
HIPAA-basis transition; the code made it the switch for the FDA-obligations display too.
**Direction:** decouple — surface the checklist as soon as the anchoring facts exist
(emergency auth date or FDA receipt date recorded), independent of promote; reword "duties
the enrollment creates."

**M12. Part-11 documentation overclaims in the present tense, and HC5's AI-attribution
promise is unimplemented for the concept layer.** *[x1: compliance L5; the HC5 half overlaps
B1]* The wiki's clause table claims role-scoped access and e-signature machinery that are
explicitly deferred/prototype-only in the code; HC5 says every AI contribution is logged with
the human reviewer's disposition — nothing captures either. The exact overclaim pattern CP4
forbids, committed in the project's own compliance narrative. **Direction:** BUILT /
NOT-YET-BUILT status column on the Part-11 clause table; one `ai_review` audit record per
concept invocation (rides with B1); build finding-disposition capture or narrow HC5's text.

**M13. Recording the IRB's concurrence requires no evidence, and the attestation statement
is synthesized by the server.** *[x1: ethics 4]*
A typed name + a readonly pre-filled role records "IRB approval" in 5 seconds; the one
human-authored element the gate design demands (the attestation) is authored by software;
no field exists for the concurrence date, concurring member, or reference number — while the
cover letter promises FDA "IRB concurrence evidence." **Direction:** for `irb-approval` (and
`informed-consent`), require a typed attestation in the signer's own words plus minimal
evidence metadata, persisted in the sign-off record; engine contract unchanged.

**M14. The IRB concurrence request asserts, unconditionally, that consent "will be obtained
before treatment begins" — false on the emergency pathway.** *[x1: ethics 6]*
On the emergency path the same document says treatment already happened; if a §50.23
exception applied, the statement to the ethics board is substantively false. **Direction:**
make the consent sentence a computed literal keyed to the pathway, backed by a physician
attestation field (HC2: never assert what wasn't entered).

**M15. The LOA request is not triage-complete for a real Medical Affairs intake.**
*[x1: manufacturer 7]*
Missing: emergency/needed-by flag (computed for the cover letter, never for the manufacturer),
drug quantity (weight/cycles), patient age/sex, physician license/state, shipping site, IRB
status, and any free-vs-cost-recovery statement (21 CFR 312.8 appears nowhere in the repo).
A real MA intake would answer with a questionnaire. **Direction:** extend the template
(reuse the cover-letter emergency computation; optional quantity/weight/site/license lines;
one-line charging statement) and badge urgency in the release snapshot/inbox.

### MINOR

**m1. `sae-causality` gate names a "medical-monitor" the physician-sponsor persona doesn't
have** *[physician 15]* — per-route role overlay or label "physician-sponsor / medical monitor."

**m2. "Enrollment" is trial vocabulary for a treatment pathway** *[physician 16]* — rename
physician-facing strings ("Record start of treatment"); naturally supplies the
`first_treatment_date` trigger M1 needs.

**m3. Matching is demo-only (5 conditions, 7 drugs) and an unrecognized diagnosis silently
yields an empty search** *[physician 17]* — say explicitly when zero predicates derived.

**m4. Engine LOA draft is thinner than the repo's own reference template; `manufacturer.address`
is collected but consumed by no generator (dead field)** *[manufacturer 9]* — fold the
reference letterhead/signatory/terms structure into `gen_loa`.

**m5. Template-corpus dotted paths diverge from the engine schema** (`drug.manufacturer`,
`loa.*`, `fda.review_division` etc. resolve to nothing) *[manufacturer 10]* — one
normalization pass or a legacy-paths note.

**m6. Manufacturer cannot pin the artifact they acted on** *[manufacturer 11]* — add
`loa_request_sha256` to the release snapshot/inbox item. (Auth half of that finding is in M9.)

**m7. eCTD map places IRB concurrence in Module 5; US regional IRB info is Module 1**
*[regulator F8 — demoted from SMALL-FIX: no exact replacement text, touches assembly-consumed
JSON]* — move `irb-concurrence-request` to Module 1 in `routes.json` ectd_map.

**m8. `Document.advance("final")` checks sign-off existence, not validity** *[ethics 7]* —
defense-in-depth: make `advance` refuse `final` for gated docs, forcing `finalize()`.

**m9. Patient status page's "what still has to happen" list is route-blind and can misstate
the emergency pathway** *[ethics 8]* — emergency variant of the three `patient_remaining_*`
lists.

**m10. Enrolled patient view drops the voluntariness thread** *[ethics 10]* — one line:
continuing is your choice; stopping won't affect regular care (50.25(a)(8)).

**m11. MIT license cannot carry the constitution's "no flag or API path goes around it"
claim for forks; the appended notice is not an enforceable restriction** *[compliance L7]* —
scope the hard-line claim to this codebase; consider trademark + conformance statement.

**m12. HC6's justification overstates what 4 regex tripwires close** (exculpatory language is
an open class — hold-harmless, cost-shifting phrasings pass) *[compliance L8]* — reword to
"deterministic tier hard-fails the enumerated constructions; judgment owns the class"; grow
tier-A from FDA's exculpatory-language guidance examples.

**m13. The 312.52 no-transfer truth is everywhere except the point of use, and re-signing
silently replaces the prior operative sign-off record** *[compliance L9]* — one sentence on
sign-off modal + promote card; supersede (with marker) rather than overwrite sign-off records
(11.10(e)).

**m14. Field/profile hashes are unkeyed SHA-256 — commit store is offline-enumerable; must
not meet real PHI** *[developer 3]* — HMAC under a server-side secret, riding INV-7. Hard
precondition for non-synthetic use (pairs with M9).

**m15. `_save_case` failures unhandled on commit/confirm/signoff/intake POST branches**
(memory/disk divergence on disk error) *[developer 5]* — uniform handler-level 500 wrapper.

**m16. 312.33 annual-report clock computed in the app, not `clocks.py`** *[developer 6]* —
move to `clocks.py` as `ind_annual_report_deadline()`; do it in the same pass as M1's clock
split.

**m17. Patient token leaks into stderr request logs; token lookup is a linear non-constant-time
scan** *[developer 7]* — mask `/api/patient/...` in `log_message`; token index +
`hmac.compare_digest`.

**m18. PDF/FDF export writes no audit record** *[developer 8]* — decide: explicit POSTed
export act or dedup'd record; don't bolt a side effect onto GET.

**m19. Match mini-eval metrics are decorative (computed atop an assertEqual that forces 1.0);
no criteria-level labels** *[developer 9]* — per-candidate expected-criteria labels; drop or
compute-before-assert the metrics.

**m20. Free-text de-identification is honor-system in the release view and egress term lookup**
(a physician typing "Jane Doe DOB 1/2/68" into diagnosis releases it) *[developer 10]* —
naive identifier lint at release/egress time, or keep as documented residual until
non-synthetic.

**m21. INV-4 live egress is a stub — the marquee gateway is the validation wall + mock
adapter; the outbound client, allow-listed registry APIs, and rate/volume mitigations remain
unbuilt** *[developer 11]* — scoping fact for planning, not a defect.

---

## 3. Cross-persona convergence map

| Issue | Personas | Rank |
|---|---|---|
| B1 concept-reviewer egress | ethics, compliance | BLOCKER |
| M1 56.104(c) wrong anchor | physician, regulator, ethics, compliance | MAJOR |
| M9 bind/auth/real-PHI cluster | developer, compliance, physician, manufacturer | MAJOR |
| M2 LOA green without manufacturer act | physician, manufacturer, (ethics) | MAJOR |
| M3 research-framed ICF | physician, ethics | MAJOR |
| M4 silent enrollment | physician, ethics | MAJOR |
| M5 undatable submission | physician, manufacturer | MAJOR |
| M6 3926 numbering | physician, regulator | MAJOR |
| M7 drug-accountability red | physician, developer | MAJOR |
| README HC/test-count drift (small fixes R1–R3) | physician, compliance, developer | SMALL |
| routes.json:46 false default (J2) | physician, manufacturer | SMALL |
| clocks.py docstring (C1) | regulator, compliance | SMALL |
| enclosure overstatement (G1) | regulator, ethics | SMALL |

## 4. Suggested sequencing

1. **Apply SMALL-FIXES.md** (one serial pass; re-run suite; expect 336 passed).
2. **B1** — greenlight + audit discipline for the concept reviewer (small, high-leverage;
   closes the HC5 half of M12 too).
3. **M1 clock-anchor split** (+ m16 clock-math consolidation in the same pass) and
   **M8 citation remap** — the two "computed, not guessed" credibility repairs; both have
   unambiguous target values and want regression tests.
4. **M2 + M5 + M7** — the ledger-honesty cluster (external-party state, `submission.date`
   field, accountability-log semantics): all intake-schema/registry work, natural one wave.
5. **M4 + M13 + M14** — the ethics-gate wave (promote advisory, sign-off evidence, pathway-
   conditional consent sentence).
6. **M3** (EA-profiled ICF) and **M6** (3926 verification pass against the official form) —
   each needs deliberate authoring/human verification, not just code.
7. **M9 + m14** before any non-synthetic pilot; **M10/M11/M12/M15** and the MINOR list
   behind those.
