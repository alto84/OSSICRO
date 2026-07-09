---
title: "Medical Monitor"
section: "01-roles-responsibilities"
status: mixed
governing_authority:
  - "21 CFR 312.32 (safety determinations)"
  - "21 CFR 312.56 (review of ongoing investigations)"
  - "21 CFR 312.52 (transferability of sponsor obligations)"
  - "ICH E6(R2) §5.3 / ICH E6(R3) Section 3 (medical expertise)"
tags: [role/medical-monitor, role/sponsor, cfr/312, ich/e6r3, ich/e2a, lifecycle/safety, lifecycle/conduct]
aliases: ["Medical Monitor", "Safety Physician", "Sponsor Medical Expert"]
updated: 2026-07-09
---

# Medical Monitor

> [!authority] Governing authority
> The title "medical monitor" does not appear in 21 CFR; the role is the operational name for the **qualified physician who discharges the sponsor's medical-judgment obligations**: safety determinations under 21 CFR 312.32, review and action on ongoing investigations under 21 CFR 312.56, and the ICH GCP requirement that the sponsor designate appropriately qualified medical personnel readily available to advise on trial-related medical questions (ICH E6(R2) §5.3, carried forward in the sponsor section of ICH E6(R3)). Status: **Mixed** — the underlying obligations are confirmed; the consolidation of them under this named role, and OSSICRO's support boundary, are interpretive framing, marked inline.

The medical monitor is the sponsor-side physician who owns the medical judgments a trial generates: whether an event is **serious**, whether it is **expected**, whether there is a **reasonable possibility the drug caused it**, and what the accumulating safety picture means for the people currently and prospectively enrolled. In a pharma organization this is a named role in Clinical Development or Drug Safety; in the OSSICRO [[sponsor-investigator]] model the function typically collapses onto the sponsor-investigator personally, unless transferred — as a sponsor obligation may be — to a legally accountable entity holding a qualified physician (21 CFR 312.52; see [[micro-cro-accountable-layer]]).

## 1. Regulatory anchor

Three confirmed obligation sets converge on this role:

1. **Safety determinations (21 CFR 312.32).** The expedited-reporting triggers are built from medical judgments: *suspected adverse reaction* requires a "reasonable possibility" causality finding; *unexpected* requires comparison of the observed event's specificity and severity against the [[investigators-brochure]]; *serious* includes the judgment call of "important medical events" that may jeopardize the patient (312.32(a)). The 15-day clock is armed by the sponsor's determination that information qualifies (312.32(c)(1)); the aggregate judgment behind an increased-rate report (312.32(c)(1)(iv)) is likewise medical. See [[pharmacovigilance-safety]] and [[safety-report-timelines-7-15-day]].
2. **Review of ongoing investigations (21 CFR 312.56).** The sponsor must review and evaluate the evidence of safety and effectiveness as it accumulates (312.56(b)–(c)) and, on determining that the drug presents an **unreasonable and significant risk** to subjects, must discontinue the affected investigations as soon as possible and no later than five working days after the determination, notifying FDA, all IRBs, and all investigators (312.56(d)). The determination is a physician-grade risk-benefit judgment.
3. **Medical expertise availability (ICH E6(R2) §5.3; E6(R3) Section 3).** GCP requires the sponsor to designate appropriately qualified medical personnel, readily available to advise on trial-related medical questions or problems — eligibility gray areas, dose-modification and stopping-rule application, management of events, and the medical dimension of protocol deviations.

> [!interpretive] OSSICRO position — why the role is named
> Consolidating these obligations under one named, credentialed human is an OSSICRO design decision, not a CFR mandate. The [[data-model]] carries `medical_monitor` as a required Gate owner on every safety-judgment gate: no SafetyReport can advance past triage, and no expedited report can be released, without a determination attributed to the named qualified physician. Naming the owner is what makes the [[non-delegable-functions-and-gates|gating matrix]] enforceable rather than aspirational.

## 2. The judgments the medical monitor owns

