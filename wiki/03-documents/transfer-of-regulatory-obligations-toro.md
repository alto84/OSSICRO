---
title: "Transfer of Regulatory Obligations (TORO)"
section: "03-documents"
status: mixed
governing_authority:
  - "21 CFR 312.52 (transfer of obligations to a contract research organization)"
  - "21 CFR 312.3(b) (definition of contract research organization)"
  - "21 CFR 312.23(a)(1)(viii) (identification of transferred obligations on the IND cover sheet, Form FDA 1571 Field 14)"
  - "ICH E6(R3) (sponsor oversight of delegated activities and service providers)"
tags: [cfr/312, role/cro, role/sponsor, role/sponsor-investigator, fda-form/1571, ossicro/micro-cro, lifecycle/activation, status/confirmed, status/interpretive]
aliases: ["TORO", "Transfer of Obligations", "312.52 transfer"]
updated: 2026-07-09
---

# Transfer of Regulatory Obligations (TORO)

> [!authority] Governing authority
> 21 CFR 312.52 (a sponsor may transfer any or all Part 312 sponsor obligations to a CRO, but only in a writing that describes the transfer; anything not described is not transferred); 21 CFR 312.3(b) (a CRO is a *person* that assumes sponsor obligations as an independent contractor); 21 CFR 312.23(a)(1)(viii) and Form FDA 1571 Field 14 (the transfer must be disclosed on the IND cover sheet). ICH E6(R3), as adopted by FDA (final guidance, September 2025), overlays a documented-oversight duty for all delegated activities. Status: **Mixed** — the 312.52 mechanics are confirmed black-letter law; the micro-CRO enumeration model is an interpretive OSSICRO position.

The TORO is the written instrument by which a [[sponsor]] (including a [[sponsor-investigator]]) transfers named regulatory obligations to a [[cro|contract research organization]]. It is the single most consequential contracting artifact in the OSSICRO architecture, because 21 CFR 312.52 is the provision that makes software disintermediation of the sponsor role legally impossible — a transferee must be a *person* — and simultaneously makes OSSICRO's thin [[micro-cro-accountable-layer|micro-CRO]] lawful: a small, legally accountable entity can assume precisely enumerated obligations, and only those, in writing. The TORO is where that enumeration lives.

## The regulatory text and its four rules

[21 CFR 312.52(a)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.52) provides, in substance:

1. **Transferability.** "A sponsor may transfer responsibility for any or all of the obligations set forth in this part to a contract research organization."
2. **Writing requirement.** "Any such transfer shall be described in writing."
3. **Enumeration rule for partial transfers.** "If not all obligations are transferred, the writing is required to describe each of the obligations being assumed by the contract research organization." A general statement that all obligations have been transferred is acceptable **only** for a total transfer.
4. **Default rule.** "Any obligation not covered by the written description shall be deemed **not** to have been transferred." Silence retains; the residual always sits with the sponsor.

312.52(b) supplies the enforcement consequence: a CRO that assumes any obligation "shall comply with the specific regulations in this chapter applicable to this obligation and shall be subject to the same regulatory action as a sponsor for failure to comply"; all references to "sponsor" in Part 312 apply to the CRO to the extent of its assumed obligations. FDA's BIMO program inspects CROs on exactly this basis.

## What can and cannot be transferred

- **Transferable:** *sponsor* obligations under Part 312 — e.g., monitoring (21 CFR 312.56(a); selection of monitors, 312.53(d)), maintaining drug-disposition and financial-interest records (312.57), assuring return/disposition of unused drug (312.59), preparation and submission mechanics of [[ind-safety-report|IND safety reports]] (312.32) and [[ind-annual-report-dsur|annual reports]] (312.33), and investigator-selection documentation (312.53).
- **Not transferable under 312.52:** *investigator* obligations (21 CFR 312.60–312.69) — protocol adherence, consent, drug control, records, reports, IRB assurance — bind the [[investigator]] personally and are outside the scope of §312.52, which addresses sponsor obligations only. Task delegation at the site runs through the [[delegation-of-authority-log]] and never transfers accountability ([[subinvestigator-and-delegation]]).
- **Not a lawful transferee:** software. 21 CFR 312.3(b) defines a CRO as "a **person** that assumes, as an independent contractor with the sponsor, one or more of the obligations of a sponsor." An open-source system such as OSSICRO is a compliance tool, not a person; it cannot assume any obligation. This is the load-bearing legal thesis of the project — see [[legal-thesis-3123-vs-31252]].
- **Never extinguished:** ultimate accountability. Under ICH E6(R3) (FDA-adopted), the sponsor retains responsibility for the quality and integrity of the trial and must maintain **documented oversight** of every service provider, including a CRO holding transferred obligations. The 312.52 transfer moves direct enforcement exposure for the enumerated items; it does not end the sponsor's oversight duty or FDA's ability to look at the whole arrangement.

## On-form disclosure

