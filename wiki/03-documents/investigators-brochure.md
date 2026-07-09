---
title: "Investigator's Brochure (21 CFR 312.55; content per 312.23(a)(5))"
section: "03-documents"
status: confirmed
governing_authority:
  - "21 CFR 312.55 (informing investigators / furnishing the IB)"
  - "21 CFR 312.23(a)(5) (IB content within the IND)"
  - "ICH E6(R3) Good Clinical Practice (IB expectations)"
tags: [cfr/312, ich/e6r3, lifecycle/ind, lifecycle/safety, ossicro/engine, status/confirmed]
aliases: ["IB", "investigator brochure", "investigators brochure", "312.55"]
updated: 2026-07-09
---

# Investigator's Brochure (21 CFR 312.55; content per 312.23(a)(5))

> [!authority] Governing authority
> **21 CFR 312.55** (sponsor duty to furnish and update the IB); **21 CFR 312.23(a)(5)** (the IB content the IND must contain); **ICH E6(R3)** GCP (IB as an essential document and the vehicle for the current risk/benefit assessment). Status: **Confirmed**. The package-insert-substitution provision is black-letter (312.55(a) / 312.23(a)(5)(ii)); OSSICRO's assembly behavior is flagged interpretive.

The **Investigator's Brochure (IB)** is the compilation of the clinical and non-clinical data on an investigational product that is relevant to its study in humans. It is the document by which the **sponsor discharges its 21 CFR 312.55 duty to inform investigators** — to give each participating [[investigator]] the information needed to conduct the study properly and to keep that information current as new safety findings emerge. The IB is a required component of the IND (21 CFR 312.23(a)(5)) and an **essential record** under ICH E6(R3). For the enrolling clinician it is the primary source for the [[informed-consent-form|informed consent]] risk disclosures and for the safety judgments that drive [[safety-reporting-lifecycle|expectedness assessment]].

## 1. The sponsor's duty to furnish and update (21 CFR 312.55)

- **312.55(a)** — Before the investigation begins, the sponsor **shall** give each participating clinical investigator an investigator's brochure containing the information described in 21 CFR 312.23(a)(5).
- **312.55(b)** — The sponsor **shall** keep each participating investigator informed of new observations discovered by or reported to the sponsor, **particularly with respect to adverse effects and safe use** — through revised brochures, reprints or published studies, reports or letters to investigators, or other appropriate means. New safety information required to be reported under 21 CFR 312.32 must reach investigators.

In the [[sponsor-investigator]] model the same physician is both furnisher and recipient: the sponsor-investigator must **maintain a current IB** (or, for a marketed drug, the current package insert plus any IND-specific safety updates) as the reference that governs their own [[safety-reporting-lifecycle|expectedness determinations]].

> [!warning] Non-delegable
> The **expectedness reference** — whether a serious adverse reaction is "unexpected" (not consistent with the risk information in the IB) and therefore triggers a 7-day/15-day [[ind-safety-report|IND safety report]] under 21 CFR 312.32 — is anchored in the IB and adjudicated by a qualified [[medical-monitor|medical/safety physician]]. OSSICRO keeps the IB current and version-controlled and pre-computes reporting **timeliness**; it never makes the expectedness/causality call. See [[non-delegable-functions-and-gates]].

## 2. Required content — 21 CFR 312.23(a)(5)

The IND's IB must contain:

1. **Drug substance and formulation** — a brief description of the drug substance and the formulation, including the structural formula, if known.
2. **Pharmacological and toxicological effects** — a summary of the pharmacological and toxicological effects of the drug in animals and, to the extent known, in humans.
3. **Pharmacokinetics and biological disposition** — a summary of the pharmacokinetics and biological disposition of the drug in animals and, if known, in humans.
4. **Safety and effectiveness in prior human studies** — a summary of information relating to safety and effectiveness in humans obtained from prior clinical studies (reprints of published prior studies may be appended).
5. **Marketing experience** — a summary of information relating to marketing experience in countries where the drug has been marketed or withdrawn from marketing for reasons related to safety or effectiveness.
6. **Possible risks, side effects, and special monitoring** — a description of possible risks and side effects to be anticipated on the basis of prior experience with the drug under investigation or with related drugs, and of precautions or special monitoring to be done as part of the investigational use of the drug.

