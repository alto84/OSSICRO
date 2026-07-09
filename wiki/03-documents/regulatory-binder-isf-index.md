---
title: "Regulatory Binder / ISF Index — Investigator Site File Table of Contents"
section: "03-documents"
status: mixed
governing_authority:
  - "ICH E6(R3) §C.2 (management of essential records) + Appendix C"
  - "21 CFR 312.57 (sponsor recordkeeping); 21 CFR 312.62 (investigator recordkeeping)"
  - "ICH E6(R2) §8 (essential documents) — cross-numbering reference"
tags: [lifecycle/activation, lifecycle/conduct, lifecycle/retention, gcp/e6r3, cfr/312, ossicro/engine, ossicro/gating, status/mixed]
aliases: ["regulatory binder", "ISF index", "Investigator Site File", "reg binder TOC", "regulatory binder table of contents"]
updated: 2026-07-09
---

# Regulatory Binder / ISF Index — Investigator Site File Table of Contents

> [!authority] Governing authority
> **ICH E6(R3) §C.2** (management of essential records) and **Appendix C** (the essential-records set); **21 CFR 312.57** (sponsor disposition/financial records) and **21 CFR 312.62** (investigator case histories and drug-disposition records); with **ICH E6(R2) §8** section numbers retained as a cross-reference because most institutional binders in circulation were built to the R2 list. Status: **Mixed** — the requirement that essential records be *readily identifiable and retrievable* is Confirmed; the specific tab structure below is an interpretive best-practice arrangement (Stanford CRQ / Harvard Catalyst / BU CRRO model), not a regulatory mandate.

