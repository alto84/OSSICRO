---
title: "Record Retention and Archival"
section: "02-lifecycle"
status: mixed
governing_authority:
  - "21 CFR 312.57(c) (sponsor retention)"
  - "21 CFR 312.62(c) (investigator retention)"
  - "21 CFR 312.58, 312.68 (FDA inspection access)"
  - "ICH E6(R3) Appendix C + essential-records management"
  - "21 CFR Part 11 (electronic records)"
tags: [lifecycle/retention, cfr/312, cfr/11, ich/e6r3, ossicro/part11, ossicro/gating]
aliases: ["record retention", "TMF archival", "2-year rule"]
updated: 2026-07-09
---

# Record Retention and Archival

> [!authority] Governing authority
> 21 CFR 312.57(c) (sponsor record retention) and 21 CFR 312.62(c) (investigator record retention) — both event-conditional two-year clocks; 21 CFR 312.58 and 312.68 (FDA inspection access to sponsor and investigator records); ICH E6(R3) Appendix C and its essential-records management provisions (retrievability, certified copies, control), FDA-adopted 2025-09-09; 21 CFR Part 11 (electronic records must remain accurately retrievable throughout the retention period, §11.10(c)). Status: **Mixed** — the CFR retention periods and inspection rights are confirmed; archival architecture and the OSSICRO retention register are interpretive operational positions.

Retention is the final obligation of a trial and the one most often mishandled, because its deadline is **conditional on future events the site does not control**: whether a marketing application is ever filed, whether it is approved, and when the sponsor formally discontinues and notifies FDA. The records retained are the evidentiary basis for every claim the trial ever supports — data integrity, subject protection, drug accountability — and remain inspectable by FDA for the full period. This page states the black-letter clocks, the E6(R3) records-management layer, and the archival discipline OSSICRO enforces.

## 1. The two CFR retention clocks

### 1.1 Sponsor — 21 CFR 312.57(c)

The sponsor must retain the records and reports required by Part 312 (including drug receipt/shipment/disposition records under 312.57(a) and financial-disclosure records under 312.57(b)/21 CFR 54.6) for:

- **2 years after a marketing application is approved** for the drug; **or**
- if no application is approved for the drug, **until 2 years after shipment and delivery of the drug for investigational use is discontinued and FDA has been so notified**.

For bioavailability/bioequivalence studies, reserve samples of the test article and reference standard are retained per 21 CFR 320.38/320.63 (five years after transmission of the study to FDA) — noted for completeness; typically inapplicable to an early-phase therapeutic IND.

### 1.2 Investigator — 21 CFR 312.62(c)

The investigator must retain the records required by 312.62 (drug disposition records and case histories, including case report forms and **signed consent documents**) for:

- **2 years following the date a marketing application is approved for the drug for the indication for which it is being investigated**; **or**
- if no application is filed, or the application is not approved for that indication, **until 2 years after the investigation is discontinued and FDA is notified**.

In the [[sponsor-investigator]] model both clocks bind the same physician; the **longer-running** condition controls in practice, and the two record sets (sponsor TMF, investigator ISF) must both survive it.

> [!warning] Non-delegable
> **No record destruction without a documented human release.** The retention end date cannot be computed at closeout — it depends on marketing-application events that may occur years later. The operating rule (E6-derived and encoded in OSSICRO): the investigator does not dispose of any record until the sponsor confirms **in writing** that retention is no longer required; the sponsor(-investigator) makes that determination against the 312.57(c)/312.62(c) conditions, on advice where needed, and signs it. FDA's inspection rights (312.58, 312.68) run for the entire period — destroying early is destroying evidence.

### 1.3 Inspection access during retention

- **Sponsor:** upon request of a properly authorized FDA employee, at reasonable times, permit access to and copying/verification of **any records and reports relating to the clinical investigation** (21 CFR 312.58; controlled-substance records also inspectable by DEA).
- **Investigator:** the same access to records under 312.62 (21 CFR 312.68). Subject identities may be withheld unless the records of particular individuals require more detailed study or there is reason to believe the records do not represent actual cases or results — the regulation's own carve-out; see also the Field 9 commitments on the [[form-fda-1572-statement-of-investigator|1572]].

## 2. The ICH E6(R3) records-management layer

E6(R3) reframes "essential documents" (E6(R2) §8) as **essential records** — records that individually and collectively permit evaluation of the conduct of the trial and the quality of the data produced — and applies risk-proportionality to what must exist ([[document-catalog]]). Its management provisions govern *how* the archive must behave:

- **Identifiable and retrievable.** Essential records must be readily identifiable, complete, and retrievable throughout the retention period, whatever the format or storage location; the [[regulatory-binder-isf-index]] is the finding aid.
- **Certified copies.** A certified copy (verified to have the same information, including data describing context, content, and structure, as the original) may replace the original.
- **Control.** The investigator/institution must maintain **control of their essential records** — the sponsor must not have exclusive control of the investigator's records (this protects the independence of the site record from sponsor alteration); conversely sponsor and investigator must each have continuous access to their respective records regardless of where a service provider hosts them.
- **Retention duration.** E6(R3) defers the retention period to **applicable regulatory requirements** (for a US IND, the 312.57(c)/312.62(c) clocks above) and to the contractual agreements among the parties; the sponsor should inform the investigator/institution in writing when the records are no longer needed (carried forward from E6(R2) §5.5.12).

