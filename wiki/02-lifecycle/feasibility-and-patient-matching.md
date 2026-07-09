---
title: "Feasibility & Patient Matching"
section: "02-lifecycle"
status: mixed
governing_authority:
  - "HIPAA Privacy Rule — 45 CFR 164.512(i)(1)(ii) (reviews preparatory to research)"
  - "45 CFR 164.508 (authorization); 45 CFR 164.512(i)(1)(i) (IRB/Privacy-Board waiver)"
  - "ClinicalTrials.gov API v2 (data source; FDAAA 801 / 42 CFR Part 11 registration context)"
tags: [lifecycle/feasibility, ossicro/matching, ossicro/gating, usc/hipaa, cfr/312, status/mixed]
aliases: ["Feasibility", "Patient Matching", "Preparatory Review"]
updated: 2026-07-09
---

# Feasibility & Patient Matching

> [!authority] Governing authority
> HIPAA Privacy Rule [45 CFR 164.512(i)(1)(ii)](https://www.ecfr.gov/current/title-45/section-164.512) (review preparatory to research); [45 CFR 164.508](https://www.ecfr.gov/current/title-45/section-164.508) (individual authorization) and [45 CFR 164.512(i)(1)(i)](https://www.ecfr.gov/current/title-45/section-164.512) (waiver of authorization) as the transition gates; ClinicalTrials.gov API v2 as the discovery data source. Status: **Mixed** — the HIPAA boundary is black-letter (confirmed); the OSSICRO semantic-matching and adjudication layer is an interpretive design position, clearly marked.

Feasibility and patient matching is the front door: a clinician has a patient (or a panel) and wants to know whether an early-phase program exists that the patient could plausibly enter, and whether the site could plausibly run it, *before* any regulated research relationship is created. This phase is the privacy fulcrum of the entire system. The single most consequential legal fact here is that identifying a candidate program from a patient's protected health information is a **review preparatory to research** — a permitted use under HIPAA that does *not* authorize enrollment, contact for recruitment beyond what the rule allows, or any PHI leaving the covered entity. The line between "matching" and "enrolling" is a HIPAA line, and OSSICRO enforces it in code, not in policy prose.

## Two distinct feasibility questions

1. **Trial/therapy feasibility (patient-facing).** Is there an open early-phase trial or an accessible investigational therapy for this patient's condition, phase-of-illness, biomarker profile, and geography? Answered by the [[matching-engine]] over [[data-integrations-ctgov-pubmed|external data sources]].
2. **Site feasibility (operations-facing).** Can this physician/site actually run the protocol — population volume, equipment, staff, lab certification, prior track record? Answered by a structured site-qualification self-assessment that feeds the [[verifiable-site-qualification-dossier]] and, in Mode A, the pharma sponsor's [[single-patient-site-and-pharma-acceptance|site-acceptance]] backend.

Both questions are answered at *draft/advisory* status. Neither the trial-match nor the site-feasibility output is an eligibility determination or an enrollment decision.

## The HIPAA preparatory-to-research boundary (confirmed)

[45 CFR 164.512(i)(1)(ii)](https://www.ecfr.gov/current/title-45/section-164.512) permits a covered entity to use or disclose PHI for a review **preparatory to research** if the covered entity obtains from the researcher representations that:

- the use or disclosure is sought **solely to prepare a research protocol** or for similar purposes preparatory to research;
- **no PHI will be removed** from the covered entity by the researcher in the course of the review; and
- the PHI is **necessary** for the research purposes.

Applied to OSSICRO: querying a patient's chart to determine whether a candidate trial exists is a preparatory review. It follows that the matching computation must run **local-first, inside the covered-entity boundary, with no PHI egress**, reading the **minimum necessary**, with **ephemeral, audited** reads. This is the design enforced by the [[privacy-state-machine]] and available as an [[offline-local-deployment|offline single-container deployment]].

> [!warning] Non-delegable
> The preparatory-review representations under [45 CFR 164.512(i)(1)(ii)](https://www.ecfr.gov/current/title-45/section-164.512) are made by the **covered entity / responsible human**, not by software. OSSICRO structures and logs the review; it does not itself "represent" anything to the covered entity, and it never removes PHI. The determination that a use is genuinely preparatory (and minimum-necessary) is the covered entity's judgment.

## The transition gate: matching → enrollment (confirmed)

Preparatory review does **not** authorize enrolling the patient, contacting the patient for recruitment beyond the covered entity's own treatment relationship, or exporting PHI to a sponsor or the OSSICRO Micro-CRO. Crossing from matching to enrollment requires one of:

- **Individual authorization** under [45 CFR 164.508](https://www.ecfr.gov/current/title-45/section-164.508) (typically the HIPAA authorization bundled with or accompanying the informed-consent process); or
- **IRB or Privacy-Board waiver** of authorization under [45 CFR 164.512(i)(1)(i)](https://www.ecfr.gov/current/title-45/section-164.512) (with the three waiver criteria satisfied).

OSSICRO models this as a **hard, logged state transition** in the [[privacy-state-machine]]: the system will not surface enrollment-phase artifacts (consent packet finalization, screening-log creation, PHI disclosure to sponsor) until the authorization/waiver basis is recorded. See [[enrollment-and-consent]] and [[hipaa-and-privacy-gating]].

## The data source: ClinicalTrials.gov API v2 (confirmed source, interpretive layer)

Discovery runs on the [ClinicalTrials.gov API v2](https://clinicaltrials.gov/data-api/api) REST interface — free, no registration wall, with structured phase/status/condition/intervention enums and a documented eligibility-criteria field. It is the authoritative registry of US trials under FDAAA 801 / [42 CFR Part 11](https://www.ecfr.gov/current/title-42/part-11) (see [[clinicaltrials-gov-registration]]). The registry is supplemented by PubMed/NCBI E-utilities (supporting and safety evidence) and openFDA (labels, FAERS) per [[data-integrations-ctgov-pubmed]].

> [!interpretive] OSSICRO position
> The ClinicalTrials.gov v2 API returns eligibility criteria as **free text** and offers no synonym/semantic matching and no biomarker-to-trial reasoning. OSSICRO layers a **semantic + mechanism-aware** matcher on top ([[matching-mechanism-graph]]) and a **retrieve→adjudicate** eligibility engine that renders a **three-valued per-criterion verdict — met / not-met / indeterminate-needs-data** — each with a chart citation and a criterion citation ([[matching-eligibility-adjudication]]). This is a deliberate design choice and its performance is a **measured claim**, evaluated on public benchmarks (CHIA, TREC Clinical Trials, n2c2) with a **recall-first** objective so the system never silently excludes a patient ([[matching-evaluation-and-benchmarks]]). Prior art reimplemented independently: Criteria2Query and EliIE (Weng, Columbia), OHDSI/OMOP, CQL.

> [!warning] Non-delegable
> Eligibility **determination** is the investigator's judgment ([[enrollment-and-consent]]; 21 CFR 312.60 protocol adherence and subject selection). The matching engine's role is **recall-first candidate surfacing with cited rationale**, not adjudication of who enrolls. An "indeterminate-needs-data" verdict is an invitation to a human to gather data, not a denial of access. A matcher that can return "no eligible trial" and thereby gate a patient's access is a **higher-influence context of use** than document drafting and is designed and evaluated as one.

## Feasibility outputs and their status

| Output | Basis | Status | Downstream |
|--------|-------|--------|-----------|
| Candidate trial list (with cited match rationale) | CT.gov v2 + semantic/mechanism layer | Draft/advisory | Triage: [[the-three-pathways-triage]] |
| Per-criterion eligibility verdicts (met/not-met/indeterminate) | Retrieve→adjudicate over chart + criteria | Draft/advisory | Investigator eligibility call |
| Site-feasibility self-assessment | Structured site inputs | Draft | [[site-activation]], [[verifiable-site-qualification-dossier]] |
| Preparatory-review audit record | 164.512(i)(1)(ii) representations + ephemeral read log | Confirmed record | [[privacy-state-machine]] audit trail |

## Where feasibility hands off

- Match found, patient is a candidate on an **open pharma protocol** → Mode A site activation ([[site-activation]], [[single-patient-site-and-pharma-acceptance]]).
- No fitting trial, physician will run one → Mode B, proceed to [[pre-ind-and-ind-preparation]].
- No trial fits, single patient, drug exists → [[expanded-access-workflow]] / [[single-patient-site-enrollment]].

## Related
- [[index]]
- [[the-three-pathways-triage]]
- [[matching-engine]]
- [[matching-eligibility-adjudication]]
- [[privacy-state-machine]]
- [[hipaa-and-privacy-gating]]
- [[enrollment-and-consent]]
- [[pre-ind-and-ind-preparation]]
- [[data-integrations-ctgov-pubmed]]

## Sources
- [45 CFR 164.512 — Uses and disclosures for which authorization is not required (eCFR)](https://www.ecfr.gov/current/title-45/section-164.512)
- [45 CFR 164.508 — Uses and disclosures for which an authorization is required (eCFR)](https://www.ecfr.gov/current/title-45/section-164.508)
- [HHS OCR — Research and the HIPAA Privacy Rule (preparatory-to-research guidance)](https://www.hhs.gov/hipaa/for-professionals/special-topics/research/index.html)
- [ClinicalTrials.gov API v2 documentation](https://clinicaltrials.gov/data-api/api)
- [42 CFR Part 11 — ClinicalTrials.gov Data Bank (eCFR)](https://www.ecfr.gov/current/title-42/part-11)
