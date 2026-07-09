---
title: "Single-Patient Site and Pharma Acceptance: The Backend to Accept an n-of-1 Site"
section: "04-coordination"
status: mixed
governing_authority:
  - "21 CFR 312.310 (individual-patient expanded access); Part 312 Subpart I"
  - "21 CFR 312.53 / Part 54 (investigator selection; financial disclosure)"
  - "21 CFR 312.32 (safety-data exchange / IND safety reporting)"
  - "FDCA §561A (manufacturer expanded-access policy); ICH E6(R3) (site selection/oversight)"
  - "42 U.S.C. §1320a-7b(b); 42 CFR 1001.952(d) (AKS + safe harbor)"
tags: [role/pharma, role/sponsor-investigator, role/sponsor, cfr/312, cfr/54, fda-form/3926, lifecycle/expanded-access, lifecycle/activation, ossicro/micro-cro, status/mixed]
aliases: ["n-of-1 site acceptance", "single patient site pharma backend", "one patient site qualification", "pharma acceptance of solo site"]
updated: 2026-07-09
---

# Single-Patient Site and Pharma Acceptance: The Backend to Accept an n-of-1 Site

> [!authority] Governing authority
> 21 CFR 312.310 and Part 312 Subpart I (individual-patient access); 21 CFR 312.53 and Part 54 (investigator qualification and financial disclosure); 21 CFR 312.32 (safety-data exchange); FDCA § 561A (the manufacturer's non-compellable decision to supply); ICH E6(R3) (risk-proportionate site selection and oversight); 42 U.S.C. § 1320a-7b(b) and 42 CFR 1001.952(d) (Anti-Kickback and safe harbor). Status: **Mixed** — the acceptance requirements and the supply/safety obligations are black-letter or binding; the "minimal-but-compliant" package, the route-likelihood ranking, and OSSICRO's dossier design are interpretive positions.

The hardest coordination problem OSSICRO solves is asymmetric: a single physician with a single patient needs a pharma company to say **yes** — supply the drug, exchange safety data, accept the site — for an engagement so small that the company's standard site-onboarding machinery is economically absurd to run for it. This page is written from the **pharma side**: what a manufacturer actually needs to accept an n-of-1 site without either (a) violating its GCP, safety, and compliance obligations, or (b) spending six-figure activation cost on a one-patient engagement. It is the counterpart to the physician-facing [single-patient-site-enrollment](../02-lifecycle/single-patient-site-enrollment.md) and [expanded-access-coordination](expanded-access-coordination.md) pages.

## The three routes an n-of-1 request can take

A "one physician, one patient, one pharma therapy" request resolves to one of three legally distinct structures — the manufacturer's backend differs for each:

| Route | Structure | Pharma role | Backend the manufacturer runs |
|-------|-----------|-------------|-------------------------------|
| **1. Individual-patient expanded access** | [§ 312.310](expanded-access-coordination.md), [Form 3926](../03-documents/form-fda-3926-expanded-access.md) | **Supplier** (must agree; not sponsor) | Expanded-access intake → LOA/supply decision → safety-data exchange |
| **2. One-patient site added to an existing sponsor protocol** | Site activation on the company's [IND](../02-lifecycle/ind-submission-and-30-day-clock.md) | **Sponsor** | Full [site qualification and activation](pharma-partner-interface-iis.md) → CTA → SIV → drug release |
| **3. Sponsor-investigator single-patient study** | Physician holds own IND; pharma supplies/funds | **Supporter** ([IIS](pharma-partner-interface-iis.md)) | Medical-Affairs IIS review → supply/grant → safety exchange |

The manufacturer's first job is to **triage to the correct route**, because the document set, the accountable parties, and the legal exposure differ entirely. OSSICRO's engine performs the same triage from the physician side; the two must agree on which route is live.

### Route likelihood is not symmetric — triage accordingly

The three routes are not equally likely to be granted, and a triage that treats them as interchangeable will send a physician down the path pharma is least likely to accept:

- **Route 1 (individual-patient expanded access)** is the purpose-built regulatory mechanism for exactly this fact pattern and is the route manufacturers most commonly grant when they grant anything. The manufacturer's role is bounded (supplier, not sponsor), the process is standing (most companies operate a § 561A-published expanded-access intake), and the marginal cost per request is low.
- **Route 3 (sponsor-investigator study)** is viable where the physician can carry sponsor obligations and the manufacturer's Medical Affairs function has an IIS program open to single-patient or small-N proposals. It shifts the sponsor burden off the company, which is often what makes it acceptable.
- **Route 2 (adding a one-patient site to an active company protocol)** is the **least likely route to be granted** and should be the default only when the sponsor has an open site-identification need that the physician's site happens to fill. See the next section for why.

This ranking is an interpretive position grounded in sponsor practice, not a regulatory requirement; it is nevertheless the ordering OSSICRO's triage applies unless facts indicate otherwise.

## Why Route 2 is the hard sell: sponsor-side costs OSSICRO cannot reduce

OSSICRO's dossier compresses the *site-side* qualification evidence, but adding any site — even a one-subject site — to an active protocol imposes **sponsor-side marginal costs that software running at the site does not absorb**:

- **Protocol-specific EDC build:** a new site account, roles, and user training in the sponsor's validated EDC instance.
- **IRT/RTSM configuration and a new drug-supply shipping lane:** randomization/trial-supply system changes plus depot-to-site logistics, qualification of the shipping route, and temperature-excursion handling for a lane that will serve one subject.
- **Monitoring:** scheduled interim monitoring visits (or risk-based remote equivalents) for a one-subject site — a per-site fixed cost that no enrollment volume amortizes.
- **Indemnification and insurance:** amendment of the sponsor's clinical-trial insurance and indemnity schedules to add the site and institution.
- **Inspection footprint:** every added site is an added [BIMO](fda-interactions-meetings-holds.md)-inspectable node the sponsor must stand behind.
- **Internal change control on an active protocol:** site-list changes ripple through the sponsor's TMF, monitoring plan, and (where applicable) regulatory notifications — process cost borne entirely by the sponsor mid-enrollment.

Because these costs are the sponsor's and are largely fixed per site, sponsors mid-enrollment **routinely refuse one-patient site additions outright**. The expected counter-offers, which the physician should anticipate rather than treat as failure:

- **Referral to the nearest active site** — the sponsor keeps its site list closed and offers the patient screening at an existing site; or
- **Individual-patient expanded access (Route 1)** — the sponsor supplies drug outside the trial, keeping the trial's site economics and data integrity untouched.

Both counter-offers are legitimate and often serve the patient faster than a site-activation fight. OSSICRO's triage therefore prefers Routes 1 and 3 and surfaces Route 2 only where travel/medical constraints rule out an existing site *and* the sponsor has signaled openness to site addition. Where a sponsor's risk assessment does permit an expedited qualification in place of a full SQV, ICH E6(R3) risk-proportionality supports it — but that is the sponsor's discretionary call, not a package the physician can compel.

## What the manufacturer needs to say yes (the acceptance gate)

A sponsor's trust gate for an unproven, tiny site is **evidence of legally-accountable GCP capacity, not software polish**. Concretely, before it will supply drug and exchange data, a manufacturer (or its Medical Affairs / expanded-access function) needs:

1. **A qualified, licensed PI** with a clean regulatory record and a signed [1572](../03-documents/form-fda-1572-statement-of-investigator.md)-equivalent commitment (or, for expanded access, the physician's § 312.310(a) determination and qualification statement).
2. **An IRB of record** — a central-IRB relationship de-risks a new site fastest (see [single-irb-mandate-and-central-irbs](single-irb-mandate-and-central-irbs.md)); for single-patient expanded access, the § 56.105 IRB-chair concurrence pathway.
3. **Demonstrable GCP training** (ICH E6(R3)) for the PI and any delegated staff.
4. **SOPs** for [informed consent](informed-consent-document-vs-event.md), [drug accountability/storage](../03-documents/drug-accountability-log.md) (temperature-monitored), source documentation, and AE/SAE reporting.
5. **[Financial disclosures](../03-documents/form-fda-3454-3455-financial-disclosure.md)** (Part 54; Forms 3454/3455) and an [FMV-set](../03-documents/clinical-trial-agreement-and-budget.md) budget where any payment flows.
6. **A validated, [Part 11](../05-ossicro-system/part-11-and-ai-credibility.md)-compliant document/data environment** — for **Routes 2 and 3**, where trial records subject to Part 11 predicate rules are created and maintained electronically. For **Route 1** (individual-patient expanded access) this is *not* a manufacturer requirement: treating physicians run expanded access on ordinary medical-records practice (paper or institutional EMR), and expanded-access coordinators do not demand Part 11 validation evidence. OSSICRO's Part 11 tooling is a convenience for the Route 1 physician, not a gate item.
7. **Pharmacovigilance intake** capable of meeting expedited-reporting timelines.
8. **Inspection readiness** ([BIMO](fda-interactions-meetings-holds.md)) — proportionate to route; for Route 1 this reduces to keeping records adequate to the § 312.310 treatment plan and reporting duties.

The [research corpus](../references/institutional-resources.md)'s load-bearing finding: "the single most persuasive artifact to a skeptical sponsor is a complete, internally-consistent essential-documents package plus a credentialed accountable investigator." That is the exact deliverable OSSICRO is built to produce.

## Drug-supply authorization — the manufacturer's letter

Nothing moves without the manufacturer's affirmative decision to supply. For **expanded access**, this takes the form of the **Letter of Authorization (LOA)** that lets FDA cross-reference the manufacturer's IND (§ 312.305(b)(1)); for a **sponsor-investigator study**, a **supply/support (grant) agreement**; for a **one-patient site on the company's protocol**, drug release at the [Site Initiation Visit](pharma-partner-interface-iis.md) after activation.

> [!warning] Non-delegable
> **The manufacturer's decision to supply the drug is the manufacturer's alone and cannot be compelled** — FDA authorization of an expanded-access request does not obligate the company to provide the product (FDCA § 561A). OSSICRO can assemble a supply-ready request package and a safe-harbor-shaped support agreement, but the supply decision, the LOA signature, and the FMV/anti-kickback judgment are the manufacturer's and its counsel's. OSSICRO never supplies, never authorizes, and never signs for the manufacturer. See [non-delegable-functions-and-gates](../05-ossicro-system/non-delegable-functions-and-gates.md).

## Safety-data exchange

Whichever route is live, a **safety-data exchange** must be defined so that adverse events reach the party that owns the [IND safety-reporting](../03-documents/ind-safety-report.md) obligation on the required timelines (§ 312.32; the 7-day and 15-day clocks — see [safety-report-timelines-7-15-day](safety-report-timelines-7-15-day.md)):

- **Expanded access / sponsor-investigator study:** the physician-as-sponsor-investigator holds the IND safety-reporting duty; the manufacturer, as the drug's developer, needs the safety data flowing back to its own pharmacovigilance so its aggregate safety profile and IB stay current. A **Safety Data Exchange Agreement (SDEA)** or equivalent defines who reports what, to whom, and by when.
- **One-patient site on the company's protocol:** the company (sponsor) holds the reporting duty; the site reports SAEs to the sponsor per protocol and [§ 312.64](../01-roles-responsibilities/investigator.md).

> [!warning] Non-delegable
> **Causality and expectedness determinations that trigger a 7-day or 15-day IND safety report are the sponsor's / medical monitor's medical judgment (21 CFR 312.32; ICH E2A).** OSSICRO intakes the event, codes it, drafts the narrative and the [MedWatch 3500A](../03-documents/form-fda-3500a-medwatch.md), and computes the deadline — it does **not** adjudicate causality or file. A qualified physician owns the call and the signature. See [safety-reporting-workflow](safety-reporting-workflow.md).

## The minimal-but-compliant package

The economic tension — full activation cost vs. a one-patient engagement — is resolved by **risk-proportionality** (ICH E6(R3)): the package is scaled to a single-patient treatment or study, not to a multi-site pivotal trial, while every irreducible element is still present. A minimal-but-compliant n-of-1 package is, per route:

- **Expanded access (Route 1):** [Form 3926](../03-documents/form-fda-3926-expanded-access.md) + clinical narrative + treatment/monitoring plan; the manufacturer's LOA; physician qualification statement; [consent form](../03-documents/informed-consent-form.md); IRB approval or § 56.105 chair concurrence; drug-accountability SOP; ordinary medical-records practice for documentation. **No CTA, no full site-activation binder, no Part 11 validation evidence** — expanded access is treatment, not a trial.
- **One-patient site (Route 2):** the standard [activation essential-document set](pharma-partner-interface-iis.md) (CTA + FMV budget, IRB approval, 1572, CVs/licenses, 3454/3455, delegation log, training, SOPs). A dossier this complete supports the *site side* of qualification, and where the sponsor's risk assessment permits, E6(R3) supports an expedited qualification in place of a full SQV — but the sponsor-side marginal costs enumerated above remain, and the realistic outcome is often a counter-offer (referral to an active site, or Route 1) rather than activation.
- **Sponsor-investigator study (Route 3):** IIS concept + protocol; support/grant agreement; the physician's own [IND package](../02-lifecycle/pre-ind-and-ind-preparation.md); SDEA; financial disclosure.

> [!interpretive] OSSICRO position
> OSSICRO's wedge on the pharma side is a **[verifiable site-qualification dossier](../05-ossicro-system/verifiable-site-qualification-dossier.md)**: a citation-complete, hash-chained manifest that maps each acceptance-gate requirement (1–8 above) to the artifact that satisfies it, its governing citation, and the human signer — rendered so a Medical Affairs reviewer or expanded-access coordinator can verify a one-patient site in a single pass instead of running full onboarding machinery. The dossier's leverage is greatest where site-side evidence is the binding constraint (Routes 1 and 3); it cannot make Route 2 economic for a sponsor, because the sponsor's own marginal costs (EDC build, IRT/supply lane, monitoring, insurance, inspection footprint, change control) are outside the site's control. The claim that a verifiable dossier is *sufficient* to change a manufacturer's acceptance calculus is interpretive and unproven at scale; what is confirmed is that a complete, credentialed, internally-consistent package is what a sponsor's trust gate actually requires. The failed disintermediation plays ([Science 37, TrialSpark](../00-overview/failed-disintermediation-case-studies.md)) warn that the dossier's value depends on a real accountable entity standing behind it — the [micro-CRO accountable layer](../01-roles-responsibilities/micro-cro-accountable-layer.md) or the sponsor-investigator personally — never the software itself. Status: interpretive.

## What OSSICRO generates vs. what stays human

- **Generates (drafts for review):** route triage (Routes 1/3 preferred; Route 2 flagged with its expected counter-offers); the per-route minimal-but-compliant package; the verifiable qualification dossier mapped to the manufacturer's acceptance gate; the LOA/supply-request and safe-harbor-shaped support agreement skeleton; the SDEA scaffold; safety-report drafts and deadline computation.
- **Stays human/entity (gated):** the manufacturer's supply decision and LOA signature; the sponsor's site-addition and SQV-waiver decisions; FMV and anti-kickback judgment; PI qualification attestation; IRB approval; the consent event; causality/expectedness determinations; and the accountable entity that stands behind the dossier.

## Related
- [[single-patient-site-enrollment]]
- [[expanded-access-coordination]]
- [[form-fda-3926-expanded-access]]
- [[pharma-partner-interface-iis]]
- [[pharma-partner-sponsor]]
- [[sponsor-investigator]]
- [[micro-cro-accountable-layer]]
- [[verifiable-site-qualification-dossier]]
- [[safety-reporting-workflow]]
- [[safety-report-timelines-7-15-day]]
- [[single-irb-mandate-and-central-irbs]]
- [[non-delegable-functions-and-gates]]

## Sources
- [21 CFR 312.310 — Individual patients, including for emergency use](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-I/section-312.310)
- [21 CFR 312.305 — Requirements for all expanded access uses (LOA / cross-reference)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-I/section-312.305)
- [21 CFR 312.53 — Selecting investigators and monitors](https://www.law.cornell.edu/cfr/text/21/312.53)
- [21 CFR 312.32 — IND safety reporting](https://www.law.cornell.edu/cfr/text/21/312.32)
- [21 CFR Part 54 — Financial disclosure by clinical investigators](https://www.law.cornell.edu/cfr/text/21/part-54)
- [FDA — Expanded Access: Information for Physicians (supply and manufacturer role)](https://www.fda.gov/news-events/expanded-access/expanded-access-information-physicians)
- [FDA Guidance — Expanded Access to Investigational Drugs for Treatment Use: Q&A](https://www.fda.gov/media/162793/download)
- [FDA — E6(R3) Good Clinical Practice guidance (risk-proportionate site selection)](https://www.fda.gov/media/169090/download)
- [42 CFR 1001.952(d) — Personal services and management contracts safe harbor](https://www.law.cornell.edu/cfr/text/42/1001.952)