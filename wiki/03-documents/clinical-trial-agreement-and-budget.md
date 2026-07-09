---
title: "Clinical Trial Agreement and Budget"
section: "03-documents"
status: mixed
governing_authority:
  - "State contract law (the CTA is a private contract, not an FDA filing)"
  - "ICH E6(R3) Appendix C; ICH E6(R2) §§8.2.4–8.2.6 (essential records: financial aspects, insurance, signed agreements)"
  - "42 U.S.C. §1320a-7b(b) (Anti-Kickback Statute)"
  - "42 CFR 1001.952(d) (personal services and management contracts safe harbor)"
  - "42 CFR 403.900–403.914 (Physician Payments Sunshine Act / Open Payments)"
tags: [ich/e6r3, usc/1320a-7b, role/sponsor, role/investigator, role/pharma, lifecycle/activation, ossicro/gating, status/confirmed, status/interpretive]
aliases: ["CTA", "Clinical Trial Agreement", "study budget"]
updated: 2026-07-09
---

# Clinical Trial Agreement and Budget

> [!authority] Governing authority
> The CTA is a private contract governed by state law — there is no FDA form and no FDA filing. Its regulatory footprint is threefold: (1) it is an essential record of the trial (ICH E6(R3) Appendix C; ICH E6(R2) §§8.2.4–8.2.6 — financial aspects, insurance statement, signed agreement between involved parties); (2) its payment terms are constrained by the federal Anti-Kickback Statute (42 U.S.C. §1320a-7b(b)), with compliance structured against the personal-services safe harbor (42 CFR 1001.952(d)); (3) payments made under it by an applicable manufacturer are publicly reportable under the Physician Payments Sunshine Act (42 CFR 403.900–403.914). Status: **Mixed** — the essential-record status and fraud-and-abuse constraints are confirmed; OSSICRO's drafting and validation positions are interpretive and flagged.

The Clinical Trial Agreement (CTA) is the executed contract among the trial [[sponsor]], the site/institution, and — where the institution is a distinct party — the [[investigator]], that makes a protocol legally performable at a site: who does what, who pays for what, who is liable for what, who owns what, and who may publish what. The **budget** is its financial exhibit. FDA never reviews the CTA, but a monitor, an auditor, and a BIMO inspector will expect to find it in the [[regulatory-binder-isf-index|site file]] and the sponsor TMF, and federal prosecutors read trial budgets when investigating inducement. For the physician-investigators OSSICRO serves, the CTA and budget are consistently among the slowest [[site-activation]] documents; OSSICRO drafts them completely, then routes them through the two human gates neither software nor the physician may skip: institutional/legal signature and the fair-market-value (FMV) determination.

## Function and legal character

The CTA is **not** a regulatory submission. It is enforceable private law between the parties, layered on top of (never substituting for) the regulatory obligations of 21 CFR Part 312: an investigator's [[form-fda-1572-statement-of-investigator|Form FDA 1572]] commitments and a sponsor's Subpart D duties exist independently of any contract term. What the CTA adds is the allocation of *costs and civil risk* — and, under ICH GCP, its existence is itself an essential record: E6(R2) §8.2.4 (documentation of the financial agreement between investigator/institution and sponsor), §8.2.5 (insurance statement, where required), and §8.2.6 (signed agreement between involved parties), carried forward in the E6(R3) Appendix C essential-records framework. See [[document-catalog]] and [[startup-tmf-checklist]].

## Parties and configurations

| Configuration | Instrument | Notes |
|---|---|---|
| **Mode A — pharma-sponsored trial, physician as site** | Two-party (sponsor–institution) or three-party (sponsor–institution–PI) CTA | The dominant industry pattern; a [[cro]] may sign as the sponsor's contracting agent. See [[pharma-partner-sponsor]] and [[sponsor-cro-site-coordination]]. |
| **Mode B — investigator-initiated study (IIS)** | Grant / research **support agreement** from the pharma supporter to the [[sponsor-investigator]] | Not a CTA in the site sense: the physician holds the IND; pharma supplies drug and/or funding. FMV discipline and documented scientific-merit review keep support from looking like inducement. See [[iis-request-workflow]]. |
| **Single-patient / n-of-1** | Abbreviated support terms plus the manufacturer's letter of authorization | See [[single-patient-site-enrollment]] and [[single-patient-site-and-pharma-acceptance]]; expanded access uses supply terms, not a trial budget ([[expanded-access-workflow]]). |

