---
title: "EU Qualified Persons — QPPV (Pharmacovigilance) and QP (IMP Release) under CTR 536/2014 and GVP Module I"
section: "01-roles-responsibilities"
status: mixed
governing_authority:
  - "Regulation (EU) No 536/2014 (Clinical Trials Regulation)"
  - "Directive 2001/83/EC Art. 104 (QPPV requirement)"
  - "Commission Implementing Regulation (EU) 520/2012 (pharmacovigilance)"
  - "EMA Good Pharmacovigilance Practices (GVP) Module I"
  - "Directive 2001/20/EC Annex 13 / EU GMP Annex 16 (QP certification of IMP)"
tags: [role/qppv, ich/e2b, status/mixed, entity/eu, lifecycle/safety]
aliases: ["QPPV", "Qualified Person for Pharmacovigilance", "QP", "Qualified Person", "EU qualified person"]
updated: 2026-07-09
---

# EU Qualified Persons — QPPV and QP under CTR 536/2014 and GVP Module I

> [!authority] Governing authority
> The EU imposes two distinct *named, personally-accountable* qualified-person roles: the **Qualified Person for Pharmacovigilance (QPPV)** under Directive 2001/83/EC Art. 104 and EMA GVP Module I, and the **Qualified Person (QP)** who certifies/releases each batch of investigational medicinal product under EU GMP Annex 16 (and, in the trials context, Regulation (EU) 536/2014). Status: **Mixed** — the EU statutory roles are confirmed; their use as a load-bearing analogue for OSSICRO's US "accountable-human" thesis is an interpretive framing, marked inline.

The EU framework is the sharpest illustration of OSSICRO's central legal fact: certain regulated functions must be held by a **named natural person** who is personally accountable to a competent authority — not by a company at large, and never by software. Where US 21 CFR 312.52 says sponsor obligations transfer only to a legally accountable *entity*, EU law goes further and, for pharmacovigilance and product release, demands a *specific individual by name*. This page documents the two roles, their statutory basis, and why they are the European mirror of the [[non-delegable-functions-and-gates|non-delegable floor]].

## The EU Clinical Trials Regulation (CTR 536/2014)

**Regulation (EU) No 536/2014**, the Clinical Trials Regulation (CTR), became applicable on **31 January 2022**, replacing the Clinical Trials Directive 2001/20/EC. It centralizes the EU trial-authorization pathway through the **Clinical Trials Information System (CTIS)**, a single portal for submission and supervision across Member States, with a coordinated assessment (a Reporting Member State leads Part I scientific review; each concerned Member State handles Part II national/ethics aspects). The CTR defines the **sponsor** as "an individual, company, institution or organisation which takes responsibility for the initiation, for the management and for setting up the financing of the clinical trial" (Art. 2(2)(14)) — and, like US law, requires a legally responsible sponsor; a sponsor established outside the EU must have a **legal representative** in the Union (Art. 74). Safety reporting under the CTR (Arts. 41-43) routes **SUSARs** to the EudraVigilance database and requires an **annual safety report** to the Agency and Member States — the EU counterpart to the US 7-/15-day [[ind-safety-report]] and [[ind-annual-report-dsur|312.33 annual report]] (see [[safety-report-timelines-7-15-day]]).

> [!interpretive] OSSICRO position
> OSSICRO is US-first (21 CFR / IND-centric). The CTR/CTIS layer is documented here as the **EU analogue** a physician-sponsor faces if a trial extends to Europe, and as evidence that the "named accountable human" principle is not a US idiosyncrasy but a convergent regulatory design. OSSICRO's engine would generate CTIS-shaped and EudraVigilance/[[ich-guideline-map|ICH E2B(R3)]]-shaped safety artifacts as drafts for the accountable human; it does not itself hold any EU qualified-person role.

## The Qualified Person for Pharmacovigilance (QPPV)

Under **Directive 2001/83/EC Art. 104** and **Commission Implementing Regulation (EU) 520/2012**, every marketing-authorization holder must have permanently and continuously at its disposal a **Qualified Person Responsible for Pharmacovigilance (QPPV)** — a single named individual, resident and operating in the EU/EEA, registered in the Article 57 database with a named deputy. **EMA GVP Module I** details the role: the QPPV is personally responsible for the establishment and maintenance of the pharmacovigilance system, has an overview of the medicinal product's safety profiles and emerging concerns, is aware of risk-management and post-authorization safety obligations, and is the **single point of contact for the competent authorities on a 24/7 basis**. The QPPV's responsibilities cannot be discharged by a committee-in-the-abstract: the accountability attaches to the named person, even where operational tasks are delegated.

