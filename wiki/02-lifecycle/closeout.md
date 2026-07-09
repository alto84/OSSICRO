---
title: "Study Closeout"
section: "02-lifecycle"
status: mixed
governing_authority:
  - "21 CFR 312.38 (withdrawal of an IND)"
  - "21 CFR 312.45 (inactive status)"
  - "21 CFR 312.59, 312.62(a) (drug disposition)"
  - "21 CFR 312.66; 21 CFR 56.108–56.109 (final IRB notice)"
  - "ICH E6(R3) §6.9 + Appendix C; ICH E3 (CSR)"
tags: [lifecycle/closeout, cfr/312, ich/e6r3, ich/e3, ossicro/engine, ossicro/gating]
aliases: ["study closeout", "close-out visit", "IND withdrawal", "IND inactivation"]
updated: 2026-07-09
---

# Study Closeout

> [!authority] Governing authority
> 21 CFR 312.59 and 312.62(a) (disposition of unused investigational drug); 21 CFR 312.38 (withdrawal of an IND) and 21 CFR 312.45 (inactive status; termination path via 312.44); 21 CFR 312.66 and 21 CFR 56.108–56.109 (final IRB notification); ICH E6(R3) §6.9 and Appendix C (close-out monitoring and after-trial essential records); ICH E3 (clinical study report); 42 CFR Part 11 (ClinicalTrials.gov results submission). Status: **Mixed** — the disposition, notification, and records obligations are confirmed; sequencing and the OSSICRO closeout engine are interpretive operational positions.

Closeout is the controlled shutdown of a trial: every subject accounted for, every query resolved, every gram of investigational product reconciled, every oversight body formally released, and the evidentiary record sealed for [[record-retention-and-archival|retention]]. Done poorly, closeout is where inspection findings concentrate — unreconciled drug, unreported final status, IRBs left open indefinitely. For the [[sponsor-investigator]] the entire checklist lands on one physician; OSSICRO's function is to make the sequence explicit, generate each artifact, and gate the two irreversible acts (drug destruction; IND disposition) on human authorization.

## 1. Closeout sequence

The canonical order, mapped to the [[closeout-tmf-checklist]]:

1. **Last subject, last visit; end of protocol-specified follow-up.** Final subject screening/enrollment logs closed (21 CFR 312.62(b) case histories complete); ongoing AEs followed to resolution or stabilization per protocol.
2. **Data cleaning and database lock.** All CRF queries resolved; for blinded studies, final **treatment decoding/unblinding documentation** filed (E6(R3) Appendix C; E6(R2) §8.4.7) so who-received-what is retrievable for analysis.
3. **Safety reconciliation.** The site AE/SAE record is reconciled against the sponsor safety database (and against the pharma partner's database where a safety-data exchange agreement exists); discrepancies resolved and documented. Feeds the final [[ind-annual-report-dsur|annual report/DSUR]] cycle and the CSR safety sections. See [[safety-reporting-lifecycle]].
4. **Final (close-out) monitoring visit (COV).** The monitor confirms data collection is complete, essential records are present and consistent in the ISF/TMF, drug accountability closes, and open action items are resolved; a **close-out monitoring visit report** is filed (ICH E6(R3) §6.9 + Appendix C; E6(R2) §8.4.1). See [[monitoring-workflow-siv-imv-cov]].
5. **Investigational product final reconciliation and disposition.** See §2.
6. **Final IRB notification.** See §3.
7. **FDA notification and IND disposition.** See §4.
8. **Clinical study report.** See §5.
9. **Results disclosure and financial tails.** See §6.
10. **Archival.** The complete TMF/ISF passes to [[record-retention-and-archival]]; a record-retention statement documents the obligation and archive location.

## 2. Drug reconciliation, return, and destruction (21 CFR 312.59, 312.62(a))

The sponsor must ensure the **return of all unused supplies** of the investigational drug from each discontinued/completed investigator, or, alternatively, may authorize **on-site disposition** — provided the disposition does not expose humans to risks from the drug. The sponsor must maintain **written records of any disposition** of the drug (312.59; sponsor receipt/shipment/disposition records under 312.57(a)). The investigator's [[drug-accountability-log]] (dates, quantities, use by subjects — 312.62(a)) must reconcile to zero: received = dispensed + returned + destroyed, each line documented. Controlled substances follow the additional disposition requirements of 21 CFR 312.69 and DEA rules.

> [!warning] Non-delegable
> **Authorization of drug destruction is a gated sponsor decision.** OSSICRO computes the reconciliation, flags variances, and drafts the return/destruction documentation; the sponsor(-investigator) authorizes disposition in writing, and where a pharma partner supplied drug under an IIS or expanded-access arrangement, the supply agreement typically reserves the return-vs-destroy election to the manufacturer ([[pharma-partner-interface-iis]]). Destruction is irreversible; no automated pathway executes it.

## 3. Final IRB notification (21 CFR 312.66; 56.108–56.109)

The investigator's assurance obligations to the IRB run until the IRB formally closes the study. A **final report/closure notice** — enrollment totals, summary of outcomes and AEs, confirmation that no further subject contact or identifiable-data analysis will occur — is submitted per the IRB's closure procedure (E6(R2) §8.4.4; E6(R3) Appendix C after-trial records). Until closure, continuing-review obligations continue to accrue (56.109(f)); leaving a completed study open is a common and avoidable compliance defect. See [[irb-review-workflow]].

## 4. FDA notification and IND disposition

Completion of a single study under a multi-study IND is reported through the next [[annual-reporting-and-amendments|annual report]] (312.33(a)) or an information amendment reporting discontinuation of the investigation (312.31(a)(3)). When the IND itself is done, three administrative paths exist:

- **Withdrawal — 21 CFR 312.38.** The sponsor may withdraw an effective IND **without prejudice** at any time. On withdrawal: FDA is notified, **all clinical investigations under the IND end**, all current investigators are notified, and all drug stocks are returned to the sponsor or otherwise disposed of per 312.59. If withdrawal is **for safety reasons**, the sponsor must **promptly** inform FDA, all participating investigators, and all reviewing IRBs of the reasons (312.38(c)).
- **Inactive status — 21 CFR 312.45.** The sponsor may request inactive status when no subjects will be entered for an extended period; FDA may itself inactivate an IND when **no subjects have been entered for two years or more**, or all investigations have remained on clinical hold for one year or more (with notice and 30 days to respond). While inactive: no new investigators may be added, no subjects entered, no drug shipped or administered — and the sponsor is **exempt from annual reports**. Reactivation requires a protocol amendment and any needed updating information (312.30). An IND inactive for **five years or more** may be terminated under 312.44.
- **Remain active.** Where further studies are planned under the same IND, the IND stays effective and the 312.33 annual-report cycle continues.

The choice among these is a regulatory-strategy decision with downstream consequences — retention clocks under [[record-retention-and-archival|312.57(c)/312.62(c)]] key off discontinuation-plus-FDA-notification — and OSSICRO surfaces it as an explicit decision point with the trade-offs stated, not a default.

## 5. The clinical study report (ICH E3)

The integrated final scientific and statistical report of the trial's conduct and results, structured per **ICH E3** (synopsis, ethics, investigators, study design, subjects, efficacy, safety, discussion, appendices with the protocol, sample CRF, and statistical documentation). For a sponsor-investigator study the CSR is authored with the [[biostatistician]] against the locked database and the [[statistical-analysis-plan]]; it goes to any pharma partner per the agreement, supports publication, and is submitted to FDA if the data will support a marketing application. See [[clinical-study-report]].

## 6. Results disclosure and financial tails

- **ClinicalTrials.gov results.** For an applicable clinical trial (a Phase 2 drug trial typically qualifies), the responsible party must submit results information generally **within one year of the primary completion date** (42 CFR 11.44; FDAAA 801). Certification obligations on FDA submissions ran through [[form-fda-3674-clinicaltrialsgov-certification|Form FDA 3674]]. See [[clinicaltrials-gov-registration]].
- **Financial disclosure tail.** The Part 54 disclosure duty covers investigator financial interests arising **through one year following completion of the study** (21 CFR 54.4); the closeout package records the diligence plan for that window. See [[form-fda-3454-3455-financial-disclosure]].
- **Contract closeout.** Final per-subject and pass-through payments settled under the [[clinical-trial-agreement-and-budget|CTA]]; contractual, not CFR-mandated, but an after-trial essential record in practice.

> [!interpretive] OSSICRO position
> OSSICRO renders closeout as a [[completeness-ledger]] instance: every item above is green (validated complete), amber (needs a human judgment — e.g., the IND-disposition election, destruction authorization), or red (missing with the exact resolving question stated). The claim that a study is "closed" is only made when the ledger shows zero red and every amber gate carries a signed human decision. This is an operating discipline, not a regulatory requirement.

## Related

- [[closeout-tmf-checklist]] — the after-trial essential-records list
- [[record-retention-and-archival]] — what happens to the sealed record
- [[drug-accountability-log]] — the reconciliation substrate
- [[monitoring-workflow-siv-imv-cov]] — the close-out visit
- [[annual-reporting-and-amendments]] — completion reporting and the final annual report
- [[clinical-study-report]] · [[statistical-analysis-plan]] — the scientific wrap-up
- [[clinicaltrials-gov-registration]] — results-posting obligations
- [[irb-review-workflow]] — IRB closure
- [[fda-interactions-meetings-holds]] — inspection readiness at end of study
- [[non-delegable-functions-and-gates]]

## Sources

- [21 CFR 312.38 — Withdrawal of an IND (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.38)
- [21 CFR 312.45 — Inactive status (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-C/section-312.45)
- [21 CFR 312.44 — Termination (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-C/section-312.44)
- [21 CFR 312.59 — Disposition of unused supply of investigational drug (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.59)
- [21 CFR 312.62 — Investigator recordkeeping and record retention (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.62)
- [21 CFR 312.66 — Assurance of IRB review (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.66)
- [21 CFR Part 54 — Financial disclosure by clinical investigators (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-54)
- [42 CFR Part 11 — Clinical trials registration and results information submission (eCFR)](https://www.ecfr.gov/current/title-42/chapter-I/subchapter-A/part-11)
- [ICH E3 — Structure and Content of Clinical Study Reports](https://database.ich.org/sites/default/files/E3_Guideline.pdf)
- [ICH E6(R3) Step 4 Final Guideline (2025-01-06)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