Standardized master templates — notably the CTSA-consortium **Accelerated Clinical Trial Agreement (ACTA)** and institutional master CTAs — exist precisely because clause-by-clause negotiation is the single largest activation delay at academic sites; OSSICRO's template library seeds from these public models.

## Core articles of a CTA

| Article | Content | Compliance anchor |
|---|---|---|
| Scope of work | Incorporates the [[clinical-protocol-and-synopsis|protocol]] by reference; version-controls amendments | Protocol adherence duty, 21 CFR 312.60 |
| Payment terms & budget | Payment schedule tied to milestones/visits; holdbacks; invoicing | AKS/FMV (below) |
| Indemnification | Typically: sponsor indemnifies site/investigator for claims arising from protocol-directed conduct and the product itself; carve-outs for site negligence, malpractice, and protocol violation | Contract law; E6(R2) §8.2.5 insurance evidence |
| Subject injury | Sponsor pays reasonable costs of treating research-related injury | Must be **consistent with the ICF injury language** — 21 CFR 50.25(a)(6); see [[informed-consent-form]] |
| Insurance | Evidence of coverage (product liability; site professional liability) | E6(R2) §8.2.5 (where required) |
| Intellectual property | Sponsor typically owns study data and inventions arising from performance of the protocol; parties retain background IP | Contract law |
| Publication | Investigator right to publish after sponsor review window (commonly 30–90 days) plus a bounded delay for patent filing; multicenter-first conventions; **no permanent suppression** | Academic norms; ICMJE |
| Confidentiality | Sponsor confidential information; survives termination | Contract law |
| Regulatory compliance | GCP/Part 312 compliance representations; **debarment certification** (no debarred person used, FD&C Act §306, 21 U.S.C. §335a); audit and inspection access | 21 CFR 312.58, 312.68 |
| Records & retention | Retention consistent with 21 CFR 312.57(c)/312.62(c) | See [[record-retention-and-archival]] |
| Term & termination | Termination for safety, IRB withdrawal, non-enrollment; wind-down and drug-return duties | 21 CFR 312.59; [[drug-accountability-log]] |

## The budget

A compliant budget is built **from the protocol's schedule of assessments outward**, never from a revenue target backward:

- **Per-visit / per-procedure costs** — each protocol-required procedure priced at a defensible local rate.
- **Effort** — PI and coordinator time, priced at documented FMV hourly/salary rates.
- **Institutional overhead / indirects** — commonly 25–30% at academic institutions.
- **Non-refundable start-up fees** — IRB fees, pharmacy setup, regulatory document preparation.
- **Screen-failure compensation** — capped, for work actually performed.
- **Invoiceables / pass-throughs** — SAE workups, unscheduled visits, long-term storage, at cost.

### Medicare coverage analysis and double-billing

Before the budget is final, a **billing coverage analysis** must sort every protocol item into sponsor-paid versus routine care billable to insurance. Medicare covers *routine costs* of qualifying clinical trials under National Coverage Determination 310.1; billing Medicare (or any payer) for an item the sponsor also pays for is a false claim. This analysis is a confirmed compliance requirement for any site billing federal healthcare programs, and OSSICRO's budget builder emits the item-by-item designation for qualified review — it does not adjudicate coverage.

## Fair market value and the Anti-Kickback Statute

