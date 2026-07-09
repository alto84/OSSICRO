## OSSICRO Wiki — Complete Information Architecture

Convention: pages live at `wiki/<section>/<page>.md` and cross-link with relative markdown links (e.g., `[sponsor-investigator](../01-roles-responsibilities/sponsor-investigator.md)`). Every page opens with a **Governing Authority** header and a **Confirmed / Interpretive** badge. This tree is the source for `wiki/INDEX.md`.

### `wiki/INDEX.md`
Master table of contents; links every section index; carries the confirmed-vs-interpretive legend and the citation-register convention.

### 00-overview/ — orientation, glossary, legal frame
- `00-overview/index.md` — Section landing; reading order for a first-time clinician vs. a regulatory reviewer.
- `00-overview/what-is-ossicro.md` — Mission, scope, the open-source + thin-micro-CRO thesis, and the HARD LINE (drafts for human review; never owns non-delegable acts).
- `00-overview/guiding-scenario.md` — "A clinician has a patient and a candidate early-phase treatment": end-to-end narrative walkthrough that threads every downstream page.
- `00-overview/the-three-pathways-triage.md` — Decision tree: (A) enroll as a site in a pharma trial, (B) sponsor-investigator IIS/IND, (C) expanded access; document sets, accountable parties, and legal exposure differ entirely (21 CFR 312.3, 312.52, Subpart I).
- `00-overview/legal-thesis-3123-vs-31252.md` — Why 312.3(b) (dual-role human) is lawful and 312.52 (transfer only to an accountable entity) makes software disintermediation illegal; the load-bearing argument.
- `00-overview/failed-disintermediation-case-studies.md` — Science 37 and TrialSpark→Formation Bio as evidence that coordination-only software captures no durable value; value follows accountability/asset.
- `00-overview/glossary.md` — Controlled-vocabulary definitions (sponsor, investigator, sponsor-investigator, CRO, SUSAR, SAE, TMF, ISF, DSMB, sIRB, IB, ICF, TORO, CtQ, COU, ALCOA++) each tagged to its citation.
- `00-overview/regulatory-landscape.md` — Map of binding law (21 CFR Parts 11, 50, 54, 56, 312; 45 CFR 46; HIPAA) vs. non-binding guidance (ICH as adopted, FDA guidances); which authorities are in active motion (E6(R3), M11, DCT, AI-credibility).
- `00-overview/entity-map.md` — The six coordinating entities and their legal relationships; diagram of who signs, who judges, who is enforceable; mirrors real institutional 3-way splits (regulatory-affairs / IRB-ethics / CTO-protocol-ops).
- `00-overview/confirmed-vs-interpretive.md` — The calibration standard for the whole wiki: black-letter requirements vs. OSSICRO-thesis interpretive positions (AI-drafted regulatory text, software-assisted monitoring boundary, AI credibility tiering).

