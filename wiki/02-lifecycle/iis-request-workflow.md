---
title: "IIS Request Workflow (Concept Synopsis → Medical Affairs → Grant → Sponsor-Investigator IND)"
section: "02-lifecycle"
status: mixed
governing_authority:
  - "21 CFR 312.3(b) (sponsor-investigator)"
  - "21 CFR 312.20-312.23 (IND submission/content)"
  - "21 CFR 312.52 (transfer of obligations — why a physician-held IIS IND is lawful)"
  - "42 U.S.C. 1320a-7b(b) (Anti-Kickback Statute)"
  - "42 CFR 403.900-403.914 (Sunshine Act / Open Payments)"
  - "PhRMA Code; FDCA §502 (promotional/off-label constraints)"
tags: [lifecycle/iis, lifecycle/ind, role/sponsor-investigator, role/pharma, cfr/312, status/mixed]
aliases: ["IIS", "IST", "investigator-initiated study", "investigator-sponsored study", "investigator-initiated trial"]
updated: 2026-07-09
---

# IIS Request Workflow (Concept Synopsis → Medical Affairs → Grant → Sponsor-Investigator IND)

> [!authority] Governing authority
> An Investigator-Initiated / Investigator-Sponsored Study (IIS/IST) makes the physician a **sponsor-investigator** under **21 CFR 312.3(b)**, holding the IND (**21 CFR 312.20-312.23**) and both obligation sets. The lawfulness of the physician (not the pharma company, not software) holding the IND rests on **21 CFR 312.52** — obligations transfer only to an accountable entity. Compensation/support is bounded by the **Anti-Kickback Statute (42 U.S.C. 1320a-7b(b))** with fair-market-value structuring, and reported under the **Sunshine Act / Open Payments (42 CFR 403.900-403.914)**. Non-promotional routing is governed by the **PhRMA Code** and **FDCA §502**. Status: **Mixed** — the pathway and the FMV/Sunshine obligations are confirmed; the OSSICRO drafting boundary is interpretive.

An IIS is the sanctioned channel through which a physician obtains a pharma company's investigational (or marketed) product **and/or funding** to run **their own** study. It is fundamentally different from joining the company's trial as a site ([[single-patient-site-enrollment]] route b) and from treatment-use expanded access ([[expanded-access-workflow]]): in an IIS the physician **becomes the sponsor-investigator**, holds the IND, and carries both the sponsor and investigator obligation sets; the pharma company is only a **supplier/funder**, never OSSICRO's transferee and never the study's sponsor ([[pharma-partner-sponsor]], [[the-three-pathways-triage]]).

This page is the end-to-end IIS lifecycle: the concept synopsis, the Medical Affairs review gate, the support/grant agreement, and the transition into a sponsor-investigator IND — with the fair-market-value and Sunshine Act constraints that govern the money, and the firewall that keeps the interaction non-promotional.

## Counterparty: Medical Affairs, not Commercial

The physician's inbound IIS request routes to the pharma company's **Medical Affairs** function, not to sales/commercial and not to Clinical Development.

- **Clinical Development** owns the company's *own* interventional trials (its protocols, its sites, its IND) — the counterparty for **site enrollment** (Mode A), not for an IIS.
- **Medical Affairs** owns non-promotional scientific exchange, the **IIS/IST grants program**, and much of expanded-access adjudication — the counterparty for an IIS.
- A compliance **firewall** separates both from Commercial/Sales. Medical Science Liaisons may respond to unsolicited scientific inquiries and route IIS concepts, but may **not** promote off-label use, may **not** tie support to prescribing, and are **not** measured on sales metrics.

> [!warning] Non-delegable
> The Medical-Affairs / Clinical-Development / Commercial firewall is a legal-compliance boundary the pharma company owns and enforces (PhRMA Code; FDCA §502). OSSICRO routes the physician's request to the correct function and keeps the record non-promotional; it cannot collapse or arbitrate that firewall. Tying any support to prescribing volume is an Anti-Kickback violation, not a documentation defect.

