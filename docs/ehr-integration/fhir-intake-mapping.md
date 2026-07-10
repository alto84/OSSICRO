# FHIR R4 → Intake Mapping — Route-3926 (Explore, Phase 1)

**Version 1.0 — 2026-07-09.** Load-bearing spec for the EHR/SMART-on-FHIR ingestion module. Maps every field in `engine/registry/routes.json` `intake_fields` (55 fields, 7 sections) to its FHIR R4 source — or marks it, honestly, as having none. Profiles cited are **US Core R4** (`http://hl7.org/fhir/us/core/StructureDefinition/...`) and **mCODE** (`http://hl7.org/fhir/us/mcode/StructureDefinition/...`). Companion artifacts: `engine/fixtures/fhir_sample_bundle.json` (synthetic bundle exercising every AUTO mapping) and `docs/ehr-integration/privacy-state-machine.md` (the enforcement design).

**The governing principle** (FRAME.md, Constitution HC1/HC2): the chart auto-populates *clinical* fields; *process* fields — FDA telephone-authorization dates, manufacturer LOA facts, IRB concurrence details, physician regulatory attestations — are not in the EHR and stay manual. The mapper never invents a source, never guesses a value, and nothing it extracts becomes intake until a named human confirms it field-by-field.

---

## 1. Classification and confidence rules

### 1.1 Field classes

| Class | Meaning | Count |
|---|---|---|
| **AUTO** | Has a FHIR chart source. The mapper proposes a value with provenance (resource type + FHIRPath + coding system) and a confidence. | **17** (1 conditional) |
| **DERIVED-LOCAL** | No chart value is copied; the app generates the value locally (pseudonym, plan id/version default). Still requires confirmation. | **3** |
| **MANUAL** | No chart source exists. Subtyped: `[process]` = regulatory/coordination fact; `[attestation]` = non-delegable physician judgment; `[external-party]` = manufacturer/IRB fact; `[authored]` = narrative composed downstream from confirmed intake, not extracted. | **35** |

### 1.2 Confidence rule (applies to every AUTO field)

| Confidence | Rule |
|---|---|
| **high** | Value read from an exactly coded element in the expected system (SNOMED CT, LOINC, RxNorm, ICD-10-CM, UCUM, or a required FHIR code binding) in a resource conforming to the cited profile, with **exactly one** candidate; only deterministic transformation applied (e.g., age computed from `birthDate`). |
| **medium** | Value from a text element (`.text`, `display`, narrative), inferred from a combination of elements, coded in a non-preferred system, composed into a narrative by the mapper, **or** any field with more than one plausible candidate (all candidates shown; confidence capped at medium). |
| **unattested** | Element absent, malformed, or ambiguous beyond the medium rule. The field is presented empty, marked *not found in chart*. **Never guessed, never defaulted from population priors.** |

Confidence is display metadata for the confirming physician; it grants nothing. High-confidence values require the same named-human confirmation as medium ones (HC1).

### 1.3 Never-extract list (hard exclusion, enforced in code)

The mapper must be structurally incapable of emitting these into a proposal value, a log line, or any outbound payload:

- `Patient.name`, `Patient.identifier` (MRN, SSN, member ids), `Patient.address`, `Patient.telecom`
- `Patient.birthDate` **as a value** (it is read to compute age, then discarded; the date itself never leaves the parse function)
- Any `Patient.contact`, `RelatedPerson`, photo, or free-text note body
- Raw resource `id`s / `fullUrl`s of patient-linked resources (kept only in the local provenance record, never in egress or generated documents)

See `privacy-state-machine.md` §4 (INV-1, INV-4, INV-8).

---

## 2. Section: Patient (coded — no PHI) — 6 fields