### 01-roles-responsibilities/ — one page per accountable role
- `01-roles-responsibilities/index.md` — Role matrix; who can delegate what; the non-delegable floor per role.
- `01-roles-responsibilities/sponsor.md` — Sponsor duties (21 CFR 312.50-312.59): investigator selection, IND maintenance, monitoring, informing investigators, recordkeeping, supply disposition.
- `01-roles-responsibilities/investigator.md` — Investigator duties (21 CFR 312.60-312.69): protocol adherence, drug control, consent, IRB assurance, records, SAE-to-sponsor, FDA inspection, controlled substances.
- `01-roles-responsibilities/sponsor-investigator.md` — The dual-role core user (21 CFR 312.3(b)): both obligation sets collapse into one person; FDA "Overview of Sponsor-Investigator Roles and Responsibilities" and the 2015 draft guidance.
- `01-roles-responsibilities/subinvestigator-and-delegation.md` — What can and cannot be delegated; the delegation-of-authority log; delegation never transfers accountability (ICH E6(R3) §2/§3; 2009 FDA Investigator Responsibilities guidance).
- `01-roles-responsibilities/cro.md` — The CRO as a legally-accountable transferee (312.52(b)); the 8 functional streams and the ~40-50% margin map; coordination-vs-accountable classification.
- `01-roles-responsibilities/micro-cro-accountable-layer.md` — OSSICRO's thin human/entity layer that holds the irreducible accountable functions when the sponsor-investigator cannot; what it is and is not.
- `01-roles-responsibilities/irb-iec.md` — IRB composition, functions, and the non-delegable approval judgment (21 CFR Part 56; 45 CFR 46).
- `01-roles-responsibilities/dsmb-dmc.md` — Independent data-monitoring body: membership, independence, COI rules, advisory (not decisional) role (FDA 2006 guidance; 2024 draft).
- `01-roles-responsibilities/pharmacovigilance-safety.md` — Safety function: intake, coding, narrative, expedited-report drafting; causality/expectedness is the medical-monitor's non-delegable call (21 CFR 312.32; ICH E2A).
- `01-roles-responsibilities/medical-monitor.md` — The qualified physician who owns seriousness/causality/expectedness and the continue/modify/stop safety judgment.
- `01-roles-responsibilities/biostatistician.md` — SAP authorship, estimand selection, randomization, TLFs; statistical sign-off is accountable (ICH E9/E9(R1)).
- `01-roles-responsibilities/clinical-monitor-cra.md` — The qualified monitor; SDV and deviation-judgment vs. automatable scheduling/reporting; risk-based scope under E6(R3).
- `01-roles-responsibilities/pharma-partner-sponsor.md` — The pharma company as trial sponsor (Mode A) or as IIS supporter/funder (Mode B) — never OSSICRO's transferee; Medical Affairs vs. Clinical Development firewall.
- `01-roles-responsibilities/fda-as-counterparty.md` — CDER/CBER review, the 30-day clock, clinical hold, BIMO inspection, and what OSSICRO must submit vs. surface.
- `01-roles-responsibilities/qualified-person-qppv-eu.md` — EU/ICH load-bearing analogue: QPPV and QP for IMP release as named accountable humans (EU CTR 536/2014; GVP Module I).

### 02-lifecycle/ — the canonical phase model
- `02-lifecycle/index.md` — The CTSA-convergent master phase list (matching→IND→IRB→activation→conduct→safety→annual/amendments→closeout→retention).
- `02-lifecycle/phase-model-overview.md` — Startup / Conduct / Closeout framing mapped to ICH E6(R3) Appendix C and 21 CFR 312.
- `02-lifecycle/feasibility-and-patient-matching.md` — Searchable early-phase program database, ClinicalTrials.gov v2 API, HIPAA "preparatory to research" basis (45 CFR 164.512(i)(1)(ii)).
- `02-lifecycle/pre-ind-and-ind-preparation.md` — Assembling the 312.23 package (1571 cover, general plan, IB, protocol, CMC, pharm/tox, prior human experience); pre-IND meeting request.
- `02-lifecycle/ind-submission-and-30-day-clock.md` — Filing, IND number, 30-day safe-to-proceed (312.40), clinical hold (312.42).
- `02-lifecycle/irb-submission-and-approval.md` — Package assembly, 56.111 approval criteria pre-check, gating enrollment on documented approval.
- `02-lifecycle/site-activation.md` — Essential-document green-light package; CTA/budget, 1572, financial disclosure, training, SIV, drug release.
- `02-lifecycle/enrollment-and-consent.md` — The consent event (non-delegable), screening/enrollment logs, eligibility judgment.
- `02-lifecycle/conduct-and-monitoring.md` — Source data, CRFs, monitoring visits, deviations, drug accountability during conduct.
- `02-lifecycle/safety-reporting-lifecycle.md` — AE→SAE→SUSAR flow; 7-day/15-day clocks; investigator→sponsor→FDA→IRB→DSMB arrows.
- `02-lifecycle/annual-reporting-and-amendments.md` — IND annual report/DSUR (312.33), protocol amendments (312.30), information amendments (312.31), IB updates.
- `02-lifecycle/closeout.md` — Final monitoring visit, drug reconciliation/destruction, FDA completion/withdrawal (312.38)/inactivation (312.45), final IRB notice, CSR.
- `02-lifecycle/record-retention-and-archival.md` — Retention rules (312.57(c), 312.62(c); E6(R3) §C.2), archival of TMF/ISF.
- `02-lifecycle/expanded-access-workflow.md` — Individual (312.310)/intermediate (312.315)/treatment (312.320); Form 3926; manufacturer letter of authorization; treatment-not-research distinction.
- `02-lifecycle/iis-request-workflow.md` — Concept synopsis → Medical Affairs IIS portal → support/grant agreement → sponsor-investigator IND; FMV and Sunshine Act reportability.

