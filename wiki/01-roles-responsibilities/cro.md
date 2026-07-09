---
title: "Contract Research Organization (CRO)"
section: "01-roles-responsibilities"
status: mixed
governing_authority:
  - "21 CFR 312.3(b) (definition of CRO)"
  - "21 CFR 312.52 (transfer of obligations to a CRO)"
  - "21 CFR 312.50-312.59 (the transferable sponsor obligation set)"
  - "ICH E6(R3) Annex 1 §3 (sponsor oversight of service providers)"
tags: [role/cro, cfr/312, ich/e6r3, entity/cro, ossicro/micro-cro, status/confirmed]
aliases: [contract-research-organization]
updated: 2026-07-09
---

# Contract Research Organization (CRO)

> [!authority] Governing authority
> 21 CFR 312.3(b) (definition); 21 CFR 312.52(a)–(b) (written transfer of obligations; transferee liability); 21 CFR 312.50–312.59 (the transferable menu); ICH E6(R3) Annex 1 §3 (sponsor responsibility for service providers). Status: **Mixed** — the transfer mechanism and liability rule are black-letter; the functional/margin decomposition is industry data, and the coordination-vs-accountable classification is an OSSICRO analytical frame, both marked below.

A Contract Research Organization is the only party to whom a [[sponsor]]'s regulatory obligations can actually move. 21 CFR 312.3(b) defines a CRO as "a person that assumes, as an independent contractor with the sponsor, one or more of the obligations of a sponsor, e.g., design of a protocol, selection or monitoring of investigations, evaluation of reports, and preparation of materials to be submitted to the Food and Drug Administration" ([eCFR](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-A/section-312.3)). The load-bearing consequence for OSSICRO's entire design is in §312.52: obligations transfer **only in writing** and **only to a legally accountable transferee** that becomes subject to the same FDA enforcement as a sponsor. Software cannot be that transferee. This page states the transfer mechanism, decomposes CRO work into its functional streams, maps where CRO margin sits, and classifies each stream as coordination labor versus accountable function — the classification that defines what OSSICRO automates and what the [[micro-cro-accountable-layer|micro-CRO]] must hold.

## The transfer mechanism — 21 CFR 312.52(a)

"A sponsor may transfer responsibility for any or all of the obligations set forth in this part to a contract research organization. Any such transfer shall be described in writing. If not all obligations are transferred, the writing is required to describe each of the obligations being assumed by the contract research organization. If all obligations are transferred, a general statement that all obligations have been transferred is acceptable. **Any obligation not covered by the written description shall be deemed not to have been transferred.**" ([21 CFR 312.52](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.52))

Three operational consequences:

1. **The writing is the operative legal instrument.** In practice this is the Transfer of Regulatory Obligations (TORO) schedule appended to the Master Services Agreement or task order — see [[transfer-of-regulatory-obligations-toro]] and [[sponsor-cro-site-coordination]].
2. **Enumeration is exact.** A partial transfer covers only what is named. Silence retains the obligation with the sponsor — the default always resolves toward the sponsor, never away.
3. **The transferable menu is Subpart D** (21 CFR 312.50–312.59): general responsibilities (312.50), selecting investigators and monitors and collecting the [[form-fda-1572-statement-of-investigator|1572]]/CV/financial disclosure (312.53), informing investigators (312.55), review of ongoing investigations (312.56), recordkeeping and retention (312.57), inspection of sponsor records (312.58), and disposition of unused drug (312.59) — plus the sponsor's FDA-facing reporting duties such as [[ind-safety-report|IND safety reports]] (312.32) and annual reports (312.33). See [[sponsor]].

## The accountability rule — 21 CFR 312.52(b)

"A contract research organization that assumes any obligation of a sponsor shall comply with the specific regulations in this chapter applicable to this obligation and shall be **subject to the same regulatory action as a sponsor** for failure to comply with any obligation assumed under these regulations. Thus, all references to 'sponsor' in this part apply to a contract research organization to the extent that it assumes one or more obligations of the sponsor."

