---
title: "IRB Submission Package — Composition and 56.111 Completeness Validator"
section: "03-documents"
status: mixed
governing_authority:
  - "21 CFR Part 56 (56.107, 56.109, 56.111, 56.115)"
  - "21 CFR Part 50 (50.25, 50.27)"
  - "21 CFR 312.66"
  - "45 CFR 46.111, 46.116"
tags: [role/irb, cfr/56, cfr/50, cfr/312, lifecycle/irb, ossicro/gating, ossicro/engine, status/mixed]
aliases: ["IRB package", "IRB submission", "56.111 checklist", "IRB initial submission"]
updated: 2026-07-09
---

# IRB Submission Package — Composition and 56.111 Completeness Validator

> [!authority] Governing authority
> 21 CFR Part 56 (Institutional Review Boards — §56.109 review, §56.111 approval criteria, §56.115 records); 21 CFR Part 50 (informed consent — §50.25 elements, §50.27 documentation); 21 CFR 312.66 (investigator assurance of IRB review); 45 CFR 46.111/46.116 (revised Common Rule, for federally-conducted or -funded research). Status: **Mixed** — the package composition and the §56.111 criteria are **confirmed** black-letter law; the automated completeness validator is an **interpretive** OSSICRO engine position, gated behind human IRB judgment.

The IRB submission package is the assembled set of documents an investigator (or [[sponsor-investigator]]) delivers to an [[irb-iec|Institutional Review Board]] to obtain the prior review and approval that [21 CFR 56.103](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-56/subpart-A/section-56.103) and [21 CFR 312.66](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.66) require before any human subject may be involved in FDA-regulated research. This page specifies the package's composition, maps each component to the authority that makes it necessary, and defines the OSSICRO **completeness validator** — a checklist engine that verifies every component the IRB needs to reach a §56.111 approval decision is present, well-formed, and internally consistent, *before* the human review begins.

The validator checks completeness. It does **not** — and by law cannot — render the approval decision. That decision is the IRB's non-delegable ethical judgment.

## What the IRB does with the package

The IRB reviews the package against the seven approval criteria of [21 CFR 56.111](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-56/subpart-C/section-56.111) (mirrored at 45 CFR 46.111) at a convened meeting of a quorum-satisfying board (§56.108(c)), or via expedited review where the study qualifies (§56.110). Approval, modification-then-approval, or disapproval is a determination reserved to the convened board. A missing or defective package component does not merely delay review — it can make a criterion **unreviewable**, which is why completeness is a precondition, not a courtesy.

## Package composition

The composition below reflects the standard FDA-regulated IND-study initial submission. Central/commercial IRBs (WCG, Advarra) publish their own submission checklists that overlay local-context forms; OSSICRO ingests those checklists and reconciles them against this canonical set.