### 03-documents/ — catalog + per-document explainers
- `03-documents/index.md` — Entry point to the catalog and the three lifecycle checklists.
- `03-documents/document-catalog.md` — The full essential-records catalog mapped to ICH E6(R3) Appendix C (with E6(R2) §8 cross-numbering) and 21 CFR; owner / receiver / confirmed-vs-conditional per record.
- `03-documents/startup-tmf-checklist.md` — Before-trial essential records.
- `03-documents/conduct-tmf-checklist.md` — During-trial essential records.
- `03-documents/closeout-tmf-checklist.md` — After-trial essential records.
- `03-documents/form-fda-1571-ind-cover.md` — IND cover/commitment (312.23(a)(1)); signature is a non-delegable sponsor attestation.
- `03-documents/form-fda-1572-statement-of-investigator.md` — Fields 1-8 + Field 9 commitments (312.53(c)); retained by sponsor, not filed direct.
- `03-documents/form-fda-3454-3455-financial-disclosure.md` — Certification vs. disclosure; $25k/$50k thresholds; self-disclosure in the S-I model (Part 54).
- `03-documents/form-fda-3500a-medwatch.md` — Mandatory ICSR/IND safety report format; causality trigger is a human judgment.
- `03-documents/form-fda-3926-expanded-access.md` — Individual-patient expanded-access IND request.
- `03-documents/form-fda-3674-clinicaltrialsgov-certification.md` — ClinicalTrials.gov registration certification accompanying the IND.
- `03-documents/ind-application-312-23.md` — Full IND content/format explainer.
- `03-documents/clinical-protocol-and-synopsis.md` — Protocol contents (312.23(a)(6)); ICH M11 CeSHarP structured target; synopsis convention.
- `03-documents/investigators-brochure.md` — IB contents (312.55); package-insert substitution for marketed drugs.
- `03-documents/informed-consent-form.md` — 21 CFR 50.25 elements + Common Rule key-information; document vs. event; eConsent (2016 FDA/OHRP + Part 11).
- `03-documents/irb-submission-package.md` — Composition and completeness validator against 56.111.
- `03-documents/dsmb-charter.md` — Charter sections; risk-tiered variants (single-site low-risk vs. multi-site high-risk).
- `03-documents/monitoring-plan.md` — Risk-based monitoring plan; CtQ factors; quality tolerance limits (E6(R3) §6.9; 2013/2023 FDA RBM).
- `03-documents/safety-management-plan.md` — AE/SAE workflow, causality routing, 7/15-day timelines, reconciliation with pharma partner.
- `03-documents/delegation-of-authority-log.md` — Task delegation, training evidence, signature/initial log.
- `03-documents/clinical-trial-agreement-and-budget.md` — CTA scope, indemnification, IP, publication, FMV-set budget; AKS safe-harbor structure.
- `03-documents/transfer-of-regulatory-obligations-toro.md` — The 312.52(a) written enumeration; each assumed obligation named; the micro-CRO instrument.
- `03-documents/statistical-analysis-plan.md` — SAP structure per ICH E9/E9(R1).
- `03-documents/clinical-study-report.md` — CSR structure per ICH E3.
- `03-documents/drug-accountability-log.md` — Receipt/storage/dispensing/return/destruction (312.57, 312.59, 312.61, 312.62).
- `03-documents/regulatory-binder-isf-index.md` — The ISF/TMF table-of-contents artifact (Stanford CRQ model).
- `03-documents/ind-annual-report-dsur.md` — 312.33 annual report; ICH E2F DSUR substitution.
- `03-documents/ind-safety-report.md` — 7-day / 15-day expedited IND safety reports (312.32).
- `03-documents/clinicaltrials-gov-registration.md` — FDAAA 801 / 42 CFR Part 11 registration and results posting obligations.

