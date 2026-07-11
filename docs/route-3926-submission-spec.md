# Route-3926 Submission Spec — Single-Patient Expanded Access

**Version 1.1 — 2026-07-11** (Overhaul P8: 3926 item-number references reconciled to the single item map `FORM_3926_ITEMS` in `engine/ossicro/pdf_3926.py`; numbering PENDING-HUMAN-VERIFICATION — see §1.1). Originally version 1.0 — 2026-07-09. Governing spec for the OSSICRO MVP. This document defines *what the FDA reviewer receives* and *what the manufacturer acts on* for a single-patient, individual-patient expanded-access request under 21 CFR 312.310, submitted via **Form FDA 3926**. It governs both the backend (engine intake → generate → check → gates → assembly) and the frontend (physician intake, package review, gate routing).

Status labels follow the Constitution (CP4): **Confirmed** = black-letter regulation or published FDA form/guidance; **Interpretive** = OSSICRO's structural design choice not directly dictated by a citation. Every field, document, and clock below carries its citation. Nothing here authorizes OSSICRO to perform a reserved act — the eight code-enforced gates (`engine/registry/gates.json`) and the four external-party decisions (physician treatment call, manufacturer supply, FDA authorization, IRB concurrence) are named at each node and fail closed via `GateViolation`.

Source basis (no new research; derived from the built corpus):
- `wiki/02-lifecycle/expanded-access-workflow.md`
- `wiki/03-documents/form-fda-3926-expanded-access.md`
- `wiki/04-coordination/single-patient-site-and-pharma-acceptance.md`
- `wiki/04-coordination/expanded-access-coordination.md`
- `wiki/02-lifecycle/safety-reporting-lifecycle.md`
- `engine/registry/documents.json` (expanded-access category), `gates.json`, `models.py`

---

## 0. Scope and the hard line

Route-3926 is **treatment, not research** (21 CFR 312.305(a)): the purpose is to treat one named patient with a serious or immediately life-threatening disease for which there is no comparable or satisfactory alternative therapy — not to generate generalizable data. No efficacy endpoint, no randomization. Authorization requires **four independent parties to concur**, and OSSICRO owns none of the four decisions:

| Node | Decision it owns | OSSICRO role | Citation |
|---|---|---|---|
| Treating physician (becomes sponsor-investigator) | Probable risk from drug ≤ probable risk from disease; submits; consents | Drafts package; never decides, signs, or consents | 21 CFR 312.310(a) |
| Manufacturer (IND/DMF holder) | Whether to supply + grant LOA | Drafts the LOA-request; records the returned LOA; never supplies/signs | FDCA §561A |
| FDA (review division) | Criteria met; allow-to-proceed or clinical hold | Assembles + validates; never files | 21 CFR 312.305/.310/.42 |
| IRB | Approval, or emergency post-hoc notification | Assembles submission or §56.105 concurrence request; never approves | 21 CFR Part 56 |

**Confirmed.** The four-party concurrence and the non-delegable acts are black-letter; OSSICRO's automation boundary is the Constitution's HC1.

---

## 1. What the FDA receives — document set, assembly order, eCTD module map

### 1.1 The package (individual-patient EA)

The complete Route-3926 submission the FDA reviewer receives, in **assembly order**:

