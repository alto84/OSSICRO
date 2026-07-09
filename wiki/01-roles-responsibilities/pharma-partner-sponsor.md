---
title: "Pharma Partner — Trial Sponsor (Mode A) vs. IIS Supporter (Mode B), and the Medical-Affairs Firewall"
section: "01-roles-responsibilities"
status: mixed
governing_authority:
  - "21 CFR 312.3(b) (sponsor / sponsor-investigator definitions)"
  - "21 CFR 312.52 (transfer of obligations — the pharma partner is never OSSICRO's transferee)"
  - "42 U.S.C. §1320a-7b(b) (Anti-Kickback Statute); 42 CFR 1001.952(d) (personal-services safe harbor)"
  - "42 CFR 403.900-403.914 (Sunshine Act / Open Payments)"
  - "PhRMA Code on Interactions with Health Care Professionals"
tags: [role/pharma, cfr/312, usc/1320a-7b, entity/pharma, lifecycle/iis, status/mixed]
aliases: ["pharma sponsor", "IIS supporter", "drug supplier", "manufacturer"]
updated: 2026-07-09
---

# Pharma Partner — Trial Sponsor (Mode A) vs. IIS Supporter (Mode B), and the Medical-Affairs Firewall

> [!authority] Governing authority
> The pharma partner's legal posture is defined by 21 CFR 312.3(b) (who is "sponsor"), 21 CFR 312.52 (obligations transfer only to a legally accountable entity), the Anti-Kickback Statute (42 U.S.C. §1320a-7b(b)) with its personal-services safe harbor (42 CFR 1001.952(d)), and the Sunshine Act (42 CFR 403.900-403.914). Status: **Mixed** — the regulatory constraints are confirmed; the mode-triage logic and OSSICRO's role framing are interpretive, marked inline.

A pharmaceutical company enters an OSSICRO-coordinated engagement in one of two fundamentally different legal postures, and the distinction determines who holds the IND, who owns the data, and who bears sponsor accountability. Getting this wrong is not a formatting error — it is a misassignment of federal legal responsibility. Critically, in **neither** mode is the pharma partner OSSICRO's transferee, and OSSICRO is never the pharma partner's CRO.

## Mode A — pharma as trial sponsor (physician as site)

In **Mode A** the pharma company is the **sponsor** of its own protocol (21 CFR 312.3(b)): it holds the IND (21 CFR 312.23), owns the protocol and [[investigators-brochure]], supplies and labels the drug (21 CFR 312.6), performs IND safety reporting (21 CFR 312.32), monitors the sites (21 CFR 312.50-312.56), and retains the records. The enrolling physician is a **site investigator** on an existing protocol and signs [[form-fda-1572-statement-of-investigator]], committing to conduct per protocol and GCP. Data flow to the sponsor. The pharma company may delegate operational conduct to a CRO under a written [[transfer-of-regulatory-obligations-toro]] instrument (21 CFR 312.52) but retains ultimate accountability.

OSSICRO's role in Mode A is to produce the **site-activation essential-document package** to sponsor standard — turning a new site's biggest liability (no track record) into a verifiable, auditable dossier (see [[verifiable-site-qualification-dossier]] and [[site-activation]]). The sponsor's trust gate is entity-shaped: it needs a GCP-qualified, licensed PI with a clean regulatory record, an IRB of record, financial disclosures (Part 54), and a Part 11-compliant document environment — not software polish.

## Mode B — pharma as IIS supporter (physician as sponsor-investigator)

In **Mode B**, an **Investigator-Initiated Study (IIS/IST)**, the physician conceives and runs their *own* study and becomes the [[sponsor-investigator]] holding both obligation sets. The pharma company is explicitly **not** the trial sponsor — it is a **supporter/funder** that may provide investigational or marketed drug supply, a grant/contract, and sometimes assay or data support. The physician writes the protocol, holds the IND where one is required, obtains IRB approval, runs pharmacovigilance, and **owns the data and publication**.

Mechanically, the physician submits a concept synopsis through the company's **IIS portal** to a Medical-Affairs-run review committee assessing scientific merit, strategic alignment, safety, and budget (see [[iis-request-workflow]]). If approved, a support/grant agreement is executed. The sponsor-investigator's obligations that *do not disappear* include IND maintenance (21 CFR 312.23), [[ind-annual-report-dsur]] (312.33), [[ind-safety-report]] (312.32), protocol amendments (312.30), monitoring, and FDA/IRB correspondence. This is the crux of OSSICRO's viable model: the dual burden is what makes the sponsor-investigator role impractical for a solo clinician, and coordination automation is precisely what makes it tractable (see [[two-modes-site-vs-sponsor-investigator]]).

> [!interpretive] OSSICRO position
> The guiding scenario ("a clinician has a patient and a candidate therapy") can resolve to Mode A, Mode B, or a third **expanded-access** branch (treatment, not research — [[expanded-access-workflow]], Form FDA 3926, manufacturer letter of authorization). OSSICRO's [[the-three-pathways-triage]] engine must classify the request to the correct pathway, because the document sets, accountable parties, and legal exposure differ entirely. The triage logic is an OSSICRO design position; the underlying pathway law is confirmed.

