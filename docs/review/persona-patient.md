# Persona review — the Patient (and family caregiver)

Reviewer stance: a patient with a serious or life-threatening illness — or the spouse/parent
reading over their shoulder — who has been handed a link by their doctor and told "you can
check where things stand here." Not technical. Not versed in FDA process. Hoping. Scared.
Every sentence is read twice, and any ambiguity is resolved toward either false hope or fear.
Method: static review of `app/static/index.html` (STRINGS.patientView, STRINGS.patientLink,
the `screen-patient` render path lines 3175–3244, patient-mode CSS lines 444–464),
`app/server.py` (patient STRINGS lines 209–279, `_case_stage` / `_patient_link` /
`_patient_view` lines 1114–1181), `docs/OSSICRO-CONSTITUTION.md` (values §II, HC1/HC6);
live instance probed read-only (bad token → plain 404 `{"error": "not found"}`, confirmed).
Date: 2026-07-11.

---

## 1. INVENTORY — what the patient actually sees and can do

**How they arrive.** The doctor mints an opaque link (`#patient=<token>`) in the physician
workspace — a named, audited act — and shares it themselves ("OSSICRO sends nothing to
anyone"). Opening the link puts the whole app into patient mode: font enlarged to 16px, and
ALL clinician chrome hidden by CSS (`body.patient-mode`, index.html:445–451) — the 5-step
wizard, persona/coordinator buttons, the "Route-3926 · 21 CFR 312.310" chip, the case chip,
the footer, and the physician draft banner. What remains is the OSSICRO wordmark, a Theme
button, and one card.

**The card, top to bottom** (`renderPatientView`, index.html:3203–3229):

1. Eyebrow "Your status page"; heading **"An update from your physician's office"**.
2. Lead sentence: *"Your physician is preparing a request to the FDA that would allow you to
   be treated with **[drug name]** under the FDA's "expanded access" program. Expanded
   access is a way to ask permission to use a medicine that is still being studied."*
3. An amber notice box: hardcoded bold **"Still in draft."** followed by the server's
   stage-conditional notice —
   - draft/committed/released: *"This page only shows status. Everything described here is
     a DRAFT that your doctor is preparing. Nothing has been submitted to the FDA, and no
     decision has been made. If you have questions, ask your doctor."*
   - enrolled: *"This page only shows status. For anything about your treatment or where
     things stand, your doctor's office is the right place to ask. They have the full
     picture."*
4. **"Where things stand"** — one bold sentence, server-canonical per stage:
   - draft: *"Your doctor is preparing a request to ask the FDA for permission to treat you
     with a medicine that is not yet approved for your condition. The request is still
     being written."*
   - committed: *"Your doctor has confirmed the details of the request. The paperwork is
     drafted, but it has not been sent anywhere yet."*
   - released: *"Your doctor has shared a draft of the request with the company that makes
     the medicine, asking for their support. The company has not decided yet."*
   - enrolled: *"Your doctor has recorded that you are enrolled in this treatment plan.
     From now on your doctor is responsible for watching your safety and sending required
     reports."*
5. **"What still has to happen"** — a numbered list (3–5 items by stage): doctor finishing
   the paperwork; *"The company that makes the medicine must agree to provide it"*; *"The
   FDA must allow the treatment to go ahead"*; *"An ethics review board (called an IRB)
   must agree"*; *"Before any treatment, you will be asked for your written permission
   (informed consent)."* At enrolled the list becomes the doctor's reporting duties plus
   *"Tell your doctor about anything you notice — new symptoms, side effects, or
   questions."*
6. Footer: *"This page is read-only. It changes as your physician's office makes progress;
   nothing here asks you to do anything or agree to anything."* Then, bold: *"This page is
   not medical advice, and it is not a promise that treatment will be approved or
   available. Please talk with your physician about what any of this means for you. They
   are the right person for every question about your care."* Then the coded reference id:
   *"Your reference code on this page is `[coded id]` — this page never shows your name,
   your medical record, or any test result."*

**Failure pages.** Bad/expired link: *"This link is not valid. / Please check that you
copied the whole link, or ask your physician's office to share it again."* — deliberately
identical for every bad token (no enumeration signal). Server trouble: *"We hit a snag. /
We could not load this page right now. Please try again in a few minutes."*

**What the patient can DO: nothing.** No buttons, no forms, no consent capture, no
messaging. The only action the page ever suggests is "ask your doctor."

**What the link exposes** (`_patient_view`, server.py:1166–1181): stage, the plain-language
status/remaining strings, the drug name, the coded patient id, and a `draft` flag. No name,
no case id, no diagnosis text, no documents. Token is an unguessable uuid; lookup is by
token value only.

---

## 2. ASSESSMENT

**What genuinely serves a frightened non-expert.**

- The plain language mostly lands at true Part-50 level: *"written permission (informed
  consent)"*, *"An ethics review board (called an IRB)"*, *"The company that makes the
  medicine"*, and expanded access explained in one sentence — *"a way to ask permission to
  use a medicine that is still being studied."* No form numbers, no CFR cites, no "sponsor-
  investigator" anywhere on the patient surface.
