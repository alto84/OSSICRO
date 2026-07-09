---
title: "What Is OSSICRO — Mission, Scope, and the Hard Line"
section: "00-overview"
status: mixed
governing_authority:
  - "21 CFR 312.3(b) (sponsor-investigator)"
  - "21 CFR 312.52 (transfer of obligations to a CRO)"
  - "21 CFR Part 11 (electronic records and signatures)"
  - "ICH E6(R3) Good Clinical Practice"
tags: [ossicro/engine, ossicro/micro-cro, ossicro/part11, status/mixed]
aliases: ["OSSICRO", "About OSSICRO", "Mission"]
updated: 2026-07-09
---

# What Is OSSICRO — Mission, Scope, and the Hard Line

> [!authority] Governing authority
> OSSICRO's architecture rests on [21 CFR 312.3(b)](https://www.law.cornell.edu/cfr/text/21/312.3) (the sponsor-investigator), is bounded by [21 CFR 312.52](https://www.law.cornell.edu/cfr/text/21/312.52) (obligations transfer only to an accountable entity), and operates on a [21 CFR Part 11](https://www.law.cornell.edu/cfr/text/21/part-11)-compliant substrate under [ICH E6(R3)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e6r3-good-clinical-practice-gcp) Good Clinical Practice. Status: **Mixed** — the regulatory frame is confirmed; the system thesis is an OSSICRO **interpretive** position, labelled throughout.

**OSSICRO — Open Source Sponsor-Investigator CRO** — is a holistic system that lets an enrolling clinician discharge the full regulatory paperwork burden required to match a patient to an early-phase program, activate a site, and reach enrollment, across every accountable entity: sponsor, CRO, investigator/[[sponsor-investigator]], [[irb-iec|IRB/IEC]], [[dsmb-dmc|DSMB]], [[pharmacovigilance-safety|pharmacovigilance]], and the [[pharma-partner-sponsor|pharma partner]]. It is five things at once: open-source software, an exhaustively-cited regulatory wiki (this corpus), a document-template library, a [[generate-check-validate-engine|generate/check/validate engine]], and a pharma-style frontend.

## The mission

Physicians who could enroll patients in the trials and early-phase therapies that might save their lives are kept out by a wall of paperwork and regulatory infrastructure they have no research office to handle. Harvard Catalyst's own consult-service literature states the problem plainly: investigator-sponsors "often do not fully appreciate their regulatory obligations nor have resources to ensure compliance" (Kim et al. 2014, [PMID 24455986](https://pubmed.ncbi.nlm.nih.gov/24455986/)). OSSICRO's mission is to make the **sponsor-investigator role tractable** for a practicing clinician — including in under-resourced settings — by absorbing the coordination labor, so that access to research is gated by clinical and ethical judgment, never by administrative capacity.

## Scope

