---
title: "Clinical Protocol and Synopsis (21 CFR 312.23(a)(6); ICH M11)"
section: "03-documents"
status: mixed
governing_authority:
  - "21 CFR 312.23(a)(6) (protocol content)"
  - "21 CFR 312.30 (protocol amendments)"
  - "ICH E6(R3) Good Clinical Practice"
  - "ICH E8(R1) General Considerations for Clinical Studies"
  - "ICH M11 (CeSHarP structured protocol template)"
tags: [cfr/312, ich/e6r3, ich/e8r1, ich/m11, lifecycle/ind, ossicro/engine, status/confirmed, status/interpretive]
aliases: ["protocol", "clinical protocol", "protocol synopsis", "312.23(a)(6)"]
updated: 2026-07-09
---

# Clinical Protocol and Synopsis (21 CFR 312.23(a)(6); ICH M11)

> [!authority] Governing authority
> **21 CFR 312.23(a)(6)** (protocol content within the IND); 21 CFR 312.30 (protocol amendments); **ICH E6(R3)** GCP (protocol design, oversight, risk-proportionality); **ICH E8(R1)** (quality-by-design, critical-to-quality factors); **ICH M11** (CeSHarP structured protocol template). Status: **Mixed** — the CFR content floor is confirmed; the M11 structured-template target and the synopsis-as-computable-source are OSSICRO interpretive positions, flagged inline.

The **protocol** is the document that defines the scientific and operational conduct of a clinical investigation: its objectives, design, population, interventions, assessments, statistical plan, and safety oversight. It is a required component of the IND (21 CFR 312.23(a)(6)) and the reference against which the [[investigator]] and [[sponsor-investigator]] commit to conduct (Form FDA 1572, Field 9; [[form-fda-1572-statement-of-investigator]]). Every downstream artifact — the [[informed-consent-form|ICF]], the [[irb-submission-package|IRB submission]], the [[monitoring-plan]], the [[safety-management-plan]], the [[statistical-analysis-plan|SAP]], and the final [[clinical-study-report|CSR]] — inherits its scope from the protocol. The **synopsis** is the structured abstract of the protocol; in OSSICRO it is also the computable source of truth from which the full protocol and its dependents are generated.

## 1. Protocol content required by 21 CFR 312.23(a)(6)

The regulation grades protocol detail to phase. **Phase 1** protocols may be brief outlines; **Phase 2 and 3** protocols must be detailed. The required elements are:

1. **Statement of objectives and purpose** of the study.
2. **Investigator and facility identification** — the name and address of each [[investigator]], each sub-investigator, each research facility, and each reviewing [[irb-iec|IRB]] (21 CFR 312.23(a)(6)(iii)(b)). This content ties directly to the 1572.
3. **Subject selection** — the criteria for **inclusion and exclusion** and an estimate of the number of subjects.
4. **Study design** — for controlled trials, a description of the design including the kind of control group and the methods to **minimize bias** on the part of subjects, investigators, and analysts (randomization, blinding).
5. **Dose and route** — the method for determining the dose(s) to be administered, the planned maximum dose, and the duration of individual subject exposure.
6. **Observations and measurements** — a description of the clinical and laboratory tests, observations, and measurements to be taken to **fulfill the objectives** of the study.
7. **Clinical procedures / safety monitoring** — the clinical procedures, laboratory tests, or other measures taken to **monitor the effects of the drug in human subjects and to minimize risk**.

> [!warning] Non-delegable
> Protocol **design decisions** — the scientific hypothesis, the risk/benefit judgment embedded in eligibility criteria and dose selection, the choice of endpoints and estimand — are the sponsor's/sponsor-investigator's and, where applicable, the biostatistician's ([[biostatistician]]) professional judgments. OSSICRO drafts, structures, and checks completeness against 312.23(a)(6); it does not author the scientific design. The [[irb-iec|IRB]]'s approval of the protocol under 21 CFR 56.111 is likewise non-delegable ([[irb-review-workflow]]).

## 2. Phase-graded expectations

- **Phase 1** — outline-level: objectives, estimated subject number, safety-driven exclusions, and dosing details (duration, dose, method of determining dose). Emphasis on subject safety, dose escalation, stopping rules.
- **Phase 2 / Phase 3** — full protocol: detailed design, controls, bias-minimization, statistical considerations, and pre-specified analysis. FDA's review objective for Phase 2/3 explicitly includes assuring the scientific quality is adequate to evaluate effectiveness (21 CFR 312.22(a)).