| # | Component | Registry id | Owner | Gate | Citation |
|---|---|---|---|---|---|
| 1 | **Cover letter** | `ind-application-cover-and-toc` (EA-profiled) | sponsor-investigator | `submission-to-fda` | 21 CFR 312.23(a)(1) |
| 2 | **Form FDA 3926** (the application; substitutes for Form 1571) | `form-fda-3926-individual-patient-expanded-access` | investigator | `submission-to-fda` | 21 CFR 312.310; Form 3926 (OMB 0910-0814) |
| 3 | **Clinical history + rationale** (narrative that the §312.305(a) / §312.310(a) criteria are met) | (part of 3926 Item 3 / attachment) | investigator | — | 21 CFR 312.305(a), 312.310(a) |
| 4 | **Expanded-access treatment plan** (dose, route, planned duration, treatment + monitoring plan) | `expanded-access-treatment-plan` | investigator | — | 21 CFR 312.305(b) |
| 5 | **Manufacturer Letter of Authorization (LOA)** — cross-references manufacturer IND/DMF | `manufacturer-letter-of-authorization` | sponsor (manufacturer) | — (external-party act) | 21 CFR 312.305(b)(1), 312.23(b); FDCA §561A |
| 6 | **Physician qualification statement** (§312.310(a) determination + credentials) | (3926 Item 6 / attachment) | investigator | — | 21 CFR 312.310(a) |
| 7 | **IRB of record** identification + concurrence evidence (or §56.105 chair-concurrence request) | `irb-submission-cover-and-checklist` (EA-profiled) | investigator/IRB | `irb-approval` (external) | 21 CFR 56.104(c), 56.105 |
| 8 | **Informed consent form** (drafted; the consent *event* is non-delegable) | `informed-consent-form-part50` | investigator | `informed-consent` | 21 CFR 50.25, 50.27 |

**Interpretive** as to bundling order; **Confirmed** as to which artifacts are required. Items 3 and 6 are captured *inside* Form 3926 or as short attachments to it — the 3926 is deliberately a single streamlined instrument (`form-fda-3926-expanded-access.md`).

> **PENDING-HUMAN-VERIFICATION — Form 3926 item numbering (Overhaul P8).** Every 3926
> item-number reference in this spec follows the single item map `FORM_3926_ITEMS` in
> `engine/ossicro/pdf_3926.py` — the one source the text template, the PDF layout, and the
> FDF field map all derive from. Best-known reconciled map: 1 date of submission; 2 nature of
> submission; 3 patient's clinical information (diagnosis, history, prior therapies, and the
> rationale — this spec previously said Field 9); 4 treatment information; 5 LOA;
> 6 physician qualification statement; 7 physician (requestor) information; 8 IRB;
> 9 **UNRESOLVED** (not enumerated by the local instructions/guidance PDF); 10 waivers
> 10.a/10.b (numbering + semantics confirmed against the local guidance PDF); 11 physician
> signature and date. The numbering is final only when a qualified human opens the official
> fillable form (OMB 0910-0814), verifies the map and the ~28 AcroForm names, and initials
> `FORM_3926_MAP_VERIFIED_BY` in `pdf_3926.py`; until then every rendered 3926 surface
> carries the pending marker.

### 1.2 New individual-patient IND vs. existing IND

Two submission targets — the intake field `submission.target` selects:

- **New individual-patient IND** (the default MVP path): Form 3926 is checked as an **initial written request**; FDA assigns a new IND number. The 3926's Fields 10.a/10.b waivers apply (§1.4 below). The package is the standalone set in §1.1.
- **Existing IND** (physician already holds an IND, or is adding this patient under an IND they hold): Form 3926 is a **follow-up** submission carrying the existing **IND number**; the package is filed as a serial amendment to that IND (information/protocol amendment, `21 CFR 312.31 / 312.30`). The LOA is unchanged if the manufacturer's cross-reference is already on file.

**Confirmed** (Field 2 initial-vs-follow-up + IND number: `form-fda-3926-expanded-access.md`).

### 1.3 eCTD module map

**Confirmed caveat first:** eCTD is **not mandatory** for an individual-patient 3926. FDA accepts single-patient expanded-access requests on paper or by fax/email to the review division per the Form 3926 guidance; the streamlined form exists precisely so a clinician with no regulatory operations can file. OSSICRO's default output is therefore a **paper/PDF assembled package** in §1.1 order. The eCTD map below is **Interpretive** structural guidance for the case where the physician (or the manufacturer's regulatory group) elects electronic submission, or where the request is a serial amendment to an **existing eCTD IND**.

