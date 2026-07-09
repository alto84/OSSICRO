---
title: "Phase-Model Overview — Startup / Conduct / Closeout"
section: "02-lifecycle"
status: confirmed
governing_authority:
  - "ICH E6(R3) Good Clinical Practice, Sections 2–6 and Appendix C (FDA-adopted 2025-09-09)"
  - "21 CFR Part 312 (Subparts B, C, D)"
  - "ICH E8(R1) General Considerations for Clinical Studies"
tags: [lifecycle/activation, lifecycle/conduct, lifecycle/closeout, cfr/312, gcp/e6r3, ich/e8r1, status/confirmed]
aliases: ["Startup Conduct Closeout", "Phase Model Overview"]
updated: 2026-07-09
---

# Phase-Model Overview — Startup / Conduct / Closeout

> [!authority] Governing authority
> ICH E6(R3) Good Clinical Practice §§2–6 and Appendix C ("Essential Records for the Conduct of a Clinical Trial"), FDA-adopted 2025-09-09; 21 CFR Part 312 Subparts B (IND content/submission), C (administrative actions), and D (sponsor and investigator responsibilities); ICH E8(R1) (study design, quality-by-design). Status: **Confirmed**, with the E6(R3) risk-proportionality reading marked interpretive where noted.

The eleven granular phases in [[index|the master phase list]] group into three regulatory epochs that structure the whole Trial Master File and every OSSICRO checklist: **Startup** (before the first subject is exposed), **Conduct** (from first enrollment through last-subject-last-visit), and **Closeout** (database lock through archival). This is the framing ICH E6(R3) uses in Appendix C, which sorts essential records into "before," "during," and "after" the clinical phase, and it is the framing FDA's IND regulation implicitly enforces through the sequence of its Subpart B/C/D obligations. This page maps the two frameworks onto one another so that every generated artifact can be filed to the correct epoch and validated against the correct authority.

