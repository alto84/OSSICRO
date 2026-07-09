---
title: "Micro-CRO Operating Model"
section: "05-ossicro-system"
status: mixed
governing_authority:
  - "21 CFR 312.52 (Transfer of obligations to a contract research organization)"
  - "21 CFR 312.3(b) (Sponsor-investigator)"
  - "21 CFR 312.50-312.59 (Sponsor responsibilities)"
  - "21 CFR 312.60-312.69 (Investigator responsibilities)"
  - "ICH E6(R3) Section 5 (Sponsor)"
tags: [ossicro/micro-cro, ossicro/gating, role/cro, role/sponsor-investigator, cfr/312, gcp/e6r3, status/interpretive]
aliases: ["Micro-CRO", "Thin Accountable Layer", "Micro-CRO Service Tiers"]
updated: 2026-07-09
---

# Micro-CRO Operating Model

> [!authority] Governing authority
> [21 CFR 312.52](https://www.law.cornell.edu/cfr/text/21/312.52) (obligations transfer, in writing, only to a legally accountable entity); [21 CFR 312.3(b)](https://www.law.cornell.edu/cfr/text/21/312.3) (the sponsor-investigator holds both obligation sets); [21 CFR 312.50-312.59](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D) (sponsor duties); ICH E6(R3) §5 (sponsor oversight of service providers is non-transferable). Status: **Mixed** — the accountability boundary is black-letter law; the thin-layer service design that operates inside it is the OSSICRO position, labelled interpretive.

The OSSICRO micro-CRO is a **thin, named, legally accountable human entity** that holds only the functions [21 CFR 312.52(b)](https://www.law.cornell.edu/cfr/text/21/312.52) requires an *entity* to hold, and only when the [[sponsor-investigator]] cannot personally hold them. It exists because the load-bearing legal fact of the whole system is that sponsor obligations transfer to a legally accountable person or entity that "shall be subject to the same regulatory action as a sponsor" — never to software. Software absorbs the *coordination labor*; the micro-CRO absorbs the *irreducible accountability* that labor sits next to. This page defines what the layer is, what it is not, its service tiers, and the exact functions it may and may not hold.

## Why a thin accountable layer must exist at all

CRO work decomposes into roughly eight functional streams — site activation, regulatory-submissions support, clinical monitoring/CRA, project management, pharmacovigilance/safety, data management, biostatistics, and medical writing. Across the industry, ~90-95% of a CRO's *direct* cost is labor (PRA Health Sciences disclosed 95.7% of direct cost as staffing in 2015), gross margins run ~40-50%, and the marked-up service margin is ~15-25% on direct cost. The margin therefore concentrates in the billable-hour coordination layers — project management, monitoring hours, data management, medical writing — which is precisely the automatable surface. See [[cro]] for the full functional/margin map.

Automating that surface does not eliminate the residue that legally *requires* an accountable party. Under [21 CFR 312.52(b)](https://www.law.cornell.edu/cfr/text/21/312.52), a transferee is directly liable to FDA — Warning Letters, injunctions, IND clinical hold, debarment run against it. A validated software system cannot be subject to that enforcement, so it cannot be a transferee. The micro-CRO is the smallest possible entity that *can* be: a named legal person (or the sponsor-investigator acting personally) plus the qualified humans who own the non-delegable acts. Everything else is open-source, templatable, physician-operable software.

> [!interpretive] OSSICRO position
> "Thin" is a design thesis, not a regulatory category. The claim is that when AI absorbs the ~90-95%-labor coordination surface, the residual entity that must exist for §312.52(b) purposes can be small enough for a solo clinician or a lightweight shared service to sustain — collapsing the economics that normally make the [[sponsor-investigator]] role impractical. The claim is defended, not assumed; the accountability floor below is black-letter.

## What the micro-CRO holds — and never holds

The default and preferred structure transfers **nothing**: a [[sponsor-investigator]] under [21 CFR 312.3(b)](https://www.law.cornell.edu/cfr/text/21/312.3) lawfully holds both the sponsor obligation set ([21 CFR 312.50-312.59](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D)) and the investigator obligation set ([21 CFR 312.60-312.69](https://www.law.cornell.edu/cfr/text/21/312.60)) in one person, and no obligation is transferred to a non-entity. The micro-CRO engages only where the clinician cannot personally discharge a *sponsor* function and elects to transfer it, in writing, via a [[transfer-of-regulatory-obligations-toro|Transfer of Regulatory Obligations (TORO)]] instrument under [21 CFR 312.52(a)](https://www.law.cornell.edu/cfr/text/21/312.52).

**Transferable to the micro-CRO** (sponsor obligations, each enumerated in the TORO — an obligation not described in writing is deemed *not* transferred):

- Selection and documentation of qualified investigators and monitors (§312.53), including collection of the [[form-fda-1572-statement-of-investigator|Form FDA 1572]], CV, and financial-disclosure package.
- Furnishing and updating the [[investigators-brochure|Investigator's Brochure]] and informing investigators of new safety findings (§312.55).
- Monitoring the progress of investigations (§312.56) via qualified monitors ([[clinical-monitor-cra]]).
- Sponsor recordkeeping, retention, and disposition of investigational supply (§312.57, §312.59).
- Drafting and administrative submission of safety reports and annual reports (§312.32, §312.33) — *drafting and clerical submission only*; the underlying medical judgments are not transferable (below).

> [!warning] Non-delegable
> The micro-CRO can **never** hold: (a) the patient [[informed-consent-form|informed-consent event]] (the investigator's act, [21 CFR Part 50](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50)); (b) [[irb-iec|IRB/ethics judgment]] ([21 CFR Part 56](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56)); (c) SAE **causality and expectedness** determination and the [[medical-monitor]]'s continue/modify/stop safety judgment ([21 CFR 312.32](https://www.law.cornell.edu/cfr/text/21/312.32)); (d) the **investigator conduct** obligations of [§312.60](https://www.law.cornell.edu/cfr/text/21/312.60), which bind the investigator personally and are not transferable to any service vendor; (e) the [[form-fda-1571-ind-cover|Form FDA 1571]] IND-holder attestation and the Form 1572 signature; (f) [[biostatistician|statistical sign-off]] on the SAP/CSR ([ICH E9](https://database.ich.org/sites/default/files/E9_Guideline.pdf)). ICH E6(R3) §5 is explicit that delegation of a function to a service provider does *not* transfer accountability for the quality and integrity of the trial — the sponsor (or sponsor-investigator) retains documented oversight regardless. The micro-CRO holds the *sponsor* functions it enumerates; it does not manufacture new capacity to own a human judgment the law assigns to a licensed person or a constituted board.

## Service tiers

The operating model is a graduated escalation from free self-serve software to full assumption of enumerated obligations. It is modeled on real institutional precedent: Harvard Catalyst's contributory-network IND/IDE consult model, Duke/ReGARDD's cross-institutional shared services, and the University of Michigan MICHR IND/IDE Investigator Assistance Program (MIAP), whose free-initial-consult-then-$90/hr structure is the closest documented analogue to a hybrid automated-triage-plus-paid-expert model.

| Tier | Name | What it delivers | Accountability held |
|---|---|---|---|
| **0** | Open-source self-serve | The wiki, template library, and generate/check/validate engine, physician-operable, no charge. | None transferred — the clinician is [[sponsor-investigator]] and holds everything. |
| **1** | Automated triage & generation | Software-driven pathway determination ([[two-modes-site-vs-sponsor-investigator|Mode A / Mode B / expanded access]]), document drafting, [[completeness-ledger|completeness ledger]], deadline tracking. | None transferred; all output is a draft for the clinician's review and signature. |
| **2** | Paid human review at gates | A qualified human ([[medical-monitor]], [[clinical-monitor-cra|monitor]], regulatory reviewer, or [[biostatistician]]) reviews the draft at a specific [[non-delegable-functions-and-gates|gate]] and provides expert judgment. | The reviewing human owns *their* professional judgment; still no §312.52 transfer of a sponsor obligation. |
| **3** | Micro-CRO assumption of obligations | The named micro-CRO entity assumes specific, enumerated sponsor obligations via a signed [[transfer-of-regulatory-obligations-toro|TORO]]. | The micro-CRO is directly liable to FDA for each enumerated obligation ([§312.52(b)](https://www.law.cornell.edu/cfr/text/21/312.52)); investigator conduct and the non-delegable judgments remain outside the transfer. |

Tiers 0-2 involve **no** §312.52 transfer — they are software, or expert consultation, layered under a clinician who remains the accountable party. Only Tier 3 is a legal transfer, and it is bounded: it can never reach investigator conduct obligations ([§312.60](https://www.law.cornell.edu/cfr/text/21/312.60)) or the non-delegable judgments, because those are not sponsor obligations available for §312.52 transfer in the first place.

> [!interpretive] OSSICRO position
> The tiering is the escalation path, not a menu of ways to offload judgment. Tier 3 exists for the genuine case where a solo clinician cannot personally hold a *sponsor* function (e.g., sustained sponsor-side monitoring of a multi-visit protocol) and needs an accountable entity to assume it. It is designed to be invoked narrowly and enumerated precisely, because every unenumerated obligation stays with the sponsor by operation of [§312.52(a)](https://www.law.cornell.edu/cfr/text/21/312.52) — the writing is the operative legal instrument, and vagueness in it defaults *toward* the sponsor, not the CRO.

## Relationship to the software system

The micro-CRO is the human backstop of the [[generate-check-validate-engine|generate/check/validate engine]]. Every validation rule that touches an accountable act *fails to a gate* rather than proceeding autonomously; the gate routes to the responsible human, who is either the sponsor-investigator directly (Tiers 0-1), a Tier-2 expert reviewer, or the Tier-3 micro-CRO's named accountable person. The [[compliance-mapping]] manifest records, per artifact, which human owns the sign-off. The [[verifiable-site-qualification-dossier]] renders the resulting requirement→artifact→citation→signer chain as a cryptographically verifiable manifest — the tangible product the micro-CRO layer stands behind and the trust wedge with a skeptical [[pharma-partner-sponsor|pharma partner]].

The layer runs a **real quality system**: SOPs, training records, and a validated Part-11 environment ([[part-11-and-ai-credibility]]). ICH E6(R3) §5's service-provider-oversight expectation applies to the micro-CRO's own use of the OSSICRO software exactly as it applies to any sponsor's use of a technology vendor — the entity retains documented oversight of the tool.

## The failed alternative this design avoids

The disintermediation temptation — "let the software be the CRO" — is foreclosed by [§312.52](https://www.law.cornell.edu/cfr/text/21/312.52) and corroborated by the market. Science 37 (decentralized-trial software, a ~$1B SPAC valuation collapsing to a ~$38M take-private) and TrialSpark→Formation Bio (which abandoned the CRO service model to become a drug *developer*) both show that coordination-only software captures no durable value; value follows the asset and the accountability, not the tooling. See [[failed-disintermediation-case-studies]]. The micro-CRO model is the structural response: it places accountability where the law requires it (a real entity), automates the labor that the law does not require an entity to perform, and keeps the two rigorously separate.

## Related

- [[micro-cro-accountable-layer]]
- [[cro]]
- [[sponsor-investigator]]
- [[transfer-of-regulatory-obligations-toro]]
- [[two-modes-site-vs-sponsor-investigator]]
- [[non-delegable-functions-and-gates]]
- [[compliance-mapping]]
- [[verifiable-site-qualification-dossier]]
- [[legal-thesis-3123-vs-31252]]
- [[failed-disintermediation-case-studies]]
- [[06-personas/micro-cro|Micro-CRO persona]]

## Sources

- [21 CFR 312.52 — Transfer of obligations to a contract research organization (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/312.52)
- [21 CFR 312.3 — Definitions (sponsor-investigator) (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/312.3)
- [21 CFR Part 312 Subpart D — Responsibilities of Sponsors and Investigators (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D)
- [21 CFR 312.32 — IND safety reporting (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/312.32)
- [FDA — Overview of Sponsor-Investigator Roles and Responsibilities (media 174660)](https://www.fda.gov/media/174660/download)
- [FDA — E6(R3) Good Clinical Practice (final guidance, Sept 2025)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e6r3-good-clinical-practice-gcp)
- [Harvard Catalyst — IND/IDE Consulting Program](https://catalyst.harvard.edu/regulatory/ind-ide-consulting/)
- [University of Michigan MICHR — IND/IDE Consultation (MIAP)](https://michr.umich.edu/offering/ind-ide-consultation/)
- Kim ES et al., "Sharing Sponsor-Investigator IND/IDE Resources: A Contributory Network Model," 2014. PMID [24455986](https://pubmed.ncbi.nlm.nih.gov/24455986/)
