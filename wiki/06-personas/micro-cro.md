---
title: "Persona: The Micro-CRO Entity"
section: "06-personas"
status: mixed
governing_authority:
  - "21 CFR 312.52 (transfer of obligations to a CRO)"
  - "21 CFR 312.50–312.59 (the transferable obligation set); 312.58 (inspection)"
  - "ICH E6(R3) (sponsor oversight of service providers)"
  - "21 CFR Part 11 (electronic records/signatures)"
tags: [role/cro, ossicro/micro-cro, cfr/312, cfr/11, entity/micro-cro, status/mixed]
aliases: ["Micro-CRO Persona", "Accountable Entity"]
updated: 2026-07-09
---

# Persona: The Micro-CRO Entity

> [!authority] Governing authority
> [21 CFR 312.52](https://www.law.cornell.edu/cfr/text/21/312.52) (transfer of obligations to a contract research organization); the transferable obligation set at [21 CFR 312.50–312.59](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-D) and [312.32–312.33](https://www.law.cornell.edu/cfr/text/21/312.32); [312.58](https://www.law.cornell.edu/cfr/text/21/312.58) (FDA inspection); ICH E6(R3) service-provider oversight; [21 CFR Part 11](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11). Status: **Mixed** — the transfer mechanics are confirmed; the thin-entity operating model and service tiers are OSSICRO **interpretive** design.

The Micro-CRO is OSSICRO's answer to the load-bearing legal fact of this entire project: sponsor obligations transfer **only to a legally accountable entity** — never to software. When a [[sponsor-investigator]] cannot personally hold a sponsor function, a named, human-staffed, FDA-inspectable entity holds it. The Micro-CRO is deliberately *thin*: it holds exactly the functions that legally require an entity, and nothing the software layer or the physician can lawfully carry.

## Legal basis — 21 CFR 312.52

Three confirmed rules define the persona:

1. **Written transfer, obligation by obligation.** A sponsor may transfer any or all obligations to a CRO, but the transfer must be **described in writing**. A partial transfer must describe **each specific obligation** assumed; only a total transfer may use a general statement ([312.52(a)](https://www.law.cornell.edu/cfr/text/21/312.52)). The written instrument is the [[transfer-of-regulatory-obligations-toro|TORO]].
2. **Silence means retained.** Any obligation **not described in the writing is deemed not transferred** — it stays with the sponsor. There is no implied assumption.
3. **Assumption means enforcement parity.** A CRO that assumes an obligation must comply with the applicable regulations and is **"subject to the same regulatory action as a sponsor"** ([312.52(b)](https://www.law.cornell.edu/cfr/text/21/312.52)) — including FDA inspection of its records ([312.58](https://www.law.cornell.edu/cfr/text/21/312.58)) and enforcement exposure. This is why the transferee must be a legal person or entity: software cannot be inspected, warned, or enjoined. See [[legal-thesis-3123-vs-31252]] and [[cro]].

Even after a valid transfer, ICH E6(R3) keeps the sponsor accountable for **documented oversight of service providers** — delegation never transfers ultimate accountability for trial quality and participant safety. In the OSSICRO model this cuts both ways: the sponsor-investigator oversees the Micro-CRO, and the Micro-CRO maintains oversight evidence for everything it assumed.

## What the Micro-CRO can hold

Obligations from the sponsor set that a TORO may enumerate, each traceable to its CFR anchor:

| Assumable obligation | Authority |
|---|---|
| Monitoring the investigation; selecting qualified monitors | [21 CFR 312.56(a)](https://www.law.cornell.edu/cfr/text/21/312.56), [312.53(d)](https://www.law.cornell.edu/cfr/text/21/312.53); [[monitoring-plan]] |
| Safety-information intake, processing, and report preparation/submission operations | [21 CFR 312.32](https://www.law.cornell.edu/cfr/text/21/312.32); [[pharmacovigilance-safety]] |
| IND annual-report preparation and maintenance operations | [21 CFR 312.33](https://www.law.cornell.edu/cfr/text/21/312.33) |
| Sponsor recordkeeping and retention (drug disposition, financial interests) | [21 CFR 312.57](https://www.law.cornell.edu/cfr/text/21/312.57) |
| Drug shipment control, return, and disposition tracking | [21 CFR 312.53(b)](https://www.law.cornell.edu/cfr/text/21/312.53), [312.59](https://www.law.cornell.edu/cfr/text/21/312.59); [[drug-accountability-log]] |
| Collection of 1572s, CVs, and financial-disclosure information from investigators | [21 CFR 312.53(c)](https://www.law.cornell.edu/cfr/text/21/312.53); [Part 54](https://www.law.cornell.edu/cfr/text/21/part-54) |
| Regulatory-submission assembly and filing operations | [21 CFR 312.23](https://www.law.cornell.edu/cfr/text/21/312.23), [312.30–312.31](https://www.law.cornell.edu/cfr/text/21/312.30) |

If a TORO transfers an obligation whose discharge requires professional judgment (e.g., safety reporting under 312.32), the Micro-CRO must staff that judgment with a **qualified human** — a physician [[medical-monitor]] for causality/expectedness, a qualified [[clinical-monitor-cra|monitor]] for monitoring judgment. Assumption of an obligation is never a license to automate its judgment core.

> [!interpretive] OSSICRO position
> By design, OSSICRO's base service tiers do **not** assume causality/expectedness determination or medical-monitor functions; those stay with the sponsor-investigator (or a qualified physician they engage) unless a Tier-3 TORO explicitly enumerates them **and** the Micro-CRO has a qualified medical monitor on staff for that study. The legally permissible scope is wider than the scope OSSICRO chooses to operate.

## What it can never hold

> [!warning] Non-delegable
> **Investigator obligations are not transferable at all.** 312.52 is a mechanism for *sponsor* obligations; the investigator duties (21 CFR 312.60–312.69) attach to the individual who signed the [[form-fda-1572-statement-of-investigator|1572]] and cannot be assumed by any CRO, micro or otherwise. The Micro-CRO likewise never conducts the [[informed-consent-document-vs-event|consent event]], never renders the [[irb-iec|IRB]] judgment, never signs another person's [[form-fda-1571-ind-cover|1571]]/1572 attestations, and never makes the medical decision to treat. And the software layer is never the transferee — the Micro-CRO is a **legal entity with named humans**, which is the entire point ([[non-delegable-functions-and-gates]]).

## The entity's own obligations: quality system and SOPs

Because 312.52(b) puts the Micro-CRO in the sponsor's enforcement shoes for whatever it assumes, it must run like a real (if small) CRO:

- **SOP set** (minimum): document control and versioning; TORO intake, scoping, and change control; safety-information intake and escalation with [[safety-clock-engine|7/15-day clock]] discipline; monitoring and visit reporting; deviation/CAPA; training and qualification records for every staffed role; vendor/technology oversight; record retention ([312.57(c)](https://www.law.cornell.edu/cfr/text/21/312.57): 2 years post-approval or post-discontinuation notice); computerized-system validation and e-signature control under [21 CFR Part 11](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11) ([[part-11-and-ai-credibility]]).
- **Inspection readiness**: BIMO-inspectable records ([[fda-as-counterparty]]); an audit trail meeting ALCOA++ expectations (E6(R3) data governance; [[data-model]]).
- **Insurance and contracts**: professional liability appropriate to assumed obligations; clear indemnification in each TORO and any [[clinical-trial-agreement-and-budget|CTA]] it touches.
- **EU/ICH analogues** where applicable: named accountable humans (QPPV, QP for IMP release) cannot be absorbed into the entity abstractly — see [[qualified-person-qppv-eu]].

## Service tiers

The operating model (detail at [[micro-cro-operating-model]]; institutional precedents: [Harvard Catalyst's consult network](https://catalyst.harvard.edu/), Duke/ReGARDD shared services, [MICHR](https://michr.umich.edu/)'s free-triage → paid-escalation model):

| Tier | Service | Accountability held |
|---|---|---|
| 0 | Open-source self-serve (software only) | None — the physician holds everything |
| 1 | Automated triage and document generation | None — drafts for the physician's review |
| 2 | Paid qualified-human review at accountable gates | Professional work product; obligations remain the sponsor-investigator's |
| 3 | Formal assumption of **enumerated** sponsor obligations via TORO | The enumerated obligations, with 312.52(b) enforcement parity |

Only Tier 3 crosses the accountability line, and only in writing, obligation by obligation. The [[verifiable-site-qualification-dossier]] is the Micro-CRO's durable asset: a citation-complete, cryptographically verifiable qualification manifest that pharma can audit — the trust product a thin entity can credibly sell (see [[pharma]]).

## Related

- [[micro-cro-accountable-layer]]
- [[micro-cro-operating-model]]
- [[transfer-of-regulatory-obligations-toro]]
- [[cro]]
- [[sponsor]]
- [[sponsor-investigator]]
- [[legal-thesis-3123-vs-31252]]
- [[non-delegable-functions-and-gates]]
- [[verifiable-site-qualification-dossier]]
- [[part-11-and-ai-credibility]]
- [[qualified-person-qppv-eu]]
- [[perspective-matrix]]

## Sources

- [21 CFR 312.52 — Transfer of obligations to a contract research organization](https://www.law.cornell.edu/cfr/text/21/312.52)
- [21 CFR Part 312 Subpart D — Responsibilities of Sponsors and Investigators](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-D)
- [21 CFR 312.58 — Inspection of sponsor's records and reports](https://www.law.cornell.edu/cfr/text/21/312.58)
- [21 CFR Part 11 — Electronic Records; Electronic Signatures (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)
- [ICH E6(R3) Step 4 Final Guideline (Jan 2025, PDF)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [FDA — E6(R3) Good Clinical Practice guidance page (final, Sept 2025)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e6r3-good-clinical-practice-gcp)
- [MICHR — Michigan Institute for Clinical & Health Research (tiered-service precedent)](https://michr.umich.edu/)
- [Kim et al., Clin Transl Sci 2014 — Harvard Catalyst investigator-sponsor support (PMID 24455986)](https://pubmed.ncbi.nlm.nih.gov/24455986/)
