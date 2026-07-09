# OSSICRO - Detailed Plan

## Executive Summary

## OSSICRO — Executive Summary

**OSSICRO (Open Source Sponsor-Investigator CRO)** is a holistic system — open-source software, an exhaustively-cited regulatory wiki, a document-template library, a generate/check/validate engine, and a pharma-style frontend — that lets an enrolling clinician coordinate the full paperwork burden required to match a patient to an early-phase (e.g., Phase 2) program, activate a site, and reach enrollment across every accountable entity: sponsor, CRO, investigator/sponsor-investigator, IRB/IEC, DSMB, pharmacovigilance, and the pharma partner.

The controlling legal fact is **21 CFR 312.52**: sponsor obligations transfer, in writing, only to a *legally-accountable CRO entity* that becomes subject to the same FDA enforcement as a sponsor — software can never be the transferee. Pure CRO disintermediation is therefore structurally illegal, and the market has proved it (Science 37's ~$1B→~$38M collapse; TrialSpark's pivot to Formation Bio as a drug *developer*). OSSICRO's viable architecture is the **sponsor-investigator IND (21 CFR 312.3(b))**: one physician lawfully holds both sponsor and investigator obligation sets, and AI absorbs the coordination labor — precisely where CRO margin concentrates (~90-95% of direct cost is labor) — that normally makes the dual role impractical for a solo clinician.

OSSICRO supports **two modes**: (a) *physician-as-site* enrolling into a pharma sponsor's protocol, and (b) *physician-as-sponsor-investigator* running an investigator-initiated trial. A parallel **expanded-access** pathway (Subpart I, Form FDA 3926) serves the single-patient treatment case. A **hard line** governs the whole system: it drafts, checks, routes, times, and version-controls, but never *owns* non-delegable human judgment — informed consent, IRB approval, SAE causality/expectedness determination, statistical sign-off, or the 1571/1572 legal attestations. Every generated artifact carries a citation to governing authority and a gate routing accountable acts to a qualified human. A **thin micro-CRO** supplies the legally-accountable functions when required; everything else is open-source and physician-operable. The design is grounded in real institutional precedent (Harvard Catalyst's IND consult network, Vanderbilt's V-CAP, NCATS/SMART IRB, Penn/Pitt template libraries) and current standards (ICH E6(R3), M11, the 2024 DCT and 2025 AI-credibility guidances).

---

## OSSICRO — Detailed Plan

### 1. Vision and the load-bearing legal frame

OSSICRO exists to make the **sponsor-investigator role tractable** for a practicing clinician. The role is legally routine — every investigator-initiated trial uses it — but operationally crushing, because one person must discharge *both* the sponsor obligation set (21 CFR 312.50-312.59, plus IND submission 312.20-312.23, safety reporting 312.32, annual reports 312.33) *and* the entire investigator obligation set (21 CFR 312.60-312.69). Harvard Catalyst's own consult-service literature states the problem plainly: investigator-sponsors "often do not fully appreciate their regulatory obligations nor have resources to ensure compliance" (Kim et al. 2014, PMID 24455986).

The disintermediation temptation — "let software be the CRO" — is foreclosed by **21 CFR 312.52**: sponsor obligations transfer, in writing, only to a CRO *entity* that thereby becomes "subject to the same regulatory action as a sponsor" (§312.52(b)). Software cannot be subject to FDA enforcement, so it cannot be the transferee. The market corroborates the law: Science 37 (DCT software, ~$1B SPAC → ~$38M eMed take-private) and TrialSpark (pivoted to Formation Bio, an AI-native drug *developer*) both show coordination-only software captures no durable value.

The lawful path is therefore **21 CFR 312.3(b)**: a single physician holds both roles, no obligation is transferred to a non-entity, and AI absorbs the coordination labor — which is exactly where CRO economics sit (~90-95% of direct cost is labor; ~40-50% gross margin). OSSICRO automates the margin-generating labor and retains a **thin, human-staffed micro-CRO** for the irreducible accountable functions.