## 3. ICH E6(R3) expectations

ICH E6(R3) treats the IB as the vehicle for the **current benefit-risk assessment** of the investigational product and as an essential document maintained in the [[document-catalog|Trial Master File]]. Under R3's principles-based, risk-proportionate approach the IB should:

- present data in a form that allows the investigator to make an **unbiased risk/benefit assessment** and to conduct the trial safely;
- be **reviewed at least annually** and revised as significant new information becomes available (consistent with the sponsor's 312.55(b) ongoing-update duty);
- carry a clear **version and date**, since the current IB defines the **reference safety information (RSI)** against which expectedness is judged.

OSSICRO records IB version, effective date, and RSI section as structured metadata so that a [[safety-clock-engine|safety-clock computation]] and an expectedness prompt always cite the **exact IB version in force at the event date**.

## 4. Package-insert substitution for a marketed drug

Where the investigational use involves a drug that is **lawfully marketed** (e.g., an approved product studied for a **new indication** under a [[sponsor-investigator]] IND), the sponsor may substitute the **current FDA-approved package insert (prescribing information)** for a from-scratch IB, provided the labeling adequately conveys the pharmacology, toxicology, prior human experience, and risk information required by 312.23(a)(5). This is expressly contemplated by 21 CFR 312.23(a)(5)(ii)/312.55(a) and is the common case for OSSICRO's core scenario: a practicing physician studying an approved drug in a new early-phase use.

> [!interpretive] OSSICRO position — IB assembly and marketed-drug branch
> For a **novel** agent, OSSICRO drafts the IB from structured nonclinical/clinical data supplied by the manufacturer or sponsor-investigator, checking section completeness against 312.23(a)(5). For a **marketed** drug, OSSICRO's engine (a) ingests the current FDA label via [[data-integrations-ctgov-pubmed|openFDA]], (b) proposes it as the IB substitute, and (c) flags any IND-specific new-use risk that the label does not cover and that must be added as a supplement. In both branches the output is a **draft for the sponsor-investigator and IRB to review and adopt**; the scientific adequacy judgment (is this IB sufficient to inform consent and conduct?) stays human. Flagged interpretive.

## 5. Downstream dependence

The IB is load-bearing for several downstream artifacts, and OSSICRO's cross-document consistency check enforces the linkage:

- **[[informed-consent-form|Informed consent]]** — the "reasonably foreseeable risks or discomforts" element (21 CFR 50.25(a)(2)) must be consistent with the IB's risk section.
- **[[safety-management-plan]] / [[safety-reporting-lifecycle]]** — the IB is the expectedness reference for 312.32 reporting.
- **[[clinical-protocol-and-synopsis|Protocol]]** — dose rationale, exclusions, and monitoring derive from IB pharmacology/toxicology.
- **[[irb-submission-package]]** — the IB is part of the IRB's review record (21 CFR 56.111 risk assessment).

## Related
- [[ind-application-312-23]]
- [[clinical-protocol-and-synopsis]]
- [[informed-consent-form]]
- [[safety-management-plan]]
- [[safety-reporting-lifecycle]]
- [[ind-safety-report]]
- [[medical-monitor]]
- [[pharmacovigilance-safety]]
- [[sponsor]]
- [[sponsor-investigator]]
- [[document-catalog]]
- [[data-integrations-ctgov-pubmed]]
- [[safety-clock-engine]]
- [[non-delegable-functions-and-gates]]

## Sources
- [21 CFR 312.55 — Informing investigators](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.55)
- [21 CFR 312.23(a)(5) — Investigator's brochure (IND content)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.23)
- [21 CFR 312.32 — IND safety reporting](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32)
- [ICH E6(R3) Good Clinical Practice — FDA guidance](https://www.fda.gov/media/169090/download)
- [openFDA drug label API (marketed-drug labeling)](https://open.fda.gov/apis/drug/label/)