- **Seriousness** of each adverse event, including the "important medical event" residual category (312.32(a); ICH E2A).
- **Expectedness** against the current IB (or protocol/general investigational plan where no IB exists), at the observed specificity and severity — which also makes the medical monitor an owner of IB currency (updates flow through 312.55(b) investigator notifications and [[annual-reporting-and-amendments|information amendments]]).
- **Causality** — the "reasonable possibility" standard of 312.32(a), applied per case and in aggregate.
- **Qualification of information for expedited reporting** and the significance analysis each IND safety report must contain (312.32(c)); the report's release to FDA is a human-authorized act ([[ind-safety-report]]).
- **The continue/modify/stop safety judgment**: acting on accumulating data (312.56), on [[dsmb-dmc|DMC]] recommendations (the DMC advises; the sponsor's physician-grade judgment informs the sponsor's decision), and on the 312.56(d) unreasonable-risk trigger with its five-working-day discontinuation clock.
- **Trial-related medical advice**: eligibility adjudication support to the investigator (final eligibility remains the investigator's call — see [[matching-eligibility-adjudication]]), dose-escalation and stopping-rule application, and medical review of deviations with safety import ([[conduct-and-monitoring]]).

## 3. Qualifications and independence

The person must be qualified by training and experience in the relevant therapeutic area to make the judgments above — for an IND drug trial, a physician. FDA does not prescribe a certification; qualification is evidenced by CV and licensure retained in the TMF ([[document-catalog]]). Independence deserves explicit attention in the sponsor-investigator model: the same physician who treats the patient also adjudicates causality on the sponsor side. That dual position is lawful (it is inherent in 21 CFR 312.3(b)) but concentrates cognitive conflict; a prudent mitigations ladder runs from documented self-review discipline, to an external safety reviewer for serious cases, to a chartered [[dsmb-dmc]] where the risk profile warrants one.

## 4. Delegation and transfer

Two distinct mechanisms, frequently confused:

- **Transfer under 21 CFR 312.52.** Medical monitoring, as a sponsor obligation, may be transferred in writing to a CRO — a legally accountable **entity** that then becomes subject to the same regulatory action as a sponsor. This is the lane by which the OSSICRO [[micro-cro-accountable-layer|micro-CRO]] can supply an independent medical monitor at its paid-escalation tier, via an enumerated [[transfer-of-regulatory-obligations-toro|TORO]] naming the assumed safety-review obligations and the qualified physician who holds them. Software is not an entity and can never be the transferee ([[legal-thesis-3123-vs-31252]]).
- **Delegation of tasks.** Case processing, intake, coding suggestions, narrative drafting, and clock tracking may be performed by others (human staff or software) under the medical monitor's oversight, per the delegation discipline of [[subinvestigator-and-delegation]] — but delegation never transfers accountability, and the determinations themselves are not tasks.

Distinguish the medical monitor from the **clinical monitor (CRA)** — the person qualified by training and experience whom the sponsor selects to monitor the conduct and progress of the investigation (21 CFR 312.53(d); FDA 2013/2023 risk-based monitoring guidance). The CRA verifies site conduct and data integrity ([[clinical-monitor-cra]], [[monitoring-plan]]); the medical monitor judges medical meaning. The EU analogue of a named accountable safety physician is the QPPV ([[qualified-person-qppv-eu]]).

> [!warning] Non-delegable
> Seriousness, expectedness, and causality determinations; the qualification of safety information for expedited reporting and its significance analysis; the 312.56(d) unreasonable-risk determination; and the continue/modify/stop safety judgment are the medical monitor's (ultimately the sponsor's/sponsor-investigator's) personal, accountable medical judgments. OSSICRO drafts case narratives, suggests codes, computes the 7- and 15-day clocks, assembles line listings, and escalates unresolved determinations ([[safety-clock-engine]]) — it never makes, defaults, or auto-advances any of these calls, and a case with an absent determination fails closed to the human gate.

## Related

- [[pharmacovigilance-safety]] · [[safety-report-timelines-7-15-day]] · [[ind-safety-report]] · [[safety-clock-engine]]
- [[dsmb-dmc]] · [[clinical-monitor-cra]] · [[biostatistician]]
- [[sponsor]] · [[sponsor-investigator]] · [[investigator]] · [[subinvestigator-and-delegation]]
- [[micro-cro-accountable-layer]] · [[transfer-of-regulatory-obligations-toro]] · [[cro]]
- [[investigators-brochure]] · [[safety-management-plan]] · [[non-delegable-functions-and-gates]] · [[qualified-person-qppv-eu]]

## Sources

- [21 CFR 312.32 — IND safety reporting (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32)
- [21 CFR 312.56 — Review of ongoing investigations (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.56)
- [21 CFR 312.52 — Transfer of obligations to a contract research organization (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.52)
- [21 CFR 312.53 — Selecting investigators and monitors (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.53)
- [ICH E6(R2) — Integrated Addendum to GCP (PDF), §5.3 Medical Expertise](https://database.ich.org/sites/default/files/E6_R2_Addendum.pdf)
- [ICH E6(R3) Step 4 Final Guideline (2025-01-06, PDF)](https://database.ich.org/sites/default/files/ICH_E6(R3)_Step4_FinalGuideline_2025_0106.pdf)
- [ICH E2A — Clinical Safety Data Management: Definitions and Standards for Expedited Reporting (PDF)](https://database.ich.org/sites/default/files/E2A_Guideline.pdf)
- [FDA Guidance (Dec 2012) — Safety Reporting Requirements for INDs and BA/BE Studies](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/safety-reporting-requirements-inds-investigational-new-drug-applications-and-babe-bioavailabilitybioequivalence-studies)
