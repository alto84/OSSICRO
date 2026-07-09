---
title: "SMART-on-FHIR Chart Ingestion — App Launch, Bulk Export, US Core and mCODE"
section: "05-ossicro-system"
status: mixed
governing_authority:
  - "45 CFR 170.315(g)(10) (ONC certified-API criterion) and 45 CFR 170.215 (adopted API standards)"
  - "45 CFR Part 171 (information blocking)"
  - "45 CFR 164.512(i), 164.502(b) (HIPAA — research provisions; minimum necessary)"
  - "21 CFR Part 11 (electronic records feeding regulated documents)"
  - "FDA Guidance — Use of Electronic Health Record Data in Clinical Investigations (2018)"
  - "ICH E6(R3) (data governance; computerized systems)"
tags: [ossicro/engine, ossicro/matching, ossicro/part11, cfr/11, ich/e6r3, lifecycle/feasibility, status/interpretive]
aliases: ["SMART on FHIR", "Chart Ingestion", "FHIR Integration"]
updated: 2026-07-09
---

# SMART-on-FHIR Chart Ingestion — App Launch, Bulk Export, US Core and mCODE

> [!authority] Governing authority
> [45 CFR 170.315(g)(10)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-D/part-170/subpart-C/section-170.315) (the ONC certified-API criterion, standards adopted at [45 CFR 170.215](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-D/part-170/subpart-B/section-170.215)) is what makes standardized chart access a regulatory *entitlement* rather than a per-vendor negotiation; [45 CFR Part 171](https://www.ecfr.gov/current/title-45/part-171) (information blocking) is its enforcement backstop. HIPAA ([45 CFR 164.512(i)](https://www.law.cornell.edu/cfr/text/45/164.512), [164.502(b)](https://www.law.cornell.edu/cfr/text/45/164.502)) constrains what OSSICRO may do with what it reads — enforced by the [[privacy-state-machine]]. FDA's [EHR-data guidance (2018)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-electronic-health-record-data-clinical-investigations-guidance-industry) and [21 CFR Part 11](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11) govern the path from chart datum to regulated record. Status: **Mixed** — the API entitlement, HIPAA constraints, and FDA data-integrity expectations are confirmed; the ingestion architecture is the OSSICRO design position.

Chart ingestion is a first-class OSSICRO subsystem, not a convenience feature. The two functions that define the product — eligibility adjudication ([[matching-eligibility-adjudication]]) and document auto-population with span-level provenance ([[draft-provenance-model]]) — are only as good as the structured clinical data behind them. A matching engine fed by manual re-keying inherits transcription error and omission; one fed directly from the certified EHR API inherits the chart itself, with a machine-readable provenance trail for every datum. This page specifies the two acquisition modes, the profile stack, the read-mostly posture, and the regulatory basis for each.

## Why the certified API is load-bearing

The 21st Century Cures Act, as implemented in the ONC Cures Act Final Rule (85 FR 25642, May 1, 2020) and updated by HTI-1 (89 FR 1192, January 9, 2024), requires certified EHR technology to expose a standardized, FHIR R4 patient-access and bulk-export API under §170.315(g)(10). The adopted standards at 45 CFR 170.215 are exactly OSSICRO's integration surface: HL7 FHIR R4 (4.0.1), the US Core Implementation Guide, the SMART App Launch Framework, and the FHIR Bulk Data Access Implementation Guide. Refusing to make electronic health information available through these interfaces can constitute information blocking under 45 CFR Part 171 unless an exception applies. The practical consequence: a solo clinician's EHR — Epic, Oracle Health, athenahealth, MEDITECH, or any other certified system — must offer this API. OSSICRO does not need vendor partnerships to read a chart; it needs correctly scoped, authorized SMART clients.

## Two acquisition modes

### Mode 1 — SMART App Launch (point of care, one patient)

The interactive mode: the clinician launches OSSICRO from within the EHR (EHR launch) or signs in from OSSICRO and picks the patient (standalone launch), per the [HL7 SMART App Launch Framework](https://hl7.org/fhir/smart-app-launch/) (OAuth 2.0 authorization-code flow with PKCE; OpenID Connect for clinician identity). The launch context binds the session to a single patient. Scopes are requested read-only and minimum-necessary in SMART v2 syntax — e.g., `patient/Condition.rs`, `patient/Observation.rs`, `patient/MedicationRequest.rs`, `patient/AllergyIntolerance.rs`, `patient/Procedure.rs`, `patient/DiagnosticReport.rs`, `patient/DocumentReference.rs` — never `.cud` (create/update/delete) scopes. This is the mode of the [[guiding-scenario]]: one physician, one patient, one candidate program; the ingested chart feeds the per-criterion eligibility verdicts and pre-populates the mode-appropriate document set ([[two-modes-site-vs-sponsor-investigator]]).

### Mode 2 — Backend Services + Bulk `$export` (panel screening)

The population mode: a SMART Backend Services client (client-credentials flow with asymmetric client authentication — a signed JWT assertion per RFC 7523, `system/*.rs` scopes) invokes the [FHIR Bulk Data Access](https://hl7.org/fhir/uv/bulkdata/) kick-off (`Group/[id]/$export` for a defined panel, or `Patient/$export`), polls the status endpoint, and retrieves NDJSON resource files. This is how a practice screens its existing panel against newly opened programs — the standing-cohort complement to point-of-care matching, and the input to the periodic re-screen that [[matching-engine]] runs when [[regulatory-change-log]]-style trial-registry updates land. Bulk export is the higher-volume, higher-sensitivity mode; it runs strictly inside the PREPARATORY state of the [[privacy-state-machine]] (local processing, no PHI egress, ephemeral audited reads) and its outputs are purged on the state machine's schedule.

## Profile stack

| Layer | Standard | What OSSICRO takes from it |
|---|---|---|
| Base | [HL7 FHIR R4 (4.0.1)](https://hl7.org/fhir/R4/) | Resource model, search, `Provenance` resource for datum-level lineage |
| US realm floor | [US Core IG](https://hl7.org/fhir/us/core/) (USCDI-aligned; HTI-1 baseline US Core 6.1.0 / USCDI v3) | The guaranteed-available data classes: problems, meds, allergies, labs, vitals, procedures, notes (`DocumentReference`), encounter and demographic data |
| Oncology | [mCODE IG](https://hl7.org/fhir/us/mcode/) | Cancer condition, staging, tumor markers, genomic variants, treatment history — the profile set that makes oncology eligibility criteria computable |
| Genomics | [Genomics Reporting IG](https://hl7.org/fhir/uv/genomics-reporting/) | Variant-level observations feeding mechanism-aware expansion ([[matching-mechanism-graph]]): biomarker → pathway → target → trials |

US Core is the floor a certified API must serve; mCODE and Genomics Reporting are richer but not certification-mandated, so the ingestion layer treats them as *progressive enhancement*: when present, criteria such as "EGFR exon 19 deletion" adjudicate directly; when absent, the engine falls back to `DocumentReference` note text and returns **indeterminate — needs data** rather than guessing ([[matching-eligibility-adjudication]], [[completeness-ledger]]).

## Read-mostly posture

OSSICRO requests read scopes only. It does not write to the EHR: no orders, no notes, no problem-list edits, no results. Documents OSSICRO drafts live in OSSICRO's own Part 11 environment ([[architecture]], [[data-model]]); if a site wants a copy of, e.g., a signed consent in the chart, that filing is the site's act in the site's system. The posture is deliberate — it keeps OSSICRO out of the EHR's clinical-decision path, keeps the certified-API interaction inside the best-supported (g)(10) read surface, and keeps the failure modes asymmetric: a read integration that breaks degrades matching; a write integration that breaks corrupts a medical record.

> [!interpretive] OSSICRO position
> "Read-mostly" (in practice, read-only against the EHR) is an OSSICRO design decision, not a regulatory requirement. A future, narrowly scoped write path (e.g., pushing a research flag or a signed document into the chart) would be re-evaluated as a separate context of use with its own risk analysis — it is not implied by anything on this page.

## From chart datum to regulated record

When an ingested datum lands in a regulated document — a diagnosis in an IND cover narrative, a lab value in an eligibility worksheet, prior-therapy history in a protocol synopsis — the FDA data-integrity frame attaches:

- **eSource and EHR guidance.** FDA's [Electronic Source Data in Clinical Investigations (2013)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/electronic-source-data-clinical-investigations) and [Use of EHR Data in Clinical Investigations (2018)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-electronic-health-record-data-clinical-investigations-guidance-industry) expect data-element identifiers, audit trails, and the ability to trace each element to its origin. The 2018 guidance explicitly encourages standards-based EHR interoperability of exactly this kind.
- **Provenance contract.** Every ingested datum carries (FHIR resource id + version, source system, retrieval timestamp, retrieving identity) and every draft span that uses it carries the triple (source datum → provenance → citation) per [[draft-provenance-model]]. The EHR remains the source; OSSICRO's copy is a traceable extract, never a silent re-statement.
- **Part 11 / ALCOA++.** The ingestion event itself is an audit-trail entry (§11.10(e)); E6(R3) data-governance expectations (attributable, original, accurate — the ALCOA++ set) apply to the extract exactly as to any other record in the [[data-model]].

## Privacy boundary

Everything on this page executes inside the [[privacy-state-machine]]. Ingestion for matching is a *review preparatory to research* (45 CFR 164.512(i)(1)(ii)): local-first, minimum-necessary ([45 CFR 164.502(b)](https://www.law.cornell.edu/cfr/text/45/164.502)), no PHI egress, every read logged, extracts ephemeral. Use of the same data for enrollment-stage documents requires the logged transition — signed [164.508](https://www.law.cornell.edu/cfr/text/45/164.508) authorization or documented IRB/Privacy-Board waiver — before a single identified datum flows into an enrollment artifact. The scope requests above are the API-level expression of minimum necessary; the state machine is the runtime enforcement. See [[hipaa-and-privacy-gating]] for the full legal analysis and [[offline-local-deployment]] for the deployment posture that makes "no PHI egress" a network-layer property.

> [!warning] Non-delegable
> Chart ingestion informs, and never makes, the eligibility determination: deciding that a specific patient meets a protocol's criteria is the investigator's judgment under [21 CFR 312.60](https://www.law.cornell.edu/cfr/text/21/312.60) (conduct according to the investigational plan) — the engine's per-criterion verdicts are decision support with citations, not decisions ([[matching-eligibility-adjudication]]). Likewise, the accuracy of case histories and source data remains the investigator's recordkeeping obligation ([21 CFR 312.62(b)](https://www.law.cornell.edu/cfr/text/21/312.62)); an automated extract does not discharge it. See [[non-delegable-functions-and-gates]].

## Related

- [[privacy-state-machine]]
- [[matching-eligibility-adjudication]]
- [[matching-engine]]
- [[matching-mechanism-graph]]
- [[patient-trial-matching]]
- [[draft-provenance-model]]
- [[completeness-ledger]]
- [[data-integrations-ctgov-pubmed]]
- [[hipaa-and-privacy-gating]]
- [[offline-local-deployment]]
- [[architecture]]
- [[data-model]]
- [[part-11-and-ai-credibility]]
- [[non-delegable-functions-and-gates]]
- [[feasibility-and-patient-matching]]

## Sources

- [45 CFR 170.315 — 2015 Edition health IT certification criteria (eCFR)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-D/part-170/subpart-C/section-170.315)
- [45 CFR 170.215 — Application programming interface standards (eCFR)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-D/part-170/subpart-B/section-170.215)
- [45 CFR Part 171 — Information Blocking (eCFR)](https://www.ecfr.gov/current/title-45/part-171)
- [ONC Cures Act Final Rule, 85 FR 25642 (May 1, 2020)](https://www.federalregister.gov/documents/2020/05/01/2020-07419/21st-century-cures-act-interoperability-information-blocking-and-the-onc-health-it-certification)
- [HTI-1 Final Rule, 89 FR 1192 (Jan 9, 2024)](https://www.federalregister.gov/documents/2024/01/09/2023-28857/health-data-technology-and-interoperability-certification-program-updates-algorithm-transparency-and)
- [HL7 SMART App Launch Framework IG](https://hl7.org/fhir/smart-app-launch/)
- [HL7 FHIR Bulk Data Access IG](https://hl7.org/fhir/uv/bulkdata/)
- [HL7 US Core Implementation Guide](https://hl7.org/fhir/us/core/)
- [HL7 mCODE Implementation Guide](https://hl7.org/fhir/us/mcode/)
- [HL7 Genomics Reporting Implementation Guide](https://hl7.org/fhir/uv/genomics-reporting/)
- [USCDI — United States Core Data for Interoperability (ASTP/ONC)](https://www.healthit.gov/isp/united-states-core-data-interoperability-uscdi)
- [FDA Guidance — Use of Electronic Health Record Data in Clinical Investigations (2018)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-electronic-health-record-data-clinical-investigations-guidance-industry)
- [FDA Guidance — Electronic Source Data in Clinical Investigations (2013)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/electronic-source-data-clinical-investigations)
- [21 CFR Part 11 — Electronic Records; Electronic Signatures (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)
- [45 CFR 164.512 — Research provisions (Cornell LII)](https://www.law.cornell.edu/cfr/text/45/164.512)