| # | Component | Why the IRB needs it | Governing authority | OSSICRO handling |
|---|-----------|----------------------|---------------------|------------------|
| 1 | **Clinical protocol + synopsis** (current version, dated) | The object of review; risk/benefit, design, eligibility, safety monitoring all derive from it | 21 CFR 56.111(a)(1)-(2); [[clinical-protocol-and-synopsis]] | Generated/checked; version + date verified |
| 2 | **Investigator's Brochure** (or package insert for a marketed drug) | Non-clinical + clinical safety basis for the risk judgment | 21 CFR 312.55; [[investigators-brochure]] | Presence + currency check |
| 3 | **Draft informed consent form(s)** with all §50.25 elements + Common Rule key-information | The IRB must approve the consent document and its process | 21 CFR 50.25, 50.27; 45 CFR 46.116; [[informed-consent-form]] | Element-by-element validator (see below) |
| 4 | **Recruitment/advertising materials** (if any) | Advertising is "an extension of the consent process"; IRB reviews it | FDA "Recruiting Study Subjects" guidance; 21 CFR 56.111(a)(3) | Flag if recruitment implied but no material submitted |
| 5 | **Investigator CV + medical license** (PI and sub-investigators) | §56.111 requires the IRB to consider investigator qualification | 21 CFR 312.53(c)(2); [[subinvestigator-and-delegation]] | Currency (signed/dated) check |
| 6 | **Form FDA 1572** (Statement of Investigator) | Evidences the investigator's protocol/consent/IRB commitments | 21 CFR 312.53(c)(1); [[form-fda-1572-statement-of-investigator]] | Field-completeness cross-check |
| 7 | **Financial disclosure** (Form FDA 3454 or 3455) | Conflict-of-interest bearing on subject protection | 21 CFR Part 54; [[form-fda-3454-3455-financial-disclosure]] | 3454-vs-3455 selection logic |
| 8 | **IND number / sponsor authorization** | Confirms an active regulatory pathway exists | 21 CFR 312.23, 312.40 | Presence check |
| 9 | **HIPAA authorization** (or waiver request) | Privacy/confidentiality protection under §56.111(a)(7) | 45 CFR 164.508, 164.512(i); [[hipaa-and-privacy-gating]] | Authorization vs. waiver branch |
| 10 | **Data & Safety Monitoring Plan** (and [[dsmb-charter\|DSMB charter]] where warranted) | §56.111(a)(6) — adequate provision for monitoring data for subject safety | 21 CFR 56.111(a)(6); [[safety-management-plan]] | Presence + DSMB-warranted flag |
| 11 | **Case report forms / data collection instruments** | Scope of data collected bears on privacy and burden | 21 CFR 56.111(a)(7) | Presence check |
| 12 | **Site/local-context information** | Local research context for the reviewing IRB | IRB SOPs; sIRB reliance context | Template per IRB |
| 13 | **Delegation-of-authority context** (staffing/qualification) | Supports the qualification prong | [[delegation-of-authority-log]] | Cross-reference |

For multi-site studies subject to the single-IRB mandate ([45 CFR 46.114](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46/subpart-A/section-46.114); NIH sIRB policy), the package additionally carries the **reliance/authorization agreement** and per-site local-context forms; see [[single-irb-mandate-and-central-irbs]].

## The §56.111 completeness validator

> [!interpretive] OSSICRO position
> OSSICRO's validator is organized **around the seven §56.111 approval criteria**, not around a flat document list. For each criterion the engine asserts: *the IRB cannot evaluate this criterion unless components X, Y, Z are present and well-formed.* The validator's output is a three-state [[completeness-ledger]] entry per criterion — **green** (all supporting components present and consistent), **amber** (present but requires human judgment), **red** (a supporting component is missing, with the exact resolving question named). It is a **reviewability precondition checker**, explicitly not an approvability predictor. The distinction is load-bearing: completeness is computable; ethical approvability is not.

Criterion-to-component mapping the validator enforces:

- **§56.111(a)(1) — Risks to subjects are minimized.** Requires: protocol (design/procedures), IB (known risk profile), monitoring plan. Validator confirms all three present and that the protocol names a monitoring mechanism.
- **§56.111(a)(2) — Risks reasonable in relation to anticipated benefits.** Requires: protocol risk/benefit section, IB. Validator confirms a stated benefit/knowledge-value rationale exists; the *reasonableness weighing is the IRB's judgment*.
- **§56.111(a)(3) — Selection of subjects is equitable.** Requires: eligibility criteria, recruitment materials, population justification. Validator flags recruitment activity with no submitted advertising, and vulnerable-population enrollment with no §56.111(b) safeguard section.
- **§56.111(a)(4) — Informed consent will be sought (§50.20, §50.25).** Requires: consent form with all basic + applicable additional elements. Validator runs the element-by-element consent check (below).
- **§56.111(a)(5) — Informed consent will be documented (§50.27).** Requires: signature block, or a documentation-waiver request. Validator confirms one or the other.
- **§56.111(a)(6) — Adequate provision for monitoring the data collected to ensure subject safety.** Requires: DSMP; DSMB charter where the design warrants one. Validator raises the "DSMB-warranted" flag on higher-risk/blinded/mortality-endpoint designs per the [[dsmb-dmc]] heuristics.
- **§56.111(a)(7) — Adequate provisions to protect privacy and maintain confidentiality.** Requires: HIPAA authorization or waiver, data-handling description. Validator branches on authorization vs. §164.512(i) waiver.
- **§56.111(b) — Additional safeguards for vulnerable populations** (children, prisoners, cognitively impaired, economically/educationally disadvantaged). Requires: a safeguards section keyed to the enrolled population and the applicable subpart (21 CFR 50 Subpart D for children; 45 CFR 46 Subparts B/C/D). Validator raises when the eligibility criteria admit a vulnerable class with no matching safeguard.