| Field id | Class | FHIR source | FHIRPath / coding | Confidence rule |
|---|---|---|---|---|
| `patient.coded_id` | **DERIVED-LOCAL** | none — **generated locally** | App assigns a pseudonym (e.g., `PT-3926-NNN`). `Patient.name`/`Patient.identifier` are on the never-extract list and MUST NOT populate this field. | n/a — app-assigned, physician confirms |
| `patient.age` | **AUTO** | US Core Patient (`us-core-patient`) | `Patient.birthDate` → age in whole years computed locally at import time; the birthDate itself is discarded (never stored, logged, or shown). If age ≥ 90, propose "90+" (safe-harbor aggregation, 45 CFR 164.514(b)(2)(i)(C)). | high if full birthDate; medium if year-only precision; absent → unattested |
| `patient.sex` | **AUTO** | US Core Patient | `Patient.gender` (FHIR administrative-gender: `male\|female\|other\|unknown`); secondary source `Patient.extension.where(url='http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex').value` — if the two disagree, present both, cap at medium | high for coded `gender`; medium on disagreement; absent → unattested |
| `patient.diagnosis` | **AUTO** | **mCODE Primary Cancer Condition** (`mcode-primary-cancer-condition`); fallback US Core Condition (`us-core-condition-problems-health-concerns`) with `clinicalStatus=active` | `Condition.code.coding` — SNOMED CT (`http://snomed.info/sct`) and/or ICD-10-CM (`http://hl7.org/fhir/sid/icd-10-cm`). Narrative composition pulls: stage from Observation `mcode-cancer-stage-group` (LOINC **21908-9** Stage group.clinical, value e.g. SNOMED 258228008 *Stage 4*); histology from the `mcode-histology-morphology-behavior` extension (SNOMED morphology); performance status from Observation `mcode-ecog-performance-status` (LOINC **89247-1**, LOINC answer list LA9622-7…LA9627-4; Karnofsky **89243-0** accepted as alternative) | Coded condition alone = high (single active cancer Condition). The composed textarea narrative (dx + stage + ECOG) = **medium always** — it is mapper-authored prose the physician must edit/confirm. Multiple active cancer Conditions → all candidates shown, medium |
| `patient.no_alternative_basis` | **MANUAL** `[attestation]` | none — physician judgment (21 CFR 312.305(a)(1)) | The *basis* that alternatives are exhausted/contraindicated/unavailable is clinical judgment, not a chart datum. The UI MAY display chart evidence (the prior-therapy list, biomarker results from `Observation`/`DiagnosticReport`) **as reference context beside the field, never as a proposed value.** | — |
| `patient.prior_therapies` | **AUTO** | **mCODE Cancer-Related Medication Request** (`mcode-cancer-related-medication-request`) / US Core MedicationRequest (`us-core-medicationrequest`) with `status in (completed\|stopped)`; mCODE surgical/radiotherapy procedure profiles for non-drug therapy | `MedicationRequest.medicationCodeableConcept.coding` (RxNorm `http://www.nlm.nih.gov/research/umls/rxnorm`); dates from `authoredOn` / `dosageInstruction.timing.repeat.bounds`; outcome evidence from Observation `mcode-cancer-disease-status` (LOINC **88040-1** Response to cancer treatment, value e.g. SNOMED 271299001 *Patient's condition worsened*) | Agent list + dates from coded, completed requests = high per agent; outcome attribution = medium (often note-derived); the composed "agents, dates, outcomes" narrative = **medium always** (mapper-authored prose) |

## 3. Section: Physician (becomes sponsor-investigator) — 8 fields

Source resolution: in a SMART App Launch the `fhirUser` claim resolves the logged-in clinician's `Practitioner`; in upload/paste mode the mapper offers `Encounter.participant` / `Condition.asserter` candidates. `fhirUser`-resolved = eligible for high; inferred-from-encounter = capped at medium (the encounter clinician may not be the requesting physician).

| Field id | Class | FHIR source | FHIRPath / coding | Confidence rule |
|---|---|---|---|---|
| `investigator.name` | **AUTO** | US Core Practitioner (`us-core-practitioner`) | `Practitioner.name` (family + given + suffix, rendered) | high if resolved via `fhirUser`; medium if inferred from Encounter/Condition participants |
| `investigator.degrees` | **AUTO** | US Core Practitioner | `Practitioner.qualification.code.coding` (system `http://terminology.hl7.org/CodeSystem/v2-0360`, e.g. `MD`); fallback `Practitioner.name.suffix` | high for v2-0360 coded; medium from suffix text; commonly absent → unattested |
| `investigator.address` | **AUTO** | US Core PractitionerRole (`us-core-practitionerrole`) → US Core Organization (`us-core-organization`) | `PractitionerRole.organization.resolve().address` (practice address — usually the right contact block); fallback `Practitioner.address` | **medium always** — which address belongs in the sponsor-investigator contact block is a human call |
| `investigator.phone` | **AUTO** | US Core PractitionerRole | `PractitionerRole.telecom.where(system='phone').value` (US Core prefers role-level telecom); fallback `Practitioner.telecom` | high from PractitionerRole; medium from Practitioner fallback |
| `investigator.email` | **AUTO** | US Core PractitionerRole | `PractitionerRole.telecom.where(system='email').value` | high from PractitionerRole; medium from fallback; absent → unattested |
| `investigator.license_number` | **AUTO** | US Core Practitioner | `Practitioner.qualification.identifier` (state licensing board system) — **NPI (`http://hl7.org/fhir/sid/us-npi`) is NOT a license number; never substitute it.** | **medium at best** (state license is inconsistently populated); very often absent → unattested → physician enters manually |
| `investigator.license_state` | **AUTO** | US Core Practitioner | `Practitioner.qualification.issuer` (display) or jurisdiction extension on the license qualification | medium; absent → unattested |
| `investigator.risk_determination` | **MANUAL** `[attestation]` | none | The §312.310(a) determination (probable risk from drug ≤ probable risk from disease) is the physician's non-delegable attestation. Never drafted from chart data. OSSICRO records it; it never makes it. | — |

## 4. Section: Drug + treatment plan — 10 fields

Investigational-agent caveat, stated once: in the **non-emergency** path the investigational drug typically is **not yet in the chart** (nothing has been ordered — that is the point of the request). The `drug.*` mappings below fire when a `MedicationRequest` for the agent exists (`intent in (proposal|plan|order)`, any status) — common in emergency/retrospective documentation, or when the EHR is used to stage the intended order. Investigational agents usually lack RxNorm codes, so `medicationCodeableConcept.text` (medium) is the expected path. Absent → unattested → manual entry. This is honest behavior, not a mapping gap.

| Field id | Class | FHIR source | FHIRPath / coding | Confidence rule |
|---|---|---|---|---|
| `drug.name` | **AUTO** | US Core MedicationRequest (`us-core-medicationrequest`) / mCODE cancer-related medication request | `MedicationRequest.medicationCodeableConcept` — RxNorm coding if present, else `.text` | high for RxNorm-coded; **medium for text-only (the expected case for investigational agents)**; absent → unattested |
| `drug.dose` | **AUTO** | US Core MedicationRequest | `dosageInstruction.doseAndRate.doseQuantity` (UCUM `http://unitsofmeasure.org`) + `dosageInstruction.timing` (frequency) rendered, e.g. "240 mg orally twice daily"; fallback `dosageInstruction.text` | medium always — dose + frequency + formulation is a mapper-rendered composite |
| `drug.route` | **AUTO** | US Core MedicationRequest | `dosageInstruction.route.coding` — SNOMED CT route (e.g., 26643006 *Oral route*) | high for SNOMED-coded; medium for text; absent → unattested |
| `drug.duration` | **AUTO** | US Core MedicationRequest | `dosageInstruction.timing.repeat.boundsDuration` or `dispenseRequest.expectedSupplyDuration`; fallback `dosageInstruction.text` | medium always; frequently absent → unattested |
| `treatment.monitoring_plan` | **MANUAL** `[attestation]` | none — prospective clinical plan | The monitoring plan is authored, forward-looking clinical judgment (21 CFR 312.305(b)(2)(vii)). Baseline labs from US Core Laboratory Result Observation (`us-core-observation-lab`, LOINC-coded, UCUM units) are shown **as reference context** (the "current baseline" panel), never as a proposed plan value. | — |
| `treatment.benefit_risk` | **MANUAL** `[attestation]` | none | Benefit-justifies-risk rationale (§312.305(a)(2)) rests on trial evidence and the physician's weighing — not chart data. | — |
| `treatment.non_interference` | **MANUAL** `[process]` | none | Whether supply interferes with the sponsor's development program is a manufacturer/program fact (§312.305(a)(3)); not in any chart. | — |
| `request.clinical_rationale` | **MANUAL** `[attestation]` | none | The §312.305(a) core narrative in the physician's words. Chart evidence (diagnosis, prior therapies, disease status) is displayed as reference context beside the editor; the narrative itself is authored. | — |
| `treatment.plan_id` | **DERIVED-LOCAL** | none | App proposes a local identifier (e.g., `TP-<drug>-<coded_id>`); physician confirms or replaces. | n/a |
| `treatment.plan_version` | **DERIVED-LOCAL** | none | App proposes `v1.0` on first authorship; increments on amendment. | n/a |

## 5. Section: Manufacturer — 6 fields — ALL MANUAL

No EHR holds the IND-holder relationship. **Do not infer the manufacturer from drug labeling, `MedicationKnowledge`, or openFDA** — the party who must decide to supply and grant the LOA is a process fact the physician establishes directly (FDCA §561A).

| Field id | Class | Reason |
|---|---|---|
| `manufacturer.name` | **MANUAL** `[external-party]` | IND/DMF-holder identity — process fact, not in the EHR. |
| `manufacturer.address` | **MANUAL** `[external-party]` | LOA letterhead block — from the manufacturer's correspondence. |
| `manufacturer.ind_dmf_reference` | **MANUAL** `[process]` | The cross-referenced application number comes from the manufacturer's LOA (21 CFR 312.305(b)(1), 312.23(b)). |
| `manufacturer.ind_on_file` | **MANUAL** `[process]` | Fact established with the manufacturer/FDA division. |
| `manufacturer.fda_division_contact` | **MANUAL** `[process]` | Documented FDA-division contact in lieu of an LOA — a coordination record. |
| `manufacturer.supply_committed` | **MANUAL** `[external-party]` | The manufacturer's decision; OSSICRO records it, never assumes it. |

## 6. Section: IRB — 4 fields — ALL MANUAL

IRB-of-record identity and the §56.105 election are administrative process facts held by the physician/institution, not chart data.

| Field id | Class | Reason |
|---|---|---|
| `irb.name` | **MANUAL** `[process]` | IRB of record (21 CFR 56.104/.105). |
| `irb.address` | **MANUAL** `[process]` | — |
| `irb.phone` | **MANUAL** `[process]` | Consent "whom to contact" element (21 CFR 50.25(a)(7)). |
| `irb.chair_concurrence` | **MANUAL** `[attestation]` | The §56.105 pathway election is the physician's; feeds Form 3926 Field 10.b. Never defaulted. |

## 7. Section: Submission control — 10 fields — 9 MANUAL, 1 conditional AUTO

The regulatory-pathway facts and elections live entirely outside the EHR.

| Field id | Class | Source / reason |
|---|---|---|
| `submission.emergency` | **MANUAL** `[attestation]` | Pathway election (21 CFR 312.310(d)); arms clock semantics. |
| `submission.emergency_auth_datetime` | **MANUAL** `[process]` | **The FDA telephone-authorization date exists only in the phone call and the physician's record of it — never in the chart.** Arms the 15-working-day clock. |
| `submission.first_treatment_date` | **AUTO (conditional)** | Base FHIR R4 `MedicationAdministration.effective[x]` for the investigational agent — present **only** in the emergency path where treatment preceded the written submission. FHIRPath: `MedicationAdministration.where(status='completed').effectiveDateTime \| effectivePeriod.start`, matched to the investigational drug. Confidence: high if the administration is coded and unambiguous; medium if matched by drug text. Non-emergency: absent by definition → unattested (correct behavior, not a gap). Note: `MedicationAdministration` is not a US Core-profiled resource; cite base R4. |
| `submission.fda_receipt_date` | **MANUAL** `[process]` | FDA's receipt of the 3926 (21 CFR 312.40(b)(1)) — a submission event, not a chart datum. |
| `submission.initial_or_followup` | **MANUAL** `[process]` | Form 3926 Field 2 election. |
| `submission.target` | **MANUAL** `[process]` | New vs existing IND (21 CFR 312.31). |
| `submission.ind_number` | **MANUAL** `[process]` | Existing IND number, if any — regulatory correspondence, not chart. |
| `submission.fda_division` | **MANUAL** `[process]` | Cover-letter addressee. A static drug-class → division suggestion table is permissible UI help; **it is app reference data, not chart extraction, and is never auto-confirmed.** |
| `waiver_10a` | **MANUAL** `[attestation]` | §312.10 waiver — physician attestation, never defaulted or auto-checked (routes.json help text is binding). |
| `waiver_10b` | **MANUAL** `[attestation]` | §56.105 waiver — same rule. |

## 8. Section: Informed consent (feeds ICF draft) — 11 fields — 10 MANUAL, 1 AUTO

The Part 50 consent elements are authored/templated content produced by the existing generate step **from already-confirmed intake** — they are downstream compositions, not chart extractions. The reasonably-foreseeable-risks element in particular sources from the manufacturer's IB, which the physician references but the EHR does not hold.

| Field id | Class | Source / reason |
|---|---|---|
| `consent.purpose` | **MANUAL** `[authored]` | 21 CFR 50.25(a)(1); generator pre-drafts from confirmed `drug.name` + `patient.diagnosis`. |
| `consent.duration` | **MANUAL** `[authored]` | 50.25(a)(1); pre-draft from confirmed `drug.duration`. |
| `consent.procedures` | **MANUAL** `[authored]` | 50.25(a)(1); pre-draft from confirmed `drug.*` + monitoring plan. |
| `consent.risks` | **MANUAL** `[authored]` | 50.25(a)(2); sourced from IB/manufacturer safety information — not in the chart. |
| `consent.benefits` | **MANUAL** `[authored]` | 50.25(a)(3). |
| `consent.alternatives` | **MANUAL** `[authored]` | 50.25(a)(4); informed by, not extracted from, `patient.no_alternative_basis`. |
| `consent.confidentiality_statement` | **MANUAL** `[authored]` | 50.25(a)(5); template boilerplate, physician-confirmed. |
| `contacts.injury_contact_name` | **MANUAL** `[process]` | 50.25(a)(6). UI default: confirmed `investigator.name` (cross-field default, not chart extraction); physician confirms. |
| `contacts.injury_contact_phone` | **MANUAL** `[process]` | 50.25(a)(6); UI default from confirmed `investigator.phone`. |
| `contacts.research_contact` | **MANUAL** `[process]` | 50.25(a)(7); UI default from confirmed investigator name + phone. |
| `site.name` | **AUTO** | US Core Encounter (`us-core-encounter`) → `Encounter.serviceProvider.resolve().name` (US Core Organization); fallback `Encounter.location.resolve().name` (US Core Location). **Medium always** — the facility where treatment *will be administered* may differ from the encounter's site; physician confirms. Absent → unattested. |

## 9. Supporting evidence that maps to no single field

Laboratory results — US Core Laboratory Result Observation (`us-core-observation-lab`): `Observation.code` (LOINC), `Observation.valueQuantity` (UCUM), `category=laboratory`, `status in (final|amended|corrected)` — do not populate an intake field. They render as the **baseline-context panel** beside `treatment.monitoring_plan` and feed the clinical-history attachment (Form 3926 Field 9 / package item 3) as *displayed evidence*, each datum carrying its own provenance. Same for vital signs (US Core vital-signs profiles) and `DiagnosticReport`. Displayed evidence follows the same privacy rules as proposals (local-only, no egress) but does not enter `Study.raw` unless the physician explicitly writes it into an authored narrative.

## 10. Summary counts

| Class | Count | Fields |
|---|---|---|
| **AUTO** (chart source) | **17** | patient: age, sex, diagnosis, prior_therapies (4) · investigator: name, degrees, address, phone, email, license_number, license_state (7) · drug: name, dose, route, duration (4) · submission.first_treatment_date (1, emergency-only conditional) · site.name (1) |
| **DERIVED-LOCAL** (app-generated, no chart value) | **3** | patient.coded_id · treatment.plan_id · treatment.plan_version |
| **MANUAL** (no chart source — process facts, attestations, external-party facts, authored narratives) | **35** | all manufacturer (6), all IRB (4), 9 of 10 submission-control, 10 of 11 consent, 4 drug-plan narratives + non_interference, risk_determination, no_alternative_basis |
| **Total** | **55** | — |

Every AUTO and DERIVED-LOCAL value passes through the field-by-field confirmation UI; only confirmed values become intake, and the confirmed profile is hashed as the generation input-of-record (FRAME success criterion 2; `privacy-state-machine.md` INV-2/INV-3).
