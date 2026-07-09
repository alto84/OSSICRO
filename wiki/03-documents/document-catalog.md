---
title: "Essential-Records Catalog — E6(R3) Appendix C × 21 CFR"
section: "03-documents"
status: mixed
governing_authority:
  - "ICH E6(R3) Appendix C (Essential Records for the Conduct of a Clinical Trial)"
  - "ICH E6(R3) Annex 1 §§1–4 and Appendices A–B (record-generating duties)"
  - "ICH E6(R2) §8.2 / §8.3 / §8.4 (legacy essential-documents cross-numbering)"
  - "21 CFR Part 312 (IND); 21 CFR Part 50 (consent); 21 CFR Part 56 (IRB); 21 CFR Part 54 (financial disclosure); 21 CFR Part 11 (electronic records/signatures)"
  - "42 CFR Part 493 (CLIA); 42 CFR Part 11 + FDAAA 801 (ClinicalTrials.gov)"
tags: [gcp/e6r3, cfr/11, cfr/312, cfr/50, cfr/56, cfr/54, lifecycle/feasibility, lifecycle/conduct, lifecycle/closeout, ossicro/engine, ossicro/part11, status/mixed]
aliases: ["document catalog", "essential records catalog", "essential documents list", "TMF catalog", "Appendix C map"]
updated: 2026-07-09
---

# Essential-Records Catalog — E6(R3) Appendix C × 21 CFR

> [!authority] Governing authority
> **ICH E6(R3) Appendix C** — "Essential Records for the Conduct of a Clinical Trial" (Step 4 adopted 2026-01-06; FDA final guidance September 2025), with **ICH E6(R2) §8** cross-numbering retained as the interpretive bridge; **21 CFR Parts 312, 50, 56, 54, 11**; **42 CFR Part 493** (CLIA) and **42 CFR Part 11 / FDAAA 801** (registration). Status: **Mixed** — each record is tagged **Confirmed** (black-letter regulatory requirement) or **Conditional / Interpretive** (design- or risk-dependent, or guidance-driven) inline.

This is the master essential-records catalog for a US [[sponsor-investigator]] early-phase (e.g., Phase 2) IND trial. It enumerates every record across the trial lifecycle, maps each to its **governing authority** and its **E6(R3)** location, and names the **owner** (who produces/holds it) and the **receiver** (who it flows to). The three lifecycle checklists — [[startup-tmf-checklist]], [[conduct-tmf-checklist]], [[closeout-tmf-checklist]] — are working extractions from this catalog; this page is the authority-carrying source of truth they cite back to.

## How to read the catalog

