---
title: "Personas — The Four Entry Points"
section: "06-personas"
status: mixed
governing_authority:
  - "21 CFR Parts 50, 54, 56, 312"
  - "45 CFR Part 164 (HIPAA); 45 CFR Part 46 (Common Rule)"
  - "ICH E6(R3)"
tags: [entity/patient, role/investigator, role/sponsor-investigator, role/cro, role/pharma, ossicro/micro-cro, status/mixed]
aliases: ["Personas", "Persona Index", "Entry-Point Personas"]
updated: 2026-07-09
---

# Personas — The Four Entry Points

> [!authority] Governing authority
> Each persona's obligation set rests on distinct binding authority: the **Patient** on [21 CFR Part 50](https://www.law.cornell.edu/cfr/text/21/part-50) and [45 CFR Part 164](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164); the **HCP** on [21 CFR 312.60–312.69](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-D) (plus the sponsor set, 312.50–312.59, when a [[sponsor-investigator]]); the **Micro-CRO** on [21 CFR 312.52](https://www.law.cornell.edu/cfr/text/21/312.52); **Pharma** on 21 CFR 312 Subpart D, [Part 54](https://www.law.cornell.edu/cfr/text/21/part-54), the [Anti-Kickback Statute](https://www.law.cornell.edu/uscode/text/42/1320a-7b), and [FDCA §561A](https://www.law.cornell.edu/uscode/text/21/360bbb-0a). Status: **Mixed** — the per-actor obligation sets are confirmed black-letter law; the four-entry-point model and the single coordination spine are OSSICRO **interpretive** design.

This section holds one page per actor who enters OSSICRO, plus the cross-actor matrix. The canonical statement of the model itself is [[four-entry-points]] (overview section); these pages carry the depth: for each actor, the full perspective, need set, document set, regulatory obligation set, and non-delegable floor.

## The model in one paragraph

Four actors enter OSSICRO — **Patient**, **HCP/physician**, **Micro-CRO**, and **Pharma** — each through a different door, each seeing a different slice of the same trial. A patient asks "is there a trial or therapy for me?"; a physician asks "my patient needs this — make me an accepted site without a research office"; the Micro-CRO exists to hold the accountable functions that legally require an entity ([21 CFR 312.52(b)](https://www.law.cornell.edu/cfr/text/21/312.52)); pharma asks "can I trust and accept this small, new, or single-patient site with product, data, and money?" All four journeys resolve onto **one coordination spine**: the same document graph, obligation graph, and gate structure, viewed from four vantage points. The frontend gives each actor a portal perspective; the regulatory substance is identical.

## Section contents

| Page | Actor | Core question |
|---|---|---|
| [[patient]] | Patient / research participant | "Is there something for me, and what protects me?" — [21 CFR Part 50](https://www.law.cornell.edu/cfr/text/21/part-50), HIPAA |
| [[hcp-physician]] | Enrolling HCP / physician | "Make me an accepted site" — the burden removed vs. the duties kept |
| [[micro-cro]] | The OSSICRO Micro-CRO entity | "Hold what needs a legally-accountable entity" — [21 CFR 312.52](https://www.law.cornell.edu/cfr/text/21/312.52), TORO, SOPs, tiers |
| [[pharma]] | Pharma sponsor / supplier | "What makes a small or single-patient site acceptable?" |
| [[perspective-matrix]] | All four | Goals / needs / documents / obligations / hand-offs, side by side |

## How origins converge

> [!interpretive] OSSICRO position
> Whichever actor enters first, the request resolves onto the same spine. This is the design thesis, not a regulatory requirement.

- **Patient-origin:** Patient → [[patient-trial-matching|matching]] (de-identified, preparatory-to-research under [45 CFR 164.512(i)(1)(ii)](https://www.ecfr.gov/current/title-45/section-164.512)) → the candidate list goes to the patient's HCP, who owns every downstream medical and regulatory judgment.
- **HCP-origin:** the [[guiding-scenario]] — the physician enters at [[the-three-pathways-triage|triage]] and OSSICRO assembles the pathway-appropriate document set.
- **Pharma-origin:** a sponsor seeking sites, an [[iis-request-workflow|IIS]] call, or an [[expanded-access-workflow|expanded-access]] intake enters at the [[pharma-partner-interface-iis|pharma interface]] and pulls HCPs in.
- **Micro-CRO:** always the escalation layer, never the front door. It is engaged when an accountable function legally requires an entity the physician cannot personally supply ([[micro-cro-accountable-layer]]).

Inter-actor traffic — messages, document exchange, status, and routing to IRB/DSMB/FDA — runs through the [[communication-hub]], role-scoped and audit-logged, respecting HIPAA and the Medical-Affairs/Clinical-Development firewall.

## The cross-actor matrix

[[perspective-matrix]] maintains the working matrix: for each actor, **goals, needs, key documents, regulatory obligations, non-delegable floor, and the hand-offs** between actors (who passes what artifact to whom, under what authority, at which lifecycle moment). Use it as the fast lookup; use the per-actor pages for the cited detail.

> [!warning] Non-delegable
> Across every persona, the same floor holds: OSSICRO drafts **complete documentation for qualified human review**. It never conducts the [[informed-consent-document-vs-event|consent event]], never renders the [[irb-iec|IRB]] judgment, never makes the [[medical-monitor|causality/expectedness]] call, never signs the [[form-fda-1571-ind-cover|1571]]/[[form-fda-1572-statement-of-investigator|1572]] attestations, and never substitutes for [[dsmb-dmc|DSMB]] oversight or any medical decision. The master gating matrix is [[non-delegable-functions-and-gates]].

## Reading order

A first-time clinician should read [[hcp-physician]] → [[the-three-pathways-triage]] → [[patient]]. A pharma reviewer evaluating OSSICRO-supported sites should read [[pharma]] → [[verifiable-site-qualification-dossier]] → [[micro-cro]]. A regulatory reviewer auditing the accountability model should read [[micro-cro]] → [[transfer-of-regulatory-obligations-toro]] → [[non-delegable-functions-and-gates]].

## Related

- [[four-entry-points]]
- [[patient]]
- [[hcp-physician]]
- [[micro-cro]]
- [[pharma]]
- [[perspective-matrix]]
- [[the-three-pathways-triage]]
- [[non-delegable-functions-and-gates]]
- [[communication-hub]]

## Sources

- [21 CFR Part 312 — Investigational New Drug Application (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312)
- [21 CFR Part 50 — Protection of Human Subjects](https://www.law.cornell.edu/cfr/text/21/part-50)
- [21 CFR 312.52 — Transfer of obligations to a contract research organization](https://www.law.cornell.edu/cfr/text/21/312.52)
- [45 CFR 164.512 — HIPAA uses and disclosures for which authorization is not required](https://www.ecfr.gov/current/title-45/section-164.512)
- [ICH E6(R3) Good Clinical Practice — FDA guidance page (final, Sept 2025)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e6r3-good-clinical-practice-gcp)
