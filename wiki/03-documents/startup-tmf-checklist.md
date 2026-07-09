---
title: "Startup TMF Checklist — Before-Trial Essential Records"
section: "03-documents"
status: mixed
governing_authority:
  - "ICH E6(R3) Appendix C (before-trial essential records); E6(R2) §8.2"
  - "21 CFR 312.20–312.23, 312.40, 312.53 (IND, may-proceed, investigator selection)"
  - "21 CFR Part 50 (consent); 21 CFR Part 56 (IRB); 21 CFR Part 54 (financial disclosure)"
tags: [lifecycle/activation, lifecycle/ind, lifecycle/irb, gcp/e6r3, cfr/312, cfr/50, cfr/56, ossicro/gating, status/mixed]
aliases: ["startup checklist", "before-trial documents", "site activation checklist", "green-light package"]
updated: 2026-07-09
---

# Startup TMF Checklist — Before-Trial Essential Records

> [!authority] Governing authority
> **ICH E6(R3) Appendix C** (before-trial essential records), with **E6(R2) §8.2** cross-numbering; **21 CFR 312.20–312.23** (IND), **312.40** (may-proceed), **312.53** (investigator selection/1572/financial disclosure); **21 CFR Part 50** (consent), **Part 56** (IRB), **Part 54** (financial disclosure). Status: **Mixed** — items are tagged Confirmed / Conditional / Interpretive.

This is the before-trial working checklist: the records that must exist, and the two hard gates that must clear, before **any subject is screened or dosed**. It is the site-activation "green-light" package for both [[two-modes-site-vs-sponsor-investigator|Mode A (physician-as-site)]] and [[two-modes-site-vs-sponsor-investigator|Mode B (sponsor-investigator IND)]]; the [[expanded-access-workflow|expanded-access]] branch uses a reduced set ([[form-fda-3926-expanded-access|Form 3926]] + manufacturer LOA + IRB concurrence). Full authority mapping for every row is in the [[document-catalog]] (section A). This page adds sequence, dependency, and the gate annotations OSSICRO enforces.

## The two hard gates before first enrollment

> [!warning] Non-delegable
> **Gate 1 — IND in effect.** No investigational drug subject to 21 CFR 312.2(a) is administered until the IND is in effect: 30 days after FDA receipt of the [[form-fda-1571-ind-cover|1571]]-covered [[ind-application-312-23|IND]] (or earlier FDA "may proceed" notice), and not on clinical hold (21 CFR 312.40, 312.42). See [[ind-submission-and-30-day-clock]].
>
> **Gate 2 — Documented IRB approval.** No subject is enrolled before the reviewing [[irb-iec|IRB]] issues written approval of the protocol and the version-stamped [[informed-consent-form|ICF]] (21 CFR 56.109, 56.115; 312.66). The IRB's approve/disapprove judgment is non-delegable. See [[irb-submission-and-approval]].
>
> OSSICRO **blocks** the site-activation package from reaching "ready to enroll" until both gate records are present and current; it never simulates or presumes either. These are the load-bearing gates of [[site-activation]].

## 1. Scientific and product records