| eCTD Module | Section | Route-3926 content |
|---|---|---|
| **Module 1** — Regional (US) administrative | 1.2 Cover letters | Cover letter (§2) |
| | 1.2 Application form | **Form FDA 3926** (in lieu of Form 1571); Form 1571 itself is *waived* by Field 10.a via §312.10 |
| | 1.3 Administrative information | Physician/sponsor-investigator contact; IRB of record |
| | 1.4 References | **Letter of Authorization** (cross-reference to manufacturer IND/DMF) |
| | 1.11 / regional | Physician qualification statement; §312.310(a) determination |
| **Module 2** — Summaries | — | Not required for single-patient EA (no CTD summaries) |
| **Module 3** — Quality (CMC) | 3.2 | **Cross-referenced** from the manufacturer's IND/DMF via the LOA — the physician does not author CMC |
| **Module 4** — Nonclinical | 4.2 | **Cross-referenced** from the manufacturer's IND via the LOA |
| **Module 5** — Clinical | 5.3.5 / treatment protocol | **Expanded-access treatment plan / protocol** (dose, route, duration, monitoring); clinical history + rationale |
| | IB reference | **Investigator's Brochure referenced**, not authored — supplied by / cross-referenced from the manufacturer (`investigators-brochure`, owner = sponsor) |

Key structural facts: (a) the **treatment plan lives in Module 5**; (b) **Module 1 carries the 3926, the cover letter, and the LOA**; (c) **CMC/nonclinical and the IB are cross-references to the manufacturer's IND**, never physician-authored content — this is the whole function of the LOA (§4).

---

## 2. The cover letter

Contents (drafted by OSSICRO, signed and filed by the physician — `submission-to-fda` gate):

1. **Addressee** — the specific FDA review division (by therapeutic area) that holds the manufacturer's IND, or CDER/CBER central receipt if unknown.
2. **Subject line** — "Individual Patient Expanded Access IND — [coded patient identifier] — [drug name]"; state **emergency** vs **non-emergency** explicitly, and **initial** vs **follow-up** (with IND number if follow-up).
3. **Statement of request** — a licensed physician requests authorization under 21 CFR 312.310 to treat one named patient with a serious/immediately life-threatening condition and no satisfactory alternative therapy.
4. **The §312.305(a) criteria, addressed in one line each** — serious/life-threatening + no alternative; benefit justifies risk; use will not interfere with clinical investigations.
5. **The §312.310(a) determination** — the physician has determined probable risk from the drug is not greater than probable risk from the disease.
6. **LOA cross-reference** — identifies the manufacturer, the referenced IND/DMF number, and that the manufacturer has authorized cross-reference (or, if no IND exists, that the physician has contacted the division to determine required supporting information — §312.305(b)(1)).
7. **Enclosures list** — the §1.1 package in order.
8. **For emergency requests** — the date/time and name of the FDA official who granted telephone authorization, and an explicit acknowledgment that this written submission is filed **within 15 working days** of that authorization (§312.310(d), §3).
9. **Contact block** — physician name, phone, email; IRB of record.

**Confirmed** as to content elements; **Interpretive** as to ordering. No EIN or account numbers ever appear (Constitution HC2 / privacy).

---

## 3. Emergency vs non-emergency pathway and the exact clocks

The intake field `submission.emergency` (boolean) selects the pathway. OSSICRO **computes** every clock deterministically (Constitution HC3 — clocks are computed, never judged); the human causality/authorization *triggers* belong to the humans (HC1).

### 3.1 Non-emergency

1. Physician determines treatment appropriate (§312.310(a)) — **human gate**.
2. Physician obtains manufacturer LOA (§4) — **external party**.
3. Physician submits Form 3926 package to FDA — `submission-to-fda` gate.
4. FDA assigns an IND number and either allows the use to proceed or imposes a **clinical hold** (§312.42).
5. **IND effective clock:** the IND goes into effect **when FDA notifies the physician it may proceed, or — absent notification — 30 calendar days after FDA receives the completed 3926** (§312.40(b)(1); Constitution HC3).
6. **Informed consent** obtained **before treatment begins** (Part 50) — `informed-consent` gate.
7. **IRB approval before treatment** (Part 56), or §56.105 chair-concurrence (§5).