The transfer is not private. 21 CFR 312.23(a)(1)(viii) requires the IND cover sheet to identify any CRO, the study involved, and **a listing of the obligations transferred**; this is Field 14 of [[form-fda-1571-ind-cover|Form FDA 1571]]. An amended TORO therefore triggers a 1571 information update. In commercial practice the TORO is a schedule appended to the Master Services Agreement or task order between sponsor and CRO ([[sponsor-cro-site-coordination]]); it is an essential record retained in the sponsor TMF ([[document-catalog]], [[startup-tmf-checklist]]).

## Anatomy of the TORO instrument

| Element | Content | Why |
|---|---|---|
| Parties | Legal names/addresses of sponsor and CRO (a person/entity) | 312.3(b); enforceability |
| Study identification | IND number, protocol number/title | 312.23(a)(1)(viii) disclosure must match |
| Effective date & term | When assumption begins/ends; amendment procedure | The default rule makes timing load-bearing |
| **Enumerated obligations schedule** | Each assumed obligation named **with its CFR citation** | 312.52(a) enumeration rule; anything omitted is retained |
| Retained obligations | Express recitation of what stays with the sponsor | Prevents ambiguity; mirrors the default rule |
| Oversight & communication | Sponsor oversight mechanism, escalation, safety-data flow to the sponsor's medical judgment holder | ICH E6(R3) documented oversight; 312.32 clocks |
| Records & inspection | CRO recordkeeping per 312.57/312.58; FDA access | 312.52(b) — CRO stands in the sponsor's shoes |
| Termination & re-transfer | Obligation hand-back mechanics; no gap in coverage | Continuity of compliance |
| Signatures | Authorized signatories of both parties | The writing requirement |

## The micro-CRO instrument

> [!interpretive] OSSICRO position
> In the OSSICRO operating model, the [[micro-cro-accountable-layer|micro-CRO]] is the 312.52 transferee for the sponsor-investigator who cannot practically carry the full sponsor load. A model enumeration — every line interpretive, requiring counsel review per engagement:
>
> | Obligation | Citation | Typical disposition |
> |---|---|---|
> | Selecting and providing qualified monitors; monitoring conduct | 312.53(d), 312.56(a) | **Transfer** to micro-CRO |
> | Maintaining drug shipment/disposition records | 312.57(a) | **Transfer** (execution) |
> | Assuring return/disposition of unused drug | 312.59 | **Transfer** (execution); destruction authorization retained |
> | Preparation and submission mechanics of IND safety reports | 312.32(c) | **Split** — micro-CRO drafts/submits on time; causality/expectedness/seriousness judgment is retained by the sponsor-investigator/[[medical-monitor]] |
> | Annual report preparation | 312.33 | **Split** — drafting transferred; content ownership and signature retained |
> | Maintaining an effective IND; FDA relationship; 1571 signature | 312.50, 312.23(a)(1) | **Retained** — never transferred in the OSSICRO model |
>
> OSSICRO the software generates the TORO, validates that every transferred item carries a citation and that the schedule reconciles against the Form 1571 Field 14 listing, and maintains the obligation-to-owner map in [[compliance-mapping]]. The signatures, and the assumption of liability they effect, belong to the humans and the entity.

> [!warning] Non-delegable
> The transferee under 21 CFR 312.52 must be a legal person or entity; **no obligation can be transferred to software**, and OSSICRO never holds, assumes, or discharges any sponsor obligation. The decision *which* obligations to transfer, the execution of the TORO by both parties, and the sponsor's continuing documented oversight of the transferee (ICH E6(R3)) are human/entity functions. Under the default rule of 312.52(a), any obligation the writing does not describe remains with the sponsor — a drafting omission is a retained legal duty, which is precisely why OSSICRO's completeness check on this instrument exists and why a qualified human must still review it.

## Related
- [[cro]]
- [[micro-cro-accountable-layer]]
- [[sponsor]]
- [[sponsor-investigator]]
- [[legal-thesis-3123-vs-31252]]
- [[sponsor-cro-site-coordination]]
- [[form-fda-1571-ind-cover]]
- [[delegation-of-authority-log]]
- [[subinvestigator-and-delegation]]
- [[ind-safety-report]]
- [[ind-annual-report-dsur]]
- [[non-delegable-functions-and-gates]]
- [[compliance-mapping]]

## Sources
- [21 CFR 312.52 — Transfer of obligations to a contract research organization (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.52)
- [21 CFR 312.52 (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/312.52)
- [21 CFR 312.3 — Definitions (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-A/section-312.3)
- [21 CFR 312.23 — IND content and format (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.23)
- [21 CFR Part 312 Subpart D — Responsibilities of Sponsors and Investigators (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D)
- [FDA — Bioresearch Monitoring (BIMO) compliance programs](https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/bioresearch-monitoring-program-bimo-compliance-programs)
- [ICH E6(R3) Step 4 Final Guideline (Jan 2025)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [FDA — E6(R3) Good Clinical Practice guidance page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e6r3-good-clinical-practice-gcp)
