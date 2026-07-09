---
title: "The Micro-CRO: OSSICRO's Thin Accountable Layer"
section: "01-roles-responsibilities"
status: mixed
governing_authority:
  - "21 CFR 312.52 (the entity requirement it exists to satisfy)"
  - "21 CFR 312.3(b) (CRO definition; sponsor-investigator definition)"
  - "21 CFR 312.50-312.59 (the obligations it may assume)"
  - "ICH E6(R3) Annex 1 §3 (quality-managed service provision)"
tags: [role/cro, ossicro/micro-cro, cfr/312, ich/e6r3, entity/micro-cro, status/interpretive]
aliases: [micro-cro-entity, thin-accountable-layer]
updated: 2026-07-09
---

# The Micro-CRO: OSSICRO's Thin Accountable Layer

> [!authority] Governing authority
> 21 CFR 312.52 (written transfer to a legally accountable entity — the requirement the micro-CRO exists to satisfy); 21 CFR 312.3(b); 21 CFR 312.50–312.59; ICH E6(R3) Annex 1 §3. Status: **Mixed** — the legal constraints the micro-CRO answers are confirmed black-letter; the micro-CRO design itself is the central **interpretive OSSICRO position**, marked throughout.

The micro-CRO is OSSICRO's answer to an unavoidable legal fact: some clinical-trial functions must be held by a **legally accountable entity or qualified human**, and software can never be either. It is a named, real, thin legal entity — with SOPs, a quality system, and qualified staff — that assumes, via a written [[transfer-of-regulatory-obligations-toro|Transfer of Regulatory Obligations]], only those enumerated sponsor obligations that a [[sponsor-investigator]] cannot practically hold personally. Everything else — the coordination labor where [[cro|CRO margin]] concentrates — stays in open-source, physician-operable software. This page defines what the micro-CRO is, the legal basis that shapes it, exactly which functions it can and cannot hold, its service tiers, and the institutional precedents it is modeled on.

## Why it must exist

Two confirmed rules bound the design space:

1. **21 CFR 312.52(b):** a transferee of sponsor obligations "shall be subject to the same regulatory action as a sponsor." Only a legal person/entity can be enforced against — Warning Letter, clinical hold, injunction, debarment. Software cannot be a transferee. See [[legal-thesis-3123-vs-31252]].
2. **21 CFR 312.52(a):** "Any obligation not covered by the written description shall be deemed not to have been transferred." Transfer is exact and enumerated; there is no ambient or implied assumption of duties.

The second rule is what makes a *thin* accountable layer coherent rather than merely small: the TORO writing defines the micro-CRO's regulatory exposure precisely, obligation by obligation. The micro-CRO assumes a short, named list; the deemed-not-transferred default keeps everything else with the sponsor-investigator. The instrument that would be a liability trap for a careless full-service CRO is, used deliberately, the mechanism that keeps the accountable layer minimal.

## What it is

> [!interpretive] OSSICRO position
> The micro-CRO design in this section is OSSICRO's thesis, not a regulatory category. "Micro-CRO" appears nowhere in 21 CFR; it is an ordinary §312.52 CRO distinguished only by deliberate minimalism — it assumes the *fewest* obligations consistent with making the sponsor-investigator role tractable, because every function it does not assume can be served by software drafting for the physician's own review and signature.

Concretely, the micro-CRO is:

- **A named legal entity** capable of contracting with the sponsor-investigator and of being subject to FDA enforcement for each obligation it assumes (21 CFR 312.52(b)).
- **A holder of enumerated obligations only.** Candidate obligations from the Subpart D menu, assumed case-by-case via TORO: monitoring oversight (21 CFR 312.56, executed through qualified monitors — see [[clinical-monitor-cra]] and [[monitoring-plan]]); sponsor recordkeeping/retention QA (312.57); regulatory-submission management and safety-report preparation and submission (312.32, with the causality/expectedness call owned by a qualified physician — see below); annual-report preparation (312.33). See [[sponsor]] for the full menu.
- **An employer/engager of the qualified humans** who own gated judgments when the sponsor-investigator does not personally: a [[medical-monitor]] (a qualified physician who owns seriousness/causality/expectedness under 21 CFR 312.32 and ICH E2A — this sponsor obligation *can* be assumed by a CRO, but only into the hands of a qualified physician, never into software), a qualified monitor, a [[biostatistician]] for statistical sign-off.
- **A quality-managed operation.** For every assumed obligation it must "comply with the specific regulations in this chapter applicable to this obligation" (312.52(b)): written SOPs, training records, an audit trail, and inspection-readiness — FDA can inspect it exactly as it inspects a sponsor (21 CFR 312.58), including under the BIMO program (see [[fda-as-counterparty]]). ICH E6(R3) Annex 1 §3 adds the risk-proportionate quality-management expectations that apply to any service provider.