### Longer horizons in practice

> [!interpretive] OSSICRO position
> The CFR two-year clocks are a **floor, not a norm**. Pharma-partner CTAs routinely impose 15–25-year retention; the EU Clinical Trials Regulation (536/2014, Art. 58) requires **25-year** TMF retention for trials in its scope; institutional and state medical-records law may run longer still, and records containing PHI carry HIPAA documentation requirements (45 CFR 164.530(j), six years for compliance documentation). OSSICRO therefore records, per study, a **retention register**: every applicable retention authority, the controlling (longest) period, the condition that starts each clock, and the named human who may authorize release. The register is itself an essential record filed at [[closeout]].

## 3. Electronic archival and Part 11

Where the TMF/ISF is electronic (OSSICRO's default), 21 CFR Part 11 applies for the archive's full life:

- **Accurate and ready retrieval** of records throughout the records retention period (§11.10(c)) — including after system decommissioning; migration must preserve content and meaning, with the audit trail intact.
- **Audit trails** (§11.10(e)) are retained **at least as long as the underlying records** and remain available for FDA review and copying.
- **E-signatures** (§§11.50–11.300) on archived documents must remain verifiably bound to their records.

OSSICRO's archival export is a hash-chained, integrity-verifiable package — the same manifest structure as the [[verifiable-site-qualification-dossier]] — so that a record produced ten years later can demonstrate it is what was sealed at closeout. Provenance and audit-trail treatment follow [[part-11-and-ai-credibility]] and [[draft-provenance-model]]; AI-authorship attribution on drafted documents is preserved into the archive, since it is part of the record's history.

## 4. What gets archived

The archival unit is the complete essential-records set at [[closeout]] — the sponsor TMF and investigator ISF halves per the [[closeout-tmf-checklist]], including: protocol and all amendments; IB versions; signed consent forms (312.62(b)); case histories/CRFs; the [[drug-accountability-log]] and disposition records; IRB correspondence through closure; all IND safety reports and the safety database ([[safety-reporting-lifecycle]]); annual reports/DSURs; monitoring visit reports; the [[delegation-of-authority-log]]; financial-disclosure records (through the one-year 21 CFR 54 tail); executed agreements ([[clinical-trial-agreement-and-budget|CTA]], [[transfer-of-regulatory-obligations-toro|TORO]] if any); the [[clinical-study-report]]; and the decoding/unblinding documentation. Subject-identifying material is archived under the same privacy controls that governed it live ([[hipaa-and-privacy-gating]]); identities never enter logs or manifests.

## 5. Retention triggers — practical decision table

| Scenario | Sponsor clock (312.57(c)) | Investigator clock (312.62(c)) |
|---|---|---|
| Marketing application approved | 2 years after approval | 2 years after approval **for the studied indication** |
| Application filed, not (yet) approved | Hold — clock not started | Hold — clock not started |
| No application; development discontinued | 2 years after investigational shipment/delivery discontinued **and FDA notified** | 2 years after investigation discontinued **and FDA notified** |
| IND withdrawn (312.38) / inactivated (312.45) | Notification event starts the discontinuation limb | Same, per study status |

The FDA-notification element is easy to miss: discontinuation alone does not start the clock — the notification (via [[annual-reporting-and-amendments|information amendment]], withdrawal letter, or final report) does. OSSICRO records the notification date as the clock-start datum.

## Related

- [[closeout]] — the process that seals the record
- [[closeout-tmf-checklist]] — what must be in the archive
- [[document-catalog]] — the full essential-records map
- [[regulatory-binder-isf-index]] — the archive's finding aid
- [[part-11-and-ai-credibility]] — electronic-records substrate
- [[draft-provenance-model]] — provenance preserved into archive
- [[hipaa-and-privacy-gating]] — privacy controls on archived PHI
- [[form-fda-1572-statement-of-investigator]] — the access commitments
- [[investigator]] · [[sponsor]] · [[sponsor-investigator]] — who holds which clock
- [[non-delegable-functions-and-gates]] — the destruction-release gate

## Sources

- [21 CFR 312.57 — Recordkeeping and record retention (sponsor) (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.57)
- [21 CFR 312.62 — Investigator recordkeeping and record retention (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.62)
- [21 CFR 312.58 — Inspection of sponsor's records and reports (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.58)
- [21 CFR 312.68 — Inspection of investigator's records and reports (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.68)
- [21 CFR Part 11 — Electronic records; electronic signatures (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)
- [21 CFR 54.6 — Recordkeeping and record retention (financial disclosure) (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/54.6)
- [ICH E6(R3) Step 4 Final Guideline (2025-01-06)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [Federal Register — FDA adoption of ICH E6(R3) (Sept. 9, 2025)](https://www.federalregister.gov/documents/2025/09/09/2025-17311/e6r3-good-clinical-practice-international-council-for-harmonisation-guidance-for-industry)
- [EU Regulation 536/2014, Art. 58 — clinical trial master file retention (EUR-Lex)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32014R0536)
- [45 CFR 164.530(j) — HIPAA documentation retention (Cornell LII)](https://www.law.cornell.edu/cfr/text/45/164.530)
