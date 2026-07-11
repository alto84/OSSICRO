# OSSICRO Review — Persona: FDA REVIEWER (single-patient expanded access)

Reviewer lens: I am the FDA review-division reviewer who receives the Route-3926
single-patient expanded-access package and must act on it under the emergency
(15-working-day) or non-emergency (30-calendar-day) clock. I care about exactly
what lands on my desk: the Form FDA 3926, the cover letter, the eCTD module map,
and every statutory citation and clock the system prints. I read the whole system
(engine, registry, app, docs) statically; I ran the suite read-only (336 passed).
Citations were spot-checked against Cornell LII / eCFR (21 CFR 312.305, 312.310,
312.40, 56.104) and the project's own guidance-cited wiki.

---

## 1. INVENTORY — what reaches the reviewer today

The FDA-facing package (`routes.json` → `fda_package`, assembled by
`assemble.assemble_submission`) is, in order:

1. **Expanded-access cover letter** (`ea_generators.gen_cover_letter`) — statement
   of request under 312.310; the §312.305(a)(1)-(3) criteria each addressed; the
   §312.310(a) risk determination; the LOA cross-reference paragraph; a computed
   CLOCK paragraph (emergency 15-working-day or non-emergency 30-calendar-day);
   enclosures list; contact block. Ends in an unsigned signature block stamped
   `[NON-DELEGABLE HUMAN ACT — gate: submission-to-fda]`.
2. **Form FDA 3926** — two renders:
   - a plain-text template (`gen_form_3926`) with `[DRAFT]` header, items 1–8,
     10.a/10.b, 11, and an unsigned signature line;
   - a **print PDF** (`pdf_3926.render_3926_pdf`) with a diagonal
     "DRAFT — NOT FOR SUBMISSION" watermark on **every** page (no un-watermarked
     render exists in code), a draft footer, and explicit "physician signs by
     hand" notices; plus an **FDF** (`fdf_3926`) whose AcroForm field names are
     openly flagged `TODO(HUMAN-VERIFY)` / synthetic-only.
3. **Expanded-access treatment plan** (`gen_treatment_plan`) — 312.305(b) content.
4. **Manufacturer Letter of Authorization** (`gen_loa`) — drafted for the
   manufacturer to sign; 312.23(b) cross-reference.
5. **IRB concurrence request** (`gen_irb_request`) — emergency 5-working-day path,
   §56.105 chair path, or standard approval path.
6. **Informed consent form** (built-in Part 50 generator).

Plus: an **eCTD module map** (Modules 1–5, `routes.json.ectd_map`), a **SHA-256
hash manifest** over every route document + a package digest, a
`submission_ready` boolean (green when no FDA-facing doc is red), a `blocking`
list, and a **computed clocks** array. The system draws a correct, explicit
line: eCTD is *Interpretive* — the spec (§1.3) states single-patient 3926 may be
filed on paper/fax/email and the default output is a paper/PDF assembled package.

**Clocks emitted** (`clocks.py`, `ea_generators.compute_clocks`,
`server._enrollment_obligations`): 15 working days (312.310(d)/(d)(2)), 5 working
days (56.104(c)), 30 calendar days (312.40(b)(1)), 15/7 calendar days
(312.32(c)(1)/(c)(2)), 60-day annual (312.33). Working-day arithmetic uses a
real federal-holiday engine (5 U.S.C. 6103 + OPM weekend-observance), verified
against a fixed table by the suite.

## 2. ASSESSMENT — does it pass initial review or bounce?

**Structurally, this would survive intake as a facially complete individual-patient
EA request.** The right instruments are present and in a defensible order; the
cover letter walks the §312.305(a) criteria and the §312.310(a) determination;
the clocks are computed deterministically from human-entered trigger dates, never
the wall clock; and the drafts-only posture is genuinely unmistakable — every
FDA-facing artifact is watermarked/stamped DRAFT, the signature is always an empty
non-delegable block, and nothing in the code path files, sends, or signs. **I found
no drafts-only, no-PHI-egress, or auto-decision hard-line violation.** Patient data
is coded-only (`patient.coded_id`, help text bans name/MRN/DOB); the separate
trial-matching egress path (`egress.py`) is de-identified against a closed
allow-list and is not part of the FDA submission.