- **E6(R3) numbering.** The Step 4 guideline is structured as Principles + **Annex 1** (§1 IRB/IEC, §2 Investigator, §3 Sponsor, §4 Data Governance) + **Appendices A** (Investigator's Brochure), **B** (Protocol), and **C** (Essential Records). There is no §5 or higher in Annex 1. The **E6 ref** column cites the Annex-1 subsection that generates the duty (e.g., monitoring is Annex 1 §3.11.4), the Appendix that specifies the document (App A/B), and **App C** where the record appears in the Essential Records Table; the legacy **E6(R2) §8** number is retained as the crosswalk. This is the same scheme the OSSICRO validation engine uses in `engine/registry/documents.json` — the catalog and the engine cite one numbering, not two.
- **E6(R3) shifted "documents" to "records"** to encompass dynamic/electronic content and data, and is **risk-proportionate**: Appendix C §C.1.1 states that the nature and extent of records depend on the trial. Treat this catalog as the *superset*; the applicable subset for a given trial is a documented, risk-based decision (see [[monitoring-plan]] and [[risk-based-monitoring-e6r3]]).
- **Confirmed** = a specific CFR section or FDA form makes the record mandatory. **Conditional** = required only for certain designs (blinded/randomized, DSMB-overseen) or when an event occurs (audit performed). **Interpretive** = best-practice or guidance-derived, not separately mandated by regulation.
- **The sponsor-investigator collapse**: records that normally flow between a sponsor and an investigator become self-directed for the dual-role physician, but the *outward* flows to FDA and [[irb-iec|IRB]] remain. Affected records are flagged.
- **Owner ≠ signatory of judgment.** OSSICRO's [[generate-check-validate-engine|engine]] can draft, version, and completeness-check almost every record below; the **non-delegable** acts embedded in some of them (consent administration, IRB approval, causality, 1571/1572 signatures) are gated to a qualified human — see the [[#Non-delegable acts embedded in these records]] section and [[non-delegable-functions-and-gates]].

---

## A. STARTUP — before-trial essential records

| # | Record | Owner → Receiver | Authority | E6 ref | Status |
|---|--------|------------------|-----------|--------|--------|
| A1 | [[clinical-protocol-and-synopsis|Clinical protocol + amendments]] | Sponsor-investigator → FDA, IRB, DSMB, site, partner | 21 CFR 312.23(a)(6); 312.30 | App B + App C; R2 §8.2.2 | Confirmed |
| A2 | [[clinical-protocol-and-synopsis|Protocol synopsis]] | S-I → IRB, DSMB, partner, sites | ICH E6(R3) App B (as protocol element; no standalone CFR mandate) | App B | Interpretive |
| A3 | [[investigators-brochure|Investigator's Brochure (IB)]] | Sponsor/manufacturer → investigators, IRB, FDA | 21 CFR 312.23(a)(5); 312.55 | App A + App C; R2 §8.2.1 | Confirmed (PI may substitute for marketed drug, 312.55) |
| A4 | [[ind-application-312-23|IND application]] — [[form-fda-1571-ind-cover|Form FDA 1571]] cover | S-I (as sponsor) → FDA/CDER or CBER | 21 CFR 312.23; 312.20; 312.40 | — | Confirmed |
| A5 | [[form-fda-1572-statement-of-investigator|Statement of Investigator — Form FDA 1572]] | Investigator (self-executed) → sponsor (retained; within IND) | 21 CFR 312.53(c)(1); 312.60 | — | Confirmed |
| A6 | [[form-fda-3454-3455-financial-disclosure|Financial disclosure — 3454 / 3455]] | Sponsor collects; each investigator completes → FDA (with marketing app) | 21 CFR Part 54 (54.4); 312.53(c)(4) | — | Confirmed |
| A7 | [[informed-consent-form|Informed Consent Form]] + assent/short form | S-I drafts; IRB approves; investigator administers → IRB, subject, file | 21 CFR 50.20, 50.25, 50.27; 45 CFR 46.116 | Annex 1 §2.8 + App C; R2 §8.2.3 | Confirmed — **administration non-delegable** |
| A8 | [[irb-submission-package|IRB submission package]] | S-I → IRB/IEC | 21 CFR 56.107, 56.109; 312.66 | Annex 1 §1.1/§2.4 | Confirmed |
| A9 | IRB approval letter (initial) + approved-document set | IRB → S-I (files), FDA on request | 21 CFR 56.109, 56.113, 56.115; 312.66 | Annex 1 §1 + App C; R2 §8.2.7 | Confirmed |
| A10 | IRB roster / statement of compliance / assurance | IRB → S-I file | 21 CFR 56.107 | Annex 1 §1.3 + App C; R2 §8.2.8 | Confirmed |
| A11 | FDA IND acknowledgment / safe-to-proceed correspondence | FDA → S-I | 21 CFR 312.20, 312.40, 312.42 | App C (regulatory authorisation/notification) | Confirmed |
| A12 | [[dsmb-charter|DSMB/DMC charter]] + membership | S-I establishes; members adopt → DSMB, IRB, FDA | FDA DMC Guidance (2006); ICH E6(R3) Annex 1 §3.6; 312.23(a)(6)(iii)(g) | Annex 1 §3.6 + App C (IDMC procedures/agreements) | Conditional |
| A13 | [[monitoring-plan|Monitoring plan (risk-based)]] | Sponsor / delegated [[clinical-monitor-cra|monitor]] → monitors, TMF | ICH E6(R3) Annex 1 §3.11.4; FDA RBM Guidance (2013) + RBM Q&A (2023); 21 CFR 312.50, 312.56 | Annex 1 §3.11.4 + App C (trial-specific plans) | Confirmed (form is risk-proportionate) |
| A14 | [[safety-management-plan|Safety management / pharmacovigilance plan]] | S-I → PV function, investigators, FDA | 21 CFR 312.32; 312.64(b); FDA IND Safety Guidance; ICH E2A | Annex 1 §3.13 + App C (trial-specific plans) | Confirmed obligation (written plan best-practice) |
| A15 | [[delegation-of-authority-log|Delegation-of-authority / task-delegation log]] | Investigator/S-I → ISF, monitor, FDA | ICH E6(R3) Annex 1 §2.3 + App C; 21 CFR 312.53(c), 312.60 | Annex 1 §2.3 + App C; R2 §8.3.24 | Confirmed |
| A16 | CVs, medical licenses, GCP training certificates (PI + sub-Is + key staff) | Each individual; investigator compiles → sponsor (in IND), IRB, file | 21 CFR 312.53(c)(2) | Annex 1 §2.1 + App C; R2 §8.2.10 | Confirmed |
| A17 | Central/local laboratory certifications (CLIA/CAP) + accreditations | Laboratory → S-I file, IRB, FDA on request | 42 CFR Part 493; 21 CFR 312.23(a)(6)(iii) | App C; R2 §8.2.12 | Confirmed |
| A18 | Laboratory normal ranges / reference values | Laboratory → S-I file, investigators | 42 CFR 493; 21 CFR 312.62 | App C; R2 §8.2.11 | Confirmed |
| A19 | [[clinical-trial-agreement-and-budget|Clinical Trial Agreement (CTA) + budget]] | Contracting parties → all signatories, files | ICH E6(R3) Annex 1 §3.5–3.6; contract law | Annex 1 §3.5–3.6 + App C (financial arrangement; signed agreements); R2 §8.2.4–8.2.6 | Confirmed (agreement/financing record) |
| A20 | Site feasibility / qualification (pre-study visit report) | Sponsor/partner issues; site completes → sponsor selection file | 21 CFR 312.53(a); ICH E6(R3) Annex 1 §3.7 | Annex 1 §3.7 + App C (site-selection monitoring report); R2 §8.2.20 | Confirmed (form best-practice) |
| A21 | [[regulatory-binder-isf-index|Regulatory binder / ISF index]] | Investigator (site); mirrors sponsor TMF → monitors, FDA | ICH E6(R3) App C §C.2.3–C.2.4; 21 CFR 312.62 | App C §C.2 | Confirmed |
| A22 | Source-document templates / source worksheets | S-I / site designs → site, monitor | ICH E6(R3) Principles + Annex 1 §4.2.1 (data capture); 21 CFR 312.62(b) | Annex 1 §4.2.1 + App C (source records) | Confirmed data-integrity need (templates best-practice) |
| A23 | Blank CRF / eCRF (version-controlled) | Sponsor designs → data management | 21 CFR 312.62(b); ICH E6(R3) Annex 1 §4.2.1 | Annex 1 §4.2.1 + App C (sample data-acquisition tools); R2 §8.2.13 | Confirmed |
| A24 | [[drug-accountability-log|Drug/IP accountability log (initialized)]] + IP management plan | Investigator/pharmacy; sponsor supplies → site file, monitor, FDA | 21 CFR 312.57, 312.61, 312.62(a) | Annex 1 §2.10/§3.15.3 + App C; R2 §8.2.15–8.2.16 | Confirmed |
| A25 | IP labeling / sample labels | Sponsor/manufacturer → site file | 21 CFR 312.6 ("Caution: New Drug…") | Annex 1 §3.15.2 + App C; R2 §8.2.14 | Confirmed |
| A26 | Randomization scheme, blinding, code-break/unblinding SOP | Sponsor (statistician) → site (sealed), pharmacy, DSMB | ICH E6(R3) Annex 1 §2.11/§4.1; 21 CFR 312.23(a)(6) | Annex 1 §2.11/§4.1 + App C (master randomisation list; emergency decoding); R2 §8.2.17–8.2.19 | Conditional (blinded/randomized designs) |
| A27 | Recruitment / advertising materials (IRB-approved) | S-I drafts; IRB approves → IRB, site file | 21 CFR 50.25; 56.111; FDA "Recruiting Study Subjects" | Annex 1 §1.1 + App C (recruitment advertisement) | Confirmed (when advertising used) |
| A28 | Insurance / indemnification certificate | Sponsor/institution → IRB, site file | ICH E6(R3) Annex 1 §3.14 + App C; jurisdiction-dependent | Annex 1 §3.14 + App C (insurance statement); R2 §8.2.9 | Conditional / Interpretive (US) |
| A29 | Manual of Operations / procedures + lab/imaging manuals | S-I → site staff, monitors | ICH E6(R3) App C (trial-specific plans/procedures; pharmacy manual) | App C | Interpretive (best-practice) |

Full working list with sequence and gate annotations: [[startup-tmf-checklist]].

---

## B. CONDUCT — during-trial essential records

| # | Record | Owner → Receiver | Authority | E6 ref | Status |
|---|--------|------------------|-----------|--------|--------|
| B1 | Signed/executed [[informed-consent-form|informed consent forms]] (per subject) | Investigator obtains → site file (originals), subject (copy) | 21 CFR 50.27; 312.62(b) | Annex 1 §2.8 + App C; R2 §8.3.12 | Confirmed — **consenting act non-delegable** |
| B2 | Screening log, enrollment log, subject identification code list | Investigator → site file; monitor verifies | 21 CFR 312.62(b) | App C (screening log; participant ID code list + enrolment log); R2 §8.3.20–8.3.22 | Confirmed |
| B3 | Source documents (completed) + completed CRFs/eCRFs + correction/audit trail | Investigator/site; sponsor holds CRF data → data mgmt, monitor SDV, FDA | 21 CFR 312.62(b); ICH E6(R3) Annex 1 §4.2 | Annex 1 §4.2 + App C (source records; data + metadata); R2 §8.3.13–8.3.14 | Confirmed |
| B4 | [[monitoring-workflow-siv-imv-cov|Monitoring visit reports]] + monitoring log + follow-up letters | Sponsor/[[clinical-monitor-cra|monitor]] ([[micro-cro-accountable-layer|micro-CRO]] where used) → sponsor TMF, site copy | ICH E6(R3) Annex 1 §3.11.4; 21 CFR 312.56 | Annex 1 §3.11.4 + App C (site + centralised monitoring reports); R2 §8.3.10 | Confirmed |
| B5 | [[form-fda-3500a-medwatch|SAE report — investigator-to-sponsor (MedWatch 3500A)]] + AE/SAE logs | Investigator reports → sponsor (safety); investigator separately reports unanticipated problems to IRB (312.66) | 21 CFR 312.64(b); Form 3500A; ICH E2A | Annex 1 §2.7.2 + App C (SAE notification to sponsor); R2 §8.3.16–8.3.18 | Confirmed — **causality/expectedness non-delegable** |
| B6 | [[ind-safety-report|IND safety reports — sponsor 7-day / 15-day]] | S-I (as sponsor) → **FDA + all participating investigators** (312.32(c)); IRB receipt runs via the separate unanticipated-problem route (312.66; 56.108(b)(1)) — see [[safety-reporting-lifecycle]] | 21 CFR 312.32(c); 312.55(b); Form 3500A/narrative | Annex 1 §3.13.2 + App C (SUSAR notifications; sponsor-to-investigator safety information) | Confirmed (self-originated in S-I model) |
| B7 | [[investigators-brochure|Investigator's Brochure updates]] / revisions | Sponsor → investigators, IRB, FDA (IND amendment) | 21 CFR 312.55(b); 312.23(a)(5) | App A + App C; R2 §8.3.1 | Confirmed |
| B8 | Protocol amendments + IRB re-approval | S-I submits → FDA (312.30), IRB (56.110/56.108) | 21 CFR 312.30; 56.108(a), 56.110; 312.66 | App B + App C (protocol + subsequent amendments) | Confirmed |
| B9 | [[irb-review-workflow|IRB continuing review]] / annual re-approval + expedited approvals | IRB → S-I file | 21 CFR 56.108(a), 56.109(f), 56.115 | Annex 1 §1 + App C (interim/annual reports to IRB) | Confirmed (FDA 56 still requires; contrast 2018 Common Rule) |
| B10 | [[ind-annual-report-dsur|IND Annual Report]] | S-I → FDA | 21 CFR 312.33 | App C (interim/annual reports to regulatory authority) | Confirmed |
| B11 | [[dsmb-workflow|DSMB/DMC meeting minutes]] + recommendations + interim-analysis reports | DSMB; sponsor files recs → S-I, IRB, FDA where applicable | FDA DMC Guidance (2006); ICH E6(R3) Annex 1 §3.6 | Annex 1 §3.6 + App C (IDMC procedures, minutes, submissions) | Conditional (DSMB exists) |
| B12 | [[drug-accountability-log|Drug accountability (ongoing)]], shipment/receipt, temperature logs | Sponsor ships/records; investigator/pharmacy dispenses → files, monitor | 21 CFR 312.57, 312.61, 312.62(a) | Annex 1 §2.10/§3.15.3 + App C (accountability; shipping; storage conditions); R2 §8.3.5–8.3.6 | Confirmed |
| B13 | Protocol deviation / violation log + notes to file | Investigator/sponsor → files, IRB (reportable), monitor | ICH E6(R3) Annex 1 §2.5/§3.12; 21 CFR 312.66; 56.108(b) | Annex 1 §2.5/§3.12 + App C (noncompliance records + CAPA) | Confirmed |
| B14 | Correspondence log (sponsor/IRB/FDA/partner) + communications | All parties → TMF/ISF | ICH E6(R3) App C (relevant communications and meetings) | App C; R2 §8.3.11 | Confirmed |
| B15 | Updated CVs/licenses/training + delegation-log updates + new-staff financial disclosures | Investigator/sponsor → files, IRB (new Is via 1572 update) | 21 CFR 312.53(c); 54.4; ICH E6(R3) Annex 1 §2.1 | Annex 1 §2.1 + App C; R2 §8.3.4 | Confirmed |
| B16 | Updated lab certifications / normal-range revisions | Laboratory → S-I file | 42 CFR Part 493 | App C; R2 §8.3.7–8.3.9 | Confirmed |
| B17 | Signature sheet (updated) + site signature/initial log | Investigator/site → site file, monitor | ICH E6(R3) Annex 1 §2.3 + App C; 21 CFR Part 11 (if e-sig) | Annex 1 §2.3 + App C (signature sheet); R2 §8.3.24 | Confirmed |

Full working list with the safety clocks and gate annotations: [[conduct-tmf-checklist]].

---

## C. CLOSEOUT — after-trial essential records

| # | Record | Owner → Receiver | Authority | E6 ref | Status |
|---|--------|------------------|-----------|--------|--------|
| C1 | [[closeout|Study closeout monitoring visit report]] | Sponsor/monitor → sponsor TMF, site copy | ICH E6(R3) Annex 1 §3.11.4 + App C | Annex 1 §3.11.4 + App C (close-out monitoring report); R2 §8.4.1 | Confirmed |
| C2 | [[drug-accountability-log|IP final reconciliation]] + return/destruction records | Investigator/pharmacy + sponsor → sponsor TMF, site file | 21 CFR 312.59; 312.62(a) | App C (IP destruction/alternative disposition); R2 §8.4.2–8.4.3 | Confirmed — **destruction authorization gated** |
| C3 | Notification to FDA of study completion / IND withdrawal or inactivation | S-I → FDA | 21 CFR 312.38; 312.45; 312.33 | — | Confirmed |
| C4 | Final IRB notification of study completion | S-I → IRB | 21 CFR 312.66; 56.108/56.109 | Annex 1 §2.13 + App C (final report to IRB/IEC); R2 §8.4.4 | Confirmed |
| C5 | [[clinical-study-report|Clinical Study Report (CSR)]] | S-I (with statistician) → FDA (if supports marketing app), partner, IRB summary | ICH E3; ICH E6(R3) Annex 1 §3.17.2 + App C; 21 CFR 312.33 | Annex 1 §3.17.2 + App C (interim/final clinical trial reports); R2 §8.4.9 | Confirmed (format per E3) |
| C6 | Treatment allocation / decoding / unblinding documentation | Sponsor/statistician → sponsor TMF, DSMB | ICH E6(R3) Annex 1 §2.11/§4.1 + App C; 21 CFR 312.62 | Annex 1 §2.11/§4.1 + App C (treatment allocation + decoding); R2 §8.4.7 | Conditional (blinded trials) |
| C7 | Audit certificate / statement (if independent audit performed) | Sponsor QA/auditor → sponsor TMF | ICH E6(R3) Annex 1 §3.11.2 + App C | Annex 1 §3.11.2 + App C (audit certificate); R2 §8.4.8 | Conditional (audit performed) |
| C8 | [[clinicaltrials-gov-registration|ClinicalTrials.gov registration + results submission]] | Responsible party (S-I) → NIH/NLM; enforced by FDA | 42 CFR Part 11; FDAAA 801; 42 U.S.C. 282(j) | — | Confirmed (applicable clinical trials) |
| C9 | [[record-retention-and-archival|Record-retention statement + archival]] | S-I + investigator → TMF/ISF (archived) | 21 CFR 312.57(c), 312.62(c); ICH E6(R3) Annex 1 §3.16.3 + App C §C.2.6–C.2.7 | Annex 1 §3.16.3 + App C §C.2; R2 §4.9.5/§5.5.11 | Confirmed |
| C10 | Final subject screening/enrollment logs + final safety reconciliation | Investigator + sponsor safety → sponsor TMF | 21 CFR 312.62(b) | App C (completed screening log; participant ID code list); R2 §8.4.5–8.4.6 | Confirmed |
| C11 | Final financial reconciliation / closeout of CTA payments | Sponsor + site/institution → contracting parties | 21 CFR 54.4; ICH E6(R3) Annex 1 §3.5; contractual | Annex 1 §3.5 | Interpretive / contractual (ties to 54.4 window) |

Full working list with retention-clock detail: [[closeout-tmf-checklist]].

---

## D. DATA GOVERNANCE — computerized-system and service-provider records

E6(R3)'s substantive addition over E6(R2) §8 is this class: Annex 1 §4 (Data Governance) and the Appendix C table make records about the *systems and vendors that touch trial data* essential in their own right. **OSSICRO itself is an in-scope trial computerized system**: its validation documentation, access records, and audit trails belong in this block of the sponsor's TMF, not outside it. This is the record-level substrate of the [[part-11-and-ai-credibility|Part 11 / AI-credibility]] position.

| # | Record | Owner → Receiver | Authority | E6 ref | Status |
|---|--------|------------------|-----------|--------|--------|
| D1 | Trial-specific computerized-system validation documentation (specifications, testing, validation report, change control) — **includes OSSICRO** | Sponsor / system owner → sponsor TMF, FDA/inspector on request | ICH E6(R3) Annex 1 §4.3.4; 21 CFR 11.10(a) | Annex 1 §4.3.4 + App C (trial-specific system validation) | Confirmed |
| D2 | Fitness-for-purpose assessment of non-trial-specific systems used in the trial (e.g., clinical-practice EHR, institutional email/eSignature platforms) | Sponsor/investigator → TMF/ISF | ICH E6(R3) Annex 1 §4.3.1; App C | Annex 1 §4.3 + App C (fitness-for-purpose assessment) | Confirmed |
| D3 | System access and user-account management records (provisioning, role assignment, deprovisioning) | Sponsor / system owner → sponsor TMF | ICH E6(R3) Annex 1 §4.3.3/§4.3.8; 21 CFR 11.10(d), (g) | Annex 1 §4.3.8 | Confirmed |
| D4 | Audit trails + documented audit-trail/metadata review (incl. data-correction documentation) | Sponsor data mgmt / investigator per system → TMF, monitor, inspector | ICH E6(R3) Annex 1 §4.2.2–4.2.4; 21 CFR 11.10(e) | Annex 1 §4.2.2–4.2.3 + App C (data + relevant metadata; corrections) | Confirmed |
| D5 | Service-provider selection, assessment, and oversight documentation + signed sponsor–service-provider agreements — **covers OSSICRO's operator and any [[micro-cro-accountable-layer|micro-CRO]]** | Sponsor → sponsor TMF | ICH E6(R3) Annex 1 §3.3/§3.9; App C; 21 CFR 312.52 where obligations are transferred ([[transfer-of-regulatory-obligations-toro|TORO]]) | Annex 1 §3.3/§3.9 + App C (service-provider selection, assessment, oversight; signed agreements) | Confirmed |
| D6 | Serious/significant noncompliance documentation: root-cause analysis, CAPA, and escalation records (beyond routine deviations in B13) | Sponsor (QA) → sponsor TMF; FDA/IRB where reporting is triggered | ICH E6(R3) Annex 1 §3.12; 21 CFR 312.56(b), 56.108(b) | Annex 1 §3.12 + App C (noncompliance records + CAPA) | Confirmed (E6(R3) duty; note the US has no standalone "serious breach" filing analogous to EU CTR Art. 52 — escalation runs through 312.56/56.108 routes) |
| D7 | Data-security-breach response procedures and breach records | Sponsor / system owner → sponsor TMF | ICH E6(R3) App C §C.3.1(bb) | App C §C.3.1(bb) | Conditional (procedures expected; records if a breach occurs) |

---

## Non-delegable acts embedded in these records

Several records above are *containers* for a judgment that OSSICRO must never make. The record can be drafted, versioned, and completeness-checked by software; the judgment inside it is gated to a qualified human. This is the operating core of the [[non-delegable-functions-and-gates|gating matrix]].

> [!warning] Non-delegable
> - **Administration of informed consent** (A7/B1; 21 CFR 50.20/50.27) — a qualified investigator/designee conducts the consent conversation and obtains the signature. OSSICRO drafts/versions/tracks the [[informed-consent-form|ICF]]; it never *consents* a subject. See [[informed-consent-document-vs-event]].
> - **IRB/IEC approval judgment** (A8/A9/B9; 21 CFR Part 56) — the approve/disapprove determination is the [[irb-iec|IRB's]]. Software prepares the submission package only.
> - **SAE causality and expectedness** (B5/B6; 21 CFR 312.32, 312.64(b); ICH E2A) — relatedness/seriousness/expectedness is the [[medical-monitor|medical monitor's]] clinical judgment. OSSICRO may pre-populate [[form-fda-3500a-medwatch|MedWatch]] fields and enforce the [[safety-clock-engine|7/15-day clocks]]; it never adjudicates causality.
> - **1571 / 1572 signature attestations** (A4/A5; 21 CFR 312.23, 312.53) — the legal commitment is signed by the accountable [[sponsor-investigator]].
> - **Transfer of sponsor obligations** (21 CFR 312.52) — obligations transfer only to a legally accountable entity ([[transfer-of-regulatory-obligations-toro|TORO]] / [[micro-cro-accountable-layer|micro-CRO]]), never to software.
> - **IP destruction authorization** (C2; 21 CFR 312.59) and **eligibility/dosing decisions** — sponsor and investigator judgments, respectively.
> - **CSR scientific conclusions and DSMB stop/continue recommendations** (C5; B11) — human sign-off required.

## OSSICRO validation hooks

Each catalog row is a rule in the [[compliance-mapping|compliance manifest]]: *record → governing authority → validation rule → responsible human sign-off*. The [[generate-check-validate-engine|check pass]] tests a package against the risk-proportionate subset; the [[completeness-ledger]] returns green/amber/red with the exact resolving question for every gap; the [[draft-provenance-model]] links each drafted span to its source datum and citation for the Part-11 audit trail ([[part-11-and-ai-credibility]]). Block D applies reflexively: OSSICRO's own validation records (D1), access records (D3), and audit trails (D4) are themselves essential records the engine must surface in the TMF it manages. Rolled up and signed, the catalog becomes the [[verifiable-site-qualification-dossier]] a [[pharma-partner-sponsor|pharma sponsor]] can trust.

> [!interpretive] OSSICRO position — the applicable subset is a documented decision
> This catalog is the superset. Under E6(R3)'s risk-proportionality (App C §C.1.1, §C.3.3), the subset that applies to a specific trial (single-site open-label Phase 2 vs. multi-site blinded) is itself a recorded, defensible judgment — not a silent omission. OSSICRO surfaces the full catalog, marks each record's applicability with its rationale, and routes "not applicable" determinations to human confirmation rather than dropping records unannounced.

## Related
- [[index]]
- [[startup-tmf-checklist]]
- [[conduct-tmf-checklist]]
- [[closeout-tmf-checklist]]
- [[regulatory-binder-isf-index]]
- [[record-retention-and-archival]]
- [[safety-reporting-lifecycle]]
- [[risk-based-monitoring-e6r3]]
- [[part-11-and-ai-credibility]]
- [[phase-model-overview]]
- [[non-delegable-functions-and-gates]]
- [[generate-check-validate-engine]]
- [[completeness-ledger]]
- [[compliance-mapping]]
- [[verifiable-site-qualification-dossier]]
- [[sponsor-investigator]]

## Sources
- [ICH E6(R3) Step 4 Final Guideline — Annex 1 + Appendices A–C](https://database.ich.org/sites/default/files/ICH_E6(R3)_Step4_FinalGuideline_2025_0106.pdf)
- [ICH GCP — Appendix C: Essential Records for the Conduct of a Clinical Trial](https://ichgcp.net/appendix-c-ich-e6-r3)
- [FDA — E6(R3) Good Clinical Practice (GCP), final guidance (September 2025)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e6r3-good-clinical-practice-gcp)
- [EMA — ICH E6(R3) Guideline on GCP, Step 5](https://www.ema.europa.eu/en/documents/scientific-guideline/ich-e6-r3-guideline-good-clinical-practice-gcp-step-5_en.pdf)
- [FDA — Oversight of Clinical Investigations: A Risk-Based Approach to Monitoring (2013)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/oversight-clinical-investigations-risk-based-approach-monitoring)
- [FDA — A Risk-Based Approach to Monitoring of Clinical Investigations: Questions and Answers (final, April 2023)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/risk-based-approach-monitoring-clinical-investigations-questions-and-answers)
- [eCFR — 21 CFR Part 312 Subpart D (Responsibilities of Sponsors and Investigators)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D)
- [eCFR — 21 CFR Part 54 (Financial Disclosure by Clinical Investigators)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-54)
- [FDA — IND Forms and Instructions (1571, 1572, 3454, 3455)](https://www.fda.gov/drugs/investigational-new-drug-ind-application/ind-forms-and-instructions)
- [FDA — Financial Disclosure by Clinical Investigators](https://www.fda.gov/science-research/clinical-trials-and-human-subject-protection/financial-disclosures-clinical-investigator)
- [NIH Clinical Center — Initial IND Application](https://www.cc.nih.gov/orcs/ind/initial-ind-application)