## The Medical Affairs vs. Clinical Development firewall

Which pharma *function* is OSSICRO's counterparty depends on the mode, and a compliance firewall separates both from Commercial/Sales.

- **Clinical Development** owns the company's own interventional trials (protocol, sites, IND) — the counterparty for **Mode A** site enrollment.
- **Medical Affairs** owns non-promotional scientific exchange, Medical Science Liaisons (MSLs), the **IIS/IST program**, and much of **expanded-access** adjudication — the counterparty for **Mode B** and the expanded-access branch.
- A **compliance firewall** walls both off from Commercial/Sales. MSLs may respond to *unsolicited* scientific inquiries and route IIS concepts, but cannot promote off-label use, cannot tie support to prescribing, and are not measured on sales.

> [!warning] Non-delegable
> **The physician's inbound request routes to Medical Affairs (grants/IIS or medical information), never to a sales representative, and the interaction must remain non-promotional and documented.** Crossing the Medical-Affairs/Clinical-Development/Commercial firewall is a legal-exposure event (FDCA §502; PhRMA Code). OSSICRO's [[communication-hub]] enforces role-scoped routing but does not adjudicate what is promotional — that judgment stays with the pharma partner's medical/compliance function.

## Money, Fair Market Value, and transparency

Every payment or transfer of value from a pharma partner to the physician is constrained by three regimes:

- **Anti-Kickback Statute (42 U.S.C. §1320a-7b(b)):** it is a felony to offer or pay remuneration to induce federally-reimbursed utilization. Paying an investigator *above* Fair Market Value (FMV), or tying payment to enrollment or prescribing, is a red flag. Compliance relies on the **personal-services safe harbor** (42 CFR 1001.952(d)): a written agreement, ≥1-year term, aggregate compensation set in advance at FMV, not determined by the volume or value of referrals. OSSICRO can template FMV-defensible [[clinical-trial-agreement-and-budget]] and IIS support-agreement structures.
- **Sunshine Act / Open Payments (42 CFR 403.900-403.914):** the applicable manufacturer must annually report drug value, grants, and service payments to physicians/teaching hospitals to CMS, published publicly (research payments are a distinct category with delayed publication for pre-approval product research).
- **Financial disclosure (21 CFR Part 54):** the sponsor must collect investigator financial-interest information (Forms [[form-fda-3454-3455-financial-disclosure|3454/3455]]).

> [!warning] Non-delegable
> **FMV determination, the anti-inducement judgment, the manufacturer's decision to supply drug, and the manufacturer's Sunshine Act reporting are the pharma partner's / counsel's functions — not the physician's and not the software's.** OSSICRO drafts FMV-structured agreements and keeps the physician's received-value record reconcilable; it does not set FMV or make the anti-kickback call (see [[non-delegable-functions-and-gates]]).

## Why the pharma partner is never OSSICRO's transferee

21 CFR 312.52 permits a sponsor to transfer obligations only to a legally accountable **CRO entity** that thereby becomes subject to the same FDA enforcement as the sponsor. In Mode B the pharma partner is a *funder*, not a sponsor, so there is nothing for it to transfer to OSSICRO. In Mode A the pharma partner *is* the sponsor and may use its own CROs, but OSSICRO — a software system — cannot be a §312.52 transferee for anyone (see [[legal-thesis-3123-vs-31252]]). When accountable functions must be held on the physician's side, they sit with the [[micro-cro-accountable-layer]], a real entity — never with the pharma partner and never with software.

## Related

- [[sponsor]]
- [[sponsor-investigator]]
- [[two-modes-site-vs-sponsor-investigator]]
- [[the-three-pathways-triage]]
- [[iis-request-workflow]]
- [[expanded-access-workflow]]
- [[clinical-trial-agreement-and-budget]]
- [[form-fda-3454-3455-financial-disclosure]]
- [[transfer-of-regulatory-obligations-toro]]
- [[micro-cro-accountable-layer]]
- [[pharma-partner-interface-iis]]
- [[non-delegable-functions-and-gates]]

## Sources

- [21 CFR 312.3 — Definitions (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/312.3)
- [21 CFR 312.52 — Transfer of obligations to a CRO (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/312.52)
- [42 U.S.C. §1320a-7b — Criminal penalties (Anti-Kickback Statute)](https://www.law.cornell.edu/uscode/text/42/1320a-7b)
- [42 CFR 1001.952(d) — Personal services and management contracts safe harbor](https://www.law.cornell.edu/cfr/text/42/1001.952)
- [42 CFR Part 403 Subpart I — Open Payments (Sunshine Act)](https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-B/part-403/subpart-I)
- [FDA — Expanded Access to Investigational Drugs for Treatment Use: Q&A](https://www.fda.gov/media/162793/download)
- [FDA — Overview of Sponsor-Investigator Roles and Responsibilities](https://www.fda.gov/media/174660/download)
- [Roche — Investigator Initiated Studies program](https://www.roche.com/innovation/clinical-trials/investigator-initiated-studies)