### 04-coordination/ — inter-entity workflows
- `04-coordination/index.md` — How the coordinating bodies are fed, timed, and connected.
- `04-coordination/inter-entity-document-flow-map.md` — The canonical arrow diagram (protocol/IB → IRB/DMC/monitors; SAE → sponsor → FDA + investigators + IRB + DMC; DMC rec → sponsor → IRB/amendment).
- `04-coordination/irb-review-workflow.md` — Initial, continuing, and expedited review; amendment approval; the ethics gate.
- `04-coordination/single-irb-mandate-and-central-irbs.md` — 45 CFR 46.114; NIH sIRB policy; WCG/Advarra; SMART IRB/IREx reliance mechanics.
- `04-coordination/informed-consent-document-vs-event.md` — The bright line OSSICRO must never cross; eConsent mechanics vs. the human consent conversation.
- `04-coordination/dsmb-workflow.md` — Charter adoption, cadence, open/closed sessions, independent statistician firewall, recommendations to sponsor.
- `04-coordination/monitoring-workflow-siv-imv-cov.md` — Visit types, visit reports, follow-up letters, TMF filing.
- `04-coordination/risk-based-monitoring-e6r3.md` — Centralized/statistical monitoring, proportionality, CtQ; the interpretive shift the engine encodes.
- `04-coordination/safety-reporting-workflow.md` — End-to-end PV routing from site AE capture to FDA submission and investigator/IRB notification.
- `04-coordination/safety-report-timelines-7-15-day.md` — The two clocks, definitions (serious/unexpected/suspected), follow-up obligations.
- `04-coordination/sponsor-cro-site-coordination.md` — MSA/task-order/TORO relationships; who is enforceable for what; the collapse in the S-I model.
- `04-coordination/pharma-partner-interface-iis.md` — Medical-Affairs routing, feasibility/SQV, CTMS/portal interoperability, what pharma needs to trust a new site.
- `04-coordination/expanded-access-coordination.md` — Physician ↔ manufacturer ↔ FDA ↔ IRB concurrence for single-patient/population access.
- `04-coordination/fda-interactions-meetings-holds.md` — Pre-IND meetings, meeting requests, clinical-hold response, BIMO inspection readiness.

### 05-ossicro-system/ — the software system
- `05-ossicro-system/index.md` — System overview and reading order.
- `05-ossicro-system/architecture.md` — Components (matching DB, generate/check/validate engine, template library, pharma-style frontend, micro-CRO service layer); Part 11 environment.
- `05-ossicro-system/generate-check-validate-engine.md` — The three passes: generate (template + structured data), check (completeness against essential-records matrix), validate (rule-engine gates traced to CFR/ICH), with human sign-off gates.
- `05-ossicro-system/data-model.md` — Entities (Study, IND, Site, Investigator, Subject-coded, Document, Obligation, Gate, Event, SafetyReport); document-state machine; Penn-style document-ID numbering; ALCOA++ audit trail.
- `05-ossicro-system/patient-trial-matching.md` — ClinicalTrials.gov v2 integration, semantic layer, HIPAA gating (matching = preparatory review; enrollment = authorization/waiver).
- `05-ossicro-system/micro-cro-operating-model.md` — The thin accountable layer; service tiers (free automated triage → paid human escalation, MICHR/MIAP precedent); what functions it legally holds.
- `05-ossicro-system/two-modes-site-vs-sponsor-investigator.md` — Mode A (physician-as-site) vs. Mode B (sponsor-investigator); how document sets, accountable parties, and gates differ; the expanded-access branch.
- `05-ossicro-system/compliance-mapping.md` — Every generated artifact → governing authority → validation rule → responsible human sign-off; the citation-carrying manifest.
- `05-ossicro-system/non-delegable-functions-and-gates.md` — The master gating matrix (consent, IRB approval, causality, 1571/1572/3454-3455 signatures, FMV/AKS, manufacturer supply, statistical sign-off, submission-to-FDA).
- `05-ossicro-system/part-11-and-ai-credibility.md` — 21 CFR Part 11 e-records/e-signatures/audit trail; FDA 2025 AI-credibility 7-step COU/risk framework and OSSICRO's low-risk-COU argument (draft status flagged).
- `05-ossicro-system/hipaa-and-privacy-gating.md` — 45 CFR 164.512(i), 164.508, waivers, limited data sets, de-identification; the privacy fulcrum of matching vs. enrollment.
- `05-ossicro-system/prior-art-vcap-irex-smartirb.md` — Vanderbilt V-CAP and NCATS IREx/SMART IRB as published design precedents for a rules-driven checklist and programmatic reliance.
- `05-ossicro-system/roadmap.md` — Phased build (see detailed plan).
- `05-ossicro-system/risks-and-limitations.md` — Legal, regulatory-motion, liability, adoption, and technical risks and mitigations.