Where it is weak is in the **pinpoint citations**, which is precisely where this
persona is asked to be unforgiving. The top-level citations are right, but **every
21 CFR 312.305(b)(2) roman-numeral sub-citation in the system is off by one** — a
systematic error a diligent reviewer or sponsor's regulatory counsel would catch
on the treatment plan and the 3926. Separately, the **5-working-day IRB clock in
the post-enrollment obligations checklist is anchored to the wrong statutory
trigger** (FDA authorization date instead of first-treatment date), contradicting
the route definition. Neither bounces the filing on its own, but both undercut the
system's core promise that "clocks and citations are computed, not guessed."

## 3. FINDINGS

### F1 — [LARGER-ISSUE] 312.305(b)(2) roman-numeral sub-citations are systematically off by one — MAJOR

Every `21 CFR 312.305(b)(2)(...)` pinpoint in the system is shifted one position
too low, because the enumeration silently omits item **(i) "a cover sheet (Form
FDA 1571)"** and starts counting substantive content at (i) instead of (ii).

Correct 312.305(b)(2) (verified against Cornell LII / eCFR):
(i) cover sheet (Form 1571); (ii) rationale + list of available therapeutic
options; (iii) patient selection / individual-patient description, history, prior
therapy; **(iv) method of administration, dose, route, duration, monitoring
procedures, discontinuation criteria**; **(v) facility where the drug is
administered**; **(vi) CMC**; **(vii) pharmacology and toxicology**; **(viii)
clinical procedures/labs/other measures to monitor effects and minimize risk**.

What the code claims vs. correct:

| Content | Code cites | Correct |
|---|---|---|
| rationale for treatment use (`_TREATMENT_PLAN_TEMPLATE` §1; `treatment_rationale`) | (b)(2)(i) | (b)(2)(ii) |
| patient description / diagnosis / prior therapies (§2; `patient_initials_coded`, `diagnosis`, `prior_therapies`) | (b)(2)(ii) | (b)(2)(iii) |
| dose / route / duration / treatment-plan summary (§3; `dose`,`route`,`duration`,`treatment_plan_summary`,`dosing_plan`) | (b)(2)(iii) | (b)(2)(iv) |
| facility / site (§4; `facility`, `site.name`) | (b)(2)(iv) | (b)(2)(v) |
| CMC + pharmacology/toxicology (§5) | (b)(2)(v)-(vi) | CMC = (vi); pharm/tox = (vii) |
| monitoring plan (§6; `monitoring_plan`) | (b)(2)(vii) | (b)(2)(viii) — monitoring procedures also appear in (iv) |

Affected locations (all must move together):
- `engine/ossicro/ea_generators.py`: lines 565–569 (`gen_form_3926` sources),
  595, 598, 603, 607, 610, 614 (`_TREATMENT_PLAN_TEMPLATE` section headers),
  637 (`dosing_plan`), 643–651 (`gen_treatment_plan` sources), 781–783
  (`gen_loa_request` dose/route/duration).
- `engine/registry/routes.json`: lines 21–24 (`drug.dose`, `drug.route`,
  `drug.duration`, `treatment.monitoring_plan`) and line 64 (`site.name`).

Why it matters to me: these parentheticals are the reviewer's cross-index into the
submission-requirements rule. When the treatment plan's monitoring section is
labeled `312.305(b)(2)(vii)` — which is **pharmacology and toxicology**, the one
section the physician explicitly does NOT author and cross-references via the LOA —
it reads as either a boilerplate error or a misunderstanding of who owns what.
This is exactly the "project has been wrong on a citation before" class.

Direction: apply the corrected mapping above in one pass. For the monitoring plan,
prefer `(b)(2)(viii)` (clinical monitoring to evaluate effects/minimize risk); if
the intent is the *monitoring procedures* enumerated alongside dose/duration, cite
`(b)(2)(iv)`. Add tests asserting the corrected pinpoints so the shift can't
regress. Because it spans ~20 sites and involves the (iv)/(viii) monitoring
judgment, I rank it a LARGER-ISSUE rather than a mechanical SMALL-FIX, but the
replacement values are unambiguous.

### F2 — [LARGER-ISSUE] Emergency 5-working-day IRB clock is anchored to the wrong statutory trigger — MAJOR

