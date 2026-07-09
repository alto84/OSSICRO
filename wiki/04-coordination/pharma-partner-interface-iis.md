---
title: "Pharma-Partner Interface: Medical Affairs Routing, Feasibility/SQV, and CTMS Interoperability"
section: "04-coordination"
status: mixed
governing_authority:
  - "21 CFR 312.3 (sponsor / sponsor-investigator; IIS structure)"
  - "21 CFR 312.53 / Part 54 (investigator selection, financial disclosure)"
  - "21 CFR Part 11 (electronic records and signatures)"
  - "42 U.S.C. §1320a-7b(b); 42 CFR 1001.952(d) (Anti-Kickback + safe harbor)"
  - "42 CFR 403.900–403.914 (Sunshine Act / Open Payments)"
tags: [role/pharma, role/sponsor-investigator, role/medical-monitor, cfr/312, cfr/11, cfr/54, lifecycle/iis, lifecycle/feasibility, ossicro/micro-cro, status/mixed]
aliases: ["pharma interface", "IIS routing", "medical affairs firewall", "feasibility SQV", "CTMS interoperability"]
updated: 2026-07-09
---

# Pharma-Partner Interface: Medical Affairs Routing, Feasibility/SQV, and CTMS Interoperability

> [!authority] Governing authority
> 21 CFR 312.3 (definitions; the investigator-initiated study structure in which the physician becomes sponsor-investigator); 21 CFR 312.53 and Part 54 (investigator selection and financial disclosure); 21 CFR Part 11 (electronic records/signatures for interoperating with sponsor systems); 42 U.S.C. § 1320a-7b(b) and 42 CFR 1001.952(d) (Anti-Kickback Statute and personal-services safe harbor); 42 CFR 403.900–403.914 (Physician Payments Sunshine Act / Open Payments); ICH E6(R3) (site selection and oversight). Status: **Mixed** — the routing, contracting, and reporting constraints are black-letter or binding-code (confirmed); OSSICRO's interoperability design and "verifiable dossier" trust wedge are interpretive.

A physician who wants a pharma company's investigational product for research has a single legitimate front door, and it is **not** the sales force. This page describes how an inbound request routes through the pharma organization, what the company evaluates before it will trust and activate a site, what systems the site must interoperate with, and the compliance rails — Medical Affairs firewall, Anti-Kickback, Sunshine Act — that constrain every dollar and every molecule that crosses the interface. The controlling insight for OSSICRO is that **pharma's trust gate is entity-shaped, not software-shaped**: the company transfers product, data, and money only to a legally-accountable investigator/site, and OSSICRO's value is producing the verifiable qualification package that makes a small or new [sponsor-investigator](../01-roles-responsibilities/sponsor-investigator.md) site fundable and activatable.

## Which pharma function is the counterparty

The physician's request routes by pathway, and the pathways sit in different parts of the company separated by a compliance firewall:

| Pathway | Pharma role | Counterparty function |
|---------|-------------|-----------------------|
| **(A) Enroll a patient as a site in the company's own protocol** | Pharma is **sponsor** | **Clinical Development** (owns the IND, protocol, sites) |
| **(B) Investigator-Initiated / Sponsored Study (IIS/IST)** | Pharma is **supporter/funder**, never sponsor | **Medical Affairs** (IIS/grants program) |
| **(C) [Expanded access](expanded-access-coordination.md) / compassionate use** | Pharma is **supplier** (must agree) | **Medical Affairs** (much expanded-access adjudication) |

> [!warning] Non-delegable
> **The Medical-Affairs / Clinical-Development / Commercial firewall is a compliance boundary the interface must respect and can never route around.** Medical Science Liaisons (MSLs) may respond to *unsolicited* scientific inquiries and route IIS concepts; they may **not** promote off-label use, may **not** tie support to prescribing, and their performance metrics are **not** sales-based (PhRMA Code; FDCA § 502). An inbound OSSICRO request must land in Medical Affairs (grants/IIS or medical information) or Clinical Development site-selection — **never a sales representative.** OSSICRO routes and documents; it does not, and must not, collapse this firewall.

## The IIS routing chain (Pathway B)

The investigator-initiated study is the sanctioned channel for a physician to obtain drug and/or funding for **their own** study. The mechanics:

1. **Concept/synopsis submission** through the company's public IIS portal (nearly every large pharma runs one — e.g., Roche, Genentech, LEO, Acadia) to a **Medical Affairs–run review committee** that assesses scientific merit, strategic alignment, safety, and budget.
2. **Award (if approved):** some combination of investigational or marketed drug supply, funding via a **grant/support agreement**, and sometimes assay/data support.
3. **Role assignment:** the physician/institution becomes the **[sponsor-investigator](../01-roles-responsibilities/sponsor-investigator.md)** — they write the protocol, hold the [IND](../02-lifecycle/ind-submission-and-30-day-clock.md) where one is required (§ 312.3 permits one person to be both sponsor and investigator), obtain [IRB approval](irb-review-workflow.md), run [pharmacovigilance](safety-reporting-workflow.md), and own the data and publication. **The pharma company is explicitly not the trial sponsor.**

The sponsor-investigator obligations that do **not** disappear under an IIS: IND maintenance (§ 312.23), [annual reports](../03-documents/ind-annual-report-dsur.md) (§ 312.33), [IND safety reports](../03-documents/ind-safety-report.md) (§ 312.32), protocol amendments (§ 312.30), monitoring and recordkeeping, and all FDA/IRB correspondence. This is precisely the dual-role burden OSSICRO exists to make tractable — see [iis-request-workflow](../02-lifecycle/iis-request-workflow.md).

## Feasibility and Site Qualification (what pharma evaluates before it says yes)

Whether the physician is a candidate Pathway-A site or a Pathway-B sponsor-investigator seeking supply, the company runs a due-diligence sequence:

1. **CDA** (Confidential Disclosure Agreement) → **feasibility questionnaire** assessing: access to the indication's patient population, PI experience and prior GCP trial history, coordinator/staff bandwidth, competing trials, pharmacy and temperature-controlled drug-storage capacity, lab/imaging capability, IRB arrangement (central vs. local), EDC/data-management readiness, and **regulatory inspection history** (Form FDA 483s, Warning Letters).
2. **Site Qualification Visit (SQV):** on-site confirmation of the questionnaire.
3. **Enrollment-realism weighting:** sponsors weight enrollment projections heavily because non-enrolling ("zero-enroller") sites are the dominant cost sink in early-phase programs.

This is exactly where a small or new site is at a structural disadvantage — no track record. The [research corpus](../references/institutional-resources.md) frames the OSSICRO response as substituting **verifiable qualification evidence** for the missing track record: a complete, internally-consistent essential-documents package plus a credentialed accountable investigator is "the single most persuasive artifact to a skeptical sponsor."

## What a site must have to be ACTIVATED

Activation ("green light" to ship drug and screen) requires a complete essential-document package: executed [CTA + FMV budget](../03-documents/clinical-trial-agreement-and-budget.md); [IRB/IEC approval](irb-review-workflow.md) of protocol and ICF; signed [Form FDA 1572](../03-documents/form-fda-1572-statement-of-investigator.md); PI/sub-I current CVs and medical licenses; [financial disclosure](../03-documents/form-fda-3454-3455-financial-disclosure.md) (Part 54; Forms 3454/3455); GCP and protocol-specific training records; signed protocol signature page; lab certifications (CLIA/CAP) and normal ranges; [delegation-of-authority log](../03-documents/delegation-of-authority-log.md); drug-accountability/storage SOPs; and pharmacy/IP setup. Only after these are filed and reconciled does the sponsor hold a **Site Initiation Visit (SIV)** to train the team and release drug. Under ICH E6(R3) these are risk-proportionate **essential records** retained in the TMF / [Investigator Site File](../03-documents/regulatory-binder-isf-index.md).

## CTMS and sponsor-portal interoperability

A sponsored trial runs on a system stack the external site must interoperate with:

| System | Function | Representative products |
|--------|----------|------------------------|
| **CTMS** | Site status, milestones, monitoring tracking | Veeva Vault CTMS, Medidata |
| **eTMF** | Essential-document management | Veeva Vault eTMF |
| **EDC** | Case-report-form data capture | Medidata Rave, Veeva Vault EDC, Oracle |
| **IRT / IWRS / RTSM** | Randomization + drug supply | (sponsor-specific) |
| **Safety database** | Pharmacovigilance/ICSR intake | Oracle Argus, ArisGlobal |
| **Site/Investigator PORTAL** | Single door for documents, e-signature, payments, queries | Veeva SiteVault; IIS/grants portals |

Every one of these is a **[21 CFR Part 11](../05-ossicro-system/part-11-and-ai-credibility.md)** environment — validated, access-controlled, audit-trailed, with compliant electronic signatures. OSSICRO's "pharma-style frontend" must speak these systems' document conventions to exchange essential records without friction.

