---
title: "Four Entry Points — Patient, HCP, Micro-CRO, Pharma"
section: "00-overview"
status: mixed
governing_authority:
  - "21 CFR 312.3(b); 312.52; 312.53"
  - "21 CFR 50 (informed consent); 45 CFR 164 (HIPAA)"
  - "21 CFR 54 (financial disclosure); 42 USC 1320a-7b (AKS)"
tags: [ossicro/matching, role/investigator, role/sponsor-investigator, role/cro, role/pharma, status/mixed]
aliases: ["Four Entry Points", "Entry Points", "Personas Overview"]
updated: 2026-07-09
---

# Four Entry Points — Patient, HCP, Micro-CRO, Pharma

> [!authority] Governing authority
> Each actor's obligations rest on distinct authority: the **Patient** on [21 CFR 50](https://www.law.cornell.edu/cfr/text/21/part-50) (consent) and [45 CFR 164](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164) (HIPAA); the **HCP** on [21 CFR 312.60–312.69](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-D) (and the full sponsor set if a [[sponsor-investigator]]); the **Micro-CRO** on [21 CFR 312.52](https://www.law.cornell.edu/cfr/text/21/312.52) (accountable transferee); the **Pharma** partner on [21 CFR 312.50–312.59](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-D), [Part 54](https://www.law.cornell.edu/cfr/text/21/part-54), and the [Anti-Kickback Statute](https://www.law.cornell.edu/uscode/text/42/1320a-7b). Status: **Mixed** — the obligation sets are confirmed; the four-entry-point model and the coordination spine are OSSICRO **interpretive** design.

OSSICRO is entered by four actors. Each has a distinct perspective, need set, document set, and regulatory obligation set — and all four resolve onto **one coordination spine**. This page is the map; each actor has a full page under [[06-personas/index|06-personas/]].

## The four actors

### 1. Patient

**Perspective:** "Is there a trial or therapy for me, and can my doctor get me in?" The patient owns nothing regulated but is the **protected subject** — the person the entire apparatus exists to keep safe.