### 2. System architecture

Five components over a 21 CFR Part 11-compliant substrate (validated system, time-stamped independent audit trails per §11.10(e), e-signature capture per §11.50-11.300, access control):

1. **Searchable program database + patient-trial matching.** Built on the ClinicalTrials.gov v2 REST API (phase/status enums; free, no registration wall) with an OSSICRO semantic-matching layer on top (the native API lacks synonym matching). HIPAA-gated: matching is a *review preparatory to research* (45 CFR 164.512(i)(1)(ii)); enrollment requires authorization (164.508) or an IRB/Privacy-Board waiver (164.512(i)(1)(i)).
2. **Generate/check/validate engine** (see §3).
3. **Template library** (see Template Manifest) seeded from public-domain government sources (NIH-FDA protocol template, NIH DSMB charters, FDA forms, ICH M11) and schema-mirrored from institutional libraries (Penn, Pitt, UNC Lineberger, Stanford CRQ).
4. **Pharma-style frontend** — a milestone/Gantt regulatory tracker across sponsor/IRB/DSMB/pharma counterparties (Yale YCCI model), interoperating with sponsor stacks (CTMS, eTMF, EDC, IRT, safety DB, site portals) on Part 11-compliant e-record conventions.
5. **Micro-CRO service layer** (see §6).

### 3. The generate / check / validate engine

Three passes, each carrying citations and human gates — the operating version of the HARD LINE:

- **Generate.** Instantiate a template from structured study data (ICH M11 CeSHarP structured protocol is the priority target schema; forms auto-populate from CV/site/financial data). Output is a draft *for qualified human review*, never a filed document.
- **Check.** Completeness validation against the essential-records matrix (ICH E6(R3) Appendix C, risk-proportionate — not a fixed checklist) and against form field-rules (Form 1572 fields 1-9; 3454-vs-3455 selection logic). Prior art: Vanderbilt's V-CAP (PMC3767144) outputs a personalized required-approvals checklist from structured inputs; OSSICRO reimplements this pattern independently.
- **Validate.** A rule engine where each rule traces to a specific CFR/ICH subsection (Mayo's report-type × trigger × deadline table is the encodable model), plus recurring compliance checks (MD Anderson's annual-per-IIT-IND audit cadence). Every rule that touches an accountable act *fails to a human gate* rather than proceeding.

The engine's own AI outputs are risk-tiered under the FDA 2025 AI-credibility draft guidance (7-step COU/model-risk framework). OSSICRO's explicit argument: document *drafting for human review* is a low-influence/low-consequence context of use — the software does not make the regulatory decision — which keeps most of the engine in a defensible, lower-credibility-burden tier. Flagged as interpretive; the guidance is draft (comments closed 2025-04-07).

### 4. Data model and clinician flow

**Core entities:** Study, IND, Site, Investigator/Sponsor-Investigator, Subject (coded; identities never in logs), Document (with a state machine: draft → checked → human-reviewed → signed → filed → archived), Obligation (CFR/ICH-keyed), Gate (non-delegable act + responsible human), Event, SafetyReport, Milestone. Document IDs follow Penn's numbered document-control scheme (e.g., 03.01.01). Audit trail is ALCOA++ per E6(R3) §6 and Part 11.