`clocks.expanded_access_emergency_deadlines(authorization_date)` computes **both**
the 15-working-day written-3926 clock **and** the 5-working-day IRB-notification
clock from the **same FDA telephone-authorization date** (clocks.py lines
137–148). But 21 CFR 56.104(c) requires emergency use be "reported to the IRB
within 5 working days" — the clock runs from the **emergency use (first
treatment)**, not from FDA's authorization. The two events are legally distinct
and treatment may begin after authorization.

The rest of the system knows this: `routes.json` emergency clock
`irb-notify-5-working-day` correctly uses `trigger_field:
submission.first_treatment_date`, and `gen_irb_request` (ea_generators.py ~825)
computes the 5-day deadline from `submission.first_treatment_date`. Only the
**post-enrollment obligations checklist** (`app/server.py._enrollment_obligations`,
lines 1249–1264) mis-anchors it, calling
`expanded_access_emergency_deadlines(auth_date)` and then labeling the returned
56.104(c) deadline as arising from the authorization date. The clocks.py docstring
("The two clocks that start when FDA authorizes emergency use by phone …
56.104(c): IRB notification within 5 working days", lines 138–147) enshrines the
same wrong anchor.

Why it matters to me: the system contradicts itself on which event starts a
statutory clock. The mis-anchored version happens to compute an *earlier* (more
conservative) deadline when treatment follows authorization, so it isn't unsafe —
but it is wrong, and a physician-sponsor who relies on the obligations checklist
is being told the IRB clock keys off the FDA call when it keys off the treatment.

Direction: give `expanded_access_emergency_deadlines` two anchors (auth date for
the 15-day, first-treatment date for the 5-day), or drop the 5-day out of that
convenience function entirely and have `_enrollment_obligations` compute it from
`submission.first_treatment_date` (as the route and `gen_irb_request` already do).
Fix the clocks.py docstring to state the 5-day clock runs from first
emergency treatment.

### F3 — [LARGER-ISSUE] Form 3926 field numbering is unverified against the official form (and skips Field 9) — MINOR/MAJOR

The rendered 3926 (`_FORM_3926_TEMPLATE` and `pdf_3926._PDF_LAYOUT`) uses items
1, 2, 3, 4, 5, 6, 7, 8, 10.a/10.b, 11 — **there is no Field 9**, and the mapping
of content to field numbers is the project's own interpretive layout. The
`FDF_3926_FIELD_MAP` right-hand AcroForm names are openly flagged as UNVERIFIED
placeholders (`TODO(HUMAN-VERIFY)`, pdf_3926.py lines 61–113) because the official
fillable Form FDA 3926 (OMB 0910-0814) was deliberately not fetched. The local
guidance PDF `sources/fda-guidance/FDA_Expanded-Access-Form-3926-Instructions.pdf`
exists but its text is font-encoded and was not reconciled against the layout.

Why it matters to me: if a filer hands me a "Form 3926" whose field numbering
doesn't match the OMB-approved form (a visible gap at 9; contact/signature under
item 11 rather than the form's actual boxes), it reads as a look-alike, not the
form — which is a bounce risk once the DRAFT status is (correctly) removed by a
human. The honesty of the TODO markers is good; the gap is that no pass has
reconciled item numbers/labels against the official instrument.

Direction: before the pilot's first real use, open the official Form 3926 in a
forms inspector, correct `FDF_3926_FIELD_MAP`, and align the `_PDF_LAYOUT` /
`_FORM_3926_TEMPLATE` item numbers and labels (including whatever the real Field 9
is) to the OMB form. Until then, the "Form FDA 3926" heading slightly overstates
fidelity — consider "Form FDA 3926 (draft layout — item numbering pending
verification against OMB 0910-0814)".

### F4 — [SMALL-FIX] Inconsistent granularity of the 15-working-day citation: 312.310(d) vs 312.310(d)(2)

The written-3926 deadline is cited as `21 CFR 312.310(d)(2)` in `clocks.py`
(lines 13–14, 140, 144) and `app/server.py` (line 1229), but as bare
`21 CFR 312.310(d)` in `ea_generators.gen_cover_letter` (lines 428, 433, 434) and
`routes.json` (lines 43, 44, 133 `basis`). The precise subsection for the
"within 15 working days" written-submission requirement is **(d)(2)**; (d) is the
whole "Emergency procedures" paragraph.