- **Needs:** access to an investigational therapy; a clinician willing and able to enroll them; a consent process they understand; privacy.
- **Documents they see/sign:** the [[informed-consent-form|informed-consent form]] (they sign; the [[informed-consent-document-vs-event|event]] is a conversation, not a signature), HIPAA authorization.
- **Regulatory protections:** [21 CFR 50.20–50.27](https://www.law.cornell.edu/cfr/text/21/50.25) consent elements + [Common Rule](https://www.ecfr.gov/current/title-45/part-46) key-information; [HIPAA 45 CFR 164.508/164.512](https://www.ecfr.gov/current/title-45/section-164.512).
- **Entry mechanism:** [[patient-trial-matching|matching]] (de-identified, preparatory-to-research) → hands the candidate to their HCP. See [[06-personas/patient]].

> [!warning] Non-delegable
> The **informed-consent event** — the human conversation in which the patient's questions are answered and voluntariness is assured — is never software. OSSICRO drafts the document; a qualified person conducts the consent ([[informed-consent-document-vs-event]]).

### 2. HCP / Physician

**Perspective:** "My patient needs this; make me an accepted site without a research office." The enrolling clinician is the load-bearing human — the [[investigator]] (Mode A) or [[sponsor-investigator]] (Mode B).

- **Needs:** to know *which pathway* ([[the-three-pathways-triage]]), a complete and correct document set, and to be trusted by a pharma sponsor despite having no track record.
- **Documents they own/sign:** [[form-fda-1572-statement-of-investigator|Form 1572]], [[form-fda-3454-3455-financial-disclosure|financial disclosure]], CV/license, [[delegation-of-authority-log|delegation log]]; in Mode B, also [[form-fda-1571-ind-cover|Form 1571]] and the full [[ind-application-312-23|IND package]].
- **Regulatory obligations:** investigator set ([312.60–312.69](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-D)); in Mode B, the sponsor set too.
- **Entry mechanism:** the [[guiding-scenario|guiding scenario]] is written from the HCP's chair. See [[06-personas/hcp-physician]].

> [!warning] Non-delegable
> The **1571/1572 signatures**, **PI qualification attestation**, **eligibility determination**, **consent**, and **SAE reporting** stay with the HCP. OSSICRO removes the document burden, not the accountability.

### 3. Micro-CRO

**Perspective:** the escalation layer — "when the physician cannot personally hold an accountable function that legally requires an entity, a real entity holds it."

- **What it is:** OSSICRO's thin, named, legally-accountable [[cro|CRO]] entity ([[micro-cro-accountable-layer]]) that can assume enumerated sponsor obligations via a [[transfer-of-regulatory-obligations-toro|TORO]] ([312.52](https://www.law.cornell.edu/cfr/text/21/312.52)) — and thereby becomes "subject to the same regulatory action as a sponsor" ([312.52(b)](https://www.law.cornell.edu/cfr/text/21/312.52)).
- **Needs:** its own quality system, SOPs, trained qualified staff, and a defensible scope of assumed obligations.
- **Regulatory obligations:** exactly and only the obligations enumerated in each TORO; undocumented obligations remain with the sponsor.
- **Service tiers:** (0) open-source self-serve → (1) automated triage/generation → (2) paid human review at accountable gates → (3) full assumption of enumerated obligations. Precedent: [MICHR](https://michr.umich.edu/) tiered service. See [[06-personas/micro-cro]] and [[micro-cro-operating-model]].

> [!warning] Non-delegable
> The Micro-CRO is a **legal entity, not software** — that is the whole point. It never assumes **investigator conduct** obligations (non-transferable), never owns **consent, IRB judgment, or causality**. It holds only what an entity must hold and a human staffs it.

### 4. Pharma

**Perspective:** "Can I trust and accept this small / new / single-patient site with product, data, and money?" The [[pharma-partner-sponsor|pharma company]] is the sponsor/supplier of the investigational product — never OSSICRO's transferee.

- **Needs:** a legally-accountable, GCP-qualified investigator/site; verifiable financial disclosure; FMV-set, AKS-defensible compensation; Sunshine-Act reportability. Pharma's trust gate is **entity-shaped, not software-shaped**.
- **Channels it offers:** (1) enroll a patient as a site on its protocol; (2) an [[iis-request-workflow|IIS/IST]] program (drug + support to a sponsor-investigator, via Medical Affairs); (3) [[expanded-access-workflow|expanded access]]; (4) medical-affairs scientific exchange (walled off from commercial promotion).
- **Regulatory obligations:** sponsor set when it is the sponsor ([312.50–312.59](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-D)); the **Medical Affairs / Clinical Development firewall** must hold.
- **Entry mechanism:** IIS portal, expanded-access intake, or protocol site-add. See [[06-personas/pharma]] and [[pharma-partner-interface-iis]].

> [!warning] Non-delegable
> The **manufacturer's decision to supply** product ([[expanded-access-coordination]]) and the **Medical-Affairs/Clinical-Development firewall** are pharma's to hold. OSSICRO produces the dossier that lets pharma say yes; it cannot make pharma say yes.

## How the journeys interlock

> [!interpretive] OSSICRO position
> The single coordination spine is the design thesis: whichever actor enters first, the request resolves onto the same document/obligation graph.

A **patient-origin** request flows Patient → matching → HCP, who triages to a pathway and (if needed) escalates accountable functions to the Micro-CRO, while Pharma supplies product and accepts the site. An **HCP-origin** request starts at triage. A **pharma-origin** request (a sponsor seeking sites, or an IIS call) enters at the pharma interface and pulls HCPs in. The Micro-CRO is always the escalation layer, never the front door. The [[communication-hub|communication hub]] carries role-scoped, auditable messaging among all four (routing to IRB/DSMB/FDA), respecting HIPAA and the Medical-Affairs firewall.

The cross-actor goals/needs/documents/obligations/hand-offs matrix is maintained at [[06-personas/perspective-matrix]].

## The four-actor summary

| Actor | Core question | Owns (regulated) | Key documents | Non-delegable |
|---|---|---|---|---|
| **Patient** | "Is there something for me?" | Nothing — is the protected subject | Consent form, HIPAA auth | The consent *event* |
| **HCP** | "Make me an accepted site" | Investigator (± sponsor) set | 1572, 1571, IND package | Signatures, eligibility, consent, SAE |
| **Micro-CRO** | "Hold what needs an entity" | Enumerated TORO obligations | TORO, SOPs, QA records | Investigator conduct; consent/IRB/causality |
| **Pharma** | "Can I trust this site?" | Sponsor set (when sponsor) | Protocol, IB, drug supply, safety-exchange | Supply decision; MA/CD firewall |

## Related

- [[06-personas/index]]
- [[06-personas/patient]]
- [[06-personas/hcp-physician]]
- [[06-personas/micro-cro]]
- [[06-personas/pharma]]
- [[06-personas/perspective-matrix]]
- [[the-three-pathways-triage]]
- [[guiding-scenario]]
- [[communication-hub]]

## Sources

- [21 CFR 312.52 — Transfer of obligations to a CRO](https://www.law.cornell.edu/cfr/text/21/312.52)
- [21 CFR Part 312 Subpart D — Sponsor & investigator obligations](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-D)
- [21 CFR 50.25 — Elements of informed consent](https://www.law.cornell.edu/cfr/text/21/50.25)
- [45 CFR 164.512 — HIPAA uses/disclosures without authorization](https://www.ecfr.gov/current/title-45/section-164.512)
- [42 USC 1320a-7b — Anti-Kickback Statute](https://www.law.cornell.edu/uscode/text/42/1320a-7b)
- [FDA — Overview of Sponsor-Investigator Roles and Responsibilities](https://www.fda.gov/media/174660/download)
- [Genentech — Investigator Initiated Studies (IIS program model)](https://www.gene.com/medical-professionals/investigator-initiated-studies)
- [Health Affairs — The Physician Payments Sunshine Act](https://www.healthaffairs.org/content/briefs/physician-payments-sunshine-act)