- [ ] **[[clinical-protocol-and-synopsis|Clinical protocol]]** (signed, version-controlled) — full-detail for Phase 2 (not a Phase 1 outline); objectives, design, eligibility, statistics, safety/stopping rules. *21 CFR 312.23(a)(6); Confirmed.*
- [ ] **[[clinical-protocol-and-synopsis|Protocol synopsis]]** — 2–5 page structured abstract for IRB/DSMB/partner review. *ICH E6(R3) §7; Interpretive (universal in practice).*
- [ ] **[[investigators-brochure|Investigator's Brochure]]** (current) — or, for a lawfully marketed drug studied under IND, the approved **package insert** substitute. *21 CFR 312.23(a)(5), 312.55; Confirmed.*
- [ ] **IP labeling / sample labels** — investigational-use caution statement ("Caution: New Drug — Limited by Federal law to investigational use"). *21 CFR 312.6; Confirmed.*
- [ ] **Randomization scheme + blinding + code-break/unblinding SOP** — sealed emergency-unblinding procedure. *21 CFR 312.23(a)(6); Conditional (randomized/blinded designs).*

## 2. Regulatory submission records (the IND)

- [ ] **[[form-fda-1571-ind-cover|Form FDA 1571]]** — IND cover; sponsor signature commits to the 30-day hold, no-conduct-on-hold, and Part 56 IRB oversight. *21 CFR 312.23(a)(1); Confirmed. **Signature non-delegable.***
- [ ] **Full 312.23 content** — introductory statement + general investigational plan, IB, protocol(s), CMC, pharm/tox, previous human experience, additional info. *21 CFR 312.23; Confirmed.* See [[ind-application-312-23]].
- [ ] **[[form-fda-3674-clinicaltrialsgov-certification|Form FDA 3674]]** — ClinicalTrials.gov registration certification accompanying the IND. *42 CFR Part 11 / FDAAA 801; Confirmed for applicable trials.*
- [ ] **FDA IND acknowledgment / safe-to-proceed correspondence** — IND number assigned; may-proceed or clinical-hold notice. *21 CFR 312.20, 312.40, 312.42; Confirmed.* **(Gate 1 record.)**

## 3. Investigator qualification and financial records

- [ ] **[[form-fda-1572-statement-of-investigator|Form FDA 1572]]** — Statement of Investigator; site, IRB, sub-investigators, facilities named. In the [[sponsor-investigator]] model this is self-executed and retained by the S-I within the IND. *21 CFR 312.53(c)(1), 312.60; Confirmed. **Signature non-delegable.***
- [ ] **[[form-fda-3454-3455-financial-disclosure|Financial disclosure — Form 3454 (certification) / 3455 (disclosure)]]** for PI + each sub-investigator; collected **before** participation. In the S-I model this becomes a **self-disclosure** (the physician cannot certify away their own interest). *21 CFR Part 54 (54.4), 312.53(c)(4); Confirmed.*
- [ ] **CVs, medical licenses, GCP training certificates** — PI + sub-investigators + key staff; current and dated. *21 CFR 312.53(c)(2); Confirmed.*
- [ ] **[[delegation-of-authority-log|Delegation-of-authority / task-delegation log]]** — who is delegated which task, with signatures, dates, and training evidence. *ICH E6(R3) §2; 21 CFR 312.53(c), 312.60; Confirmed.*
- [ ] **Site signature/initial log (initialized)** — maps every signature/initial to a named authorized person. *ICH E6(R3) §2; Part 11 if electronic; Confirmed.*

## 4. Ethics records (the IRB package and approval)

- [ ] **[[irb-submission-package|IRB submission package]]** — protocol, ICF, IB, recruitment materials, investigator CV, 1572, budget/COI, agreement. *21 CFR 56.107, 56.109, 312.66; Confirmed.*
- [ ] **[[informed-consent-form|Informed Consent Form]]** + assent/short form (draft submitted to IRB) — 8 basic + additional elements per 21 CFR 50.25. *21 CFR 50.20, 50.25, 50.27; Confirmed. **Administration non-delegable.***
- [ ] **Recruitment / advertising materials** (IRB-approved). *21 CFR 50.25, 56.111; Confirmed (when used).*
- [ ] **IRB approval letter (initial)** + version-stamped approved-document set + approval/expiration dates. *21 CFR 56.109, 56.113, 56.115, 312.66; Confirmed.* **(Gate 2 record.)**
- [ ] **IRB roster / statement of compliance / assurance** — evidence the IRB is constituted per Part 56. *21 CFR 56.107; Confirmed.*

## 5. Oversight and safety records

- [ ] **[[monitoring-plan|Monitoring plan (risk-based)]]** — scope, methods (on-site/central/RBM), frequency, SDV approach, escalation. *ICH E6(R3) §6.9; FDA RBM Guidance (2013, rev.); 21 CFR 312.50, 312.56; Confirmed (form risk-proportionate).* See [[risk-based-monitoring-e6r3]].
- [ ] **[[safety-management-plan|Safety management / pharmacovigilance plan]]** — AE/SAE collection, causality/expectedness workflow, [[safety-report-timelines-7-15-day|7-day/15-day]] IND safety-report timelines, MedWatch routing, partner reconciliation. *21 CFR 312.32, 312.64(b); ICH E2A; Confirmed obligation (written plan best-practice).*
- [ ] **[[dsmb-charter|DSMB/DMC charter]]** + membership — mandate, stopping guidelines, cadence, unblinding procedure. *FDA DMC Guidance (2006); ICH E6(R3) §5; Conditional (higher-risk/blinded early-phase).* See [[dsmb-dmc]].

## 6. Operational, laboratory, and agreement records

- [ ] **[[clinical-trial-agreement-and-budget|Clinical Trial Agreement (CTA) + budget]]** — executed; scope, indemnification, IP, publication, FMV-set payment schedule. *ICH E6(R3) §5; Confirmed (agreement/financing record).*
- [ ] **Site feasibility / qualification (pre-study visit report)** — sponsor's investigator-selection due diligence. *21 CFR 312.53(a); Confirmed (form best-practice).*
- [ ] **Laboratory certifications (CLIA/CAP)** + accreditations. *42 CFR Part 493; Confirmed.*
- [ ] **Laboratory normal ranges / reference values** (version/date-controlled). *42 CFR 493; 21 CFR 312.62; Confirmed.*
- [ ] **[[regulatory-binder-isf-index|Regulatory binder / ISF index]]** (initialized) — the master TOC controlling location/version of every essential record. *ICH E6(R3) §C.2; 21 CFR 312.62; Confirmed.*
- [ ] **Source-document templates / worksheets** — ALCOA-C source capture. *ICH E6(R3) §6; 21 CFR 312.62(b); Confirmed data-integrity need.*
- [ ] **Blank CRF / eCRF** (version-controlled). *21 CFR 312.62(b); Confirmed.*
- [ ] **[[drug-accountability-log|Drug/IP accountability log (initialized)]]** + IP management plan — receipt/storage/dispensing/return chain of custody. *21 CFR 312.57, 312.61, 312.62(a); Confirmed.*
- [ ] **Insurance / indemnification certificate** — where local law/IRB requires. *ICH E6(R3) App C; Conditional/Interpretive (US).*
- [ ] **Manual of Operations / procedures + lab/imaging manuals**. *ICH E6(R3) §6.9/§7; Interpretive (best-practice).*

## Sponsor-investigator collapse at startup

In [[two-modes-site-vs-sponsor-investigator|Mode B]] the same physician signs the **1571 (as sponsor)** and executes the **1572 (as investigator)**, and the financial disclosure becomes a self-disclosure. The IB may be authored by the S-I or supplied by the [[pharma-partner-sponsor|pharma manufacturer]] who provides drug. None of the startup obligations disappear when the roles merge — they are simply held by one accountable person. FDA's **2015 draft guidance** on sponsor-investigator INDs is the on-point walkthrough (cite as current thinking, not a mandate). See [[sponsor-cro-site-coordination]].

## How OSSICRO drives the startup package

> [!interpretive] OSSICRO position
> OSSICRO's [[generate-check-validate-engine|engine]] instantiates each drafted record (protocol to M11 schema, forms auto-populated from CV/site/financial data), then the **check** pass tests the package against the risk-proportionate startup subset of the [[document-catalog]]. The [[completeness-ledger]] renders the checklist live: **green** where validated, **amber** where a human judgment is required (e.g., the sponsor's "reasonably safe" conclusion, the IRB submission's readiness), **red** where a required record is missing with the exact resolving question. The package cannot advance past **Gate 1** or **Gate 2** in software — those are human-authorized/IRB-issued events. The signed rollup is the [[verifiable-site-qualification-dossier]] that makes a new site credible to a [[pharma-partner-sponsor|pharma sponsor]].

> [!warning] Non-delegable
> At startup the gated acts are: the **1571/1572 signatures**, the **IRB approval**, the **consent process design sign-off**, and the sponsor's **"reasonably safe to proceed" conclusion** (21 CFR 312.23(a)(8)). OSSICRO checks completeness and timeliness; qualified humans own the judgments and the submissions. See [[non-delegable-functions-and-gates]].

## Related
- [[document-catalog]]
- [[conduct-tmf-checklist]]
- [[closeout-tmf-checklist]]
- [[site-activation]]
- [[ind-submission-and-30-day-clock]]
- [[irb-submission-and-approval]]
- [[ind-application-312-23]]
- [[form-fda-1571-ind-cover]]
- [[form-fda-1572-statement-of-investigator]]
- [[informed-consent-form]]
- [[monitoring-plan]]
- [[safety-management-plan]]
- [[non-delegable-functions-and-gates]]
- [[completeness-ledger]]
- [[verifiable-site-qualification-dossier]]

## Sources
- [ICH E6(R3) Step 4 Final Guideline — Appendix C](https://database.ich.org/sites/default/files/ICH_E6(R3)_Step4_FinalGuideline_2025_0106.pdf)
- [eCFR — 21 CFR 312.23 (IND content and format)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.23)
- [eCFR — 21 CFR 312.40 (may-proceed)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-C/section-312.40)
- [eCFR — 21 CFR 312.53 (selecting investigators; 1572, CV, financial disclosure)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.53)
- [eCFR — 21 CFR 56.109 / 56.115 (IRB review and records)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56)
- [FDA — IND Forms and Instructions (1571, 1572, 3454, 3455)](https://www.fda.gov/drugs/investigational-new-drug-ind-application/ind-forms-and-instructions)
- [FDA Draft Guidance (2015) — IND Applications Prepared and Submitted by Sponsor-Investigators](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/investigational-new-drug-applications-prepared-and-submitted-sponsor-investigators)