The **regulatory binder** — synonymous with the **Investigator Site File (ISF)** in ICH usage — is the site-held half of the trial documentation. The **[[document-catalog|Trial Master File (TMF)]]** is the sponsor-held half; the ISF is the investigator-held mirror at the site. This page specifies the **index** — the version-controlled table of contents that governs where every essential record lives, in what version, and who owns it. Under [ICH E6(R3) §C.2](https://database.ich.org/sites/default/files/ICH_E6(R3)_Step4_FinalGuideline_2025_0106.pdf) the operative standard is not a fixed list of tabs but the ability to *reconstruct and evaluate the conduct of the trial* — records must be attributable, complete, and retrievable regardless of medium or location. The index is the artifact that makes that reconstruction possible; it is the first thing an FDA [BIMO inspector](../01-roles-responsibilities/fda-as-counterparty.md) or a [monitor](../01-roles-responsibilities/clinical-monitor-cra.md) asks for.

In the [[sponsor-investigator]] model the TMF/ISF distinction largely collapses: one physician holds both the sponsor's disposition and financial records (§ 312.57) and the investigator's case histories and drug records (§ 312.62). The two record sets do not merge into one undifferentiated pile, however — the accountability behind each remains distinct, and the index must still show which record discharges which obligation. OSSICRO's engine treats the regulatory-binder index as its **primary output artifact**: the [[generate-check-validate-engine|generate/check/validate]] pipeline is, at bottom, a binder-assembly-and-completeness engine.

## What the index is (and is not)

The index is **a map, not the records themselves**. Each row points to a record, names the governing authority, states the current version and date, identifies the owner and receiver, and carries a present/absent/not-applicable status. E6(R3)'s risk-proportionality principle applies: not every tab is mandatory for every trial (a single-site open-label study has no randomization/unblinding tab), so the index must mark *not-applicable-with-rationale* distinctly from *missing*. Conflating "N/A" with "absent" is the most common binder defect an inspector cites.

> [!interpretive] OSSICRO position
> OSSICRO generates a **per-trial** binder index rather than a generic template. Prior art is explicit: Vanderbilt's V-CAP produces a *personalized* required-approvals checklist from structured study inputs (PMC3767144), and Stanford's Clinical Research Quality (CRQ) service distributes a "Regulatory Binder Table of Contents (IND studies)" as its flagship deliverable. OSSICRO reimplements this pattern independently: from the Study, Site, IND, and Obligation entities in the [[data-model]], it emits the index tailored to the trial's mode, phase, blinding, and risk tier — then drives the [[completeness-ledger]] against it. The tab numbering follows Penn's numbered document-control scheme (e.g., 03.01.01) so every record has a stable, citable identifier.

## Canonical tab structure

The arrangement below is the OSSICRO default, synthesized from the Stanford CRQ, Harvard Catalyst (Regulatory Binder 2025), BU CRRO, and Colorado Anschutz templates. Section letters mirror the lifecycle checklists ([[startup-tmf-checklist|startup]] / [[conduct-tmf-checklist|conduct]] / [[closeout-tmf-checklist|closeout]]); each tab maps to a row in the [[document-catalog]] with its full authority citation.

### Tab 1 — Protocol and amendments
- Signed, version-controlled **[[clinical-protocol-and-synopsis|protocol]]** and every executed amendment; protocol signature page. *21 CFR 312.23(a)(6), 312.30.*
- **Synopsis** for rapid review. *ICH E6(R3) §7 (interpretive).*

### Tab 2 — Investigator's Brochure
- Current **[[investigators-brochure|IB]]**, superseded versions retained; or the marketed-drug package-insert substitute. *21 CFR 312.23(a)(5), 312.55.*

### Tab 3 — IND and FDA correspondence
- **[[form-fda-1571-ind-cover|Form FDA 1571]]** and the **[[ind-application-312-23|full 312.23 submission]]** index; **[[form-fda-3674-clinicaltrialsgov-certification|Form FDA 3674]]**; the **FDA IND acknowledgment / safe-to-proceed** letter and IND number; all subsequent FDA correspondence, meeting minutes, and any **clinical-hold** notice/response. *21 CFR 312.20, 312.23, 312.40, 312.42.*

### Tab 4 — IRB records
- **[[irb-submission-package|IRB submission package]]**, **IRB approval letter (initial)** with version-stamped approved documents, **continuing-review** approvals, amendment approvals, IRB correspondence, and the **IRB roster / statement of compliance / assurance**. *21 CFR 56.107–56.115, 312.66.* See [[irb-review-workflow]].

### Tab 5 — Informed consent
- IRB-approved **[[informed-consent-form|ICF]]** (all versions and translations), assent/short forms, and — during conduct — the **signed-consent log** (originals filed per site policy; the log lives here). *21 CFR 50.20–50.27.* The **consent event** is not a document (see [[informed-consent-document-vs-event]]).

### Tab 6 — Investigator qualification and financial disclosure
- **[[form-fda-1572-statement-of-investigator|Form FDA 1572]]**; **CVs, medical licenses, GCP training** certificates (PI + sub-investigators + key staff); **[[form-fda-3454-3455-financial-disclosure|Financial disclosure — Form 3454/3455]]** for each; **[[delegation-of-authority-log|delegation-of-authority log]]** and site signature/initial log. *21 CFR 312.53(c)(1)–(4), 312.60; Part 54; ICH E6(R3) §2.*

### Tab 7 — Laboratory and technical
- **CLIA/CAP** certifications, **normal ranges / reference values** (version/date-controlled), equipment calibration/accreditation. *42 CFR Part 493; 21 CFR 312.62.*

### Tab 8 — Agreements and financial
- Executed **[[clinical-trial-agreement-and-budget|CTA and budget]]**, indemnification/insurance certificates, **site feasibility / pre-study qualification** report, and (Mode B) the **[[transfer-of-regulatory-obligations-toro|TORO]]** instrument if any obligation is transferred to the [[micro-cro-accountable-layer|micro-CRO]]. *ICH E6(R3) §5; 21 CFR 312.52, 312.53(a).*

### Tab 9 — Monitoring
- **[[monitoring-plan|Risk-based monitoring plan]]**; **SIV / IMV / COV** visit reports and follow-up letters. *ICH E6(R3) §6.9; FDA RBM guidance.* See [[monitoring-workflow-siv-imv-cov]].

### Tab 10 — Safety and oversight
- **[[safety-management-plan|Safety management / pharmacovigilance plan]]**; **AE/SAE logs**; **[[ind-safety-report|IND safety reports (7-/15-day)]]**; investigator→sponsor SAE reports; **unanticipated-problem** reports to the IRB; **[[dsmb-charter|DSMB/DMC charter]]**, membership, and recommendation letters (open-session output filed here; closed-session data stays behind the firewall). *21 CFR 312.32, 312.64(b); FDA DMC guidance.* See [[safety-reporting-workflow]].

### Tab 11 — Investigational product
- **[[drug-accountability-log|Drug/IP accountability log]]**, receipt/shipment records, storage/temperature logs, IP labeling samples, return/destruction records, and the randomization/unblinding SOP (sealed). *21 CFR 312.57, 312.59, 312.61, 312.62; 312.6.*

### Tab 12 — Data collection
- **Blank CRF/eCRF** (version-controlled), **source-document templates/worksheets**, data-management and code-list documentation. *21 CFR 312.62(b); ICH E6(R3) §6.*

### Tab 13 — Annual and periodic reports
- **[[ind-annual-report-dsur|IND annual report / DSUR]]** copies (312.33), progress reports, IB-update transmittals. *21 CFR 312.33; ICH E2F.*

### Tab 14 — Closeout and retention
- Final monitoring/close-out visit report, drug reconciliation and destruction records, **[[clinical-study-report|CSR]]**, **[[clinicaltrials-gov-registration|ClinicalTrials.gov]]** results confirmation, final IRB notification, IND completion/withdrawal (312.38)/inactivation (312.45), and the **record-retention statement**. *21 CFR 312.38, 312.45, 312.57(c), 312.62(c).* See [[closeout]] and [[record-retention-and-archival]].

## E6(R3) shift: "records," not "documents"

E6(R3) deliberately renamed *essential documents* to **essential records** to encompass dynamic and electronic content (audit trails, database exports, system validation evidence) that a paper binder cannot hold. The index must therefore point to electronic locations — an eISF/eTMF path, an EDC export, a validated-system audit trail — not only to physical tabs. The E6(R2) **2-year fixed retention** language was removed; retention now defers to applicable regulatory and contractual requirements (in the US, the 21 CFR 312.57(c)/312.62(c) rules govern). OSSICRO stores the index as structured data with each record's medium, location, hash, and version, so a "binder" is a *view* over the record graph, not a filing cabinet. See [[part-11-and-ai-credibility]] for the electronic-records treatment.

## Non-delegable and gating notes

> [!warning] Non-delegable
> The binder index is clerical infrastructure OSSICRO may fully automate — assembling, versioning, and completeness-checking it is exactly the coordination labor the system exists to absorb. But the **records it points to** are discharged by accountable humans: the [[form-fda-1571-ind-cover|1571]]/[[form-fda-1572-statement-of-investigator|1572]] signatures, the [[irb-iec|IRB]] approval, the causality determinations behind the safety reports, and the sponsor's disposition judgments. OSSICRO must never generate a *record* that requires a human attestation and mark it present on the strength of its own draft; a drafted-but-unsigned record is tracked as **amber** (awaiting the named human), never green. The index cannot report "inspection-ready" until every gated record carries a real human signature. See [[non-delegable-functions-and-gates]].

> [!interpretive] OSSICRO position
> The completed, signed binder index is the backbone of the **[[verifiable-site-qualification-dossier]]**: a citation-complete, hash-chained manifest (requirement → record → citation → signer) that a [[pharma-partner-sponsor|pharma sponsor]] can verify without a pre-study site visit. Turning "a new site with no track record" into "a site with a cryptographically verifiable regulatory binder" is the pharma-trust wedge and the tangible product of the [[micro-cro-accountable-layer|micro-CRO]] layer. Every auto-populated index entry carries its provenance per the [[draft-provenance-model]] so the manifest doubles as the [ALCOA++](../05-ossicro-system/part-11-and-ai-credibility.md) audit trail.

## Related
- [[document-catalog]]
- [[startup-tmf-checklist]]
- [[conduct-tmf-checklist]]
- [[closeout-tmf-checklist]]
- [[delegation-of-authority-log]]
- [[drug-accountability-log]]
- [[ind-annual-report-dsur]]
- [[ind-safety-report]]
- [[clinicaltrials-gov-registration]]
- [[record-retention-and-archival]]
- [[verifiable-site-qualification-dossier]]
- [[completeness-ledger]]
- [[non-delegable-functions-and-gates]]

## Sources
- [ICH E6(R3) Step 4 Final Guideline — §C.2 and Appendix C](https://database.ich.org/sites/default/files/ICH_E6(R3)_Step4_FinalGuideline_2025_0106.pdf) — local: `../../sources/ich/ICH_E6R3_Step4_FinalGuideline_2025-01-06.pdf`
- [eCFR — 21 CFR 312.57 (sponsor recordkeeping)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.57)
- [eCFR — 21 CFR 312.62 (investigator recordkeeping)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.62)
- [Harvard Catalyst — Regulatory Binder (2025)](https://catalyst.harvard.edu/wp-content/uploads/regulatory/Regulatory-Binder-2025.pdf)
- [Stanford Medicine CRQ — IND/IDE Tools and Templates (Regulatory Binder Table of Contents)](https://med.stanford.edu/spectrum/researcher-resources/clinical-research-quality-crq/ind_ide-tools-and-templates.html)
- [BU CRRO — Regulatory Binder FAQs](https://www.bumc.bu.edu/crro/files/2019/06/Regulatory-binder-FAQs-6-26-2019.pdf) — local: `../../sources/protocol-template/bu-crro-regulatory-binder-faqs.pdf`
- Vanderbilt V-CAP required-approvals checklist — PMC3767144
