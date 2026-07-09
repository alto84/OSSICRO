---
title: "Two Modes — Physician-as-Site vs. Sponsor-Investigator"
section: "05-ossicro-system"
status: mixed
governing_authority:
  - "21 CFR 312.3(b) (Sponsor-investigator)"
  - "21 CFR 312.50-312.59 (Sponsor responsibilities)"
  - "21 CFR 312.60-312.69 (Investigator responsibilities)"
  - "21 CFR 312.20-312.23 (IND submission)"
  - "21 CFR Part 312 Subpart I / 312.310 (Expanded access)"
tags: [ossicro/engine, ossicro/gating, role/sponsor-investigator, role/investigator, cfr/312, lifecycle/ind, lifecycle/expanded-access, status/interpretive]
aliases: ["Two Modes", "Mode A vs Mode B", "Site vs Sponsor-Investigator"]
updated: 2026-07-09
---

# Two Modes — Physician-as-Site vs. Sponsor-Investigator

> [!authority] Governing authority
> [21 CFR 312.3(b)](https://www.law.cornell.edu/cfr/text/21/312.3) (sponsor-investigator dual role); [21 CFR 312.50-312.59](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D) (sponsor duties); [21 CFR 312.60-312.69](https://www.law.cornell.edu/cfr/text/21/312.60) (investigator duties); [21 CFR 312.20-312.23](https://www.law.cornell.edu/cfr/text/21/312.23) (IND submission); [21 CFR Part 312 Subpart I](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-I) (expanded access). Status: **Mixed** — the mode definitions and their obligation sets are black-letter law; the claim that a single document engine can serve all three is the OSSICRO position, labelled interpretive.

OSSICRO supports two operating modes plus one branch, because the *accountable party*, the *document set*, and the *gates* differ entirely by which one a clinician is in — and getting the mode wrong is a legal error, not a workflow inconvenience. **Mode A** is the physician enrolling as a *site* on a pharma sponsor's protocol. **Mode B** is the physician acting as [[sponsor-investigator|sponsor-investigator]] on their own IND. The **expanded-access branch** serves the single-patient treatment case where no trial fits. This page is the triage that routes a clinician into the correct mode and states, for each, who is accountable, what OSSICRO generates, and what remains non-delegable. The narrative triage that feeds this page is [[the-three-pathways-triage]].

## The distinction that governs everything downstream

The controlling variable is **who holds the IND and the sponsor obligation set**.

- In **Mode A**, the pharma company is the sponsor and holds the IND ([21 CFR 312.50-312.59](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D)); the physician is *only* an investigator and carries only the investigator obligation set ([21 CFR 312.60-312.69](https://www.law.cornell.edu/cfr/text/21/312.60)).
- In **Mode B**, the physician is a [[sponsor-investigator]] under [21 CFR 312.3(b)](https://www.law.cornell.edu/cfr/text/21/312.3) and carries **both** obligation sets simultaneously — the definition is explicit that "the obligations of a sponsor-investigator include both those of a sponsor and those of an investigator," and the role "does not include any person other than an individual."
- In the **expanded-access branch**, the physician typically holds an individual-patient IND ([21 CFR 312.310](https://www.law.cornell.edu/cfr/text/21/312.310)) but the activity is *treatment, not research* — no generalizable-data expectation — and the manufacturer's decision to supply is a separate non-delegable counterparty judgment.

Everything else — which forms, which gates, which counterparties, what OSSICRO drafts — is downstream of this single fork.

## Mode A — Physician-as-site

The pharma company is sponsor; the physician joins an existing protocol as a site investigator. The physician's biggest liability is the absence of a track record — a new site with no research office is exactly what a sponsor's feasibility process is built to screen out. OSSICRO's job is to convert that liability into a **verifiable site-activation dossier** produced to sponsor standard.

**Accountable party:** the pharma [[pharma-partner-sponsor|sponsor]] holds the IND and sponsor obligations; the physician holds investigator obligations ([21 CFR 312.60-312.69](https://www.law.cornell.edu/cfr/text/21/312.60)).

**OSSICRO generates** (the site-activation essential-document package — see [[site-activation]] and [[startup-tmf-checklist]]):

- [[form-fda-1572-statement-of-investigator|Form FDA 1572]] (Statement of Investigator), draft for signature.
- Investigator CV, medical license, and PI qualification documentation.
- [[form-fda-3454-3455-financial-disclosure|Financial disclosure]] (Form FDA 3454/3455 inputs).
- GCP/protocol training records; delegation-of-authority log ([[delegation-of-authority-log]]).
- [[clinical-trial-agreement-and-budget|CTA and budget]] drafts (FMV-set); lab certifications; drug-accountability SOPs ([[drug-accountability-log]]).
- The [[irb-submission-package|IRB submission package]] and evidence of approval.

> [!warning] Non-delegable (Mode A)
> The PI qualification attestation and the [[form-fda-1572-statement-of-investigator|Form 1572]] signature (the investigator's personal commitment to conduct per protocol, obtain consent under [Part 50](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50), and ensure [Part 56](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56) IRB review); the patient [[informed-consent-form|informed-consent event]]; [[irb-iec|IRB approval]]; SAE reporting to the sponsor ([21 CFR 312.64](https://www.law.cornell.edu/cfr/text/21/312.64)); and the eligibility judgment at [[enrollment-and-consent|enrollment]]. OSSICRO drafts the package; the investigator owns and signs every one of these acts.

## Mode B — Sponsor-investigator IND

The physician holds the IND and both obligation sets. This is the OSSICRO-viable structure that makes the whole thesis lawful: no obligation is transferred to a non-entity, and AI absorbs the coordination labor that normally makes the dual role impractical for a solo clinician. The legal argument is developed at [[legal-thesis-3123-vs-31252]].

**Accountable party:** the physician, as [[sponsor-investigator]], holds **both** [21 CFR 312.50-312.59](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D) *and* [21 CFR 312.60-312.69](https://www.law.cornell.edu/cfr/text/21/312.60), plus IND submission ([312.20-312.23](https://www.law.cornell.edu/cfr/text/21/312.23)), safety reporting ([312.32](https://www.law.cornell.edu/cfr/text/21/312.32)), and annual reporting ([312.33](https://www.law.cornell.edu/cfr/text/21/312.33)). A [[micro-cro-operating-model|micro-CRO]] may hold enumerated *sponsor* functions via a [[transfer-of-regulatory-obligations-toro|TORO]] where the clinician cannot personally discharge them.

**OSSICRO generates** (the full IND package — see [[pre-ind-and-ind-preparation]] and [[ind-application-312-23]]):

- [[form-fda-1571-ind-cover|Form FDA 1571]] (IND cover/commitment) draft.
- General investigational plan; [[clinical-protocol-and-synopsis|clinical protocol]] (ICH M11 structured target); [[investigators-brochure|Investigator's Brochure]]; CMC, pharm/tox, and prior-human-experience sections ([312.23](https://www.law.cornell.edu/cfr/text/21/312.23)).
- The 30-day-clock tracker ([[ind-submission-and-30-day-clock]]) and the maintenance artifacts: [[ind-safety-report|IND safety reports]] ([312.32](https://www.law.cornell.edu/cfr/text/21/312.32)), [[ind-annual-report-dsur|annual report/DSUR]] ([312.33](https://www.law.cornell.edu/cfr/text/21/312.33)), and the six protocol/information amendment types ([312.30-312.31](https://www.law.cornell.edu/cfr/text/21/312.30)).
- Plus the entire Mode A site-level package, because the sponsor-investigator is *also* the site.

Any pharma partner in Mode B is **only** an IIS supplier/funder — Medical Affairs, fair-market-value-set, [[iis-request-workflow|Sunshine-reportable]] — never OSSICRO's transferee and never the sponsor. See [[pharma-partner-interface-iis]].

> [!warning] Non-delegable (Mode B)
> Everything in Mode A's non-delegable list **plus** the [[form-fda-1571-ind-cover|Form 1571]] IND-holder attestation, IND-holder accountability itself, the causality/expectedness determination that triggers a 7- or 15-day [[ind-safety-report|IND safety report]] ([21 CFR 312.32](https://www.law.cornell.edu/cfr/text/21/312.32) — the [[medical-monitor]]'s judgment), [[biostatistician|statistical sign-off]], and the decision to discontinue an investigation presenting unreasonable risk within 5 working days ([312.56(d)](https://www.law.cornell.edu/cfr/text/21/312.56)). The [[safety-clock-engine]] computes and escalates the deadlines; it never makes the causality call and never files.

## The expanded-access branch

For "no trial fits, single patient," the pathway is treatment under [21 CFR Part 312 Subpart I](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-I): individual-patient expanded access ([312.310](https://www.law.cornell.edu/cfr/text/21/312.310)), intermediate-size ([312.315](https://www.law.cornell.edu/cfr/text/21/312.315)), or treatment IND/protocol ([312.320](https://www.law.cornell.edu/cfr/text/21/312.320)). The individual-patient route uses [[form-fda-3926-expanded-access|Form FDA 3926]], a manufacturer letter of authorization, and IRB concurrence. It is surfaced as a distinct workflow with **no generalizable-data expectation** — it is not research. See [[expanded-access-workflow]] and [[single-patient-site-enrollment]].

> [!warning] Non-delegable (expanded access)
> The manufacturer's decision to supply the investigational product is a counterparty judgment that no software and no micro-CRO can make on the manufacturer's behalf ([FDCA §561A](https://www.govinfo.gov/content/pkg/USCODE-2018-title21/html/USCODE-2018-title21-chap9-subchapV-partE-sec360bbb-0.htm)). The physician's consent event and the [[irb-iec|IRB concurrence]] remain non-delegable as in the two modes.

## How the document sets and gates diverge — at a glance

| | Mode A (site) | Mode B (sponsor-investigator) | Expanded access |
|---|---|---|---|
| **Who holds the IND** | Pharma sponsor | The physician | The physician (individual-patient IND) |
| **Obligation set on the physician** | Investigator only (§312.60-312.69) | **Both** sponsor + investigator (§312.3(b)) | Treating physician; §312.310 obligations |
| **Core OSSICRO output** | Site-activation dossier | Full IND package + site package | Form 3926 + LOA + IRB concurrence |
| **Signature gate** | Form 1572 | Form 1571 **and** Form 1572 | Form 3926 |
| **Safety reporting** | AE→sponsor (§312.64) | AE→SAE→FDA/IRB/investigators (§312.32) | Follow-up per §312.310(c) |
| **Pharma role** | Sponsor | IIS supplier/funder only | Manufacturer (supply authorization) |
| **Data expectation** | Generalizable (research) | Generalizable (research) | Treatment — **not** research |

> [!interpretive] OSSICRO position
> The interpretive claim is that **one** generate/check/validate engine, parameterized by mode, can serve all three — because the underlying essential-records matrix (ICH E6(R3) Appendix C, risk-proportionate) is shared, and the mode selects which subset of records, which forms, and which gate set instantiates. The engine never *chooses* the mode for the clinician; mode selection is presented as an explicit triage with the accountability consequences stated, because misclassification (e.g., running expanded-access supply as if it were a Mode A enrollment) is a regulatory error the clinician must own. The [[completeness-ledger]] tracks the mode-appropriate open items; the [[non-delegable-functions-and-gates|gating matrix]] enumerates which gates fire in which mode.

## Related

- [[the-three-pathways-triage]]
- [[sponsor-investigator]]
- [[sponsor]]
- [[investigator]]
- [[legal-thesis-3123-vs-31252]]
- [[micro-cro-operating-model]]
- [[expanded-access-workflow]]
- [[single-patient-site-enrollment]]
- [[site-activation]]
- [[ind-application-312-23]]
- [[non-delegable-functions-and-gates]]
- [[compliance-mapping]]
- [[pharma-partner-interface-iis]]

## Sources

- [21 CFR 312.3 — Definitions (sponsor-investigator) (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/312.3)
- [21 CFR Part 312 Subpart D — Responsibilities of Sponsors and Investigators (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D)
- [21 CFR 312.23 — IND content and format (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/312.23)
- [21 CFR 312.32 — IND safety reporting (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/312.32)
- [21 CFR 312.33 — Annual reports (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/312.33)
- [21 CFR Part 312 Subpart I — Expanded Access to Investigational Drugs (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-I)
- [21 CFR 312.310 — Individual patients, including for emergency use (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/312.310)
- [FDA — Overview of Sponsor-Investigator Roles and Responsibilities (media 174660)](https://www.fda.gov/media/174660/download)
- [FDA — IND Application Procedures: Investigator's Responsibilities](https://www.fda.gov/drugs/investigational-new-drug-ind-application/ind-application-procedures-investigators-responsibilities)