### Consent-form element validator (§50.25)
The validator confirms the presence of each **basic** element — purpose and duration; procedures (identifying experimental ones); reasonably foreseeable risks/discomforts; benefits; alternatives; confidentiality; compensation/injury provisions for >minimal-risk research; contacts (research questions, subject rights, injury); voluntariness — and each **additional** element where applicable (unforeseeable risks; involuntary-termination circumstances; costs; consequences of withdrawal; new-findings notification; number of subjects). It also confirms the revised-Common-Rule **key-information** summary at the front (45 CFR 46.116(a)(5)) where the study is Common-Rule-covered. Presence is checkable; adequacy of the *language* to a specific subject population is IRB judgment.

## Non-delegable gate

> [!warning] Non-delegable
> The IRB **approval determination** — the weighing of risks against benefits, the equity of subject selection, the adequacy of consent and safeguards under 21 CFR 56.111 — is the independent judgment of a convened, quorum-satisfying IRB (21 CFR 56.107-56.111). OSSICRO validates that the package is **complete and reviewable**; it never renders, predicts, or substitutes for the approval decision, and it never marks a study "IRB-ready" in any sense that implies approvability. Enrollment is hard-gated on a **documented IRB approval letter** filed to the [[regulatory-binder-isf-index|ISF/TMF]] (21 CFR 56.109(d)); the engine will not advance a study to [[enrollment-and-consent|enrollment]] without that letter present. See [[non-delegable-functions-and-gates]].

## OSSICRO engine behavior
- **Generate:** assembles the package from the study's structured record — protocol, IB, consent form, forms, financial disclosure, monitoring plan — each as a draft carrying its authority citation.
- **Check:** runs the §56.111 criterion-mapped completeness validator and the §50.25 element validator; emits the green/amber/red [[completeness-ledger]].
- **Validate:** cross-document consistency (protocol version on the 1572 matches the submitted protocol; consent risks match protocol risks; eligibility matches the recruitment material); holds the package in a gated "reviewable" state for human submission. The engine transmits nothing to the IRB and asserts no approval.

## Related
- [[irb-iec]]
- [[irb-submission-and-approval]]
- [[irb-review-workflow]]
- [[informed-consent-form]]
- [[informed-consent-document-vs-event]]
- [[single-irb-mandate-and-central-irbs]]
- [[safety-management-plan]]
- [[dsmb-charter]]
- [[completeness-ledger]]
- [[hipaa-and-privacy-gating]]
- [[non-delegable-functions-and-gates]]

## Sources
- [21 CFR 56.111 — Criteria for IRB approval of research](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-56/subpart-C/section-56.111)
- [21 CFR 56.109 — IRB review of research](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-56/subpart-C/section-56.109)
- [21 CFR 56.115 — IRB records](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-56/subpart-C/section-56.115)
- [21 CFR 50.25 — Elements of informed consent](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-50/subpart-B/section-50.25)
- [21 CFR 312.66 — Assurance of IRB review](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.66)
- [45 CFR 46.111 — Criteria for IRB approval (Common Rule)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46/subpart-A/section-46.111)
- [FDA — Recruiting Study Subjects (Information Sheet)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/recruiting-study-subjects)
- [ICH E6(R3) Good Clinical Practice — Step 4 Final Guideline (2025)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