## What it is not

- **Not a full-service CRO.** It does not sell project management, data management, or medical-writing hours; those are software functions in OSSICRO ([[generate-check-validate-engine]]). Its unit economics are the inverse of the industry's: the [[cro|~40–50% margin coordination layer]] is deliberately given away as open source.
- **Not a metasite or a technology vendor.** Science 37 failed as coordination software plus telehealth network; TrialSpark exited the model entirely ([[failed-disintermediation-case-studies]]). The micro-CRO holds *accountability*, which is exactly what those plays lacked.
- **Not the sponsor of record.** In Mode B the sponsor-investigator holds the IND and signs [[form-fda-1571-ind-cover|Form 1571]]; the micro-CRO is transferee of enumerated obligations, never the IND holder. See [[two-modes-site-vs-sponsor-investigator]].
- **Not software.** The software drafts, checks, routes, times, and version-controls; the micro-CRO's humans review, judge, and sign.

> [!warning] Non-delegable
> Functions the micro-CRO can **never** hold, under any TORO drafting:
> - **Investigator conduct obligations** (21 CFR 312.60–312.69): protocol adherence, drug control, case histories, SAE reporting to the sponsor, IRB assurance. These bind the licensed [[investigator]] personally and are non-transferable to any vendor or entity — see [[subinvestigator-and-delegation]].
> - **Informed consent** (21 CFR Part 50): obtained under the investigator's responsibility at the site; see [[informed-consent-document-vs-event]].
> - **IRB/ethics judgment** (21 CFR Part 56): an independent constituted board's determination — see [[irb-iec]].
> - **The sponsor-investigator's own attestations:** the 1571 and [[form-fda-1572-statement-of-investigator|1572]] signatures and [[form-fda-3454-3455-financial-disclosure|Part 54 financial certification/disclosure]] are personal legal acts.
> - **DSMB deliberation** ([[dsmb-dmc]]) and the manufacturer's decision to supply drug ([[pharma-partner-sponsor]]).
> Within the micro-CRO itself, assumed judgments stay with named qualified humans — causality with its physician medical monitor, deviation judgment with its qualified monitor — never with the OSSICRO engine. The engine's [[safety-clock-engine|safety clocks]] compute deadlines and escalate; they never make the causality call and never file.

## Service tiers

> [!interpretive] OSSICRO position
> Tiering below follows the precedent of MICHR's IND/IDE Investigator Assistance Program (free consult, then fee-based human assistance at ~$90/hr) — see [[micro-cro-operating-model]] for the full operating detail.

| Tier | Service | Who acts | Legal posture |
|---|---|---|---|
| 0 | Open-source self-serve | The physician, using OSSICRO software | No micro-CRO involvement; sponsor-investigator holds everything |
| 1 | Automated triage and generation | Software drafts; physician reviews/signs | No obligations transferred |
| 2 | Paid human review at accountable gates | Micro-CRO's qualified humans review specific artifacts/judgments | Consulting; obligations still not transferred |
| 3 | Assumption of enumerated obligations | Micro-CRO becomes §312.52 transferee via TORO | Direct FDA accountability for each named obligation |

The tier boundary that matters legally is 2→3: below it the micro-CRO advises and the sponsor-investigator remains obligated for everything; at Tier 3 the TORO writing moves named obligations and FDA enforcement follows them.

## Institutional precedents

The micro-CRO is a formalization of support structures academic medicine already runs, which is both design validation and citable evidence that sponsor-investigators need an accountable support layer:

- **Harvard Catalyst IND/IDE Consult Service** — a shared regulatory-consult layer across a decentralized network of academic medical centers, built explicitly because investigator-sponsors "often do not fully appreciate their regulatory obligations nor have resources to ensure compliance" (Kim MJ et al., *Clin Transl Sci* 2014; PMID [24455986](https://pubmed.ncbi.nlm.nih.gov/24455986/); [DOI 10.1111/cts.12146](https://doi.org/10.1111/cts.12146)); plus the Massachusetts "contributory network model" for sharing sponsor-investigator IND/IDE resources across institutions.
- **MICHR MIAP** (University of Michigan) — free automated/initial triage escalating to fee-based ($90/hr) human regulatory assistance; the direct pricing/tier precedent ([MICHR IND/IDE consultation](https://michr.umich.edu/offering/ind-ide-consultation/)).
- **Duke ORAQ / ReGARDD** — cross-institutional sponsor-investigator training and regulatory support shared beyond Duke at no cost ([Duke ORAQ sponsor resources](https://medschool.duke.edu/research/research-support/research-support-offices/office-regulatory-affairs-and-quality/sponsor-0)).
- **Vanderbilt V-CAP** — the published rules-driven personalized-approvals checklist ([PMC3767144](https://pmc.ncbi.nlm.nih.gov/articles/PMC3767144/)); precedent for the software side the micro-CRO sits behind — see [[prior-art-vcap-irex-smartirb]].

None of these entities takes §312.52 transfer — they consult while the investigator retains everything. The micro-CRO's Tier 3 goes one deliberate step further, and that step is precisely what pharma counterparties need: a named, enforceable entity behind a new site. The [[verifiable-site-qualification-dossier]] — requirement → artifact → citation → responsible-human signature, hash-chained into the Part 11 audit trail — is the micro-CRO's trust product toward [[pharma-partner-sponsor|pharma partners]] evaluating a small or single-patient site (see [[single-patient-site-and-pharma-acceptance]]).

## Related

- [[cro]]
- [[micro-cro-operating-model]]
- [[micro-cro]]
- [[transfer-of-regulatory-obligations-toro]]
- [[sponsor-investigator]]
- [[sponsor]]
- [[legal-thesis-3123-vs-31252]]
- [[failed-disintermediation-case-studies]]
- [[non-delegable-functions-and-gates]]
- [[medical-monitor]]
- [[clinical-monitor-cra]]
- [[verifiable-site-qualification-dossier]]
- [[single-patient-site-and-pharma-acceptance]]
- [[two-modes-site-vs-sponsor-investigator]]
- [[prior-art-vcap-irex-smartirb]]
- [[qualified-person-qppv-eu]]

## Sources

- [eCFR — 21 CFR 312.52 Transfer of obligations to a contract research organization](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.52)
- [eCFR — 21 CFR 312.3 Definitions and interpretations](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-A/section-312.3)
- [Cornell LII — 21 CFR Part 312 Subpart D](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-D)
- [FDA — Overview of Sponsor-Investigator Roles and Responsibilities](https://www.fda.gov/media/174660/download)
- [FDA — Investigational New Drug Applications Prepared and Submitted by Sponsor-Investigators (draft guidance, 2015)](https://www.fda.gov/files/drugs/published/Investigational-New-Drug-Applications-Prepared-and-Submitted-by-Sponsor-Investigators.pdf)
- [Kim MJ, Winkler SJ, Bierer BE, Wolf D. The Harvard Catalyst IND/IDE Consult Service. Clin Transl Sci. 2014;7(2):150-5. PMID 24455986](https://doi.org/10.1111/cts.12146)
- [Harvard Catalyst — Sharing Sponsor-Investigator IND/IDE Resources: A Contributory Network Model](https://catalyst.harvard.edu/publications-documents/sharing-sponsor-investigator-ind-ide-resources-a-contributory-network-model-of-scalable-adaptable-support-services-across-massachusetts-academic-institutions/)
- [University of Michigan MICHR — IND/IDE Investigator Assistance Program (MIAP)](https://michr.umich.edu/offering/ind-ide-consultation/)
- [Duke ORAQ — Sponsor-investigator resources (ReGARDD-distributed training)](https://medschool.duke.edu/research/research-support/research-support-offices/office-regulatory-affairs-and-quality/sponsor-0)
- [Vanderbilt V-CAP methodology (PMC3767144)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3767144/)
- [ICH Efficacy Guidelines — E6(R3) Good Clinical Practice](https://www.ich.org/page/efficacy-guidelines)
