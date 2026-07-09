---
title: "Offline / Local Deployment — Single Container, No PHI Egress"
section: "05-ossicro-system"
status: mixed
governing_authority:
  - "45 CFR 164.308, 164.312 (HIPAA Security Rule — administrative and technical safeguards)"
  - "45 CFR 164.512(i), 164.502(b), (e) (Privacy Rule — research; minimum necessary; business associates)"
  - "21 CFR Part 11 (electronic records; electronic signatures)"
  - "21 CFR 312.57(c), 312.62(c) (record retention)"
  - "ICH E6(R3) (computerized systems; data governance)"
tags: [ossicro/engine, ossicro/part11, ossicro/gating, cfr/11, cfr/312, ich/e6r3, status/interpretive]
aliases: ["Local Deployment", "Offline Deployment", "Single-Container Deployment"]
updated: 2026-07-09
---

# Offline / Local Deployment — Single Container, No PHI Egress

> [!authority] Governing authority
> The HIPAA Security Rule ([45 CFR 164.308](https://www.law.cornell.edu/cfr/text/45/164.308), [164.312](https://www.law.cornell.edu/cfr/text/45/164.312)) and Privacy Rule ([164.512(i)](https://www.law.cornell.edu/cfr/text/45/164.512), [164.502](https://www.law.cornell.edu/cfr/text/45/164.502)) define what a PHI-touching deployment must safeguard; [21 CFR Part 11](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11) and ICH E6(R3)'s computerized-systems expectations define what a regulated-records deployment must validate and retain; [21 CFR 312.57(c)](https://www.law.cornell.edu/cfr/text/21/312.57)/[312.62(c)](https://www.law.cornell.edu/cfr/text/21/312.62) fix retention. Status: **Mixed** — the safeguard, validation, and retention requirements are confirmed; the single-container local architecture is the OSSICRO design position.

OSSICRO's reference deployment is a single container running inside the covered entity's own boundary — a clinic workstation, an on-premises server, or the practice's existing private infrastructure. Nothing about the design requires a data center, a vendor cloud tenancy, or a standing internet connection. Two motivations, one architecture: **privacy** (the §164.512(i)(1)(ii) preparatory-review basis requires that no PHI leave the covered entity during matching — trivial to demonstrate when the software physically runs inside it) and **adoption in low-resource settings** (the physicians OSSICRO most wants to reach — solo practices, community sites, under-resourced institutions in the US and abroad — are exactly those without an IT department to stand up a compliant SaaS relationship). The local deployment makes "no PHI egress" a network-layer property of the container instead of a clause in a vendor contract.

## Deployment model

One OCI image (Docker/Podman-compatible) containing the full stack: the matching and adjudication engines ([[matching-engine]], [[matching-eligibility-adjudication]]), the [[generate-check-validate-engine]], the template library, the [[privacy-state-machine]], the embedded database (with encryption at rest), the Part 11 audit-trail service ([[data-model]]), and a bundled copy of this wiki and the citation maps. The frontend serves locally; users authenticate against local, per-individual credentials (a Part 11 requirement — §11.100(a) signatures unique to one individual; shared logins are structurally impossible to make compliant). SMART-on-FHIR ingestion ([[smart-on-fhir-integration]]) talks to the site's EHR endpoint over the local network or the EHR vendor's API endpoint; ingested data never leaves the container's storage.

Images are versioned, signed, and content-addressed. The running image digest is part of the validated-system record: an inspector (or a sponsor auditing the site — [[verifiable-site-qualification-dossier]]) can verify exactly which build produced which records.

## No PHI egress as a code property

The container ships with a default-deny egress policy. Outbound connectivity, when present, is restricted to an explicit allowlist of public, non-PHI endpoints — ClinicalTrials.gov API v2, NCBI E-utilities/PubMed, openFDA ([[data-integrations-ctgov-pubmed]]) — and every outbound query passes a scrubbing layer that permits only de-identified parameters (condition codes, biomarker terms, age bands, geography at the region level). There is no telemetry, no usage analytics, no "phone home." In the [[privacy-state-machine]]'s `S1 PREPARATORY` state this egress policy is what mechanically discharges the §164.512(i)(1)(ii)(B) representation that no PHI is removed from the covered entity; attempted violations are refused and logged as audit-trail events.

## AI drafting under the egress constraint

The honest tension in this design: OSSICRO's drafting and QC agents ([[claude-sdk-ai-in-the-loop]]) are strongest when backed by frontier hosted models, and a hosted model call is an egress event. The deployment offers three postures, strictest first, and the operator's choice is a recorded configuration state:

1. **Fully offline.** All inference local (bundled open-weight models sized to commodity hardware). No drafting-related egress at all. Adjudication and generation quality degrade relative to frontier models; the [[completeness-ledger]] and [[single-pass-review-ux]] lanes compensate by routing more output to human review rather than by hiding the quality difference.
2. **Hybrid, de-identified.** Hosted-model calls are permitted but pass the same scrubbing layer as registry queries: prompts may carry de-identified clinical abstractions ([45 CFR 164.514(b)](https://www.law.cornell.edu/cfr/text/45/164.514) — safe-harbor stripped or expert-determined), never direct identifiers. De-identified data is not PHI, so the preparatory-state representation is preserved.
3. **BAA-backed.** Identified data may flow to a hosted model only where the model provider is engaged as a business associate under a written agreement ([45 CFR 164.502(e)](https://www.law.cornell.edu/cfr/text/45/164.502), [164.308(b)](https://www.law.cornell.edu/cfr/text/45/164.308); business associate defined at [45 CFR 160.103](https://www.law.cornell.edu/cfr/text/45/160.103)). This posture leaves the "local" architecture but not the compliance architecture; it is a covered entity's decision to make, with counsel, not an OSSICRO default.

The default is posture 2. Posture 3 is never silently enabled; switching to it is a logged administrative act.

## Offline operation

A site with intermittent or no connectivity still functions:

- **Trial registry.** The image bundles a dated ClinicalTrials.gov snapshot; matching runs against it offline, and every match rationale is stamped with the snapshot date so a stale registry is visible, not silent.
- **Templates and rules.** The template library and the CFR/ICH-traced validation rule sets are versioned into the image. Rule-set version appears in every [[completeness-ledger]].
- **Regulatory currency.** When connectivity is available, the deployment syncs registry deltas, template updates, and [[regulatory-change-log]] flags. Pages, templates, or rules affected by a flagged regulatory change are marked for the human curator; an offline site sees an explicit "last synced" banner rather than an implied currency it does not have.
- **What offline does not change.** Deadlines run on statute, not on connectivity: the [[safety-clock-engine]] computes 7-/15-day windows locally, and an unfiled IND safety report is late regardless of the site's network state. Offline mode never converts a filing obligation into a queued intention without loud escalation.

## Part 11 and validation responsibilities in a local deployment

Running the regulated-records environment on-site moves operational duties to the site that a SaaS vendor would otherwise hold. The image ships with a validation pack — intended-use specification, requirements traceability, executed test evidence per release, and an installation-qualification checklist — supporting §11.10(a) validation and E6(R3)'s computerized-systems expectations, and the deployment enforces NTP (or documented manual) time synchronization for trustworthy audit-trail timestamps (§11.10(e)). But the following remain the deploying site's, and the documentation says so explicitly:

| Site responsibility | Anchor |
|---|---|
| Backup and disaster recovery of the record store | §11.10(c); [45 CFR 164.308(a)(7)](https://www.law.cornell.edu/cfr/text/45/164.308) contingency plan |
| Record retention for the required period, across hardware and image upgrades | [21 CFR 312.57(c)](https://www.law.cornell.edu/cfr/text/21/312.57), [312.62(c)](https://www.law.cornell.edu/cfr/text/21/312.62); E6(R3) essential-records retention ([[record-retention-and-archival]]) |
| Physical and workstation security of the host | [45 CFR 164.310](https://www.law.cornell.edu/cfr/text/45/164.310) |
| Access provisioning/deprovisioning; per-individual credentials | §11.10(d), (g); §§11.100–11.300; [45 CFR 164.312(a)](https://www.law.cornell.edu/cfr/text/45/164.312) |
| The Security Rule risk analysis covering the deployment | [45 CFR 164.308(a)(1)(ii)(A)](https://www.law.cornell.edu/cfr/text/45/164.308) |
| Producing records and audit trails for FDA inspection | §11.10(b); [21 CFR 312.58](https://www.law.cornell.edu/cfr/text/21/312.58), [312.68](https://www.law.cornell.edu/cfr/text/21/312.68) |

> [!warning] Non-delegable
> Deploying OSSICRO locally transfers no compliance obligation to OSSICRO. The site remains the covered entity under HIPAA; the sponsor-investigator remains the holder of every Part 312 obligation; the records belong to, and must be retained and producible by, the regulated parties ([21 CFR 312.62](https://www.law.cornell.edu/cfr/text/21/312.62), [312.68](https://www.law.cornell.edu/cfr/text/21/312.68)). Software cannot be a business associate to itself, a transferee of sponsor obligations ([21 CFR 312.52](https://www.law.cornell.edu/cfr/text/21/312.52)), or the accountable party for a missed retention or backup duty. Where a site cannot carry these operational duties, the answer is the human [[micro-cro-operating-model|Micro-CRO]] tier — a named accountable entity — not a quieter default. See [[non-delegable-functions-and-gates]].

## Low-resource-site posture

The container targets commodity hardware: a single modern workstation runs the full stack in postures 1–2, with local-model quality scaling to available compute rather than gating installation. Documentation assumes no dedicated IT staff — installation is one image pull plus the IQ checklist; upgrades are atomic image swaps with automatic schema migration and a pre-upgrade record export. For sites outside the US, the HIPAA-specific machinery still runs (it is never weaker than local law is likely to demand), but the deployment does not represent compliance with non-US privacy regimes; that mapping is future work and is flagged, not assumed ([[risks-and-limitations]]).

> [!interpretive] OSSICRO position
> Local-first is a deliberate inversion of the clinical-software default, adopted because OSSICRO's two hardest constraints — the preparatory-review no-egress representation and trust-building with sites that have no compliance apparatus — are both easier to *demonstrate* when the entire PHI-touching surface is a single auditable container inside the covered entity. The cost (operational duties land on the site, hosted-model quality requires explicit postures) is acknowledged above rather than engineered around silently.

## Related

- [[privacy-state-machine]]
- [[smart-on-fhir-integration]]
- [[hipaa-and-privacy-gating]]
- [[architecture]]
- [[data-model]]
- [[part-11-and-ai-credibility]]
- [[claude-sdk-ai-in-the-loop]]
- [[data-integrations-ctgov-pubmed]]
- [[matching-engine]]
- [[completeness-ledger]]
- [[safety-clock-engine]]
- [[regulatory-change-log]]
- [[record-retention-and-archival]]
- [[verifiable-site-qualification-dossier]]
- [[micro-cro-operating-model]]
- [[non-delegable-functions-and-gates]]
- [[risks-and-limitations]]

## Sources

- [45 CFR 164.308 — Administrative safeguards (Cornell LII)](https://www.law.cornell.edu/cfr/text/45/164.308)
- [45 CFR 164.310 — Physical safeguards (Cornell LII)](https://www.law.cornell.edu/cfr/text/45/164.310)
- [45 CFR 164.312 — Technical safeguards (Cornell LII)](https://www.law.cornell.edu/cfr/text/45/164.312)
- [45 CFR 164.502 — Uses and disclosures of PHI: general rules (Cornell LII)](https://www.law.cornell.edu/cfr/text/45/164.502)
- [45 CFR 164.512 — Research provisions (Cornell LII)](https://www.law.cornell.edu/cfr/text/45/164.512)
- [45 CFR 164.514 — De-identification; limited data set (Cornell LII)](https://www.law.cornell.edu/cfr/text/45/164.514)
- [45 CFR 160.103 — Definitions (business associate) (Cornell LII)](https://www.law.cornell.edu/cfr/text/45/160.103)
- [21 CFR Part 11 — Electronic Records; Electronic Signatures (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)
- [FDA Guidance — Part 11, Electronic Records; Electronic Signatures: Scope and Application (2003)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/part-11-electronic-records-electronic-signatures-scope-and-application)
- [21 CFR 312.57 — Recordkeeping and record retention (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/312.57)
- [21 CFR 312.62 — Investigator recordkeeping and record retention (Cornell LII)](https://www.law.cornell.edu/cfr/text/21/312.62)
- [ICH E6(R3) Step 4 Final Guideline (Jan 2025, PDF)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [ClinicalTrials.gov API v2 documentation](https://clinicaltrials.gov/data-api/api)
