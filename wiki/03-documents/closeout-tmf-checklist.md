---
title: "Closeout TMF Checklist — After-Trial Essential Records"
section: "03-documents"
status: mixed
governing_authority:
  - "ICH E6(R3) Appendix C (after-trial essential records) and §C.2 (retention); E6(R2) §8.4"
  - "21 CFR 312.38 (withdrawal), 312.45 (inactivation), 312.59 (disposition), 312.57(c) / 312.62(c) (retention)"
  - "42 CFR Part 11 + FDAAA 801 (ClinicalTrials.gov results); ICH E3 (CSR)"
tags: [lifecycle/closeout, lifecycle/retention, gcp/e6r3, cfr/312, ich/e3, ossicro/gating, status/mixed]
aliases: ["closeout checklist", "after-trial documents", "study closure records", "archival checklist"]
updated: 2026-07-09
---

# Closeout TMF Checklist — After-Trial Essential Records

> [!authority] Governing authority
> **ICH E6(R3) Appendix C** (after-trial essential records) and **§C.2** (management/retention), with **E6(R2) §8.4** cross-numbering; **21 CFR 312.38** (withdrawal), **312.45** (inactivation), **312.59** (disposition), **312.57(c)/312.62(c)** (retention); **42 CFR Part 11 / FDAAA 801** (ClinicalTrials.gov results); **ICH E3** (CSR). Status: **Mixed** — items tagged Confirmed / Conditional inline.

This is the after-trial working checklist: the records that formally end the trial, close each oversight relationship, and start the record-retention clock. Closeout is where accountability is *evidenced complete* — drug reconciled and destroyed under authorization, FDA and [[irb-iec|IRB]] notified, the [[clinical-study-report|CSR]] issued, ClinicalTrials.gov results posted, and the [[record-retention-and-archival|TMF/ISF archived]]. Full authority mapping for each row is in the [[document-catalog]] (section C). See [[closeout]] for the workflow view and [[record-retention-and-archival]] for the retention rules.

## 1. Site closure and monitoring

- [ ] **[[closeout|Study closeout monitoring visit report]]** — confirms all data collected/queries resolved, drug reconciled/returned, records complete and archived, outstanding issues closed. *ICH E6(R3) §6.9 + App C; E6(R2) §8.4.1; Confirmed.*
- [ ] **Final subject screening/enrollment logs** — closes accountability for all subjects. *21 CFR 312.62(b); Confirmed.*
- [ ] **Final safety reconciliation** — site AE/SAE database reconciled against the sponsor safety database. *21 CFR 312.62(b); Confirmed.*

## 2. Investigational product disposition

- [ ] **[[drug-accountability-log|IP final reconciliation]] + return/destruction records** — accounts for all dispensed/returned/destroyed drug; documents authorized destruction. *21 CFR 312.59, 312.62(a); E6(R2) §8.4.2–8.4.3; Confirmed.*

> [!warning] Non-delegable
> **Authorization of investigational-product destruction and final disposition** is a sponsor decision (21 CFR 312.59). OSSICRO reconciles quantities and drafts the destruction record; the [[sponsor-investigator|sponsor(-investigator)]] authorizes the destruction. Software does not release drug for destruction any more than it releases it for use. See [[non-delegable-functions-and-gates]].

## 3. Regulatory and ethics closure

- [ ] **Notification to FDA of study completion / IND withdrawal or inactivation** — study/IND complete, withdrawn (312.38), or inactivated (312.45); final safety and disposition wrap-up. *21 CFR 312.38, 312.45, 312.33; Confirmed.*
- [ ] **Final IRB notification of study completion** — completion report + summary of results/AEs; closes IRB oversight. *21 CFR 312.66, 56.108/56.109; E6(R2) §8.4.4; Confirmed.*

## 4. Scientific and statistical final records

- [ ] **[[clinical-study-report|Clinical Study Report (CSR)]]** — integrated final scientific + statistical report; format per **ICH E3**. Filed to FDA if used to support a marketing application; summary to partner/IRB. *ICH E3; ICH E6(R3) App C; 21 CFR 312.33; E6(R2) §8.4.9; Confirmed.*
- [ ] **Treatment allocation / decoding / unblinding documentation** — the final code-break so who received what is retrievable for analysis. *ICH E6(R3) App C; 21 CFR 312.62; E6(R2) §8.4.7; Conditional (blinded trials).*
- [ ] **Audit certificate / statement** — attests an independent QA audit occurred. *ICH E6(R3) §5 + App C; E6(R2) §8.4.8; Conditional (audit performed).*

> [!warning] Non-delegable
> The **CSR's scientific conclusions** and any **[[dsmb-dmc|DSMB]] stop/continue recommendation** underlying study termination are human judgments requiring sign-off. OSSICRO assembles the CSR shell from the [[statistical-analysis-plan|SAP]] outputs, [[clinical-protocol-and-synopsis|protocol]], and safety data ([[draft-provenance-model|each span traced to source]]); the [[sponsor-investigator]] and [[biostatistician]] own the interpretation and sign.