A defining structural fact governs all three epochs in the OSSICRO core case: in the **sponsor-investigator** model ([21 CFR 312.3(b)](https://www.ecfr.gov/current/title-21/section-312.3)), a single physician holds both the sponsor obligation set (312.50–312.59, plus IND submission 312.20–312.23, safety reporting 312.32, annual reporting 312.33) and the entire investigator obligation set (312.60–312.69). The epochs do not divide the work between two parties; they order one party's concentrated burden in time. See [[sponsor-investigator]].

## Startup — before first subject exposure

Startup is everything that must be *complete and documented* before a human subject is exposed to the investigational product. Its regulatory spine:

- **IND establishment.** Assemble and submit the [21 CFR 312.23](https://www.ecfr.gov/current/title-21/section-312.23) content-and-format package (Form FDA 1571 cover, general investigational plan, investigator's brochure, protocol, CMC, pharmacology/toxicology, prior human experience). See [[pre-ind-and-ind-preparation]] and [[ind-application-312-23]].
- **The 30-day safe-to-proceed clock.** The IND may not go into effect until 30 days after FDA receipt, absent earlier notification ([21 CFR 312.40](https://www.ecfr.gov/current/title-21/section-312.40)); FDA may impose a clinical hold ([21 CFR 312.42](https://www.ecfr.gov/current/title-21/section-312.42)). See [[ind-submission-and-30-day-clock]].
- **IRB review and approval.** No FDA-regulated human research may begin without prior IRB review and approval against the [21 CFR 56.111](https://www.ecfr.gov/current/title-21/section-56.111) criteria. See [[irb-submission-and-approval]].
- **Site activation.** The essential-document green-light package — signed Form FDA 1572 ([312.53(c)](https://www.ecfr.gov/current/title-21/section-312.53)), CVs/licenses, financial disclosure (Parts 54: Forms 3454/3455), GCP training, executed CTA/budget, delegation-of-authority log, lab certifications, drug release. See [[site-activation]].

> [!warning] Non-delegable
> The Form FDA 1571 and Form FDA 1572 signatures are legal attestations by the sponsor-investigator ([21 CFR 312.23(a)(1)](https://www.ecfr.gov/current/title-21/section-312.23), [312.53(c)](https://www.ecfr.gov/current/title-21/section-312.53)). IRB approval is the IRB's independent ethical judgment under Part 56. OSSICRO assembles and checks these packages; a qualified human owns and signs each attestation and the IRB owns the approval decision. Neither may be automated.

## Conduct — first enrollment through last-subject-last-visit

Conduct is the period during which subjects are enrolled, exposed, and followed. Its spine:

- **Enrollment and consent.** Legally-effective informed consent is obtained from each subject before any study procedure (Part 50, [50.20](https://www.ecfr.gov/current/title-21/section-50.20)–[50.27](https://www.ecfr.gov/current/title-21/section-50.27)); screening/enrollment logs and the eligibility determination are maintained. See [[enrollment-and-consent]].
- **Investigational-product control and case histories.** Drug accountability ([312.61](https://www.ecfr.gov/current/title-21/section-312.61), [312.62](https://www.ecfr.gov/current/title-21/section-312.62)); adequate and accurate case histories; source data and CRFs. See [[conduct-and-monitoring]] and [[drug-accountability-log]].
- **Monitoring.** The sponsor monitors trial conduct ([312.56](https://www.ecfr.gov/current/title-21/section-312.56)) under a risk-based monitoring plan (SIV/IMV/COV), now governed by ICH E6(R3) §6 and its critical-to-quality (CtQ) and quality-tolerance-limit apparatus. See [[conduct-and-monitoring]] and [[risk-based-monitoring-e6r3]].
- **Safety reporting.** The AE→SAE→SUSAR flow: investigator reports SAEs to the sponsor immediately ([312.64(b)](https://www.ecfr.gov/current/title-21/section-312.64)); the sponsor files expedited IND safety reports to FDA and all investigators — 7 calendar days for unexpected fatal/life-threatening suspected reactions, 15 calendar days for other SUSARs ([312.32(c)](https://www.ecfr.gov/current/title-21/section-312.32)). See [[safety-reporting-lifecycle]].
- **Amendments and annual reporting.** Protocol amendments ([312.30](https://www.ecfr.gov/current/title-21/section-312.30)), information amendments ([312.31](https://www.ecfr.gov/current/title-21/section-312.31)), IB updates, IRB continuing review, and the IND annual report within 60 days of the IND anniversary ([312.33](https://www.ecfr.gov/current/title-21/section-312.33); ICH E2F DSUR substitution). See [[annual-reporting-and-amendments]].

> [!warning] Non-delegable
> Serious-adverse-event causality and expectedness determination is medical judgment ([21 CFR 312.32(a)](https://www.ecfr.gov/current/title-21/section-312.32); ICH E2A). It triggers the 7-day/15-day clocks but is owned and signed by the medical monitor / sponsor-investigator, never by software. See [[medical-monitor]] and [[non-delegable-functions-and-gates]].

## Closeout — database lock through archival

Closeout is the orderly termination of the trial and the IND. Its spine:

- **Final monitoring visit and reconciliation.** Confirms data collected and queries resolved; investigational-product final reconciliation and return/destruction ([312.59](https://www.ecfr.gov/current/title-21/section-312.59), [312.62](https://www.ecfr.gov/current/title-21/section-312.62)). See [[closeout]].
- **FDA and IRB termination notices.** Study completion; IND withdrawal ([312.38](https://www.ecfr.gov/current/title-21/section-312.38)), inactivation ([312.45](https://www.ecfr.gov/current/title-21/section-312.45)); final IRB notification of completion. See [[closeout]].
- **Clinical study report.** The integrated final scientific/statistical report per ICH E3. See [[clinical-study-report]].
- **Record retention and archival.** Retention through the statutory horizon (2 years after marketing approval for the indication, or 2 years after IND discontinuation and FDA notification, whichever is applicable — [312.57(c)](https://www.ecfr.gov/current/title-21/section-312.57), [312.62(c)](https://www.ecfr.gov/current/title-21/section-312.62); ICH E6(R3) §C.2). See [[record-retention-and-archival]].

## The E6(R3) shift and OSSICRO's use of it

E6(R3) reframes "essential documents" as **"essential records"** — encompassing dynamic and electronic content — and applies **risk-proportionality**: the nature and extent of records depend on the trial's design and the materiality of each record, so not every Appendix C item is mandatory for every trial. This is a genuine change from the fixed E6(R2) §8 list.

> [!interpretive] OSSICRO position
> OSSICRO's completeness checker treats the E6(R3) Appendix C matrix as **risk-proportionate, not a fixed checklist**: for a low-risk single-site early-phase study, the [[completeness-ledger]] marks conditionally-required records (e.g., a DSMB charter, a centralized-monitoring plan) as *amber — needs human judgment* rather than *red — missing*, and routes the proportionality decision to the sponsor-investigator. This reading is defensible under E6(R3) §§2 and 6 but is an OSSICRO design interpretation, not a black-letter FDA instruction. The proportionality call itself is a human gate.

## Mapping table — epoch × authority × OSSICRO artifact

| Epoch | Primary CFR | ICH E6(R3) locus | Representative OSSICRO output | Terminal gate |
|-------|-------------|------------------|------------------------------|---------------|
| Startup | 312.20–312.23; 312.40–312.42; Part 56; 312.53 | App. C "before"; §2 | IND package, IRB package, activation dossier | 1571/1572 signature; IRB approval |
| Conduct | Part 50; 312.32; 312.56–312.64 | App. C "during"; §§5, 6 | Consent set, monitoring reports, IND safety reports, annual report | Consent event; causality call |
| Closeout | 312.38; 312.45; 312.57(c)/312.62(c) | App. C "after"; §C.2 | CSR, reconciliation records, retention statement | Study-completion attestation |

## Related
- [[index]]
- [[sponsor-investigator]]
- [[feasibility-and-patient-matching]]
- [[pre-ind-and-ind-preparation]]
- [[ind-submission-and-30-day-clock]]
- [[document-catalog]]
- [[completeness-ledger]]
- [[non-delegable-functions-and-gates]]

## Sources
- [ICH E6(R3) Good Clinical Practice — Step 4 Final Guideline (ICH)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [21 CFR Part 312 (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312)
- [ICH E8(R1) General Considerations for Clinical Studies (ICH)](https://database.ich.org/sites/default/files/ICH_E8-R1_Guideline_Step4_2021_1006.pdf)
- [FDA adoption notice, E6(R3) (Federal Register 2025-17311)](https://www.federalregister.gov/documents/2025/09/09/2025-17311)
- [ICH E2F Development Safety Update Report (ICH)](https://database.ich.org/sites/default/files/E2F_Guideline.pdf)