Changes to a protocol after the IND is in effect are governed by **21 CFR 312.30** (protocol amendments): a new protocol or a change to an existing protocol that significantly affects subject safety, scope, or scientific quality is submitted as a protocol amendment, and (for changes affecting safety) may not be implemented until the amendment is submitted and IRB approval obtained, except to eliminate an apparent immediate hazard. See [[annual-reporting-and-amendments]].

## 3. Design quality — ICH E8(R1) and E6(R3)

**ICH E8(R1)** frames **quality-by-design** and **critical-to-quality (CtQ) factors**: the protocol should identify, prospectively, the factors most critical to the reliability of results and the safety of participants, and design around them rather than attempting to eliminate all risk. **ICH E6(R3)** operationalizes this in GCP: the protocol should be designed to be fit-for-purpose, with risk-proportionate procedures, clear roles/oversight, and data-governance/ALCOA++ expectations built in. OSSICRO's protocol template surfaces the CtQ factors so they flow into the [[monitoring-plan|risk-based monitoring plan]] (E6(R3) §6.9; quality tolerance limits) and the [[risk-based-monitoring-e6r3]] workflow.

## 4. The synopsis

The **synopsis** is the standardized, front-of-protocol summary: title, phase, objectives, design, population and key eligibility, intervention/dose, endpoints (primary/secondary), sample size and statistical approach, and duration. Regulators, IRBs, and DSMBs read the synopsis first; it is also the field set most amenable to structured capture.

> [!interpretive] OSSICRO position — synopsis as computable source of truth
> OSSICRO treats the synopsis as a **structured data object**, not merely a prose abstract. The clinician populates the synopsis fields once; the [[generate-check-validate-engine]] then instantiates (a) the full protocol body, (b) the IRB-facing summary, (c) the ICF's study-description and risks sections, and (d) the SAP skeleton — each span carrying a [[draft-provenance-model|provenance triple]] back to the synopsis datum and its governing citation. This is a design position, flagged interpretive; the regulatory requirement is the 312.23(a)(6) content, regardless of how it is authored.

## 5. ICH M11 — the structured protocol target

> [!interpretive] OSSICRO position — M11 CeSHarP as priority schema
> **ICH M11 (Clinical electronic Structured Harmonised Protocol, "CeSHarP")** defines a harmonized template and a machine-readable technical specification for clinical protocols. FDA has adopted M11 (final template published 2025-11-19). OSSICRO builds its protocol schema to M11 so that one structured protocol source populates the IND [[ind-application-312-23|312.23]] protocol section, the [[clinical-study-report|E3 CSR]], and the [[statistical-analysis-plan|E9 SAP]] without re-keying. **Status:** M11 is a forward standard and an OSSICRO design choice; it does not displace the black-letter 312.23(a)(6) content requirements, and adoption timelines are versioned per [[regulatory-change-log]].

## 6. Cross-document consistency

Because the protocol is upstream of most trial documents, an error in the protocol propagates. OSSICRO's **check** pass (the elevated cross-document consistency engine) verifies that eligibility criteria, endpoints, visit schedule, and safety definitions are **identical** across the protocol, the [[informed-consent-form|ICF]], the [[irb-submission-package|IRB package]], and the [[safety-management-plan]] — a common source of protocol deviations and IRB queries when authored by hand. Discrepancies are surfaced to the reviewer via the [[single-pass-review-ux|attention-triaged review UX]] rather than silently reconciled.

## Related
- [[ind-application-312-23]]
- [[investigators-brochure]]
- [[informed-consent-form]]
- [[irb-submission-package]]
- [[statistical-analysis-plan]]
- [[clinical-study-report]]
- [[monitoring-plan]]
- [[safety-management-plan]]
- [[form-fda-1572-statement-of-investigator]]
- [[annual-reporting-and-amendments]]
- [[risk-based-monitoring-e6r3]]
- [[biostatistician]]
- [[sponsor-investigator]]
- [[generate-check-validate-engine]]
- [[draft-provenance-model]]
- [[non-delegable-functions-and-gates]]

## Sources
- [21 CFR 312.23(a)(6) — Protocols (IND content and format)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.23)
- [21 CFR 312.30 — Protocol amendments](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.30)
- [ICH E6(R3) Good Clinical Practice — FDA guidance](https://www.fda.gov/media/169090/download)
- [ICH E8(R1) General Considerations for Clinical Studies](https://database.ich.org/sites/default/files/ICH_E8-R1_Guideline_Step4_2021_1006.pdf)
- [ICH M11 — Clinical electronic Structured Harmonised Protocol (CeSHarP)](https://www.ich.org/page/multidisciplinary-guidelines)
- [NIH-FDA Clinical Trial Protocol Template](https://osp.od.nih.gov/clinical-research/clinical-trials/)
