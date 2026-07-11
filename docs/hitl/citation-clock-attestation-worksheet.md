# OSSICRO — Citation & Statutory-Clock Attestation Worksheet

**Generated:** 2026-07-15 (regenerate with `python tools/attestation_worksheet.py`).  
**Purpose (HITL-2).** Before any real use, a qualified human verifies every regulatory citation and every statutory clock the engine emits, against the **primary source** (eCFR / U.S.C.). This is the single highest-risk pass in the system: a wrong citation or an off-by-one deadline can delay a patient's access or get a submission rejected. AI review is **not** a substitute for a named qualified human's sign-off here.

**How to use.** For each row: open the primary source, confirm the citation says what the *Asserts / used-for* column claims, mark ✅ or ✍️ (needs change), and initial + date. For clocks, also confirm the day-count, the working-vs-calendar basis, and the trigger against the regulation, then check the computed example by hand. Record any correction in *Notes*; corrections become code changes tracked separately.

**Attester (fill in):** name ______________________  role ______________________  date __________  signature ______________________

> This attestation certifies citation/clock correctness only. It is **not** an IRB > approval, informed consent, sponsor signature, or FDA submission — those remain > non-delegable human acts performed elsewhere (Constitution HC1).

## 1. Statutory clocks (3)

| ✔ | Clock | Route | Rule | Trigger field | Citation (primary source) | Computed example | Correct? | Init/Date | Notes |
|---|-------|-------|------|---------------|---------------------------|------------------|----------|-----------|-------|
| ☐ | IND effective (non-emergency) | `route-3926` | 30 CALENDAR days after the trigger | `submission.fda_receipt_date` | 21 CFR 312.40(b)(1) | trigger 2026-07-15 → due 2026-08-14 | ☐ | | |
| ☐ | Written 3926 after emergency phone authorization | `route-3926-emergency` | 15 WORKING days after the trigger (weekends + observed federal holidays skipped) | `submission.emergency_auth_datetime` | 21 CFR 312.310(d)(2) | trigger 2026-07-15 → due 2026-08-05 | ☐ | | |
| ☐ | IRB notification after emergency treatment | `route-3926-emergency` | 5 WORKING days after the trigger (weekends + observed federal holidays skipped) | `submission.first_treatment_date` | 21 CFR 56.104(c) | trigger 2026-07-15 → due 2026-07-22 | ☐ | | |

_Federal-holiday basis for working-day clocks: 5 U.S.C. 6103 with the OPM weekend-observance rule (Saturday→Friday, Sunday→Monday). Verify the holiday table in `engine/ossicro/clocks.py::federal_holidays` against OPM for the relevant year._

## 2. Citations (53 distinct)

