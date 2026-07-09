---
title: "ClinicalTrials.gov Registration and Results — FDAAA 801 / 42 CFR Part 11"
section: "03-documents"
status: confirmed
governing_authority:
  - "FDAAA 801 (Pub. L. 110-85 §801; 42 U.S.C. 282(j))"
  - "42 CFR Part 11 (Clinical Trials Registration and Results Information Submission — Final Rule)"
  - "Form FDA 3674 (certification of compliance)"
tags: [lifecycle/activation, lifecycle/conduct, lifecycle/closeout, usc/282j, fda-form/3674, role/sponsor, role/sponsor-investigator, ossicro/engine, ossicro/gating, status/confirmed]
aliases: ["ClinicalTrials.gov", "CT.gov", "FDAAA 801", "42 CFR Part 11", "trial registration", "results reporting", "NCT number"]
updated: 2026-07-09
---

# ClinicalTrials.gov Registration and Results — FDAAA 801 / 42 CFR Part 11

> [!authority] Governing authority
> **FDAAA 801** (Food and Drug Administration Amendments Act of 2007, §801; **Pub. L. 110-85**), codified at **42 U.S.C. 282(j)**, and its implementing regulation **42 CFR Part 11** (the "Final Rule," effective Jan 18 2017). The IND-side certification is **Form FDA 3674**, which accompanies the [[ind-application-312-23|IND]]. Enforcement is by FDA (civil money penalties, potential grant-funding consequences). Status: **Confirmed** — statutory and regulatory obligations for **applicable clinical trials**.

ClinicalTrials.gov registration and results reporting is a **statutory obligation owned by the "responsible party."** It is distinct from IND submission, IRB approval, and safety reporting: it is a **public-transparency** duty enforced under a different statute (FDAAA 801 / 42 U.S.C. 282(j)) and regulation (42 CFR Part 11), administered by the **National Library of Medicine (NLM/NIH)** on the ClinicalTrials.gov platform, with FDA holding the enforcement authority. For a Phase 2 drug trial — OSSICRO's central scenario — the trial is almost always an **"applicable clinical trial" (ACT)**, so the obligation attaches. This page specifies who the responsible party is, what qualifies as an ACT, the two clocks (registration and results), and how OSSICRO drives the submission without ever owning the human attestations.

In the [[sponsor-investigator]] model the responsible party is **the sponsor-investigator themselves** — the same physician who holds the IND. There is no institutional sponsor to default the obligation to. This is one more duty that concentrates on the solo investigator and one more clock that is easy to miss without a coordination layer watching it; the **21-day registration window** in particular runs fast against a first-enrollment date that a busy clinician may not flag.

## Who is the "responsible party"

Under 42 CFR 11.4, the responsible party is either:
- the **sponsor** of the clinical trial (as defined in 21 CFR 50.3 — the person who initiates the trial), **or**
- the **principal investigator**, if so designated by the sponsor, provided the PI is responsible for conducting the trial, has access to and control over the data, has the right to publish results, and can meet all the reporting obligations.