- The single most important sentence for a hoping family is present and bold: *"it is not a
  promise that treatment will be approved or available."* Nothing on the page implies
  approval, likelihood, or timeline. The stage verbs are honest — the FDA *"must allow"*
  (not "approve you"), the company *"has not decided yet"*, enrollment is *"recorded"* (the
  system claims only what it knows, not that treatment has begun).
- "What still has to happen" is the page's quiet masterpiece: it tells the patient the true
  shape of the road — four independent gates — instead of vague reassurance. A caregiver
  can read it aloud and everyone understands why this takes time.
- Privacy reassurance is concrete, not legalistic: *"this page never shows your name, your
  medical record, or any test result."*
- The error pages are humane ("We hit a snag") and always route to a person, not a retry
  spinner.
- Voice: the notice box and footer repeat "ask your doctor" — the page consistently refuses
  to become the patient's counterpart, which is exactly right.

**Where it is confusing, cold, or wrong.**

- **The page lies at the one stage that matters most.** The bold **"Still in draft."** lead
  is hardcoded into the notice box (index.html:3218) for every stage, including enrolled.
  The MAJOR-2 fix made the server's notice stage-conditional and hid the physician draft
  bar in patient mode — but this third copy of the draft claim was missed. An enrolled
  patient sees, in the same amber box: "**Still in draft.** This page only shows status…"
  directly above "Your doctor has recorded that you are enrolled." That contradiction
  either frightens ("did my enrollment fall through?") or teaches the family the page
  cannot be trusted. Finding 1.
- The lead sentence has the same staleness: *"Your physician is preparing a request…"* is
  wrong at released (the drafting is done and shared) and at enrolled. Finding 2.
- **Voluntariness is never conveyed.** *"you will be asked for your written permission"*
  says a signature event will occur; it never says the patient may refuse. For a document
  family that reads consent as a formality, one clause fixes this. Finding 3.
- At the enrolled stage, informed consent vanishes from the page entirely — the remaining
  list becomes reporting duties. OSSICRO cannot verify consent happened (HC1: it never
  obtains it), so a patient enrolled-in-the-record but not yet consented loses the only
  sentence telling them their permission is still required and still theirs to give.
  Finding 5.
- The API sends `"draft": True` unconditionally, even when enrolled — a falsehood-in-data
  waiting for the first consumer to render it as a badge. Finding 4.
- The physician is told the link is *"private; treat it like a password"* — the patient is
  told nothing. A patient who posts the link in a support-group forum has published their
  drug name (often tantamount to their diagnosis) to anyone who clicks. Finding 6.
- Register wobbles between "your physician" (client strings) and "your doctor" (server
  strings), sometimes in adjacent sentences. "Doctor" is the plainer word. Finding 7.
- Minor redundancy at the draft stage: the lead, the notice, and the status box all say a
  request "is being prepared" — three near-identical sentences in the first screenful.
  Finding 2's rewrite removes one of them; acceptable after that (repetition aids
  comprehension here more than it annoys).