FDA enforcement — Warning Letters, clinical hold, injunction, debarment — runs against the CRO directly for assumed obligations. This is why the transferee must be a legal person or entity capable of being enforced against: **software cannot be "subject to the same regulatory action as a sponsor," so software can never be a §312.52 transferee.** Pure software disintermediation of the CRO is structurally foreclosed by regulation, not merely commercially difficult. The full argument, and its pairing with the lawful [[sponsor-investigator]] path under 312.3(b), is at [[legal-thesis-3123-vs-31252]]; the market evidence (Science 37's ~$1B-to-~$38M collapse; TrialSpark's pivot into Formation Bio as a drug developer) is at [[failed-disintermediation-case-studies]].

Two boundary rules complete the frame:

- **Investigator obligations never transfer to a CRO.** 21 CFR 312.60–312.69 bind the clinical [[investigator]] personally — conduct per protocol, consent, drug control, records, SAE reporting to the sponsor, IRB assurance. A CRO can supply monitors to *verify* investigator compliance; it cannot *assume* investigator conduct duties. See [[subinvestigator-and-delegation]].
- **ICH E6(R3) adds an oversight layer, not an escape.** E6(R3) Annex 1 §3 (which broadens "CRO" to the wider "service provider" vocabulary) requires the sponsor to oversee service providers under a risk-proportionate quality-management system; delegation to a service provider never displaces the sponsor's ultimate accountability for participant safety and data reliability ([ICH efficacy guidelines](https://www.ich.org/page/efficacy-guidelines); FDA adopted E6(R3) as final guidance September 2025).

## The eight functional streams

CRO work decomposes into approximately eight streams. The classification column is the OSSICRO analytical frame (interpretive — see callout below): **coordination** = automatable labor; **accountable residue** = the judgment or attestation a qualified human/entity must own.

| # | Stream | Content | Classification |
|---|---|---|---|
| 1 | Start-up / site activation | Feasibility, site selection, contracts/budgets, regulatory-document collection (1572s, CVs, [[form-fda-3454-3455-financial-disclosure|financial disclosure]], IRB approvals), essential-document/TMF assembly | Mostly coordination; residue = sponsor QA sign-off. See [[site-activation]] |
| 2 | Regulatory submissions support | IND assembly ([[form-fda-1571-ind-cover|Form 1571]]), eCTD publishing, annual reports, safety reports | Coordination-heavy drafting; residue = 1571 signature and IND-holder accountability |
| 3 | Clinical monitoring (CRA) | SDV, protocol-compliance review, on-site/remote visits | Hybrid: deviation *judgment* needs a qualified [[clinical-monitor-cra|monitor]]; scheduling/tracking/report-drafting is coordination. See [[risk-based-monitoring-e6r3]] |
| 4 | Project management | Timelines, vendor coordination, status reporting | Pure coordination |
| 5 | Pharmacovigilance / safety | SAE intake, MedDRA coding, narrative writing, expedited 7/15-day submissions, aggregate reports | Intake/coding/narrative-draft = coordination; causality and expectedness = non-delegable [[medical-monitor]] judgment (21 CFR 312.32; ICH E2A). See [[pharmacovigilance-safety]] |
| 6 | Data management | EDC build, CRF design, edit checks, query management, database lock | Highly automatable coordination |
| 7 | Biostatistics | SAP, randomization, TLFs, analysis | Automatable computation; residue = [[biostatistician]] sign-off on SAP/CSR (ICH E9) |
| 8 | Medical writing | Protocol, IB, ICF, CSR | Drafting automatable; residue = qualified-author and sponsor approval |

## The margin map

Industry financial data — market evidence, not regulation:

- CRO **gross margins run ~40–50%** industry-wide; the marked-up service margin on direct cost is typically **~15–25%** (negotiable) ([IntuitionLabs CRO cost guide](https://intuitionlabs.ai/articles/evaluate-cro-cost-clinical-trial); [Healthcare IB — the CRO business model](https://ibinterviewquestions.com/guides/healthcare-investment-banking/cro-business-model)).
- **~90–95% of a CRO's direct cost is labor** — PRA Health Sciences disclosed 95.7% of direct cost as employee/staffing-agency labor in 2015.
- Full-Service Outsourcing carries mid-to-high-teens EBITDA versus high-single/low-teens for Functional Service Provider work.

The margin therefore concentrates in the billable-hour coordination layers — project management, monitoring hours, data management, medical writing (streams 3, 4, 6, 8) — which are exactly the streams with the *least* irreducible legal accountability. This asymmetry is the economic core of the OSSICRO thesis.

> [!interpretive] OSSICRO position
> The coordination-vs-accountable classification above, and the conclusion drawn from it, are OSSICRO's analytical frame: software can lawfully absorb the coordination labor of streams 1–8 **so long as every accountable residue is gated to a qualified human or accountable entity** — the sponsor-investigator personally, or the [[micro-cro-accountable-layer|micro-CRO]] as a §312.52 transferee of enumerated obligations. This is supportable under the plain text of 312.52 and E6(R3)'s risk-based provisions, but FDA has no settled position on AI-drafted regulatory documents (the 2025 AI-credibility framework is draft); the boundary of software-assisted monitoring judgment under E6(R3) is likewise interpretive. Every OSSICRO artifact is a draft for qualified human review — see [[non-delegable-functions-and-gates]] and [[confirmed-vs-interpretive]].

> [!warning] Non-delegable
> No transfer instrument can move these to software, and a CRO transferee must staff them with qualified humans: informed consent (21 CFR Part 50, obtained under the investigator's responsibility); IRB judgment (Part 56, an independent constituted board — [[irb-iec]]); SAE causality/expectedness determination (21 CFR 312.32; ICH E2A — a qualified physician); the investigator's conduct obligations (312.60–312.69, non-transferable to any vendor); the 1571/1572 signatures; and the §312.52(b) accountable-entity function itself. OSSICRO drafts and routes; a named human owns and signs each.

## Related

- [[sponsor]]
- [[sponsor-investigator]]
- [[micro-cro-accountable-layer]]
- [[transfer-of-regulatory-obligations-toro]]
- [[legal-thesis-3123-vs-31252]]
- [[failed-disintermediation-case-studies]]
- [[sponsor-cro-site-coordination]]
- [[subinvestigator-and-delegation]]
- [[clinical-monitor-cra]]
- [[medical-monitor]]
- [[pharmacovigilance-safety]]
- [[biostatistician]]
- [[non-delegable-functions-and-gates]]
- [[micro-cro-operating-model]]
- [[entity-map]]

## Sources

- [eCFR — 21 CFR 312.52 Transfer of obligations to a contract research organization](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.52)
- [eCFR — 21 CFR 312.3 Definitions and interpretations](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-A/section-312.3)
- [Cornell LII — 21 CFR Part 312 Subpart D (sponsor and investigator obligations)](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-D)
- [FDA — Overview of Sponsor-Investigator Roles and Responsibilities](https://www.fda.gov/media/174660/download)
- [ICH Efficacy Guidelines — E6(R3) Good Clinical Practice](https://www.ich.org/page/efficacy-guidelines)
- [Quanticate — What is a CRO (functional service breakdown)](https://www.quanticate.com/blog/what-is-a-cro)
- [IntuitionLabs — Evaluating CRO Costs (margins, markup)](https://intuitionlabs.ai/articles/evaluate-cro-cost-clinical-trial)
- [Healthcare IB Guide — The CRO Business Model (margins, FSO vs FSP)](https://ibinterviewquestions.com/guides/healthcare-investment-banking/cro-business-model)
- [MedCity News — Science 37 take-private at a fraction of its $1B valuation](https://medcitynews.com/2024/01/decentralized-clinical-trials-software-mobile-app-science-37-covid-19/)
- [PR Newswire — TrialSpark rebrands as Formation Bio](https://www.prnewswire.com/news-releases/trialspark-rebrands-as-formation-bio-continuing-its-commitment-to-advancing-drug-development-innovation-302006328.html)