| ✔ | Citation | Asserts / used-for | Where used | Correct? | Init/Date | Notes |
|---|----------|--------------------|------------|----------|-----------|-------|
| ☐ | 21 CFR 312.10 | Waiver 10.a (§312.10 — waive 1571/1572 requirements) | field:waiver_10a | ☐ | | |
| ☐ | 21 CFR 312.20, 312.23, 312.40; FD&C Act 505(i) | submission-to-fda | gate:submission-to-fda | ☐ | | |
| ☐ | 21 CFR 312.23(a)(1); 21 CFR 312.52; Form FDA 1571 | ind-1571-signature | gate:ind-1571-signature | ☐ | | |
| ☐ | 21 CFR 312.23(b) | Manufacturer address; Signed LOA — document SHA-256 (optional) | field:manufacturer.address, field:manufacturer.loa_document_sha256 | ☐ | | |
| ☐ | 21 CFR 312.305(a) | Age; Sex | field:patient.age, field:patient.sex | ☐ | | |
| ☐ | 21 CFR 312.305(a)(1) | Diagnosis (serious / immediately life-threatening); No comparable / satisfactory alternative therapy — basis | field:patient.diagnosis, field:patient.no_alternative_basis | ☐ | | |
| ☐ | 21 CFR 312.305(a)(2) | Benefit-justifies-risk rationale | field:treatment.benefit_risk | ☐ | | |
| ☐ | 21 CFR 312.305(a)(3) | Non-interference-with-investigations basis | field:treatment.non_interference | ☐ | | |
| ☐ | 21 CFR 312.305(a); 312.310(a) | Clinical rationale (the §312.305(a) core narrative) | field:request.clinical_rationale | ☐ | | |
| ☐ | 21 CFR 312.305(b) | Investigational drug name | field:drug.name | ☐ | | |
| ☐ | 21 CFR 312.305(b)(1) | FDA-division contact (if no IND on file); Manufacturer has an IND on file? | field:manufacturer.fda_division_contact, field:manufacturer.ind_on_file | ☐ | | |
| ☐ | 21 CFR 312.305(b)(1), 312.23(b) | IND / DMF number to cross-reference | field:manufacturer.ind_dmf_reference | ☐ | | |
| ☐ | 21 CFR 312.305(b)(2)(iv) | Dose; Planned duration of treatment; Route of administration | field:drug.dose, field:drug.duration, field:drug.route | ☐ | | |
| ☐ | 21 CFR 312.305(b)(2)(v) | Treatment facility / site name | field:site.name | ☐ | | |
| ☐ | 21 CFR 312.305(b)(2)(viii) | Treatment + monitoring plan | field:treatment.monitoring_plan | ☐ | | |
| ☐ | 21 CFR 312.305; 312.310 | FDA authorization (allow-to-proceed) date | field:submission.fda_authorization_date | ☐ | | |
| ☐ | 21 CFR 312.31 | Target: new IND vs existing IND | field:submission.target | ☐ | | |
| ☐ | 21 CFR 312.310 | Coded patient identifier (study-assigned code preferred) | field:patient.coded_id | ☐ | | |
| ☐ | 21 CFR 312.310(a) | Degrees; License state; Medical license number; Physician name; Prior therapies tried / failed; §312.310(a) determination (probable risk from drug ≤ probable risk from disease) | field:investigator.degrees, field:investigator.license_number, field:investigator.license_state, field:investigator.name, field:investigator.risk_determination, field:patient.prior_therapies | ☐ | | |
| ☐ | 21 CFR 312.310(c)(2) | Treatment-conclusion date | field:treatment.conclusion_date | ☐ | | |
| ☐ | 21 CFR 312.310(d) | Emergency request?; FDA review division (cover-letter addressee); FDA telephone-authorization date (emergency) | field:submission.emergency, field:submission.emergency_auth_datetime, field:submission.fda_division | ☐ | | |
| ☐ | 21 CFR 312.32(a), 312.32(b), 312.32(c); ICH E2A | sae-causality | gate:sae-causality | ☐ | | |
| ☐ | 21 CFR 312.32(a)-(c); ICH E2A | R-SAE-CAUSALITY | rule:R-SAE-CAUSALITY | ☐ | | |
| ☐ | 21 CFR 312.40(b)(1) | FDA receipt date of the 3926 (non-emergency); R-1571-30DAY | field:submission.fda_receipt_date, rule:R-1571-30DAY | ☐ | | |
| ☐ | 21 CFR 312.53(c)(1)(iv) | R-1572-IRB | rule:R-1572-IRB | ☐ | | |
| ☐ | 21 CFR 312.53(c)(1)(vii) | R-1572-PHASE | rule:R-1572-PHASE | ☐ | | |
| ☐ | 21 CFR 312.53(c)(1); Form FDA 1572 | 1572-signature | gate:1572-signature | ☐ | | |
| ☐ | 21 CFR 312.8 | Cost-recovery / charging statement | field:submission.cost_recovery_statement | ☐ | | |
| ☐ | 21 CFR 50.20, 50.25, 50.27; 21 CFR 312.60 | informed-consent | gate:informed-consent | ☐ | | |
| ☐ | 21 CFR 50.20; 50.23 | Consent timing — physician attestation | field:consent.timing_attestation | ☐ | | |
| ☐ | 21 CFR 50.25(a)(1) | Consent: expected duration of participation; Consent: procedures (experimental identified); Consent: research statement / purpose | field:consent.duration, field:consent.procedures, field:consent.purpose | ☐ | | |
| ☐ | 21 CFR 50.25(a)(1)-(8) | R-ICF-50.25; R-ICF-50.25-ADEQ; R-ICF-50.25-EA | rule:R-ICF-50.25, rule:R-ICF-50.25-ADEQ, rule:R-ICF-50.25-EA | ☐ | | |
| ☐ | 21 CFR 50.25(a)(1)-(8); 21 CFR 50.25(b)(3)-(5) | R-ICF-50.25-ADEQ-EA | rule:R-ICF-50.25-ADEQ-EA | ☐ | | |
| ☐ | 21 CFR 50.25(a)(2) | Consent: reasonably foreseeable risks | field:consent.risks | ☐ | | |
| ☐ | 21 CFR 50.25(a)(3) | Consent: reasonably expected benefits | field:consent.benefits | ☐ | | |
| ☐ | 21 CFR 50.25(a)(4) | Consent: appropriate alternative procedures | field:consent.alternatives | ☐ | | |
| ☐ | 21 CFR 50.25(a)(5) | Consent: confidentiality of records | field:consent.confidentiality_statement | ☐ | | |
| ☐ | 21 CFR 50.25(a)(6) | Consent: compensation / medical treatment if injury occurs; Consent: injury contact name; Consent: injury contact phone | field:consent.injury_compensation_statement, field:contacts.injury_contact_name, field:contacts.injury_contact_phone | ☐ | | |
| ☐ | 21 CFR 50.25(a)(7) | Consent: research contact; IRB phone | field:contacts.research_contact, field:irb.phone | ☐ | | |
| ☐ | 21 CFR 50.25(b)(3); 312.8(d) | Consent: additional costs to the patient | field:consent.cost_statement | ☐ | | |
| ☐ | 21 CFR 54.4; Forms FDA 3454/3455 | financial-disclosure-certification | gate:financial-disclosure-certification | ☐ | | |
| ☐ | 21 CFR 56.104(c) | First-treatment date (emergency) | field:submission.first_treatment_date | ☐ | | |
| ☐ | 21 CFR 56.104/.105 | IRB of record — address; IRB of record — name | field:irb.address, field:irb.name | ☐ | | |
| ☐ | 21 CFR 56.105 | Waiver 10.b (§56.105 — chair concurrence in lieu of convened IRB); §56.105 chair-concurrence pathway elected? | field:irb.chair_concurrence, field:waiver_10b | ☐ | | |
| ☐ | 21 CFR 56.108-56.111; 21 CFR 312.66 | irb-approval | gate:irb-approval | ☐ | | |
| ☐ | FDCA 561A | Drug needed by (clinical urgency date); Manufacturer name; Quantity of drug requested from the manufacturer; Supply commitment received? | field:drug.quantity_requested, field:manufacturer.name, field:manufacturer.supply_committed, field:submission.needed_by_date | ☐ | | |
| ☐ | FDCA 561A; 21 CFR 312.23(b) | Signed LOA received — date; Signed LOA — signatory (name / title) | field:manufacturer.loa_received_date, field:manufacturer.loa_signatory | ☐ | | |
| ☐ | Form FDA 3926 | Address; Email; Existing IND number (if follow-up / existing IND); Initial or follow-up; Phone | field:investigator.address, field:investigator.email, field:investigator.phone, field:submission.ind_number, field:submission.initial_or_followup | ☐ | | |
| ☐ | Form FDA 3926 field 1 | Preparation / planned submission date | field:submission.date | ☐ | | |
| ☐ | ICH E6(R3) 2.7; 21 CFR 312.60 | R-DOA-PI | rule:R-DOA-PI | ☐ | | |
| ☐ | ICH E6(R3) 4 (documentation) | Treatment-plan identifier (for the consent form); Treatment-plan version | field:treatment.plan_id, field:treatment.plan_version | ☐ | | |
| ☐ | ICH E9 / E9(R1); ICH E3 | statistical-signoff | gate:statistical-signoff | ☐ | | |
| ☐ | ICH M11; ICH E6(R3) Appendix B | R-PROT-VERSION | rule:R-PROT-VERSION | ☐ | | |

## 3. Sign-off

- [ ] All statutory clocks verified against primary source (§1).
- [ ] All citations verified against primary source (§2).
- [ ] Corrections (if any) filed as code-change items and re-verified.

Attester signature: ______________________  Date: __________