**In scope:** US IND-phase, human-subjects clinical research and single-patient treatment access — the domain of [21 CFR Parts 11, 50, 54, 56, and 312](https://www.law.cornell.edu/cfr/text/21/part-312), the [Common Rule (45 CFR 46)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46), [HIPAA (45 CFR Parts 160/164)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164), and ICH guidances as adopted by FDA. OSSICRO supports **two modes plus a branch** (detailed in [[the-three-pathways-triage]] and [[two-modes-site-vs-sponsor-investigator]]):

- **Mode A — physician-as-site:** the physician joins a pharma sponsor's existing protocol as a site [[investigator]]. OSSICRO produces the site-activation essential-document package to sponsor standard.
- **Mode B — sponsor-investigator IND:** the physician holds their own IND and both obligation sets ([[sponsor-investigator]]). OSSICRO assembles the full [312.23](https://www.law.cornell.edu/cfr/text/21/312.23) IND package and maintains the IND.
- **Expanded-access branch:** for "no trial fits, single patient" — [Form FDA 3926](https://www.fda.gov/media/162793/download), manufacturer letter of authorization, IRB concurrence under [Subpart I](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-I). This is *treatment, not research*. See [[expanded-access-workflow]].

**Out of scope:** OSSICRO gives no clinical recommendation, makes no eligibility determination, and files nothing autonomously. It is a documentation and coordination system, not a clinical decision-support tool and not a regulated medical device in its documentation function.

## The open-source + thin-micro-CRO thesis

> [!interpretive] OSSICRO position
> This is the central architectural bet, and it is interpretive.

The CRO industry's margin sits in labor: roughly **90–95% of a CRO's direct cost is labor**, gross margins run **~40–50%**, and CRO work decomposes into about eight functional streams (start-up/site activation, regulatory submissions support, clinical monitoring/CRA, project management, pharmacovigilance, data management, biostatistics, medical writing). Most of that labor is *coordination* — assembling, checking, routing, timing, and version-controlling documents — which is exactly the automatable surface. OSSICRO's thesis is a clean cut through that surface:

1. **Everything automatable and non-accountable is open-source software** that a physician can operate: the [[generate-check-validate-engine|engine]], the [[document-catalog|template library]], the [[patient-trial-matching|matching layer]], and the [[architecture|frontend]]. Open source is a deliberate choice — the mission is access, and the code that removes the barrier should not itself be a barrier.
2. **Everything that legally requires an accountable entity is a thin, human-staffed [[micro-cro-accountable-layer|micro-CRO]]** — a real, named legal person that can hold transferred sponsor obligations via a [[transfer-of-regulatory-obligations-toro|TORO]] instrument under [312.52](https://www.law.cornell.edu/cfr/text/21/312.52) when the sponsor-investigator cannot. Its service tiers run from free automated triage to paid human review at accountable gates, following the [MICHR](https://michr.umich.edu/) tiered-service precedent.

The result: OSSICRO automates the margin-generating coordination labor and retains only the irreducible accountable core in a lawful entity. It never claims software as the transferee — the boundary that killed the pure-coordination-software companies (see [[failed-disintermediation-case-studies]]).

## The HARD LINE

The whole system is governed by one non-negotiable rule:

> [!warning] Non-delegable
> OSSICRO drafts, checks, routes, times, and version-controls. It **never owns non-delegable human judgment.** The reserved acts — informed consent ([21 CFR 50.25/50.27](https://www.law.cornell.edu/cfr/text/21/50.25)), IRB review and approval ([21 CFR 56.109–56.111](https://www.law.cornell.edu/cfr/text/21/56.111)), SAE causality/expectedness determination triggering an IND safety report ([21 CFR 312.32](https://www.law.cornell.edu/cfr/text/21/312.32)), statistical sign-off ([ICH E9](https://www.ich.org/page/efficacy-guidelines)), the drug-supply decision by the manufacturer ([FDCA §561A](https://uscode.house.gov/)), and the 1571/1572 legal attestations ([312.23(a)(1)](https://www.law.cornell.edu/cfr/text/21/312.23), [312.53(c)](https://www.law.cornell.edu/cfr/text/21/312.53)) — each stays with a qualified human or accountable entity. OSSICRO produces a DRAFT and a gate; a human owns and signs.

Operationally, the HARD LINE is enforced in code by the [[generate-check-validate-engine|three-pass engine]]: every rule that touches an accountable act **fails to a human gate** rather than proceeding. The master matrix of gates is [[non-delegable-functions-and-gates]], and each generated artifact carries a citation-to-authority manifest ([[compliance-mapping]]) so a reviewer can trace every span to the requirement it satisfies. AI authorship is recorded in the [Part 11](https://www.law.cornell.edu/cfr/text/21/part-11) audit trail (attribution, model/version, input hash, human reviewer, timestamp); see [[part-11-and-ai-credibility]].

This wiki (Phase 0 of the roadmap; see [[roadmap]]) is the compliance-mapping spine everything else validates against. Nothing OSSICRO generates is trusted because the software produced it; it is trusted because it is complete, internally consistent, cited to authority, and signed by an accountable human.

## Related

- [[legal-thesis-3123-vs-31252]]
- [[the-three-pathways-triage]]
- [[guiding-scenario]]
- [[micro-cro-accountable-layer]]
- [[generate-check-validate-engine]]
- [[non-delegable-functions-and-gates]]
- [[failed-disintermediation-case-studies]]
- [[confirmed-vs-interpretive]]

## Sources

- [21 CFR 312.3 — Definitions](https://www.law.cornell.edu/cfr/text/21/312.3)
- [21 CFR 312.52 — Transfer of obligations to a CRO](https://www.law.cornell.edu/cfr/text/21/312.52)
- [21 CFR Part 11 — Electronic Records; Electronic Signatures](https://www.law.cornell.edu/cfr/text/21/part-11)
- [FDA — E6(R3) Good Clinical Practice guidance (PDF)](https://www.fda.gov/media/169090/download)
- [FDA — Overview of Sponsor-Investigator Roles and Responsibilities](https://www.fda.gov/media/174660/download)
- [Kim ES et al., 2014 — investigator-sponsor regulatory burden (PMID 24455986)](https://pubmed.ncbi.nlm.nih.gov/24455986/)
- [Healthcare IB Guide — The CRO Business Model (margins, FSO vs FSP)](https://ibinterviewquestions.com/guides/healthcare-investment-banking/cro-business-model)
