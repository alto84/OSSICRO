---
title: "Investigator — Responsibilities under 21 CFR 312.60-312.69"
section: "01-roles-responsibilities"
status: mixed
governing_authority:
  - "21 CFR 312.60-312.69"
  - "21 CFR Part 50"
  - "21 CFR Part 56"
  - "21 CFR Part 54"
  - "ICH E6(R3) Annex 1, Section 2 (Investigator)"
tags: [role/investigator, cfr/312, cfr/50, cfr/56, cfr/54, fda-form/1572, gcp/e6r3, lifecycle/conduct, ossicro/gating]
aliases: ["investigator responsibilities", "312.60"]
updated: 2026-07-09
---

# Investigator — Responsibilities under 21 CFR 312.60-312.69

> [!authority] Governing authority
> 21 CFR 312 Subpart D, §§312.60-312.69 (investigator responsibilities; §§312.63, 312.65, and 312.67 are reserved); 21 CFR Part 50 (informed consent); 21 CFR Part 56 (IRB); 21 CFR Part 54 and 312.64(d) (financial disclosure); Form FDA 1572 per 312.53(c); ICH E6(R3) Annex 1, Section 2 — Investigator (corresponds to E6(R2) §4); FDA Guidance, *Investigator Responsibilities* (October 2009). Status: **Mixed** — CFR duties confirmed; OSSICRO automation-boundary claims marked interpretive.

An **investigator** is "an individual who actually conducts a clinical investigation (i.e., under whose immediate direction the drug is administered or dispensed to a subject)"; where a team conducts the investigation, the investigator is the responsible leader (21 CFR 312.3(b)). The investigator is the trial's patient-facing accountable human: protocol conduct, subject protection, informed consent, drug control, and records all terminate in this one person, whose commitments are memorialized in the signed [[form-fda-1572-statement-of-investigator|Form FDA 1572]]. In OSSICRO's Mode A the enrolling physician holds exactly this role at a pharma sponsor's site; in Mode B the same duties are one half of the [[sponsor-investigator]]'s double burden ([[two-modes-site-vs-sponsor-investigator]]).

## General responsibilities — 21 CFR 312.60

An investigator is responsible for: **ensuring that the investigation is conducted according to the signed investigator statement (Form FDA 1572), the investigational plan, and applicable regulations**; **protecting the rights, safety, and welfare of subjects** under the investigator's care; and **controlling the drugs under investigation**. In accordance with Part 50, the investigator shall **obtain the informed consent of each human subject** to whom the drug is administered. Section 312.60 is the umbrella; the 1572's Field 9 commitments restate and personalize it (see [[form-fda-1572-statement-of-investigator]]).

> [!warning] Non-delegable
> The informed-consent obligation is a relational, judgment-bearing act between a qualified member of the investigational team and the subject (21 CFR Part 50; 50.20 general requirements; 50.25 elements; 50.27 documentation). OSSICRO drafts, versions, and completeness-checks the [[informed-consent-form|ICF]]; it never conducts, replaces, or simulates the consent conversation. The bright line is treated at [[informed-consent-document-vs-event]].

## Control of the investigational drug — 21 CFR 312.61

The investigator shall administer the drug **only to subjects under the investigator's personal supervision or under the supervision of a subinvestigator responsible to the investigator**, and shall **not supply the investigational drug to any person not authorized under Part 312 to receive it**. Practical implementation runs through the [[drug-accountability-log]] and, for scheduled substances, 312.69 below.

## Recordkeeping and retention — 21 CFR 312.62

