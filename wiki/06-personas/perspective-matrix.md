---
title: "Perspective Matrix — Goals, Needs, Documents, Obligations, Hand-offs"
section: "06-personas"
status: mixed
governing_authority:
  - "21 CFR Parts 50, 54, 56, 312"
  - "45 CFR Part 164 (HIPAA)"
  - "42 USC 1320a-7b (AKS); FDCA §561A"
tags: [entity/patient, role/investigator, role/sponsor-investigator, role/cro, role/pharma, ossicro/micro-cro, status/mixed]
aliases: ["Perspective Matrix", "Cross-Actor Matrix"]
updated: 2026-07-09
---

# Perspective Matrix — Goals, Needs, Documents, Obligations, Hand-offs

> [!authority] Governing authority
> Composite. Each cell traces to the authority cited on its actor page: [[patient]] ([21 CFR Part 50](https://www.law.cornell.edu/cfr/text/21/part-50), [45 CFR 164](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164)); [[hcp-physician]] ([21 CFR 312.60–312.69](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-D), 312.3(b)); [[micro-cro]] ([21 CFR 312.52](https://www.law.cornell.edu/cfr/text/21/312.52)); [[pharma]] (21 CFR 312 Subpart D, [Part 54](https://www.law.cornell.edu/cfr/text/21/part-54), [AKS](https://www.law.cornell.edu/uscode/text/42/1320a-7b)). Status: **Mixed** — obligations confirmed; the matrix framing and hand-off routing are OSSICRO **interpretive** design.

This page is the fast lookup across all four entry points: what each actor wants, what each needs, what each signs or owns, what the law requires of each, and how work passes between them. For cited depth, use the per-actor pages; for the model itself, [[four-entry-points]].

## Master matrix

| | **Patient** | **HCP / Physician** | **Micro-CRO** | **Pharma** |
|---|---|---|---|---|
| **Goal** | Access to an investigational therapy, safely and privately | Enroll their patient; become an accepted site (or sponsor-investigator) without a research office | Hold — cleanly and only — the accountable functions that legally require an entity | Advance its asset; supply product only where a legally accountable, GCP-qualified counterparty exists |
| **Core needs** | A match; an understandable [[informed-consent-document-vs-event\|consent process]]; privacy; the right to withdraw | Pathway [[the-three-pathways-triage\|triage]]; complete document sets; deadline machinery; pharma trust despite no track record | Its own quality system/SOPs; qualified staff; a defensible, enumerated TORO scope; inspection readiness | Verifiable site qualification; enrollment realism; FMV/AKS-clean money; safety-data flow; the MA/CD firewall intact |
| **Key documents (sees / signs / owns)** | Signs: [[informed-consent-form\|ICF]], HIPAA authorization ([45 CFR 164.508](https://www.ecfr.gov/current/title-45/section-164.508)); child assent where applicable | Signs/owns: [[form-fda-1572-statement-of-investigator\|1572]], [[form-fda-3454-3455-financial-disclosure\|3454/3455]], CV/license, [[delegation-of-authority-log\|delegation log]]; Mode B adds [[form-fda-1571-ind-cover\|1571]] + [[ind-application-312-23\|IND package]], [[ind-safety-report\|safety reports]], [[ind-annual-report-dsur\|annual report]] | Owns: [[transfer-of-regulatory-obligations-toro\|TORO]] instruments, SOPs, training/QA records, monitoring reports for assumed functions | Owns: protocol, [[investigators-brochure\|IB]], drug supply + labeling, [[clinical-trial-agreement-and-budget\|CTA/budget]], letter of authorization (expanded access), safety-data exchange agreement |
| **Regulatory obligations** | None owed — is the *protected* party (21 CFR 50/56; HIPAA) | Investigator set ([312.60–312.69](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-D)); + full sponsor set in Mode B ([312.50–312.59](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-D), [312.32](https://www.law.cornell.edu/cfr/text/21/312.32)–[312.33](https://www.law.cornell.edu/cfr/text/21/312.33)) | Exactly the obligations enumerated in each TORO — with 312.52(b) enforcement parity; silence = retained by sponsor | Sponsor set when sponsor (Mode A); Part 54 collection; AKS/Sunshine on all money; [§561A](https://www.law.cornell.edu/uscode/text/21/360bbb-0a) expanded-access policy |
| **Non-delegable floor** | Their own voluntary agreement — no one consents for a competent adult | 1571/1572 signatures; personal supervision; eligibility; consent; immediate SAE reporting ([312.64(b)](https://www.law.cornell.edu/cfr/text/21/312.64)); Mode B causality + IND accountability | Being a real entity with named humans; never investigator conduct, consent, IRB judgment, or another's signatures | The decision to supply product; the MA/CD firewall; sponsor accountability that survives all delegation (E6(R3) oversight) |
| **Entry mechanism** | [[patient-trial-matching\|Matching]] (preparatory-to-research; no PHI egress) → their HCP | [[guiding-scenario]] → triage → mode-appropriate document engine | Escalation only — Tier 2 human review or Tier 3 TORO; never the front door | [[pharma-partner-interface-iis\|IIS portal]], expanded-access intake, or protocol site-add |

## Hand-offs between actors

Each row is a transfer of an artifact or duty from one actor to another, with the authority that governs it. This is the coordination spine rendered as a table; the full arrow diagram is [[inter-entity-document-flow-map]].

| # | From → To | Artifact / act | Governing authority | Gate |
|---|---|---|---|---|
| 1 | Patient → HCP | Clinical picture; the request for options | Treatment relationship; [45 CFR 164.512(i)(1)(ii)](https://www.ecfr.gov/current/title-45/section-164.512) preparatory review | No PHI egress ([[privacy-state-machine]]) |
| 2 | HCP → Patient | Candidate options; the **consent conversation**; signed ICF copy | 21 CFR [50.25](https://www.law.cornell.edu/cfr/text/21/50.25)/[50.27](https://www.law.cornell.edu/cfr/text/21/50.27) | Consent event — human only |
| 3 | HCP → IRB | [[irb-submission-package\|Submission package]] (protocol, ICF, IB, qualifications) | [21 CFR Part 56](https://www.law.cornell.edu/cfr/text/21/part-56); [56.111](https://www.law.cornell.edu/cfr/text/21/56.111) criteria | IRB approval judgment — board only; enrollment gated on it |
| 4 | HCP → Pharma | Feasibility responses; signed 1572; [[verifiable-site-qualification-dossier\|qualification dossier]]; financial disclosure | [312.53(c)](https://www.law.cornell.edu/cfr/text/21/312.53); [Part 54](https://www.law.cornell.edu/cfr/text/21/part-54) | Pharma acceptance — counterparty judgment |
| 5 | Pharma → HCP | Protocol, [[investigators-brochure\|IB]] ([312.55(a)](https://www.law.cornell.edu/cfr/text/21/312.55)), drug shipment ([312.53(b)](https://www.law.cornell.edu/cfr/text/21/312.53)), CTA, ongoing safety updates ([312.55(b)](https://www.law.cornell.edu/cfr/text/21/312.55)); LOA for expanded access | 21 CFR 312 Subpart D; [Subpart I](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-I) | Supply decision — pharma only; drug ships only after 1572 + activation |
| 6 | HCP (S-I) → Micro-CRO | Enumerated sponsor obligations via [[transfer-of-regulatory-obligations-toro\|TORO]] | [21 CFR 312.52(a)](https://www.law.cornell.edu/cfr/text/21/312.52) | Written, obligation-by-obligation; undescribed = retained |
| 7 | Micro-CRO → FDA | Discharge of assumed obligations (e.g., monitoring records, report submission operations) | [312.52(b)](https://www.law.cornell.edu/cfr/text/21/312.52) enforcement parity; [312.58](https://www.law.cornell.edu/cfr/text/21/312.58) inspection | Qualified human performs any judgment core |
| 8 | HCP (S-I) → FDA | IND ([[form-fda-1571-ind-cover\|1571]] + [312.23](https://www.law.cornell.edu/cfr/text/21/312.23) package); [[ind-safety-report\|7/15-day safety reports]]; [[ind-annual-report-dsur\|annual report]] | [312.20–312.23](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-B), [312.32](https://www.law.cornell.edu/cfr/text/21/312.32), [312.33](https://www.law.cornell.edu/cfr/text/21/312.33) | Submission is an explicit human-authorized act; 30-day clock ([[ind-submission-and-30-day-clock]]) |
| 9 | Patient → HCP → Sponsor → FDA/IRB/DSMB | AE → **immediate** SAE report with causality → expedited IND safety report + IRB/DSMB notification | [312.64(b)](https://www.law.cornell.edu/cfr/text/21/312.64) → [312.32(c)](https://www.law.cornell.edu/cfr/text/21/312.32) → [312.66](https://www.law.cornell.edu/cfr/text/21/312.66) | Causality/expectedness — qualified physician only ([[medical-monitor]]); clocks computed by [[safety-clock-engine]], never auto-filed |
| 10 | Pharma ↔ HCP (S-I) | Safety-data exchange (ICSRs both directions, per agreement) | [312.32](https://www.law.cornell.edu/cfr/text/21/312.32); contractual ([[safety-management-plan]]) | Reconciliation is a tracked obligation |
| 11 | Pharma → HCP | IIS grant / drug support, FMV-set | [AKS](https://www.law.cornell.edu/uscode/text/42/1320a-7b) + [safe harbor](https://www.law.cornell.edu/cfr/text/42/1001.952); [Sunshine](https://www.cms.gov/priorities/key-initiatives/open-payments) reportable | Medical Affairs only — never Commercial |

## Accountability by pathway

The same four actors, but the accountable-party assignments shift with the pathway ([[the-three-pathways-triage]]):

| Pathway | Trial sponsor | IND holder | Pharma's role | Micro-CRO eligible? | Patient's status |
|---|---|---|---|---|---|
| **Mode A** — site on pharma protocol | Pharma | Pharma | Sponsor | For pharma's obligations, in principle — but pharma uses its own CROs; OSSICRO serves the site | Research subject |
| **Mode B** — IIS / sponsor-investigator | The physician ([312.3(b)](https://www.law.cornell.edu/cfr/text/21/312.3)) | The physician | Supporter/supplier only (Medical Affairs) | Yes — TORO for enumerated **sponsor** obligations | Research subject |
| **Expanded access** ([312.310](https://www.law.cornell.edu/cfr/text/21/312.310)) | Physician (as S-I on [[form-fda-3926-expanded-access\|3926]]) or manufacturer's IND via LOA | Physician or manufacturer | Must agree to supply ([§561A](https://www.law.cornell.edu/uscode/text/21/360bbb-0a)) | Limited — treatment context; consent/IRB still apply | Patient (treatment, not research) |

> [!warning] Non-delegable
> No cell in any table above moves a non-delegable act to software or to an unqualified party: the consent **event** (Patient row), the IRB **judgment** (hand-off 3), causality/expectedness (hand-off 9), the 1571/1572 **signatures** (hand-off 8), the supply **decision** (hand-off 5), and statistical sign-off ([[biostatistician]]) all terminate in a qualified human. OSSICRO drafts complete documentation for those humans; the master gate list is [[non-delegable-functions-and-gates]].

> [!interpretive] OSSICRO position
> The matrix itself — treating four legally heterogeneous actors as symmetric "entry points" on one spine — is design, not law. Its value is operational: any request, from any door, resolves to (pathway, document set, obligation set, gate set) deterministically, and every hand-off above is carried by the [[communication-hub]] with role-scoped access and an auditable log.

## Related

- [[four-entry-points]]
- [[06-personas/index]]
- [[patient]]
- [[hcp-physician]]
- [[micro-cro]]
- [[pharma]]
- [[inter-entity-document-flow-map]]
- [[the-three-pathways-triage]]
- [[non-delegable-functions-and-gates]]
- [[communication-hub]]
- [[document-catalog]]

## Sources

- [21 CFR Part 312 — Investigational New Drug Application (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312)
- [21 CFR 312.52 — Transfer of obligations to a CRO](https://www.law.cornell.edu/cfr/text/21/312.52)
- [21 CFR 312.64 — Investigator reports](https://www.law.cornell.edu/cfr/text/21/312.64)
- [21 CFR 50.25 / 50.27 — Informed consent elements and documentation](https://www.law.cornell.edu/cfr/text/21/50.25)
- [21 CFR 56.111 — Criteria for IRB approval of research](https://www.law.cornell.edu/cfr/text/21/56.111)
- [45 CFR 164.512 — HIPAA research provisions](https://www.ecfr.gov/current/title-45/section-164.512)
- [42 USC 1320a-7b — Anti-Kickback Statute](https://www.law.cornell.edu/uscode/text/42/1320a-7b)
- [21 USC 360bbb-0a (FDCA §561A) — Expanded access policy requirement](https://www.law.cornell.edu/uscode/text/21/360bbb-0a)
- [FDA — Overview of Sponsor-Investigator Roles and Responsibilities](https://www.fda.gov/media/174660/download)