## Step 1 — Concept synopsis

The physician submits a **concept synopsis** (short proposal) through the company's IIS **portal** (nearly every large pharma runs a public web portal for concept submission — e.g., Roche/Genentech, LEO, Acadia programs). The synopsis states the scientific question, rationale, hypothesis, high-level design, target population, endpoints, requested support (drug supply and/or funding), and the investigator's qualifications. OSSICRO's [[generate-check-validate-engine]] drafts the synopsis from structured study data and the physician's CV/site profile, formatted to the target program's intake schema.

## Step 2 — Medical Affairs review committee

The company's Medical Affairs-run review committee evaluates the concept on **scientific merit, strategic alignment, safety, and budget**. Outcomes: decline, request revision, or advance to a full protocol and support agreement. This is a business/scientific decision internal to the company; OSSICRO cannot influence or predict it.

> [!warning] Non-delegable
> The company's decision to support an IIS — and on what terms — is a counterparty judgment (scientific, strategic, safety, budget). OSSICRO prepares a complete, credible concept and protocol package to make the request reviewable; the grant decision is the company's.

## Step 3 — Full protocol + support/grant agreement

On approval-in-principle, the physician develops the **full protocol** ([[clinical-protocol-and-synopsis]]) and the parties execute a **support/grant agreement** (a form of [[clinical-trial-agreement-and-budget]]) governing drug supply, funding, IP, publication rights, data ownership, subject-injury coverage, and safety-data exchange. Two compliance regimes bind the money:

### Fair Market Value + Anti-Kickback Statute

Support and any compensation must be set at **fair market value (FMV)**, established **in advance**, and **not tied to volume or value of referrals/prescribing**. This structures the arrangement to fit the AKS personal-services/research safe-harbor conditions (42 U.S.C. 1320a-7b(b); safe harbor 42 CFR 1001.952). OSSICRO can template FMV-defensible budget structures, but:

> [!warning] Non-delegable
> The FMV determination and the anti-inducement judgment are human/counsel functions (Anti-Kickback Statute, 42 U.S.C. 1320a-7b(b); HHS-OIG guidance). OSSICRO drafts a budget in an FMV-defensible structure and flags the determination; the FMV valuation and the legal sign-off belong to the parties and their counsel ([[clinical-trial-agreement-and-budget]]).

### Sunshine Act / Open Payments

Under the Physician Payments Sunshine Act (ACA §6002; 42 CFR 403.900-403.914), "applicable manufacturers" must annually report to CMS essentially all payments and transfers of value to physicians — including **research payments** made under a written agreement/protocol — published on the public **Open Payments** database. The **manufacturer** is the reporting party, but the physician should maintain a corresponding reportable-value record for reconciliation.

> [!interpretive] OSSICRO position
> OSSICRO maintains the physician-side reportable-value record and a reconciliation view against the anticipated Open Payments research-payment category. This is bookkeeping/tracking, not a legal filing; the manufacturer owns the CMS submission. Flagged interpretive because the physician-side reconciliation is an OSSICRO convenience, not a black-letter physician obligation.

## Step 4 — Sponsor-investigator IND

Because the physician runs their own study, they must hold an **IND** (unless a narrow exemption under 21 CFR 312.2(b) applies — an exemption determination that is itself a regulatory judgment). The physician becomes the **sponsor-investigator** (21 CFR 312.3(b)) and OSSICRO assembles the full 312.23 package and drives the 30-day clock:

- **[[form-fda-1571-ind-cover]]** — the IND cover/commitment; the signature is a non-delegable sponsor attestation.
- **[[clinical-protocol-and-synopsis]]** — protocol per 312.23(a)(6) (ICH M11 structured target).
- **[[investigators-brochure]]** — IB per 312.55, or the approved package insert for a marketed drug supplied by the manufacturer.
- **CMC and pharm/tox** — ordinarily satisfied by the manufacturer's **Letter of Authorization** (LOA) to cross-reference the company's IND/DMF, so the physician need not reproduce proprietary manufacturing data.
- **[[form-fda-1572-statement-of-investigator]]** — the physician's own Statement of Investigator (the sponsor-investigator signs both the sponsor and investigator instruments).
- **[[form-fda-3674-clinicaltrialsgov-certification]]** and **[[form-fda-3454-3455-financial-disclosure]]** — accompanying certifications; in the S-I model the physician self-discloses financial interests (21 CFR Part 54).