`engine/registry/routes.json` line 133, current:
`"basis": "21 CFR 312.310(d)"`
replace with:
`"basis": "21 CFR 312.310(d)(2)"`

And in `engine/ossicro/ea_generators.py` line 434, current:
`            clock_cite = "21 CFR 312.310(d)"`
replace with:
`            clock_cite = "21 CFR 312.310(d)(2)"`

(Non-blocking; harmonizes the citation to the more precise, correct subsection the
clocks engine already uses.)

### F5 — [SMALL-FIX] clocks.py docstring conflates 56.104(c) with the quorum/waiver path

`engine/ossicro/clocks.py` lines 15–16, current:
`- 5 WORKING DAYS — IRB notification after emergency/single-patient use where the`
`  expedited/less-than-quorum path is used (21 CFR 56.104(c) / 56.108).`

56.104(c) is the **emergency-use exemption** ("reported to the IRB within 5
working days"); "less-than-quorum / chair concurrence" is a different mechanism
(§56.105 / §56.108) and does not govern the 5-working-day clock. Replace with:

`- 5 WORKING DAYS — IRB notification after emergency use of the test article`
`  (21 CFR 56.104(c)); the clock runs from the emergency use (first treatment).`

### F6 — [SMALL-FIX] Cover-letter enclosure calls the IRB document "concurrence evidence" when it is a request

`engine/ossicro/ea_generators.py` line 371 (`_COVER_TEMPLATE`, enclosures), current:
`6. ENCLOSURES. Form FDA 3926; expanded-access treatment plan; manufacturer`
`   Letter of Authorization; IRB concurrence evidence; informed consent form.`

The document the system actually generates and bundles is the **IRB concurrence
request** (`irb-concurrence-request`), not evidence that concurrence was obtained.
Listing "IRB concurrence evidence" as an enclosure overstates what is in the
package to me. Replace `IRB concurrence evidence` with
`IRB of record and concurrence request (or approval evidence, if obtained)`.

### F7 — [SMALL-FIX] "Day 31 is the earliest dose day" is an off-by-one description of the 30-day wait

`engine/ossicro/clocks.py` lines 152–153, current:
`    """21 CFR 312.40(b)(1): the IND goes into effect 30 calendar days after FDA`
`    receipt (absent hold or earlier notification). Day 31 is the earliest dose day."""`

The IND "goes into effect 30 days after FDA receives the IND"; the computed due
date (`receipt + 30`) is the effective date and the earliest day use may begin.
The "Day 31" gloss is a hand-count that contradicts the returned date and is not
emitted to FDA, but it's a latent confusion. Replace the final sentence with:
`The returned date is the IND-effective date (30 calendar days after receipt) and the earliest day treatment may begin absent earlier FDA notification.`

### F8 — [SMALL-FIX] eCTD map places IRB concurrence in Module 5; US regional IRB info normally lives in Module 1

`engine/registry/routes.json` lines 95 and 130 (`ectd_map` Module 5), current
`doc_ids` include `irb-concurrence-request`. In US eCTD, IRB documentation and the
IRB of record are Module 1 (regional administrative), not Module 5 (clinical). The
map is labeled Interpretive and eCTD isn't required for single-patient 3926, so
this is not a bounce — but the placement is imprecise for a reviewer reading the
map literally. Direction (optional): move `irb-concurrence-request` to the Module 1
entry, leaving treatment plan + informed consent in Module 5. Flagged as the
lowest-priority item.

---

### Hard-line check (explicit)

- **Drafts-only:** HELD. Watermark on every PDF page with no un-watermarked render
  in code; `[DRAFT]` headers on every template; signature blocks always empty and
  labeled non-delegable; FDF field names openly synthetic. No code path files,
  sends, or signs.
- **No-PHI-egress:** HELD. FDA package uses coded patient id only; the separate
  matching egress is de-identified against a closed allow-list and is not part of
  the submission.
- **Nothing auto-decided:** HELD. All clock triggers are human-entered; unarmed
  clocks surface a resolving question, never a wall-clock guess; gates fail closed.

No BLOCKER-level violation found. The two MAJORs (F1 citation shift, F2 IRB clock
anchor) are correctness/consistency defects in what the system asserts, not
breaches of the drafts-only / privacy / no-decision lines.