### 3.2 Emergency (§312.310(d))

Where the patient must be treated before a written submission can be made:

1. Physician makes a **telephone (or other rapid-means) request** to the FDA review division, explaining how the use meets §§312.305 and 312.310.
2. **FDA may authorize the use by telephone.** Shipment/use may begin on that authorization.
3. **CLOCK — 15 WORKING DAYS:** the physician **must submit the written expanded-access application (Form 3926) within 15 working days of the FDA authorization** (§312.310(d)). OSSICRO computes this deadline from the authorization date/time entered by the physician and escalates as it approaches; it never files.
4. **Informed consent** is still required **before treatment**, including in emergencies, unless a Part 50 exception applies.
5. **CLOCK — 5 WORKING DAYS (IRB):** for emergency use, treatment may proceed before IRB review provided the **IRB is notified within 5 working days of the treatment** (§56.104(c)). OSSICRO computes this deadline from the treatment date and escalates.

### 3.3 The clock table (both pathways)

| Clock | Trigger (human-entered) | Deadline | Basis | Owner of the trigger |
|---|---|---|---|---|
| Written 3926 after emergency phone authorization | FDA telephone authorization | **15 working days** | 21 CFR 312.310(d) | Physician |
| IRB notification after emergency treatment | First treatment administered | **5 working days** | 21 CFR 56.104(c) | Physician |
| IND effective (non-emergency) | FDA receipt of complete 3926 | FDA notice, else **30 calendar days** | 21 CFR 312.40(b)(1) | FDA |
| Post-authorization: IND safety report (7/15-day) | Physician's causality/expectedness determination | see §7 | 21 CFR 312.32(c) | Physician / medical monitor |

**Working days** (business days, excluding weekends/federal holidays) for the emergency 3926 and IRB clocks; **calendar days** for the 30-day IND wait and the safety clocks. The backend clock engine must implement two distinct day-count calendars. **Confirmed.**

---

## 4. Manufacturer requirements

Nothing moves without the manufacturer's affirmative decision to supply — an act OSSICRO cannot make or compel (FDCA §561A; Constitution HC1).

### 4.1 The Letter of Authorization (LOA)

The pivot of the whole coordination. Registry id `manufacturer-letter-of-authorization`; owner = **sponsor (manufacturer)**; receiver = **FDA**.

- **Function:** permits FDA to **cross-reference the manufacturer's existing IND (or DMF)** — its CMC, nonclinical, and safety data — so the physician need not author Modules 3/4 or the IB (§312.305(b)(1), §312.23(b)).
- **Required content** (`documents.json` required_fields): `manufacturer_name`, `drug_master_file_reference` (the IND/DMF number being cross-referenced), `authorized_party` (the physician/patient the authorization covers).
- **No LOA possible** (supplier has no IND on file): the physician contacts the FDA review division to determine what supporting information FDA needs to evaluate the request directly. This branch is captured by intake field `manufacturer.ind_on_file = false`, which routes the validate pass to require a **documented FDA-division contact** in lieu of an LOA reference.
- **The manufacturer signs the LOA; OSSICRO records it.** OSSICRO drafts the *request* to the manufacturer and the LOA-acceptance record; the manufacturer's signature is theirs alone.

### 4.2 The LOA-request the physician sends to the manufacturer

OSSICRO drafts (physician sends — never auto-sent, Constitution HC1) a request to the manufacturer's expanded-access / Medical Affairs intake containing:

1. Physician + patient (coded) identification and the serious/life-threatening indication.
2. The specific investigational product, and the request to **supply the drug** for single-patient treatment use.
3. The request to **issue an LOA cross-referencing the manufacturer's IND/DMF** to FDA.
4. The treatment plan summary (dose, route, duration) so the manufacturer can assess supply quantity.
5. A statement that FDA authorization of expanded access does **not** obligate supply, and that the decision, LOA signature, and any FMV/anti-kickback judgment (42 U.S.C. §1320a-7b) are the manufacturer's (FDCA §561A) — set expectations honestly (CP4).

### 4.3 Drug-supply commitment

The manufacturer's supply decision is a counterparty business/medical judgment. Route 1 (individual-patient EA) is the route manufacturers most commonly grant because their role is bounded (**supplier, not sponsor**) and most operate a §561A-published expanded-access intake. OSSICRO records the returned supply commitment + LOA as facts; it never assumes them. **Confirmed** (obligation) / **Interpretive** (route-likelihood).

### 4.4 What OSSICRO does NOT require of the manufacturer for Route 1

Individual-patient expanded access runs on ordinary medical-records practice. **No CTA, no full site-activation binder, no Part 11 validation evidence** is demanded of the physician or manufacturer for Route 1 (`single-patient-site-and-pharma-acceptance.md`). OSSICRO's Part 11 tooling is a convenience here, not a gate item.

---

## 5. IRB concurrence for individual-patient EA

**Confirmed.** IRB review is required and is **not waived** for expanded-access treatment use (Part 56).

- **Standard (non-emergency):** IRB approval **before treatment begins** (`irb-approval` external gate).
- **§56.105 waiver (Form 3926 Field 10.b):** for single-patient use, FDA may accept **concurrence of the IRB chairperson (or a designated IRB member)** in lieu of a convened full-board meeting. Checking and signing Field 10.b requests this §56.105 waiver of the §56.108(c) convened-IRB requirement. OSSICRO drafts the chair-concurrence request; the concurrence judgment is the IRB's.
- **Emergency use (§56.104(c)):** treatment may proceed before IRB review provided the **IRB is notified within 5 working days** (the §3.2 clock).

OSSICRO assembles the IRB submission package and surfaces IRB concurrence (or the 5-working-day emergency notification) as a **blocking gate**; it never renders or records an approval on the IRB's behalf (`gates.json` → `irb-approval`).

---

## 6. Form FDA 3926 waiver checkboxes (regulatory weight)

Two checkboxes carry legal effect and must be surfaced as explicit physician decisions in intake (`form-fda-3926-expanded-access.md`):

| Field | Effect when checked + signed | Authority |
|---|---|---|
| **10.a** | FDA treats the 3926 as a **§312.10 waiver request** of the additional Part 312 IND-submission requirements otherwise met via Forms **1571 and 1572** (their identity/qualification content is unnecessary for a single-patient use) | 21 CFR 312.10 |
| **10.b** | FDA treats the 3926 as a **§56.105 waiver request** of the §56.108(c) convened-IRB requirement, appropriate when the physician obtains IRB-chair (or designated member) concurrence before treatment | 21 CFR 56.105, 56.108(c) |

These are physician attestations captured by intake booleans `waiver_10a` / `waiver_10b`, signed by the physician — never defaulted or auto-checked by OSSICRO.

---

## 7. Post-authorization safety clocks (attach once treatment begins)

Once authorized and the drug supplied, the physician carries sponsor-investigator IND safety-reporting duties (§312.32). OSSICRO drafts the narrative + Form 3500A and **computes** the deadline; the seriousness/causality/expectedness determinations that *arm* each clock are non-delegable medical judgment (`gates.json` → `sae-causality`; Constitution HC1/HC3).

| Trigger | Clock start (human-entered determination) | Deadline | Recipient | Basis |
|---|---|---|---|---|
| Serious + unexpected + suspected adverse reaction | Physician determines it qualifies | **15 calendar days** | FDA + participating investigators | 21 CFR 312.32(c)(1) |
| Unexpected **fatal / life-threatening** suspected AR | Physician's initial receipt of info | **7 calendar days** (complete report within 15) | FDA | 21 CFR 312.32(c)(2) |
| AE later determined reportable | Reportability determination made | **15 calendar days** after determination | FDA + investigators | 21 CFR 312.32(d)(3) |