**Clinician flow (guiding scenario):** (1) clinician enters de-identified clinical picture → matching returns candidate early-phase programs (preparatory-review basis); (2) triage to Mode A / Mode B / expanded access; (3) engine assembles the mode-appropriate document set with a live milestone tracker; (4) at each gate the clinician (or the micro-CRO's qualified human) reviews, judges, and signs; (5) submissions to FDA/IRB are explicit human-authorized actions; (6) conduct, safety, and closeout tracked against deadlines.

### 5. The two supported modes (+ the expanded-access branch)

- **Mode A — physician-as-site.** The pharma company is sponsor; the physician is a site investigator on an existing protocol. OSSICRO produces the site-activation essential-document package to sponsor standard (1572, CVs/licenses, 3454/3455, GCP training, CTA/budget, IRB approval, lab certs, delegation log, drug-accountability SOPs) — turning a new site's biggest liability (no track record) into a verifiable dossier. Non-delegable: PI qualification attestation, consent, IRB approval, causality.
- **Mode B — sponsor-investigator IND.** The physician holds the IND and both obligation sets. OSSICRO assembles the full 312.23 IND package, tracks the 30-day clock, and maintains the IND (safety reports 312.32, annual report/DSUR 312.33, amendments 312.30). The pharma partner, if any, is only an IIS supplier/funder (Medical Affairs, FMV-set, Sunshine-reportable). Non-delegable: 1571/1572 signatures, IND-holder accountability, all of Mode A's gates.
- **Expanded-access branch.** For "no trial fits, single patient" — Form 3926, manufacturer letter of authorization, IRB concurrence (Subpart I). Treatment, not research; surfaced as a distinct workflow with no generalizable-data expectation. Manufacturer's decision to supply is a non-delegable counterparty judgment (FDCA §561A).

### 6. The micro-CRO operating model

A thin, named, legally-accountable layer that holds only the functions §312.52(b) requires an entity for, when the sponsor-investigator cannot personally hold them. Precedents: Harvard Catalyst's contributory-network model, Duke/ReGARDD's cross-institutional shared services, MICHR's tiered service (free automated triage → $90/hr human escalation). Service tiers: (0) open-source self-serve; (1) automated triage/generation; (2) paid human review at accountable gates; (3) full micro-CRO assumption of enumerated obligations via a TORO instrument. The layer never assumes investigator conduct obligations (those are non-transferable) and never owns consent, IRB judgment, or causality.

### 7. Phased roadmap

- **Phase 0 — Regulatory wiki + citation map (this deliverable).** The exhaustively-cited knowledge base; the compliance-mapping spine everything else validates against.
- **Phase 1 — Template library, public-domain first.** Seed from NIH-FDA protocol template, NIH DSMB charters, FDA forms, ICH M11/E6(R3); schema-mirror institutional libraries with license verification.
- **Phase 2 — Form 1572 generate/check/validate.** The most tractable first target (fixed FDA schema, official field instructions, TransCelerate cross-check). Proves the engine pattern end-to-end with a real gate (the signature).
- **Phase 3 — IND assembly engine.** Full 312.23 package for Mode B, ICH M11 structured protocol output, the 6-amendment-type document state machine (Pitt taxonomy).
- **Phase 4 — Coordination engine.** Inter-entity document-flow routing, milestone tracker, IRB reliance via SMART IRB/IREx pattern, safety-report timers.
- **Phase 5 — Matching + frontend.** ClinicalTrials.gov v2 integration + semantic layer + HIPAA gating; the pharma-style frontend.
- **Phase 6 — Micro-CRO service layer.** Stand up the accountable entity, TORO tooling, and the human-escalation tiers.

### 8. Risks and mitigations

- **Legal (highest).** Any drift toward software-as-transferee is illegal (312.52). Mitigation: hard-coded gates; the micro-CRO is a real entity; every accountable act routes to a named human. Product liability and unauthorized-practice exposure for a system touching medical decisions — mitigation: draft-for-review framing, no clinical recommendation, counsel review of the service model.
- **Regulatory motion.** E6(R3) FDA-adopted 2025-09-09 (no US compliance date set yet), M11 final template 2025-11-19, DCT final 2024-09-18, AI-credibility still draft. Mitigation: build to R3/M11 as forward standards; version every citation with adoption date; flag draft guidances in-page.
- **AI-generated regulatory text acceptance.** Not a settled FDA position. Mitigation: low-risk-COU argument + mandatory human sign-off; never assert automation-permitted where only human-sign-off is.
- **Template licensing.** TransCelerate CPT is consortium IP behind a gate; Advarra templates are proprietary. Mitigation: prefer public-domain government sources; verify reuse terms before verbatim adoption; document provenance in `references/external-templates-and-licenses.md`.
- **Adoption/trust.** Pharma's trust gate is entity-shaped, not software-shaped. Mitigation: OSSICRO's deliverable is a complete, internally-consistent, credentialed dossier — the single most persuasive artifact to a skeptical sponsor.
- **Privacy.** Mishandling PHI at matching. Mitigation: the 164.512(i) preparatory-review boundary is enforced in code; enrollment gated on authorization/waiver.
---

## Addendum 2026-07-09 — Four entry points, the n-of-1 site, and AI-in-the-loop

### Four entry points (personas)
OSSICRO is entered by four actors, each with a distinct perspective, need set, document set, and regulatory obligation set, all resolving onto one coordination spine:
- **Patient** — wants access to an investigational therapy; owns nothing regulated but is the protected subject (informed consent, privacy). Entry: "is there a trial/therapy for me, and can my doctor get me in?"
- **HCP / physician** — the enrolling clinician; becomes a site investigator (Mode A) or sponsor-investigator (Mode B). Entry: "my patient needs this; make me an accepted site without a research office."
- **Micro-CRO** — the thin legally-accountable OSSICRO entity that can hold transferred sponsor obligations (21 CFR 312.52) when the physician cannot; runs a real quality system/SOPs. Entry: the escalation layer.
- **Pharma** — sponsor/supplier of the investigational product; must be able to trust and accept a small/new/single-patient site. Entry: IIS portal, expanded-access intake, or protocol site-add.

Each persona gets a portal perspective in the frontend and a documentation/obligation page under `06-personas/`.

### The single-patient (n-of-1) site
A first-class scenario: one physician + one patient + one pharma early-phase drug. Three compliant routes, each with its own backend and document package: (a) single-patient **expanded access** (individual-patient IND, 21 CFR 312.310, Form 3926 + manufacturer LOA + IRB concurrence); (b) adding a **one-patient site** to an existing sponsor protocol (expedited site qualification + minimal essential-document set); (c) a **sponsor-investigator single-patient study** (own IND). OSSICRO generates the document set and drives the pharma-acceptance backend for whichever route fits.

### AI-in-the-loop (Claude Agent SDK)
The generate/check/validate engine is implemented with the **Claude Agent SDK**: drafting agents produce document drafts from structured study data + templates; review/QC agents check completeness against the essential-records matrix and flag inconsistencies; coordination agents route artifacts between entities. Every AI action is a DRAFT behind a human sign-off gate; permission modes enforce that non-delegable functions are never auto-executed. AI authorship is recorded in the Part-11 audit trail (attribution, model/version, input hash, human reviewer, timestamp).

### Data integrations
ClinicalTrials.gov API v2 (discovery, eligibility, sites), PubMed/E-utilities (evidence + safety literature), openFDA (labels/FAERS), and IB/protocol ingestion feed matching, drafting, and safety surveillance.

### Matching engine + communication hub (2026-07-09b)
- **Matching engine** — multi-directional matching across trial / condition / medication: patient profile → eligible trials; condition/diagnosis → trials + available therapies; medication/mechanism → trials, labels, and supporting evidence. Sources: ClinicalTrials.gov API v2, PubMed/E-utilities, openFDA. Computable-eligibility parsing turns free-text criteria into checkable predicates with a transparent, cited match rationale. This is the shared discovery front-door for all four entry points.
- **Communication hub** — role-scoped, auditable messaging and document exchange connecting Patient, HCP, Micro-CRO, and Pharma, with routing to oversight entities (IRB/DSMB/FDA), status tracking, and notifications; privacy-preserving (HIPAA) and respecting the Medical-Affairs/Clinical-Development firewall.
- **Reinforced principle** — OSSICRO drafts COMPLETE documentation to remove the paperwork barrier; it never replaces human, board/ethics, or medical judgment. Every artifact is a draft for qualified human review and the appropriate oversight bodies.