- **(a) Disposition of drug.** Maintain adequate records of the disposition of the drug, including **dates, quantity, and use by subjects**. If the investigation is terminated, suspended, discontinued, or completed, return unused supplies to the sponsor or otherwise provide for disposition per 312.59.
- **(b) Case histories.** Prepare and maintain **adequate and accurate case histories that record all observations and other data pertinent to the investigation** on each individual administered the drug or employed as a control. Case histories include case report forms and supporting data — signed and dated consent forms, medical records (progress notes, hospital charts, nurses' notes). **The case history must document that informed consent was obtained prior to participation.**
- **(c) Retention.** Retain the records required by Part 312 for **2 years following the date a marketing application is approved for the drug for the indication being investigated**; or, if no application is to be filed or the application is not approved, **until 2 years after the investigation is discontinued and FDA is notified** ([[record-retention-and-archival]]).

## Investigator reports — 21 CFR 312.64

- **(a) Progress reports.** Furnish all reports to the sponsor, who is responsible for collecting and evaluating results and submitting annual reports to FDA (312.33; [[ind-annual-report-dsur]]).
- **(b) Safety reports.** **Immediately report to the sponsor any serious adverse event, whether or not considered drug related**, including those listed in the protocol or [[investigators-brochure|investigator's brochure]], and include **an assessment of whether there is a reasonable possibility that the drug caused the event**. Study endpoints that are serious adverse events are reported per protocol unless there is evidence suggesting a causal relationship. Record non-serious adverse events and report them to the sponsor per the protocol's timetable. This feeds the sponsor's 7-/15-day clocks under 312.32 ([[safety-reporting-lifecycle]], [[ind-safety-report]]).
- **(c) Final report.** Provide the sponsor an adequate report shortly after completion of the investigator's participation.
- **(d) Financial disclosure.** Provide the sponsor sufficient accurate financial information to allow complete and accurate Part 54 certification or disclosure ([[form-fda-3454-3455-financial-disclosure]]); **promptly update** the information on any relevant change during the study and **for 1 year following study completion**.

> [!warning] Non-delegable
> The 312.64(b) seriousness and causality assessment is the investigator's clinical judgment. OSSICRO may capture, structure, pre-populate, route, and time-stamp the SAE report — and compute the downstream sponsor deadlines ([[safety-clock-engine]]) — but the medical assessment belongs to the investigator (and, on the sponsor side, to the [[medical-monitor]]).

## Assurance of IRB review — 21 CFR 312.66

The investigator shall **assure that an IRB complying with Part 56 will be responsible for the initial and continuing review and approval** of the clinical investigation; **promptly report to the IRB all changes in the research activity and all unanticipated problems involving risk to human subjects or others**; and **make no changes in the research without IRB approval, except where necessary to eliminate apparent immediate hazards to human subjects**. Enrollment is gated on documented IRB approval ([[irb-submission-and-approval]], [[irb-iec]]); the IRB's judgment itself is a non-delegable committee act (21 CFR 56.111).

## Inspection of records — 21 CFR 312.68

Upon request of a properly authorized FDA officer or employee, at reasonable times, the investigator shall permit access to, and copying and verification of, any records or reports made under 312.62. **The investigator is not required to divulge subject names** unless the records of particular individuals require more detailed study, or unless there is reason to believe the records do not represent actual case studies or actual results. This is the regulatory basis of the BIMO site inspection ([[fda-as-counterparty]]).

## Controlled substances — 21 CFR 312.69

If the investigational drug is subject to the Controlled Substances Act, the investigator shall take adequate precautions to prevent theft or diversion into illegal channels, **including storage in a securely locked, substantially constructed cabinet or other securely locked, substantially constructed enclosure, access to which is limited**.

## Consequences of non-compliance — 21 CFR 312.70

Although outside the 312.60-312.69 duty set proper, investigators should know the enforcement backstop: an investigator who repeatedly or deliberately fails to comply with Part 312 (or Parts 50/56), or who submits false information to the sponsor or FDA, is subject to the disqualification procedures of 312.70. Signing the 1572 without meeting its commitments is itself a basis for regulatory action.

## Delegation and the ICH E6(R3) layer

The investigator may delegate specific trial **tasks** to qualified subinvestigators and staff — documented in a signed, dated [[delegation-of-authority-log]] with supporting training records — but delegation never transfers accountability; supervision and the acts tied to the 1572 signature remain personal (FDA 2009 *Investigator Responsibilities* guidance; ICH E6(R3) Annex 1 §2). E6(R3) adds: demonstrated qualification and resources; documented supervision of delegated activities and oversight of services used at the site; investigational-product accountability at the site; adherence to the protocol and to randomization/blinding procedures; data recording that meets ALCOA expectations; and cooperation with monitoring and audits ([[subinvestigator-and-delegation]], [[clinical-monitor-cra]]).

> [!interpretive] OSSICRO position
> OSSICRO classifies as automatable coordination labor: assembling the site regulatory binder ([[regulatory-binder-isf-index]]), drafting and versioning the ICF, maintaining the delegation log and training matrix, structuring case-history documentation, pre-populating SAE forms, computing report deadlines, and completeness-checking the investigator site file against ICH E6(R3) Appendix C ([[completeness-ledger]]). The non-delegable floor — consent, eligibility and clinical judgments, SAE assessment, supervision, the 1572 signature, and IRB interaction decisions — stays with the qualified human ([[non-delegable-functions-and-gates]]). OSSICRO drafts complete documentation for qualified human review; it never replaces the investigator's judgment or the IRB's review.

## Related

- [[sponsor]]
- [[sponsor-investigator]]
- [[subinvestigator-and-delegation]]
- [[form-fda-1572-statement-of-investigator]]
- [[form-fda-3454-3455-financial-disclosure]]
- [[informed-consent-form]]
- [[informed-consent-document-vs-event]]
- [[irb-iec]]
- [[irb-submission-and-approval]]
- [[delegation-of-authority-log]]
- [[drug-accountability-log]]
- [[record-retention-and-archival]]
- [[safety-reporting-lifecycle]]
- [[enrollment-and-consent]]
- [[non-delegable-functions-and-gates]]

## Sources

- [21 CFR 312.60 — General responsibilities of investigators (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.60)
- [21 CFR 312.61 — Control of the investigational drug (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.61)
- [21 CFR 312.62 — Investigator recordkeeping and record retention (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.62)
- [21 CFR 312.64 — Investigator reports (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.64)
- [21 CFR 312.66 — Assurance of IRB review (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.66)
- [21 CFR 312.68 — Inspection of investigator's records and reports (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.68)
- [21 CFR 312.69 — Handling of controlled substances (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.69)
- [21 CFR 312.70 — Disqualification of a clinical investigator (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.70)
- [21 CFR Part 50 — Protection of Human Subjects (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50)
- [21 CFR Part 56 — Institutional Review Boards (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56)
- [FDA Guidance — Investigator Responsibilities: Protecting the Rights, Safety, and Welfare of Study Subjects (2009)](https://www.fda.gov/media/77765/download)
- [FDA — Frequently Asked Questions: Statement of Investigator (Form FDA 1572)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/frequently-asked-questions-statement-investigator-form-fda-1572)
- [FDA — Instructions for Filling Out Form FDA 1572](https://www.fda.gov/media/79326/download)
- [ICH E6(R3) Step 4 Final Guideline (2025-01-06)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