See [[pre-ind-and-ind-preparation]], [[ind-submission-and-30-day-clock]], and the full obligation set at [[sponsor-investigator]]. Once the IND is effective, the sponsor-investigator carries safety reporting (312.32; [[safety-reporting-lifecycle]]), annual reporting/DSUR (312.33; [[annual-reporting-and-amendments]]), and amendments (312.30/312.31) for the life of the study.

> [!warning] Non-delegable
> The 1571 and 1572 signatures are legal attestations of sponsor and investigator accountability that only the sponsor-investigator can execute (21 CFR 312.23(a)(1), 312.53(c)). OSSICRO drafts, checks, and assembles the IND; the human holds the IND and signs. Software is never the IND holder — that is the load-bearing consequence of 21 CFR 312.52 ([[legal-thesis-3123-vs-31252]]).

## Why the IIS IND is lawful where software-as-CRO is not

The IIS pathway is the concrete instance of OSSICRO's core legal thesis. Sponsor obligations transfer, in writing, **only to a legally-accountable entity** subject to the same FDA enforcement as a sponsor (21 CFR 312.52(b)). Software cannot be that transferee. In an IIS the obligations are never transferred to a non-entity: the **physician** holds them as sponsor-investigator, and OSSICRO merely absorbs the coordination labor — the drafting, checking, timing, and version control — that normally makes the dual role impractical for a solo clinician ([[legal-thesis-3123-vs-31252]], [[what-is-ossicro]]). Where the physician cannot personally hold an accountable function, it routes to the thin, human-staffed [[micro-cro-accountable-layer]] via a written [[transfer-of-regulatory-obligations-toro]] — an entity, not a script.

## Related

- [[the-three-pathways-triage]]
- [[expanded-access-workflow]]
- [[single-patient-site-enrollment]]
- [[sponsor-investigator]]
- [[pharma-partner-sponsor]]
- [[pharma-partner-interface-iis]]
- [[pre-ind-and-ind-preparation]]
- [[ind-submission-and-30-day-clock]]
- [[clinical-trial-agreement-and-budget]]
- [[legal-thesis-3123-vs-31252]]
- [[transfer-of-regulatory-obligations-toro]]
- [[form-fda-1571-ind-cover]]
- [[form-fda-1572-statement-of-investigator]]
- [[non-delegable-functions-and-gates]]

## Sources

- [21 CFR 312.3 — Definitions (sponsor, investigator, sponsor-investigator) (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-A/section-312.3)
- [21 CFR 312.52 — Transfer of obligations to a CRO (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.52)
- [21 CFR 312.23 — IND content and format (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.23)
- [FDA — Investigational New Drug Applications Prepared and Submitted by Sponsor-Investigators (guidance)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/investigational-new-drug-applications-prepared-and-submitted-sponsor-investigators)
- [Roche — Investigator Initiated Studies program](https://www.roche.com/innovation/clinical-trials/investigator-initiated-studies)
- [Genentech — Investigator Initiated Studies](https://www.gene.com/medical-professionals/investigator-initiated-studies)
- [Advarra — Beginner's Guide to Investigator-Initiated Trials](https://www.advarra.com/blog/beginners-guide-to-investigator-initiated-trials/)
- [IntuitionLabs — Fair Market Value (FMV) in Clinical Trial Investigator Compensation](https://intuitionlabs.ai/articles/fair-market-value-clinical-trials)
- [Health Affairs — The Physician Payments Sunshine Act (brief)](https://www.healthaffairs.org/content/briefs/physician-payments-sunshine-act)
