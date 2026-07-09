---
title: "Persona: Pharma Sponsor / Supplier"
section: "06-personas"
status: mixed
governing_authority:
  - "21 CFR 312.50–312.59 (sponsor set); 312.53 (site selection)"
  - "21 CFR Part 54 (financial disclosure)"
  - "42 USC 1320a-7b (Anti-Kickback Statute); 42 USC 1320a-7h (Sunshine Act)"
  - "FDCA §561/§561A (expanded access; 21 USC 360bbb, 360bbb-0a)"
tags: [role/pharma, role/sponsor, cfr/312, cfr/54, lifecycle/iis, lifecycle/expanded-access, status/mixed]
aliases: ["Pharma Persona", "Pharma Partner Persona", "Sponsor Company"]
updated: 2026-07-09
---

# Persona: Pharma Sponsor / Supplier

> [!authority] Governing authority
> [21 CFR 312.50–312.59](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-D) (sponsor obligations, including [312.53](https://www.law.cornell.edu/cfr/text/21/312.53) investigator selection); [21 CFR Part 54](https://www.law.cornell.edu/cfr/text/21/part-54); the [Anti-Kickback Statute, 42 USC 1320a-7b](https://www.law.cornell.edu/uscode/text/42/1320a-7b) with the personal-services safe harbor at [42 CFR 1001.952(d)](https://www.law.cornell.edu/cfr/text/42/1001.952); the [Sunshine Act, 42 USC 1320a-7h](https://www.law.cornell.edu/uscode/text/42/1320a-7h); [FDCA §561A (21 USC 360bbb-0a)](https://www.law.cornell.edu/uscode/text/21/360bbb-0a). Status: **Mixed** — the sponsor duties and trust requirements are confirmed; the acceptance workflow OSSICRO builds around them is **interpretive**.

Pharma is the counterparty OSSICRO must satisfy without ever representing. Its entry question: *"Can I trust and accept this small, new, or single-patient site with investigational product, safety data, and money?"* The controlling insight: **pharma's trust gate is entity-shaped, not software-shaped.** No demo persuades a sponsor; a complete, verifiable, internally consistent dossier held by legally accountable humans does.

## The four channels pharma offers an outside physician

1. **Site on pharma's protocol (Mode A).** Pharma is sponsor and owns the IND, protocol, [[investigators-brochure|IB]], drug supply, [[ind-safety-report|IND safety reporting]], and monitoring (21 CFR 312 Subpart D); the physician is a site [[investigator]]. Counterparty: **Clinical Development**.
2. **Investigator-Initiated Study ([[iis-request-workflow|IIS]]/IST).** The physician submits a concept through the company's IIS portal to a **Medical Affairs** review committee (scientific merit, strategic fit, safety, budget). If approved, pharma supplies drug and/or a grant — but the physician becomes the [[sponsor-investigator]], holds the IND, and owns the data. Pharma is a supporter, **never the trial sponsor and never OSSICRO's transferee**.
3. **[[expanded-access-workflow|Expanded access]]** ([21 CFR 312 Subpart I](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-I)): treatment, not research. FDA authorization does not compel supply — the **manufacturer must agree**, via a letter of authorization referencing its IND. Under [FDCA §561A](https://www.law.cornell.edu/uscode/text/21/360bbb-0a) (21st Century Cures), manufacturers of investigational drugs for serious conditions must make their expanded-access policy publicly available.
4. **Medical-information exchange.** MSLs may answer unsolicited scientific questions and route IIS concepts; they may not promote off-label use or tie support to prescribing ([PhRMA Code](https://www.phrma.org/codes-and-guidelines/code-on-interactions-with-health-care-professionals)).

> [!warning] Non-delegable
> Two things are pharma's alone: the **manufacturer's decision to supply** an investigational product (expanded access or IIS — a counterparty judgment no dossier can compel; [[expanded-access-coordination]]), and the integrity of the **Medical Affairs / Clinical Development / Commercial firewall**. OSSICRO produces the package that lets pharma say yes; it cannot make pharma say yes, and it never routes a physician's request toward a commercial function.

## What pharma evaluates before accepting a site

The standard funnel — CDA → **feasibility questionnaire** → Site Qualification Visit (SQV) → activation — screens for: patient population and access to the indication; PI experience and prior GCP trial history; coordinator/staff bandwidth; competing trials; pharmacy and temperature-controlled storage; lab/imaging capability (CLIA/CAP); IRB arrangement (central vs. local; [[single-irb-mandate-and-central-irbs]]); EDC/data-management readiness; and regulatory history (Form 483s, warning letters). Sponsors weight **enrollment realism** heavily because zero-enrolling sites are the dominant cost sink in early-phase programs — precisely why a new site with no track record is presumptively rejected.

**Activation** (the green light to ship drug and screen) then requires the complete essential-document package: executed [[clinical-trial-agreement-and-budget|CTA + budget]]; IRB approval of protocol and ICF; signed [[form-fda-1572-statement-of-investigator|1572]] ([21 CFR 312.53(c)(1)](https://www.law.cornell.edu/cfr/text/21/312.53) — pharma cannot ship drug to an investigator who has not provided one, [312.53(b)](https://www.law.cornell.edu/cfr/text/21/312.53)); CVs and licenses; [[form-fda-3454-3455-financial-disclosure|financial disclosure]] per [Part 54](https://www.law.cornell.edu/cfr/text/21/part-54) (the $25,000 compensation and $50,000 equity thresholds); GCP and protocol training; lab certifications; [[delegation-of-authority-log]]; drug-handling SOPs — then the Site Initiation Visit and drug release ([[site-activation]], [[monitoring-workflow-siv-imv-cov]]).

## What makes a small or single-patient site acceptable

> [!interpretive] OSSICRO position
> The single most persuasive artifact to a skeptical sponsor is a **complete, internally consistent, verifiable dossier** — not an assertion of competence but evidence of it. OSSICRO's answer to the no-track-record problem is the [[verifiable-site-qualification-dossier]]: every activation requirement mapped requirement → artifact → citation → signer, hash-chained to the [[part-11-and-ai-credibility|Part 11]] audit trail, so the sponsor's reviewer can verify rather than trust. Paired with the [[completeness-ledger]] (no silent gaps — every open item is explicit) and [[safety-clock-engine|demonstrable safety-clock discipline]], a one-physician site presents better-organized evidence than many experienced sites. The n-of-1 acceptance workflow is specified at [[single-patient-site-and-pharma-acceptance]] and [[single-patient-site-enrollment]].

What pharma still legitimately requires and OSSICRO cannot synthesize: a qualified PI ([312.53(a)](https://www.law.cornell.edu/cfr/text/21/312.53)); real access to the patient (for n-of-1, enrollment risk is definitionally solved — the patient exists); an accountable entity behind any assumed sponsor functions (the [[micro-cro|Micro-CRO]], never software); and a **safety-data exchange agreement** so ICSRs flow both directions on contractual timelines — the sponsor-investigator's [312.32](https://www.law.cornell.edu/cfr/text/21/312.32) duties to FDA plus contractual reporting to the manufacturer, reconciled in the [[safety-management-plan]].

## Money: FMV, AKS, Sunshine

All compensation flowing to the physician/site must be **fair-market-value** for services actually rendered, in a written agreement — structured for the [personal-services safe harbor, 42 CFR 1001.952(d)](https://www.law.cornell.edu/cfr/text/42/1001.952), because trial payments to prescribers sit squarely in [Anti-Kickback](https://www.law.cornell.edu/uscode/text/42/1320a-7b) territory. Research payments are reportable under [Open Payments](https://www.cms.gov/priorities/key-initiatives/open-payments) ([42 USC 1320a-7h](https://www.law.cornell.edu/uscode/text/42/1320a-7h)); IIS grants are FMV-set and Sunshine-reportable ([[iis-request-workflow]], [[clinical-trial-agreement-and-budget]]). OSSICRO drafts budgets against these constraints; the FMV determination and any AKS judgment are human/counsel calls ([[non-delegable-functions-and-gates]]).

## Interfaces OSSICRO must speak

Pharma runs trials on a stack the site must interoperate with: CTMS, eTMF, EDC, IRT/RTSM, a safety database, and increasingly an investigator portal as the single document/e-signature/payments door; IIS programs run public submission portals (e.g., [Genentech's IIS program](https://www.gene.com/medical-professionals/investigator-initiated-studies)). OSSICRO's pharma-style frontend mirrors these conventions — Part 11-compliant e-records/e-signatures, audit trails — so a small site's paperwork arrives in the shape pharma's machinery expects ([[architecture]], [[communication-hub]], [[pharma-partner-interface-iis]]).

## Pharma's own obligation floor

When pharma is the sponsor (Mode A), the full Subpart D set is its burden, not the site's: qualified-investigator selection ([312.53](https://www.law.cornell.edu/cfr/text/21/312.53)), the IB and ongoing safety information ([312.55](https://www.law.cornell.edu/cfr/text/21/312.55)), monitoring and compliance-securing ([312.56](https://www.law.cornell.edu/cfr/text/21/312.56) — including the 5-working-day unreasonable-risk discontinuation at 312.56(d)), records ([312.57](https://www.law.cornell.edu/cfr/text/21/312.57)), drug disposition ([312.59](https://www.law.cornell.edu/cfr/text/21/312.59)), and [[ind-safety-report|7/15-day IND safety reports]] ([312.32](https://www.law.cornell.edu/cfr/text/21/312.32)). See [[sponsor]] and [[pharma-partner-sponsor]] for the full treatment.

## Related

- [[pharma-partner-sponsor]]
- [[pharma-partner-interface-iis]]
- [[single-patient-site-and-pharma-acceptance]]
- [[single-patient-site-enrollment]]
- [[iis-request-workflow]]
- [[expanded-access-workflow]]
- [[expanded-access-coordination]]
- [[verifiable-site-qualification-dossier]]
- [[site-activation]]
- [[clinical-trial-agreement-and-budget]]
- [[safety-management-plan]]
- [[micro-cro]]
- [[hcp-physician]]
- [[perspective-matrix]]

## Sources

- [21 CFR Part 312 Subpart D — Responsibilities of Sponsors and Investigators](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-D)
- [21 CFR 312.53 — Selecting investigators and monitors](https://www.law.cornell.edu/cfr/text/21/312.53)
- [21 CFR Part 54 — Financial Disclosure by Clinical Investigators](https://www.law.cornell.edu/cfr/text/21/part-54)
- [21 CFR 312 Subpart I — Expanded Access to Investigational Drugs for Treatment Use](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-I)
- [21 USC 360bbb-0a (FDCA §561A) — Expanded access policy requirement](https://www.law.cornell.edu/uscode/text/21/360bbb-0a)
- [42 USC 1320a-7b — Anti-Kickback Statute](https://www.law.cornell.edu/uscode/text/42/1320a-7b)
- [42 CFR 1001.952(d) — Personal services and management contracts safe harbor](https://www.law.cornell.edu/cfr/text/42/1001.952)
- [CMS — Open Payments (Sunshine Act)](https://www.cms.gov/priorities/key-initiatives/open-payments)
- [PhRMA Code on Interactions with Health Care Professionals](https://www.phrma.org/codes-and-guidelines/code-on-interactions-with-health-care-professionals)
- [FDA — Expanded Access to Investigational Drugs for Treatment Use: Q&A (guidance)](https://www.fda.gov/media/85675/download)
- [Genentech — Investigator Initiated Studies (IIS program model)](https://www.gene.com/medical-professionals/investigator-initiated-studies)