OSSICRO never starts a safety clock on its own inference and never files. **Confirmed.**

---

## 8. The physician intake field set

The minimum structured intake a physician provides. Each field maps to its citation and the document(s) it feeds. Backend: these populate the `Study.raw` dict (`models.py`); every generated span traces to a dotted path here and carries a `ProvenanceRecord` (Constitution HC4). Empty attestation = honestly unattested, never fabricated (`StudyFact`).

### 8.1 Patient (coded — no PII externalized)

| Field | Dotted path | Feeds | Citation |
|---|---|---|---|
| Coded patient identifier / initials | `patient.coded_id` | 3926, cover letter, consent | 21 CFR 312.310 |
| Age / sex (as clinically needed) | `patient.age`, `patient.sex` | 3926 clinical info, treatment plan | 21 CFR 312.305(a) |
| Diagnosis (serious / immediately life-threatening) | `patient.diagnosis` | 3926, cover letter, criteria narrative | 21 CFR 312.305(a)(1) |
| No comparable/satisfactory alternative — basis | `patient.no_alternative_basis` | Cover letter, 3926 rationale | 21 CFR 312.305(a)(1) |
| Prior therapies tried/failed | `patient.prior_therapies` | Clinical history, rationale | 21 CFR 312.310(a) |

### 8.2 Physician (becomes sponsor-investigator)

| Field | Dotted path | Feeds | Citation |
|---|---|---|---|
| Name, degrees | `investigator.name`, `investigator.degrees` | 3926 Field 6, cover letter, qualification stmt | 21 CFR 312.310(a) |
| Address, phone, email | `investigator.address`, `.phone`, `.email` | 3926 contact, cover letter | Form 3926 |
| Medical license number + state | `investigator.license_number`, `.license_state` | Physician qualification statement | 21 CFR 312.310(a) |
| §312.310(a) determination (risk drug ≤ risk disease) | `investigator.risk_determination` | 3926, cover letter (physician attestation) | 21 CFR 312.310(a) |

### 8.3 Drug + treatment plan

| Field | Dotted path | Feeds | Citation |
|---|---|---|---|
| Investigational drug name | `drug.name` | 3926, LOA request, treatment plan | 21 CFR 312.305(b) |
| Dose, route | `drug.dose`, `drug.route` | Treatment plan, 3926 treatment info | 21 CFR 312.305(b) |
| Planned duration | `drug.duration` | Treatment plan | 21 CFR 312.305(b) |
| Treatment + monitoring plan | `treatment.monitoring_plan` | `expanded-access-treatment-plan` | 21 CFR 312.305(b) |
| Benefit-justifies-risk rationale | `treatment.benefit_risk` | Cover letter, 3926 rationale | 21 CFR 312.305(a)(2) |
| Non-interference-with-investigations basis | `treatment.non_interference` | Cover letter, 3926 | 21 CFR 312.305(a)(3) |

### 8.4 Manufacturer

| Field | Dotted path | Feeds | Citation |
|---|---|---|---|
| Manufacturer name | `manufacturer.name` | LOA request, LOA record, cover letter | FDCA §561A |
| IND/DMF number to cross-reference | `manufacturer.ind_dmf_reference` | LOA, 3926 LOA reference, Module 1.4 | 21 CFR 312.305(b)(1), 312.23(b) |
| IND on file? (else FDA-division-contact branch) | `manufacturer.ind_on_file` | Validate-pass routing | 21 CFR 312.305(b)(1) |
| Supply commitment received? | `manufacturer.supply_committed` | Package readiness | FDCA §561A |

### 8.5 IRB