> [!warning] Non-delegable
> **The QPPV is a named natural person personally accountable for the pharmacovigilance system; the role cannot be held by a company generically, by an unnamed function, or by software.** OSSICRO may draft, code (ICH E2B(R3)), route, and time individual case safety reports and aggregate safety documents, and maintain the audit trail — but the QPPV owns the safety-system oversight and the signal/benefit-risk judgments (Directive 2001/83/EC Art. 104; EMA GVP Module I). This is the EU-side expression of the same rule that keeps SAE causality/expectedness with the [[medical-monitor]] under 21 CFR 312.32.

While the QPPV requirement formally attaches to authorized products (post-marketing), the **trial-stage analogue** in the CTR context is the sponsor's obligation to run an ongoing safety evaluation and expedited/annual reporting (Arts. 41-43); many sponsors extend QPPV-style oversight to the investigational phase. The through-line for OSSICRO is that safety-system accountability is a personal, non-delegable human function on both sides of the Atlantic.

## The Qualified Person (QP) for IMP certification and release

A structurally different EU role — sharing the "QP" abbreviation but not the function — is the **Qualified Person (QP)** who certifies and releases each batch of medicinal product. Under **EU GMP Annex 16** (and, for trials, the IMP requirements carried into Regulation (EU) 536/2014 and its delegated act **(EU) 2017/1569** on GMP for investigational medicinal products), **no batch of investigational medicinal product may be used in a trial until a QP has certified that it complies with GMP, the product specification, and the approved trial documentation.** The QP is a named individual with defined qualifications (pharmacy/chemistry/biology background plus practical experience per Directive 2001/83/EC Art. 49) who takes **personal legal responsibility** for each certification, recorded in a register.

> [!warning] Non-delegable
> **QP batch certification/release is a personal legal act by a named, qualified individual; investigational product may not be administered in the EU until a QP has certified the batch.** OSSICRO can assemble the certification dossier, cross-check the [[drug-accountability-log|accountability]] and labeling records, and track the release status — but the certification itself, and the personal responsibility for it, are the QP's (EU GMP Annex 16; Reg. (EU) 2017/1569). This mirrors the US-side [[investigational-product-and-drug-supply|IMP control]] and the manufacturer's supply decision.

## Why this matters to a US sponsor-investigator

For an OSSICRO physician the EU roles matter in two situations: (1) a US [[sponsor-investigator]] IIS that expands to an EU site, which pulls in CTR/CTIS authorization, EudraVigilance safety reporting, and — if IMP is manufactured or imported into the EU — QP certification; and (2) a [[pharma-partner-sponsor|pharma partner]] whose product is EU-authorized, where the manufacturer's QPPV and QP already sit in the supply and safety chain. In both, OSSICRO's role is unchanged: **draft, check, validate, route, and time; never hold the named-person accountability.**

> [!interpretive] OSSICRO position
> The QPPV and QP are the cleanest available proof of OSSICRO's thesis. When a legal system is forced to name the party it will hold responsible for drug safety and product release, it names a *person*, by name, resident in the jurisdiction, reachable 24/7 — never a piece of software and never a diffuse corporate function. OSSICRO's [[micro-cro-accountable-layer]] is the US-side embodiment of the same necessity: a real, named, accountable human/entity for the irreducible functions, with automation absorbing everything around it.

## Related

- [[non-delegable-functions-and-gates]]
- [[pharmacovigilance-safety]]
- [[medical-monitor]]
- [[ind-safety-report]]
- [[safety-report-timelines-7-15-day]]
- [[ind-annual-report-dsur]]
- [[sponsor-investigator]]
- [[pharma-partner-sponsor]]
- [[micro-cro-accountable-layer]]
- [[ich-guideline-map]]
- [[regulatory-landscape]]

## Sources

- [Regulation (EU) No 536/2014 — Clinical Trials Regulation (EUR-Lex)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32014R0536)
- [EMA — Clinical Trials Regulation (overview & CTIS)](https://www.ema.europa.eu/en/human-regulatory-overview/research-development/clinical-trials-human-medicines/clinical-trials-regulation)
- [Directive 2001/83/EC — Community code relating to medicinal products for human use (Art. 104, QPPV) (EUR-Lex)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32001L0083)
- [Commission Implementing Regulation (EU) No 520/2012 — performance of pharmacovigilance activities (EUR-Lex)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32012R0520)
- [EMA — Good Pharmacovigilance Practices (GVP) Module I: Pharmacovigilance systems and their quality systems](https://www.ema.europa.eu/en/human-regulatory-overview/post-authorisation/pharmacovigilance-post-authorisation/good-pharmacovigilance-practices)
- [EU GMP Annex 16 — Certification by a Qualified Person and Batch Release (EudraLex Vol. 4)](https://health.ec.europa.eu/medicinal-products/eudralex/eudralex-volume-4_en)
- [Commission Delegated Regulation (EU) 2017/1569 — GMP for investigational medicinal products (EUR-Lex)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32017R1569)
