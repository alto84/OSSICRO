# Persona review — IRB / Research-Ethics Reviewer

Reviewer persona: an IRB member / research-ethics reviewer asking whether OSSICRO respects
informed consent, IRB oversight, and the protection of a vulnerable, desperate patient.
Review date: 2026-07-11. Method: static read of engine/, app/, engine/registry/, docs/, wiki
references; test suite run read-only (336 passed); sample EA case rendered through the engine
to inspect the actual ICF a subject would be handed.

---

## Part 1 — INVENTORY: what the system offers this persona today

**Consent artifacts.** One ICF generator (`engine/ossicro/generate.py`,
`informed-consent-form-part50`, reused by the EA route via `ea_generators.gen_icf`). The
template is structured into the eight 21 CFR 50.25(a) basic elements as verbatim-locked,
SHA-256-verified section headings (rule `R-ICF-50.25`), filled from physician-entered
`consent.*` intake fields. Content adequacy is a separate, explicitly **deferred** concept rule
(`R-ICF-50.25-ADEQ`, "not executed by run_rules"). HC6 (no exculpatory language, 21 CFR 50.20)
is enforced deterministically by four Tier-A regex tripwires scoped to `consent`-category
documents (`engine/registry/banned-constructions.json`, `register_linter.py`) — these hard-fail
and cannot be waived.

**Consent event vs. consent form.** The distinction is held cleanly and repeated everywhere:
gate `informed-consent` (`engine/registry/gates.json`) states the consent EVENT "is a human act
between a qualified clinician and the subject and can never be executed by software." The ICF
itself renders with a footer: "consent itself is obtained by a qualified human."

**IRB flow.** An IRB concurrence request generator (`ea_generators.gen_irb_request`) with three
computed pathways: standard Part 56 approval, §56.105 chair concurrence (Form 3926 Field 10.b),
and emergency use under 56.104(c) with the computed 5-working-day notification deadline. Gate
`irb-approval` (responsible role `irb`) blocks the document from `final`; the completeness
ledger shows it amber until a sign-off with role exactly `irb` is recorded. Waivers 10.a/10.b
are never defaulted or auto-checked ("[Fields 10.a / 10.b are physician attestations; OSSICRO
never defaults or auto-checks them.]").

**Emergency-use ethics.** Both emergency clocks exist and are computed deterministically (HC3):
15 working days for the written 3926 (312.310(d)(2), anchored on the FDA phone-authorization
date) and 5 working days for IRB notification (56.104(c)). In `routes.json` the IRB clock is
correctly anchored on `submission.first_treatment_date`. Clocks never arm from the wall clock;
absent trigger dates render honestly as UNARMED with a resolving question.

**Gate enforcement (the fail-closed claim).** Verified in code: `Document.advance("final")`
raises `GateViolation` for a gated document with no recorded sign-off (`models.py:200-206`),
`gates.finalize` re-validates sign-offs at read time (`has_valid_signoff` + `signoff_problems`),
`record_signoff` refuses missing names, wrong roles, missing attestation statements. No app
endpoint calls `finalize` at all; the server only RECORDS sign-offs and the ledger's
amber-to-green move is derived from them. The 3926 PDF/FDF carry a permanent DRAFT watermark
with "no flag to remove it." The pipeline is escalate-only: a clean AI review can never clear a
gate, turn red green, or alter a deadline (`pipeline.py`). I found **no** configuration flag or
API path around any gate. The fail-closed claim holds.

**Patient persona.** A read-only, plain-language status page reachable only via an opaque
token minted by a named-human act (`POST /patient-link`, audited). The strings are honest and
non-pressuring: "Nothing has been submitted to the FDA... no decision has been made," "This
page... is not a promise that treatment will be approved or available," "nothing here asks you
to do anything or agree to anything." No payment framing, no urgency framing, no benefit
inflation anywhere in the patient-facing surface. Writing principle P2 makes promotional
framing "severity-critical in consent" text.

**Enrollment.** `POST /promote` records the preparatory-review → enrollment transition with a
named actor and one of three explicit HIPAA legal bases (never assumed), and arms the
post-enrollment sponsor-investigator obligation clocks.