- Deliberate trade-off, judged acceptable: showing the **drug name** is the one clinically
  loaded fact on the page. It is also the single thing the patient most wants to see, they
  already hold it, and the physician-side caption ("shows no clinical detail the patient
  does not already have") makes the trade explicit. Keep it — but pair it with the
  link-privacy line (Finding 6).

---

## 3. FINDINGS

1. **[SMALL-FIX] — severity if unfixed: BLOCKER.** Hardcoded "Still in draft." shown at the
   enrolled stage, contradicting the server's stage-correct notice on the same screen.
   `app/static/index.html:3218` — current:
   ```
   <div class="ptnotice"><b>${esc(T.draftBarLead)}</b> ${esc(asText(d.notice || d.draft_notice) || T.draftNotice)}</div>
   ```
   replacement (suppress the draft lead once the request is no longer a draft — the same
   stage test MAJOR-2 applied server-side):
   ```
   <div class="ptnotice">${String(d.stage).toLowerCase() === "enrolled" ? "" : `<b>${esc(T.draftBarLead)}</b> `}${esc(asText(d.notice || d.draft_notice) || T.draftNotice)}</div>
   ```

2. **[SMALL-FIX]** Lead sentence claims the request "is being prepared" at every stage —
   stale at released, false at enrolled. `app/static/index.html:1068` — current:
   ```
   lead1: "Your physician is preparing a request to the FDA that would allow you to be treated with",
   ```
   replacement (tense-neutral, true at all four stages, and removes one of the three
   "preparing" repetitions at the draft stage):
   ```
   lead1: "This page follows your physician's request to the FDA for permission to treat you with",
   ```
   (Reads: "This page follows your physician's request to the FDA for permission to treat
   you with **[drug]** under the FDA's "expanded access" program." — `lead2` unchanged.)

3. **[SMALL-FIX]** Voluntariness of consent is never stated (21 CFR 50.20 substance:
   consent is a choice, not a step). `app/server.py` — the identical bullet appears in
   `patient_remaining_draft` (:243), `patient_remaining_committed` (:253), and
   `patient_remaining_released` (:265). Current (all three occurrences):
   ```
        "Before any treatment, you will be asked for your written "
        "permission (informed consent).",
   ```
   replacement (replace all three):
   ```
        "Before any treatment, you will be asked for your written "
        "permission (informed consent). Saying yes or no is always "
        "your choice.",
   ```

4. **[SMALL-FIX]** `_patient_view` hardcodes `"draft": True` even when enrolled — a false
   field any future consumer will faithfully render. `app/server.py:1180` — current:
   ```
        "draft": True,
   ```
   replacement:
   ```
        "draft": stage != "enrolled",
   ```

5. **[LARGER-ISSUE — MAJOR]** At the enrolled stage every mention of informed consent
   disappears from the patient page. Enrollment can be recorded under three legal bases
   (`promote`), and OSSICRO by design cannot verify that Part-50 consent has been signed
   (HC1). A patient whose enrollment is recorded before they sign — a real sequence on the
   waiver/treatment-disclosure paths — now reads a page that says they are enrolled and
   lists only the doctor's reporting duties, with no remaining trace that their written
   permission is still required and still refusable. Why it matters: this is the exact
   population Part 50 protects, at the exact moment the protection binds. Direction: add a
   consent-status-agnostic bullet to `patient_remaining_enrolled` (server.py:272), e.g.
   *"If you have not already signed the written permission (informed consent), you will be
   asked before treatment starts — and it is still your choice."* The conditional phrasing
   stays honest whether or not consent has occurred, without OSSICRO claiming to know.

6. **[SMALL-FIX]** The patient is never told the link itself is sensitive (the physician
   is: "treat it like a password", index.html:1048). `app/static/index.html` — two edits.
   In `patientView` (after `refCodeNote`, :1077), current:
   ```
   refCodeNote: "— this page never shows your name, your medical record, or any test result.",
   ```
   replacement:
   ```
   refCodeNote: "— this page never shows your name, your medical record, or any test result.",
   linkPrivacyNote: "This link is for you. Anyone who has it can open this page, so share it only with people you trust.",
   ```
   And in `renderPatientView` (:3224), current:
   ```
        <p>${esc(T.readOnlyNote)}</p>
   ```
   replacement:
   ```
        <p>${esc(T.readOnlyNote)}</p>
        <p>${esc(T.linkPrivacyNote)}</p>
   ```

7. **[LARGER-ISSUE — MINOR]** Register split: client strings say "your physician" /
   "your physician's office" (title, leads, footer) while every server string says "your
   doctor" — the two alternate within one screen. "Doctor" is the plainer, warmer word and
   the server strings are the tested-canonical ones. Direction: converge the patientView
   client strings on "doctor" ("An update from your doctor's office", "ask your doctor's
   office to share it again", etc.) in the Wave-5 jargon pass; do not touch the
   physician-workspace strings, where "physician" is the correct register.

8. **[SMALL-FIX]** Dead string that re-arms a fixed bug: `patientView.draftBar` is rendered
   nowhere (only `draftBarLead` is used), and its text — "Nothing has been sent to the FDA
   yet…" — is exactly the unconditional claim MAJOR-2 removed. If a future dev "wires it
   back," the enrolled-stage falsehood returns. `app/static/index.html:1064` — current:
   ```
   draftBar: "Nothing has been sent to the FDA yet. Everything shown here is still being " +
     "prepared by your physician's office.",
   ```
   replacement: delete both lines (no reference exists; `draftNotice` at :1072 remains the
   render fallback).

---

**Bottom line for this persona.** The patient surface is, sentence for sentence, the most
humane part of OSSICRO: honestly staged, genuinely plain, structurally incapable of asking
the patient for anything, and explicit that nothing is promised. Its one real defect is
that the draft-honesty machinery was fixed in two places and missed in a third, so the page
tells an enrolled patient — the person with the most at stake — something false in bold.
That, the missing "it is your choice," and the enrolled-stage consent gap are the three
changes that matter; everything else is polish.