The Anti-Kickback Statute, [42 U.S.C. §1320a-7b(b)](https://www.law.cornell.edu/uscode/text/42/1320a-7b), is a criminal statute: knowingly and willfully offering, paying, soliciting, or receiving remuneration to induce referrals of items or services reimbursable by a federal healthcare program is a felony. Investigator compensation is squarely within its shadow because investigators generate downstream drug utilization. The operative defense is the **personal services and management contracts safe harbor**, [42 CFR 1001.952(d)](https://www.ecfr.gov/current/title-42/chapter-V/subchapter-B/part-1001/section-1001.952), whose elements (as amended by the HHS-OIG final rule effective January 19, 2021) require, in substance:

1. A **written agreement, signed by the parties**, covering all services for its term;
2. A **term of not less than one year**;
3. The **methodology for determining compensation set in advance**, consistent with **fair market value** in an arm's-length transaction, and **not determined in a manner that takes into account the volume or value of referrals** or other federal-program business generated;
4. Services that do not exceed those reasonably necessary and do not involve promotion of unlawful activity.

**Red flags OSSICRO's validate pass detects structurally:** per-enrollment bonuses that scale with volume; compensation above documented FMV benchmarks; "finder's fees" for referrals; payment for no identifiable service; budgets untethered to the schedule of assessments. The physician self-referral (Stark) law, 42 U.S.C. §1395nn, imposes parallel civil constraints where the investigator refers designated health services. Payments to investigators also feed the [[form-fda-3454-3455-financial-disclosure|Part 54 financial-disclosure]] obligation — above-threshold payments and interests must be disclosed to FDA.

## Sunshine Act reportability

Applicable manufacturers must report research payments and transfers of value to physicians and teaching hospitals to CMS under 42 CFR 403.900–403.914 (Open Payments); research payments are a distinct reporting category, and payments under product-development research agreements for new products may be delayed from publication until approval or four years after payment, whichever is earlier. The reporting obligation sits with the **manufacturer**, not the physician — but the physician's Open Payments record is public, and OSSICRO surfaces expected reportability to the investigator at contracting time.

> [!warning] Non-delegable
> Three functions in this document never belong to software: (1) the **FMV determination and the anti-inducement judgment** are human counsel/compliance functions — OSSICRO templates FMV-defensible structures and flags red-flag structures, but a qualified human decides that a rate is FMV; (2) **contract execution** — only an authorized institutional official, the sponsor's signatory, and (where a party) the investigator can bind the parties; (3) the **billing coverage designation** of protocol items against NCD 310.1 requires qualified billing-compliance review. OSSICRO drafts complete instruments for these humans; it never replaces their judgment.

> [!interpretive] OSSICRO position
> OSSICRO generates the CTA from vetted master templates (ACTA-class), builds the budget mechanically from the protocol's schedule of assessments with cited FMV benchmark sources, cross-validates the subject-injury clause against the ICF's 50.25(a)(6) language, verifies the safe-harbor structural elements (writing, ≥1-year term, compensation methodology set in advance, no volume/value linkage), and blocks "ready" status on any enrollment-scaled bonus structure pending counsel sign-off. Each check is traced in [[compliance-mapping]] and surfaced in the [[completeness-ledger]] as an amber (human-judgment) item, per the [[generate-check-validate-engine]] design and the [[non-delegable-functions-and-gates]] matrix.

## Related
- [[site-activation]]
- [[iis-request-workflow]]
- [[pharma-partner-sponsor]]
- [[sponsor-cro-site-coordination]]
- [[form-fda-3454-3455-financial-disclosure]]
- [[informed-consent-form]]
- [[startup-tmf-checklist]]
- [[transfer-of-regulatory-obligations-toro]]
- [[single-patient-site-and-pharma-acceptance]]
- [[non-delegable-functions-and-gates]]
- [[micro-cro-accountable-layer]]

## Sources
- [42 U.S.C. §1320a-7b — Criminal penalties for acts involving Federal health care programs (Anti-Kickback Statute)](https://www.law.cornell.edu/uscode/text/42/1320a-7b)
- [42 CFR 1001.952 — Exceptions (safe harbors), incl. (d) personal services and management contracts](https://www.ecfr.gov/current/title-42/chapter-V/subchapter-B/part-1001/section-1001.952)
- [HHS-OIG — Safe Harbor Regulations](https://oig.hhs.gov/compliance/safe-harbor-regulations/)
- [42 CFR Part 403, Subpart I — Transparency Reports (Open Payments)](https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-B/part-403/subpart-I)
- [CMS — Open Payments program](https://www.cms.gov/priorities/key-initiatives/open-payments)
- [CMS NCD 310.1 — Routine Costs in Clinical Trials](https://www.cms.gov/medicare-coverage-database/view/ncd.aspx?ncdid=1)
- [42 U.S.C. §1395nn — Limitation on certain physician referrals (Stark)](https://www.law.cornell.edu/uscode/text/42/1395nn)
- [21 U.S.C. §335a — Debarment (FD&C Act §306)](https://www.law.cornell.edu/uscode/text/21/335a)
- [ICH E6(R3) Step 4 Final Guideline (Jan 2025), Appendix C — Essential Records](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [FDA — E6(R3) Good Clinical Practice guidance page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e6r3-good-clinical-practice-gcp)
- [21 CFR 50.25 — Elements of informed consent](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50/subpart-B/section-50.25)