---

## Part 2 — ASSESSMENT

**What genuinely serves this persona.** The gate architecture is real, not decorative: I tried
to find a bypass (config flag, API path, persistence re-apply, AI-review promotion) and there
is none; invalid persisted sign-offs are re-caught at read time and demote green→amber. The
drafts-only line is enforced in the artifact itself (watermark, DRAFT banners, signature blocks
labeled NON-DELEGABLE). The patient page is the best patient-facing status text I have seen in
a tool of this kind — calibrated, non-promising, and it explicitly names the IRB and written
consent as steps that must still happen. The 50.20 exculpatory tripwires are exactly the kind
of bright line an IRB wants deterministic. The four-party framing ("Four decisions, four
owners... OSSICRO owns none of them") is repeated at every surface a physician touches.

**Where it is weak for this persona.**

1. *The consent gate goes silent at the moment that matters.* Enrollment can be recorded with
   zero consent and zero IRB sign-off, and nothing even warns (Finding 5). The system's own
   ethics architecture — its proudest feature — is not consulted at its single most
   ethics-laden transition.
2. *The ICF is a generic trial ICF wearing an EA costume.* It tells the subject "You are being
   asked to take part in a research study" while the physician-facing UI says "Treatment, not
   research." It has no EA-specific disclosures, and its injury-compensation element is
   structurally incapable of satisfying 50.25(a)(6) (Finding 6). For a desperate patient the
   therapeutic-misconception risk runs both directions and neither is managed.
3. *Recording the IRB's act is too easy and too thin.* A readonly pre-filled role plus a typed
   name, with the attestation statement synthesized by the server, records "IRB approval" with
   no evidence object at all (Finding 7).
4. *One deadline, two answers.* The 56.104(c) IRB-notification clock is anchored on the first
   treatment in one code path and on the FDA phone call in another (Finding 8) — a genuine HC3
   correctness defect on the shortest, most ethics-loaded clock in the system.
5. *A silent AI egress channel.* /check ships the full rendered documents to an external model
   whenever an environment variable exists, un-audited (Finding 1) — governance asymmetric with
   the meticulously gated registry egress.

None of these break the drafts-only / nothing-auto-decided lines. One (Finding 1) is a
conditional hard-line concern on the no-PHI-egress line and is flagged at BLOCKER rank per the
review charter.

---

## Part 3 — FINDINGS

### Larger issues

**1. [LARGER-ISSUE] [BLOCKER — conditional hard-line: no-PHI-egress] Concept-reviewer egress is
silent, un-gated, and un-audited.**
`app/server.py:_select_reviewer` (line ~562) auto-selects `ClaudeConceptReviewer` whenever
`ANTHROPIC_API_KEY` is set in the server's environment; `GET /api/case/{id}/check` and
`GET /package` then transmit the **full rendered documents** — diagnosis, age, sex, prior
therapies, coded id, physician identity, site — to the Anthropic API
(`engine/ossicro/review_claude.py:_call`). Contrast the registry-egress discipline (INV-4,
`engine/ossicro/egress.py`): a closed six-field de-identified struct, live egress hard-failing
with `EgressDisabled` behind an explicit greenlight, and an `egress_query` audit record for
every call. The concept-review egress has none of that: no fail-closed flag, no per-call audit
record (the case audit trail has actions `commit/reconfirm/signoff/release/patient_link/
promote/bundle_loaded/egress_query` — no `concept_review`), and no user-facing disclosure that
document text left the machine beyond a `reviewer.model` string. This is also an HC5 gap: "Every
AI contribution is logged with the model, its version, the input hash, a timestamp, and the
identity and disposition of the human reviewer" — the ReviewReport's model/timestamp live only
in the ephemeral HTTP response, never in the durable audit trail. Caveats stated honestly:
`egress.py` names `review_claude.py` as a sanctioned outbound module, and the pilot is
synthetic-only, so no real PHI has left. But the moment a real chart enters, the no-PHI-egress
hard line is broken by an env var rather than by a named-human greenlight. **Why it matters to
this persona:** an IRB's first question about any AI tool is "what leaves the machine, when, and
who consented to that"; today the honest answer is "everything in the draft, whenever the server
happens to have a key, and nobody is asked or told." **Direction:** route the concept reviewer
through the same discipline as INV-4 — an explicit, audited, human-flipped greenlight; one
audit record per review (model, version, doc ids, input hash, timestamp); a visible "documents
were/were not reviewed by an external model" line in the check UI; and a documented
de-identification stance for review payloads.

**2. [LARGER-ISSUE] [MAJOR] Enrollment can be recorded with no consent and no IRB sign-off, and
the system does not even mention it.**
`app/server.py:_promote` (lines ~1297-1339) requires a committed profile, a named actor, and a
HIPAA legal basis — and nothing else. It never consults the `informed-consent` or `irb-approval`
gates. A physician can record enrollment on a case whose ledger still shows both gates amber;
the response contains no warning; the obligations checklist that comes back lists safety
reports and annual reports but not the unsigned consent; and the patient status page flips to
"Your doctor has recorded that you are enrolled in this treatment plan." Consent-before-
treatment (21 CFR 50.20/312.60) and IRB review/concurrence-before-treatment (Part 56, outside
56.104(c)) are the two ethics preconditions of the entire enterprise, and this is the one
transition in the product that operationally marks "treatment relationship begins." The
`authorization-164.508` basis description does say the patient "signed a written HIPAA
authorization... alongside 21 CFR Part 50 informed consent" — but that text appears only inside
one of three radio-button descriptions, and the other two bases carry no consent language at
all. **Why it matters to this persona:** the system's whole ethical proposition is that gates
make skipped ethics steps loud; here the most consequential step can be skipped in silence.
**Direction (escalate-only, consistent with CP5):** at minimum, `_promote` should append a
prominent, persisted advisory when either gate lacks a recorded sign-off ("Enrollment recorded
with the informed-consent gate unsigned — consent before treatment is required by 21 CFR
312.60/Part 50 except under a §50.23 exception; record the sign-off or document the
exception"), surface the same advisory in the check ledger and the promote response, and
consider refusing outright on the non-emergency route (fail-closed is the house style; a
refusal naming the unsigned gates is more OSSICRO than a warning).

**3. [LARGER-ISSUE] [MAJOR] The ICF is a generic clinical-trial ICF, not an expanded-access
ICF — therapeutic-misconception risk is unmanaged.**
Three connected defects in `engine/ossicro/generate.py` (template
`informed-consent-form-part50`, lines 111-156):
(a) **50.25(a)(6) cannot be satisfied by this template.** Element 6 renders only: "If you
believe you have been injured as a result of this research, contact {{injury_contact_name}} at
{{injury_contact_phone}}." The regulation requires, for greater-than-minimal-risk research, "an
explanation as to whether any compensation and an explanation as to whether any medical
treatments are available if injury occurs and, if so, what they consist of." No intake field
exists for that whether-statement (`routes.json` has only `contacts.injury_contact_name/phone`),
so even a diligent physician cannot make the drafted ICF compliant without hand-editing —
and the verbatim-heading rule `R-ICF-50.25` shows green ("contains all 8 basic-element
sections") over the non-compliant content.
(b) **The framing contradicts the product's own framing.** The ICF opens "You are being asked
to take part in a research study" while the physician start screen (`app/static/index.html:534`)
says "Treatment, not research (21 CFR 312.305(a))" and the spec's §0 heading is "treatment, not
research." Part 50 applies either way, but for single-patient expanded access FDA's own
guidance frames consent around *treatment use of an investigational drug*. A desperate patient
reading "research study" gets the wrong mental model in the very first sentence; a patient told
elsewhere it is "treatment" may over-read the drug's promise. Both directions of the
therapeutic misconception are live and unaddressed.
(c) **No EA-specific disclosures.** Missing content an IRB would require for EA consent: the
drug is not FDA-approved for this condition and FDA permission to use it is not evidence it
works; the manufacturer may decline or stop supplying at any time; whether the patient may be
charged (21 CFR 312.8(d) permits cost recovery — 50.25(b)(3) additional costs); significant
new findings will be communicated (50.25(b)(5)); consequences/procedure of stopping treatment
(50.25(b)(4)). Also `R-ICF-50.25-ADEQ` is deferred and the default `DeterministicStubReviewer`
only lints mannerisms, so nothing in the running system evaluates whether the risks section
actually informs. **Direction:** build an EA-profiled ICF template (the EA generators already
exist as the natural home), add intake fields for the injury-compensation statement and the
cost statement, replace the "research study" opener with FDA's EA consent framing, and treat
activating the adequacy review (live concept reviewer or human checklist) as a release gate for
any real-patient use.

**4. [LARGER-ISSUE] [MAJOR] Recording the IRB's concurrence requires no evidence and the
attestation statement is synthesized by software.**
The sign-off flow (`app/static/index.html:openSignoff`, lines 2230-2272 →
`app/server.py:_record_signoff`, lines 1412-1459 → `_apply_signoffs`, lines 505-529) records
gate `irb-approval` from: a typed name, today's date, and a **readonly role field pre-filled**
with `irb`. The engine's `record_signoff` requires "the signer's attestation statement," but the
app layer satisfies that by synthesizing one itself ("Recorded human act: %s (%s) performed this
act outside OSSICRO..."), so the one human-authored element the gate's design demands is
authored by the server. There is no place to record the concurrence letter, its date, the
concurring chair/member's identity as distinct from whoever typed the form, or an IRB reference
number — yet the cover letter's enclosure list promises FDA "IRB concurrence evidence" (see
Finding 12), and the ledger turns the item green on the bare record. Persona-auth is honestly
documented as deferred (INV-7), and the "records a fact that happened outside" framing is
legitimate — but a recording system for an ethics determination should capture the minimum
facts that make the record checkable. **Why it matters:** the practical failure mode of
single-patient EA is not a physician forging an IRB letter; it is a rushed physician recording
"chair said yes on the phone" weeks before the concurrence actually issues — and this UI makes
that a 5-second act indistinguishable from the real thing. **Direction:** for `irb-approval`
(and `informed-consent`), require a typed attestation in the signer's own words plus minimal
evidence metadata (concurrence date, concurring member name, IRB reference / "letter received
y/n"); persist them in the sign-off record; keep the engine contract unchanged.

**5. [LARGER-ISSUE] [MAJOR] The 56.104(c) 5-working-day IRB-notification deadline is anchored
on the wrong date in the post-enrollment obligations checklist (HC3 correctness defect).**
21 CFR 56.104(c) runs the five working days from the **emergency use** (the treatment).
`engine/registry/routes.json` gets it right (`irb-notify-5-working-day`, trigger
`submission.first_treatment_date`), as does the spec (§3.3: "Trigger... First treatment
administered"). But `engine/ossicro/clocks.py:expanded_access_emergency_deadlines` (lines
137-148) computes **both** emergency deadlines from `authorization_date`, and
`app/server.py:_enrollment_obligations` (lines 1249-1274) uses that function, so the enrolled
case's obligations checklist anchors the IRB notification on
`submission.emergency_auth_datetime` — and the string `obligation_irb_notify_q`
(`server.py:337-340`) even instructs: "Enter the FDA telephone-authorization date... to arm the
5-working-day IRB-notification deadline." The same case can therefore display two different
due dates for the same statutory duty (the /check clock vs. the obligations row), and the
instruction text teaches the physician the wrong trigger. (The auth-anchored date is usually
earlier, i.e., conservative — but HC3's promise is *computed correctly*, not *computed
safely-wrong*.) **Direction:** split the pair in `clocks.py` (15-wd from authorization; 5-wd
from first treatment), pass `submission.first_treatment_date` into the obligations builder, and
rewrite `obligation_irb_notify_q` to name the first-treatment date. Update the clocks.py
docstring line 15-16 in the same pass.

**6. [LARGER-ISSUE] [MAJOR] The IRB concurrence request asserts, unconditionally, "Informed
consent per 21 CFR Part 50 will be obtained before treatment begins" — false on the emergency
pathway.**
`engine/ossicro/ea_generators.py:809` (fixed line of `_IRB_REQUEST_TEMPLATE`). On the emergency
path the same document's computed `pathway_statement` says treatment "may proceed before IRB
review... within 5 WORKING DAYS of the first treatment (2026-…)" — i.e., treatment has already
happened — while two lines later the fixed prose promises consent *will be* obtained before
treatment *begins*. If consent was obtained pre-treatment, the tense is wrong; if a §50.23
exception applied (the realistic emergency scenario where the patient could not consent), the
statement to the ethics board is substantively false. A drafted misstatement in the one
document addressed to the IRB is exactly what this persona exists to catch. **Direction:** make
the consent sentence a computed literal like `pathway_statement`: non-emergency → present text;
emergency → "Informed consent per 21 CFR Part 50 was obtained before treatment, or the
treatment proceeded under a §50.23 exception as documented by the physician — [physician
attests which]." (An intake attestation field would keep HC2 honesty: never assert what wasn't
entered.)

**7. [LARGER-ISSUE] [MINOR] `Document.advance("final")` checks sign-off existence, not
validity.**
`engine/ossicro/models.py:200` guards with `self.has_signoff(self.gate_id)` (any record with a
matching gate_id), while `gates.finalize` uses `has_valid_signoff` (role, named person,
statement re-checked at read time). `gates.py`'s own docstring notes sign-offs "can be
re-applied from persistence... without passing through record_signoff" — precisely the case
where an invalid record (wrong role) exists on the document. Anything calling
`doc.advance("final")` directly instead of `finalize()` would accept it. No current caller does,
so this is defense-in-depth alignment, not a live hole. **Direction:** either have
`advance("final")` for gated docs demand validation via an injected check, or document loudly
that `finalize()` is the only sanctioned path and make `advance` refuse `final` for gated
documents outright (forcing callers through `finalize`).

**8. [LARGER-ISSUE] [MINOR] The patient status page's "what still has to happen" list is
route-blind and can misstate the emergency pathway.**
`app/server.py` STRINGS `patient_remaining_draft/committed/released` always include "The FDA
must allow the treatment to go ahead," "An ethics review board (called an IRB) must agree," and
"Before any treatment, you will be asked for your written permission (informed consent)." On an
emergency case, FDA may already have authorized by phone, the IRB step is a 5-day notification
rather than prior agreement, and treatment (and consent, or a 50.23 exception) may already have
occurred. A patient on the emergency route reads a checklist that does not match what is
happening to them. **Direction:** an emergency variant of the three `patient_remaining_*` lists
(the server already knows `submission.emergency`), keeping the same plain-language register.

**9. [LARGER-ISSUE] [MINOR] `submission_ready: true` while consent and IRB gates are unsigned
invites over-reading.**
`engine/ossicro/assemble.py` computes `submission_ready` from "no FDA-facing document is red";
pending non-delegable gates (amber) deliberately do not block it, with a documented rationale
(gates are "human acts at/after filing"). Regulatorily defensible for `submission-to-fda`; but
a physician glancing at `submission_ready: true` with the consent form unsigned may file and
treat on momentum. **Direction:** rename or annotate in the payload/UI: "documentation ready —
N non-delegable human acts still outstanding (listed)" so the flag can never be read as
"everything done."

**10. [LARGER-ISSUE] [MINOR] The enrolled patient view drops the voluntariness thread.**
`patient_remaining_enrolled` (`app/server.py:271-278`) lists the doctor's reporting duties and
"Tell your doctor about anything you notice" — nothing reminds the patient that continuing is
their choice. 50.25(a)(8)'s promise ("you may discontinue participation at any time without
penalty") should survive into the ongoing-treatment surface a patient actually looks at.
**Direction:** add one line, e.g. "Continuing this treatment is your choice. You can stop at
any time — tell your doctor, and your regular care will not be affected."

### Small fixes

**11. [SMALL-FIX] Version renders as "vv1.0" in the ICF an IRB would review.**
The ICF template hardcodes a "v" prefix (`Protocol: {{protocol_number}} v{{protocol_version}}`),
but the intake help, the sample fixture, and the FHIR-derived default all supply values already
carrying "v", so the rendered ICF header reads `Protocol: TP-CYTO-3926-014 vv1.0` (verified by
rendering the sample case). Fix the data side to match the template's convention — four exact
edits:
- `engine/registry/routes.json` line 29: current `"help": "e.g. v1.0. Feeds the consent form's
  version field so amendments are traceable."` → `"help": "e.g. 1.0 (the form adds the 'v').
  Feeds the consent form's version field so amendments are traceable."`
- `engine/fixtures/ea_sample_case.json`: current `"treatment.plan_version": "v1.0"` →
  `"treatment.plan_version": "1.0"`
- `engine/ossicro/fhir_ingest.py` line 895: current
  `out.append(_proposal("treatment.plan_version", "v1.0", "(none)",` →
  `out.append(_proposal("treatment.plan_version", "1.0", "(none)",`
- `engine/tests/test_fhir_ingest.py` line 170: current
  `self.assertEqual(by["treatment.plan_version"]["value"], "v1.0")` →
  `self.assertEqual(by["treatment.plan_version"]["value"], "1.0")`

**12. [SMALL-FIX] Cover letter enclosure list promises FDA "IRB concurrence evidence" the
package does not contain.**
`engine/ossicro/ea_generators.py` lines 370-371 (`_COVER_TEMPLATE`): the route's `fda_package`
contains only the concurrence *request* (`irb-concurrence-request`); no artifact slot for the
IRB's actual concurrence exists (see Finding 4). Current:
`6. ENCLOSURES. Form FDA 3926; expanded-access treatment plan; manufacturer` /
`   Letter of Authorization; IRB concurrence evidence; informed consent form.`
Replace the second line with:
`   Letter of Authorization; IRB concurrence request (the IRB's concurrence` /
`   evidence is attached when received); informed consent form.`

**13. [SMALL-FIX] ICF element 1 runs the purpose and duration together into one unpunctuated
sentence.**
`engine/ossicro/generate.py` (template `informed-consent-form-part50`, element 1) renders e.g.
"…that has not responded to approved therapy Expected duration of participation: …". Current
template line:
`   {{purpose}} Expected duration of participation: {{duration}}`
Replace with:
`   {{purpose}}` + newline + `   Expected duration of participation: {{duration}}`
(i.e., `"   {{purpose}}\n   Expected duration of participation: {{duration}}"`). The
verbatim-locked span for element 1 is the heading line only, so this does not disturb
`R-ICF-50.25` hashes. Plain-language readability of the consent's first element is a Part 50
"understandable to the subject" concern, not cosmetics.

**14. [SMALL-FIX] Patient-view stage heading for "enrolled" implies treatment has begun.**
`app/static/index.html` lines 1094-1095: enrollment is a records/legal-basis transition
(`_promote`), not the first dose; a patient reading "The formal treatment process has begun"
before any drug ships is being told something the system does not know. Current:
`      "enrollment": "The formal treatment process has begun",` /
`      "enrolled": "The formal treatment process has begun"`
Replace with:
`      "enrollment": "Your enrollment has been recorded",` /
`      "enrolled": "Your enrollment has been recorded"`
(The server-side `patient_stage_enrolled` sentence, "Your doctor has recorded that you are
enrolled in this treatment plan…", is accurate and needs no change.)

---

## Hard-line verdict

- **Drafts-only:** HOLDS. No finalize path from the app; `advance("final")` and `finalize()`
  fail closed; permanent DRAFT watermark with no removal flag; nothing sends anywhere.
- **Nothing-auto-decided:** HOLDS. Escalate-only pipeline verified; AI findings can never clear
  a gate; waivers never defaulted; clocks never armed from the wall clock; release, patient
  link, enrollment, commit are all named-human acts with audit records.
- **No-PHI-egress:** HOLDS today only because the pilot is synthetic and the key may be absent.
  Finding 1 (concept-reviewer egress: silent env-var enablement, no audit record, no
  greenlight gate, full document text off-machine) is flagged BLOCKER-rank as a conditional
  hard-line violation: it must be brought under the INV-4 discipline before any real chart
  data enters the system.