> [!interpretive] OSSICRO position
> OSSICRO's differentiator at the pharma interface is a **verifiable [site-qualification dossier](../05-ossicro-system/verifiable-site-qualification-dossier.md)** — a citation-complete, hash-chained manifest that maps each sponsor/IIS-committee requirement to the artifact that satisfies it, its governing citation, and the human signer, rendered in the document conventions of the sponsor's portal and Part-11 audit trail. This turns a new site's biggest liability (no track record, no coordinator army) into an auditable dossier that a Medical Affairs reviewer or a CRO start-up lead can verify in one pass. The interoperability claim is interpretive: OSSICRO can *produce* Part-11-conformant, portal-shaped records, but the sponsor's acceptance of a novel site remains a human judgment, and OSSICRO does not assert any automated write-access into a sponsor's validated CTMS/EDC. Status: interpretive. See [single-patient-site-and-pharma-acceptance](single-patient-site-and-pharma-acceptance.md).

## The money rails: Anti-Kickback and Sunshine Act

Every payment or transfer of value across the interface is constrained by two federal regimes:

- **Anti-Kickback Statute (42 U.S.C. § 1320a-7b(b)):** a felony to offer/pay/solicit/receive remuneration to induce federally-reimbursed utilization. Paying an investigator **above FMV**, or tying payment to **enrollment volume or prescribing**, is a red flag because investigators generate downstream drug utilization. Compliance relies on the **personal-services safe harbor (42 CFR 1001.952(d))**: written agreement, ≥ 1-year term, aggregate compensation **set in advance at FMV**, not determined by volume/value of referrals.
- **Sunshine Act / Open Payments (42 CFR 403.900–403.914):** applicable manufacturers must publicly report virtually all payments/transfers of value to physicians and teaching hospitals — including **drug value, grants, and service payments**. Research payments are a distinct reportable category with a delayed-publication provision for pre-approval product research. The reporting duty sits with the **manufacturer**, but every dollar of drug value or grant the physician receives is reportable and public.

> [!warning] Non-delegable
> **The Fair Market Value determination and the anti-inducement judgment are human/counsel functions.** OSSICRO can template an FMV-defensible budget and safe-harbor-shaped support agreement, but the FMV valuation, the anti-kickback assessment, and the sponsor's decision to fund are legal/compliance decisions owned by qualified humans — surfaced and gated, never automated (see [non-delegable-functions-and-gates](../05-ossicro-system/non-delegable-functions-and-gates.md)). The manufacturer's Sunshine Act reporting sits with the manufacturer, not the physician or the software.

## What OSSICRO generates vs. what stays human

- **Generates (drafts for review):** the IIS concept synopsis and full protocol draft; the feasibility-questionnaire response and a verifiable qualification dossier; the activation essential-document set (1572, CVs, 3454/3455, delegation log, SOPs) checked against the sponsor's package; the FMV-set budget and safe-harbor-shaped support/CTA skeleton; Part-11-conformant, portal-shaped records.
- **Stays human/entity (gated):** the PI qualification attestation and 1572 signature; IRB approval; FMV determination and AKS judgment; the pharma committee's funding/supply decision; and the causality/safety determinations under the [safety-reporting-workflow](safety-reporting-workflow.md).

## Related
- [[pharma-partner-sponsor]]
- [[sponsor-investigator]]
- [[iis-request-workflow]]
- [[expanded-access-coordination]]
- [[single-patient-site-and-pharma-acceptance]]
- [[clinical-trial-agreement-and-budget]]
- [[form-fda-1572-statement-of-investigator]]
- [[form-fda-3454-3455-financial-disclosure]]
- [[verifiable-site-qualification-dossier]]
- [[part-11-and-ai-credibility]]
- [[non-delegable-functions-and-gates]]

## Sources
- [21 CFR 312.3 — Definitions (sponsor, investigator, sponsor-investigator)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-A/section-312.3)
- [21 CFR 312.53 — Selecting investigators and monitors](https://www.law.cornell.edu/cfr/text/21/312.53)
- [21 CFR Part 54 — Financial disclosure by clinical investigators](https://www.law.cornell.edu/cfr/text/21/part-54)
- [21 CFR Part 11 — Electronic Records; Electronic Signatures](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)
- [42 U.S.C. § 1320a-7b(b) — Anti-Kickback Statute (Cornell LII)](https://www.law.cornell.edu/uscode/text/42/1320a-7b)
- [42 CFR 1001.952(d) — Personal services and management contracts safe harbor](https://www.law.cornell.edu/cfr/text/42/1001.952)
- [42 CFR 403.900–403.914 — Open Payments (Sunshine Act)](https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-B/part-403/subpart-I)
- [FDA — E6(R3) Good Clinical Practice guidance](https://www.fda.gov/media/169090/download)
- [Genentech — Investigator Initiated Studies](https://www.gene.com/medical-professionals/investigator-initiated-studies)
- [Roche — Investigator Initiated Studies program](https://www.roche.com/innovation/clinical-trials/investigator-initiated-studies)