| Field | Dotted path | Feeds | Citation |
|---|---|---|---|
| IRB of record name + address | `irb.name`, `irb.address` | 3926 Field 8, IRB submission, consent | 21 CFR 56.104/.105 |
| §56.105 chair-concurrence pathway elected? | `irb.chair_concurrence` | Field 10.b, IRB request | 21 CFR 56.105 |

### 8.6 Submission control

| Field | Dotted path | Feeds | Citation |
|---|---|---|---|
| Emergency? | `submission.emergency` | Pathway select, clock engine | 21 CFR 312.310(d) |
| FDA telephone-authorization date/time (emergency) | `submission.emergency_auth_datetime` | 15-working-day clock | 21 CFR 312.310(d) |
| First-treatment date (emergency) | `submission.first_treatment_date` | 5-working-day IRB clock | 21 CFR 56.104(c) |
| Initial or follow-up | `submission.initial_or_followup` | 3926 Field 2, target routing | Form 3926 |
| Target: new IND vs existing IND (+ number) | `submission.target`, `submission.ind_number` | 3926, amendment routing | 21 CFR 312.31 |
| FDA review division | `submission.fda_division` | Cover letter addressee | 21 CFR 312.310(d) |
| Waiver 10.a (§312.10) | `waiver_10a` | Form 3926 Field 10.a | 21 CFR 312.10 |
| Waiver 10.b (§56.105) | `waiver_10b` | Form 3926 Field 10.b | 21 CFR 56.105 |

**Confirmed** as to which facts each document requires (from `documents.json` required_fields + the wiki); **Interpretive** as to the dotted-path naming (the engine's `Study.resolve` contract).

---

## 9. Gate map (what the build enforces)

The Route-3926 package touches these code-enforced gates (`engine/registry/gates.json`); each fails closed via `GateViolation` and blocks a document from reaching `final` without a recorded `HumanSignoff`:

| Gate id | Applies to | Responsible role | Citation |
|---|---|---|---|
| `submission-to-fda` | Cover letter, Form 3926, treatment plan | sponsor-investigator | 21 CFR 312.20/.23/.40 |
| `informed-consent` | Informed consent form | investigator | 21 CFR 50.20/.25/.27 |
| `irb-approval` | IRB submission / concurrence | irb (external) | 21 CFR 56.108-56.111; 312.66 |
| `sae-causality` | Post-authorization safety reports | medical-monitor / physician | 21 CFR 312.32; ICH E2A |

External-party acts with no code gate but which OSSICRO only *records*, never performs: **manufacturer supply + LOA signature** (FDCA §561A), **FDA authorization** (§312.42), **IRB concurrence deliberation** (Part 56). The completeness ledger marks a document present-but-gate-pending as **amber**; missing/invalid as **red** (`models.py` `LedgerItem`). A clean concept review never promotes amber→green (`pipeline.py` escalate-only).

---

## 10. Build acceptance (success criteria)

The MVP is done for Route-3926 when:

1. Intake collects the §8 field set with provenance and honest unattested marking.
2. Generate produces the §1.1 package (cover letter, Form 3926 incl. Fields 10.a/10.b, treatment plan, LOA request) with every span carrying a `ProvenanceRecord` and citation (HC2/HC4).
3. Check validates that each §312.305(a) and §312.310(a) criterion is addressed, that an LOA reference **or** a documented FDA-division contact is present, and that consent-before-treatment and IRB (or 5-working-day emergency notification) are surfaced as blocking gates.
4. The clock engine computes the 15-working-day, 5-working-day, and 30-calendar-day clocks (and the 7/15-calendar-day post-authorization safety clocks) deterministically, with working-day vs calendar-day calendars distinguished.
5. No document reaches `final` without the recorded human sign-off for its gate — the `GateViolation` path is exercised and passes.
6. The FDA-reviewer view (assembled package + eCTD module map) and the manufacturer view (LOA request + supply record) are both rendered — the reviewer receives a package, the manufacturer acts on a request.