### references/ — citation infrastructure
- `references/index.md` — How to cite in OSSICRO; register conventions.
- `references/cfr-citation-map.md` — Every 21 CFR / 45 CFR / 42 CFR / 42 USC section used, with eCFR/Cornell URLs and the pages that cite it.
- `references/ich-guideline-map.md` — E6(R3), E8(R1), E9/E9(R1), E2A/E2B(R3)/E2D/E2F, E3, M11 — status and adoption dates.
- `references/fda-guidance-map.md` — DCT (2024), AI-credibility (2025 draft), eConsent (2016), Sponsor-Investigator IND (2015 draft), Investigator Responsibilities (2009), DMC (2006 + 2024 draft), RBM (2013/2023), Expanded Access Q&A.
- `references/fda-form-index.md` — 1571, 1572, 3454, 3455, 3500A, 3500, 3926, 3674 with OMB numbers and download URLs.
- `references/bibliography.md` — Consolidated deduped bibliography (regulatory + peer-reviewed with PMID/DOI).
- `references/institutional-resources.md` — The academic/CRO/gov resource table with reuse-license status.
- `references/external-templates-and-licenses.md` — Provenance and license status of every seed template (public-domain vs. gated/consortium).
---

## Addendum 2026-07-09 — Four entry points, single-patient site, AI-in-the-loop, data integrations

### 00-overview/ (added)
- `00-overview/four-entry-points.md` — The four actors who enter OSSICRO — Patient, HCP (physician/site), Micro-CRO, Pharma — each with a distinct perspective, needs, document set, and regulatory obligations; how their journeys interlock into one coordinated trial.

### 06-personas/ — per-actor perspective, needs, documents, regulatory requirements
- `06-personas/index.md` — The four-entry-point model and the cross-actor responsibility/needs matrix; how a patient-origin, HCP-origin, or pharma-origin request flows through the same coordination spine.
- `06-personas/patient.md` — Patient/participant perspective: access to investigational therapy, informed-consent rights (21 CFR 50; Common Rule key-information), privacy (HIPAA 45 CFR 164), what the patient sees and signs, what documentation protects them; the non-delegable consent event ([[informed-consent-document-vs-event]]).
- `06-personas/hcp-physician.md` — The enrolling HCP/physician (as site investigator or [[sponsor-investigator]]): needs, the intimidation points of site start-up, the document burden OSSICRO removes vs the non-delegable duties they keep.
- `06-personas/micro-cro.md` — The OSSICRO Micro-CRO entity: the legally-accountable transferee layer ([[transfer-of-regulatory-obligations-toro]], 21 CFR 312.52), what obligations it can hold, its own SOPs / quality system / regulatory obligations, and its service tiers.
- `06-personas/pharma.md` — The pharma sponsor/supplier perspective: what it needs to trust and accept a small / new / single-patient site; IIS and expanded-access intake; Medical Affairs vs Clinical Development firewall; contracting, drug supply, and safety-data exchange.
- `06-personas/perspective-matrix.md` — Cross-actor matrix: for each of the four actors — goals, needs, key documents, regulatory obligations, and the hand-offs between them.

### 02-lifecycle/ (added)
- `02-lifecycle/single-patient-site-enrollment.md` — The n-of-1 pathway: one physician, one patient, one pharma early-phase therapy. The three routes — single-patient expanded access (individual-patient IND, 21 CFR 312.310, [[form-fda-3926-expanded-access]]), a one-patient site added to an existing sponsor protocol, and a [[sponsor-investigator]] single-patient study — with document set, timelines, and accountable parties for each.

### 04-coordination/ (added)
- `04-coordination/single-patient-site-and-pharma-acceptance.md` — The pharma-side backend to accept a single-physician/single-patient site: intake, lightweight feasibility, expedited site qualification, drug-supply authorization (manufacturer letter of authorization), safety-data exchange agreement, and the minimal-but-compliant document package that makes a one-patient site acceptable to a sponsor.

### 05-ossicro-system/ (added)
- `05-ossicro-system/claude-sdk-ai-in-the-loop.md` — AI-in-the-loop via the Claude Agent SDK: document drafting, document review/QC, completeness checking against the essential-records matrix, and coordination agents — always behind human sign-off gates ([[non-delegable-functions-and-gates]]); permission modes and human-in-the-loop patterns; how SDK agents map onto the [[generate-check-validate-engine]]; and the Part-11 / audit-trail treatment of AI-authored drafts (attribution, versioning, review evidence).
- `05-ossicro-system/data-integrations-ctgov-pubmed.md` — External data sources: ClinicalTrials.gov API v2 (trial discovery, eligibility parsing, site/contact data), PubMed / NCBI E-utilities (supporting evidence and safety literature), openFDA (labels, FAERS), and IB/protocol ingestion; how each feeds [[patient-trial-matching]], document drafting, and safety surveillance.