In a [[sponsor-investigator]] IND both definitions land on the **same person**, so the sponsor-investigator is unambiguously the responsible party. In [[two-modes-site-vs-sponsor-investigator|Mode A]] (physician-as-site on a [[pharma-partner-sponsor|pharma sponsor's]] protocol), the **pharma sponsor** is the responsible party and registration is *their* duty — the OSSICRO site does not register the trial, and confirming that the sponsor has registered is part of the site's due diligence.

## What is an "applicable clinical trial" (ACT)

The ACT definition (42 CFR 11.22) is the gating question. In brief, an **applicable drug clinical trial** is a controlled clinical investigation (other than a Phase 1 trial) of a drug or biologic subject to FDA regulation, that meets one of the ACT-specifying conditions (e.g., has one or more sites in the US, is conducted under an IND, or involves a drug manufactured in and exported from the US). Key consequences for OSSICRO's scenario:

- **Phase 1 trials are excluded** from the ACT definition — a first-in-human Phase 1 study generally does not carry the FDAAA registration/results duty (though NIH-funded trials carry a separate NIH policy obligation to register *all* NIH-funded trials, and voluntary registration is permitted).
- **Phase 2 and later drug trials under an IND are ACTs** — OSSICRO's central early-phase scenario qualifies, so the obligation attaches by default. The engine flags Phase-1-only studies as *presumptively out of scope* (with the NIH-funding caveat surfaced) and Phase-2+ studies as *in scope*.

> [!warning] Non-delegable
> The **ACT determination** ("is this trial an applicable clinical trial?"), the **responsible-party designation**, and the **Form FDA 3674 certification** are legal attestations owned by the responsible party (the [[sponsor-investigator]] or pharma sponsor). Form 3674 certifies to FDA that the applicable requirements of 42 U.S.C. 282(j) have been met — a **false certification is a prohibited act** under the FDCA. OSSICRO may *analyze* the ACT question and *pre-populate* the 3674, but it must never machine-certify compliance or machine-decide that a borderline trial is out of scope. The human responsible party makes the determination and signs. See [[non-delegable-functions-and-gates]].

## The two clocks

### Registration — within 21 days of first enrollment
The responsible party must **register** the ACT on ClinicalTrials.gov **not later than 21 calendar days after the first human subject is enrolled**. Registration produces the **NCT number** — the trial's public identifier, which then propagates into the [[investigators-brochure|IB]], the [[informed-consent-form|ICF]] (the consent form must disclose that trial information will be posted), publications, and the [[regulatory-binder-isf-index|regulatory binder]]. Registration content (42 CFR 11.28) includes descriptive information, recruitment information, location/contact information, and administrative data.

### Results — generally within 1 year of primary completion
The responsible party must submit **results information** **not later than 1 year after the primary completion date** (the date of final data collection for the primary outcome measure). Results content (42 CFR 11.48) includes the **participant flow, demographic and baseline characteristics, outcome measures and statistical analyses, and adverse-event information** (serious and other adverse events by arm). Deadline extensions and delayed-submission mechanisms exist under 42 CFR 11.44 (e.g., for good cause or where the drug is not yet approved), but they must be requested — the default clock runs at one year.

OSSICRO computes both clocks from the **first-enrollment date** and the **primary-completion date** in the [[data-model]] and drives them through the same milestone tracker that runs the [[safety-clock-engine]] and the [[ind-annual-report-dsur|annual-report]] clock. Registration is a **startup/early-conduct** event; results submission is a **closeout** event (see [[closeout]]).

## Form FDA 3674 — the IND-side certification

Form FDA 3674 is the **certification of compliance** with the ClinicalTrials.gov requirements that accompanies certain FDA submissions, including the IND. It certifies either that the trial is not an ACT, or that the ACT registration requirement has been (or will be) met, with the NCT number where available. It is a load-bearing form in the [[startup-tmf-checklist|startup package]] and is detailed on its own page: [[form-fda-3674-clinicaltrialsgov-certification]]. The 3674 is retained in the [[regulatory-binder-isf-index|regulatory binder]] (Tab 3, with the IND correspondence).

## Enforcement and why it matters

FDAAA 801 non-compliance is enforceable: FDA may issue a **Notice of Noncompliance**, impose **civil money penalties**, and NIH may withhold or recover grant funds for federally-funded trials. Non-compliant registration/results status is also increasingly a **journal-publication barrier** (ICMJE requires prospective registration as a condition of publication) and a **pharma-partner trust signal**. For OSSICRO's mission — making a small or new site credible to a sponsor — a clean, on-time ClinicalTrials.gov record is part of the [[verifiable-site-qualification-dossier]].

> [!interpretive] OSSICRO position
> OSSICRO integrates the **ClinicalTrials.gov API v2** for *discovery* (the [[matching-engine|matching]] and [[feasibility-and-patient-matching|feasibility]] front-door reads the public registry) and drives the *submission* side through the deadline engine and the Protocol Registration and Results System (PRS) data model. The "generate" pass drafts the registration record and the results tables from the trial database; the "check" pass verifies the 42 CFR 11.28 / 11.48 required elements are present; the "validate" pass holds the submission in a **gated** state until the responsible party confirms the ACT determination, verifies the content, and authorizes the human PRS submission. The engine **never** submits to ClinicalTrials.gov on its own and **never** machine-certifies the 3674. Note the two roles the registry plays for OSSICRO are cleanly separated: *reading* it for matching is unregulated public-data ingestion; *writing* to it is a gated responsible-party act. See [[data-integrations-ctgov-pubmed]].

## Related
- [[form-fda-3674-clinicaltrialsgov-certification]]
- [[ind-application-312-23]]
- [[startup-tmf-checklist]]
- [[closeout-tmf-checklist]]
- [[closeout]]
- [[regulatory-binder-isf-index]]
- [[informed-consent-form]]
- [[feasibility-and-patient-matching]]
- [[matching-engine]]
- [[data-integrations-ctgov-pubmed]]
- [[verifiable-site-qualification-dossier]]
- [[non-delegable-functions-and-gates]]

## Sources
- [eCFR — 42 CFR Part 11 (Clinical Trials Registration and Results Information Submission)](https://www.ecfr.gov/current/title-42/chapter-I/subchapter-A/part-11)
- [42 U.S.C. 282(j) — Clinical trial registry data bank (Cornell LII)](https://www.law.cornell.edu/uscode/text/42/282)
- [FDAAA 801 — Pub. L. 110-85 §801 (govinfo)](https://www.govinfo.gov/content/pkg/PLAW-110publ85/html/PLAW-110publ85.htm)
- [FDA — ClinicalTrials.gov: Definitions, Laws, and Regulations](https://www.fda.gov/science-research/clinical-trials-and-human-subject-protection/clinicaltrialsgov) — local: `../../sources/fda-guidance/FDA_ClinicalTrialsGov-Definitions-Laws-Regs.pdf`
- [ClinicalTrials.gov — How to Register and Report Results](https://clinicaltrials.gov/policy)
- [ClinicalTrials.gov Data API (v2)](https://clinicaltrials.gov/data-api) — used for discovery/matching
- Local regulation copy: `../../sources/cfr/42CFR-Part11-ClinicalTrialsGov_2025.pdf`