## 5. Public reporting

- [ ] **[[clinicaltrials-gov-registration|ClinicalTrials.gov registration + results submission]]** — statutory registration (within 21 days of first enrollment; a startup obligation) and **results posting** (generally within 1 year of primary completion) for applicable clinical trials. A Phase 2 drug trial typically qualifies. *42 CFR Part 11; FDAAA 801 (Pub. L. 110-85 §801); 42 U.S.C. 282(j); Confirmed.*

## 6. Retention and archival

- [ ] **Record-retention statement + archival** — documents the retention obligation and the archive location for all essential records; TMF/ISF placed in controlled archive. *21 CFR 312.57(c) (sponsor), 312.62(c) (investigator); ICH E6(R3) §C.2/§5; E6(R2) §4.9.5/§5.5.11; Confirmed.*
- [ ] **Final financial reconciliation / closeout of CTA payments** — settles budget, per-subject payments, pass-through costs; supports the 1-year-post financial-disclosure window. *21 CFR 54.4; ICH E6(R3) §5; contractual; Interpretive/contractual.*

### Retention clock

> [!note] How long to keep records
> **FDA (21 CFR 312.57(c) / 312.62(c)):** retain records for **2 years after a marketing application is approved** for the indication — or, if no application is filed or the application is not approved, **2 years after the IND is discontinued and FDA is notified**. **ICH E6(R3) §C.2:** retain until at least **2 years after the last marketing-application approval** or after **formal discontinuation of clinical development** of the investigational product; sponsor informs the investigator/institution when records no longer need to be retained. Apply the **longer** applicable period, and confirm any partner-agreement or jurisdiction-specific extension. See [[record-retention-and-archival]].

## Sponsor-investigator collapse at closeout

At closeout the [[sponsor-investigator]] issues **both** the sponsor's FDA completion/withdrawal notice (312.38/312.45) **and** the investigator's final IRB report — filings that, for a two-entity trial, would originate separately. The physician also holds **both** retention obligations (312.57(c) sponsor and 312.62(c) investigator) over the same archive. The financial-disclosure window (21 CFR Part 54) runs **1 year past study completion**, so the closeout financial reconciliation is not the end of the Part 54 obligation. See [[sponsor-cro-site-coordination]].

## How OSSICRO drives closeout

> [!interpretive] OSSICRO position
> OSSICRO treats closeout as the moment the [[completeness-ledger]] must reach **all-green** for the confirmed after-trial subset, or carry an explicit, human-signed rationale for any residual amber/red. The [[verifiable-site-qualification-dossier|verifiable dossier]] is finalized and hash-chained to the Part-11 audit trail, giving the [[sponsor-investigator]] a cryptographically verifiable, citation-complete record of a compliant trial. OSSICRO also computes and surfaces the **retention expiry date** and the **ClinicalTrials.gov results deadline** as tracked obligations — it schedules and reminds, it does not post results or authorize destruction on its own.

> [!warning] Non-delegable
> At closeout the gated acts are: **IP-destruction authorization** (312.59), the **decision to file** the FDA completion/withdrawal notice, the **CSR scientific sign-off**, and the **ClinicalTrials.gov results certification**. OSSICRO reconciles, drafts, tracks deadlines, and archives; qualified humans authorize, conclude, and submit. See [[non-delegable-functions-and-gates]].

## Related
- [[document-catalog]]
- [[startup-tmf-checklist]]
- [[conduct-tmf-checklist]]
- [[closeout]]
- [[record-retention-and-archival]]
- [[clinical-study-report]]
- [[clinicaltrials-gov-registration]]
- [[drug-accountability-log]]
- [[ind-annual-report-dsur]]
- [[biostatistician]]
- [[non-delegable-functions-and-gates]]
- [[completeness-ledger]]
- [[verifiable-site-qualification-dossier]]

## Sources
- [ICH E6(R3) Step 4 Final Guideline — Appendix C and §C.2 (essential records; retention)](https://database.ich.org/sites/default/files/ICH_E6(R3)_Step4_FinalGuideline_2025_0106.pdf)
- [eCFR — 21 CFR 312.38 (withdrawal of an IND)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-C/section-312.38)
- [eCFR — 21 CFR 312.45 (inactive status)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-C/section-312.45)
- [eCFR — 21 CFR 312.57 (sponsor recordkeeping and retention)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.57)
- [eCFR — 21 CFR 312.62 (investigator recordkeeping and retention)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.62)
- [ICH E3 — Structure and Content of Clinical Study Reports](https://database.ich.org/sites/default/files/E3_Guideline.pdf)
- [ClinicalTrials.gov — FDAAA 801 and the Final Rule (42 CFR Part 11)](https://clinicaltrials.gov/policy/fdaaa-801-final-rule)