### 05-ossicro-system/ (added 2026-07-09b — matching & communication)
- `05-ossicro-system/matching-engine.md` — Trial / condition / medication matching: multi-directional discovery (patient profile → trials; condition/diagnosis → trials & therapies; medication/mechanism → trials, labels, evidence) over ClinicalTrials.gov API v2 + PubMed + openFDA, with computable-eligibility parsing and a transparent, cited match rationale. The discovery front-door for all four entry points ([[four-entry-points]]).
- `05-ossicro-system/communication-hub.md` — Inter-actor communication & coordination: secure, role-scoped messaging and document exchange among Patient, HCP, Micro-CRO, and Pharma (with routing to IRB/DSMB/FDA), status tracking, notifications, and an auditable communication log — respecting HIPAA and the Medical-Affairs/Clinical-Development firewall.

### Design principle (reinforced)
OSSICRO drafts **complete, compliant documentation** to eliminate the paperwork barrier that keeps physicians out of research. It does **not** replace thoughtful human-in-the-loop judgment, IRB / ethics-board review, DSMB oversight, or medical/safety decisions. Every generated artifact is a **draft for qualified human review** and the appropriate oversight bodies; non-delegable functions are surfaced and gated (see [[non-delegable-functions-and-gates]]). This principle is foregrounded on every system and persona page.

### 05-ossicro-system/ (added 2026-07-09c — strategist improvements)
- `05-ossicro-system/smart-on-fhir-integration.md` — Chart ingestion as a first-class subsystem: SMART App Launch (point-of-care) + Backend Services / Bulk `$export` (panel screening); US Core R4 + mCODE + FHIR Genomics; feeds both [[matching-eligibility-adjudication]] and document auto-population. Read-mostly.
- `05-ossicro-system/privacy-state-machine.md` — Code-enforced HIPAA boundary: 45 CFR 164.512(i)(1)(ii) review-preparatory-to-research (local-first, minimum-necessary, no PHI egress, ephemeral audited reads) with a hard logged transition preparatory->enrollment (164.508 authorization or 164.512(i)(1)(i) waiver). Extends [[hipaa-and-privacy-gating]].
- `05-ossicro-system/matching-eligibility-adjudication.md` — Retrieve->adjudicate matching: per-criterion three-valued verdict (met / not-met / indeterminate-needs-data) with chart + criterion citations; recall-first; eligibility determination stays the investigator's non-delegable call. Prior art: Criteria2Query, EliIE, OHDSI/OMOP, CQL.
- `05-ossicro-system/matching-mechanism-graph.md` — Mechanism-aware candidate expansion: biomarker/variant -> pathway -> drug target -> trials, so mutation-matched basket/umbrella trials surface across stated conditions.
- `05-ossicro-system/matching-evaluation-and-benchmarks.md` — "Near-perfect" as a measured claim: eval harness on CHIA, TREC Clinical Trials, n2c2; recall/precision by phase; recall-first objective.
- `05-ossicro-system/single-pass-review-ux.md` — Attention-triaged review: three lanes (deterministic / boilerplate / inferred-interpretive) so reviewer attention goes only to judgment calls; the mechanism that makes one-pass HITL real.
- `05-ossicro-system/draft-provenance-model.md` — Every span carries (source datum -> provenance -> citation) triples; provenance == the ALCOA++/Part-11 audit trail rendered as UX and as the generation output contract.
- `05-ossicro-system/completeness-ledger.md` — Open-items contract per package: green (validated) / amber (needs human judgment = gate) / red (missing data + exact resolving question). The operating definition of COMPLETE documentation.
- `05-ossicro-system/verifiable-site-qualification-dossier.md` — Cryptographically verifiable, citation-complete manifest (requirement -> artifact -> citation -> signer, hash-chained to the Part-11 audit trail); pharma trust wedge and tangible Micro-CRO moat.
- `05-ossicro-system/safety-clock-engine.md` — Dedicated 7/15-day IND safety-report (21 CFR 312.32) deadline computation + escalation; computes and escalates but never files and never makes the causality call (medical monitor owns causality).
- `05-ossicro-system/offline-local-deployment.md` — Single-container local deployment inside the covered-entity boundary (no PHI egress, no data-center dependency); privacy + low-resource-site adoption.

### references/ (added 2026-07-09c)
- `references/regulatory-change-log.md` — Living-compliance change-watch: diffs FDA/ICH/eCFR on a cadence and flags every affected page/template/validation rule via the citation-dependency graph; human curator confirms. Anti-rot moat.
