---
title: "Roles and Responsibilities — Role Matrix and the Non-Delegable Floor"
section: "01-roles-responsibilities"
status: mixed
governing_authority:
  - "21 CFR 312.3(b)"
  - "21 CFR 312.50-312.70"
  - "21 CFR Parts 50, 54, 56"
  - "ICH E6(R3)"
tags: [role/sponsor, role/investigator, role/sponsor-investigator, role/cro, role/irb, role/dsmb, cfr/312, gcp/e6r3, ossicro/gating]
aliases: ["role matrix", "non-delegable floor"]
updated: 2026-07-09
---

# Roles and Responsibilities — Role Matrix and the Non-Delegable Floor

> [!authority] Governing authority
> 21 CFR 312.3(b) (definitions of sponsor, investigator, sponsor-investigator, subinvestigator, CRO); 21 CFR 312 Subpart D (312.50-312.70); 21 CFR Parts 50, 54, 56; ICH E6(R3) (Step 4 final 2025-01-06; FDA final guidance Sept 2025). Status: **Mixed** — the role definitions and duty assignments are confirmed black-letter law; the classification of functions as "OSSICRO-draftable" is an interpretive OSSICRO position, marked inline.

Every obligation in an IND-phase clinical investigation attaches to a defined, legally accountable party. 21 CFR 312.3(b) defines the parties; 21 CFR 312 Subpart D distributes the duties between sponsor (312.50-312.59) and investigator (312.60-312.69); Parts 50, 54, and 56 add the consent, financial-disclosure, and IRB obligations. This section gives one page per accountable role. This index page carries the cross-role matrix and the single most load-bearing concept in the OSSICRO design: the **non-delegable floor** — the set of judgments, attestations, and relational acts that must stay with a qualified human or accountable entity no matter what software exists.

## The three legal mechanisms for moving work

Understanding who may do what requires distinguishing three mechanisms that are often conflated:

1. **Task delegation (investigator side).** An investigator may delegate specific trial *tasks* to qualified subinvestigators and staff, documented in a [[delegation-of-authority-log]] (ICH E6(R3), Annex 1 §2; FDA 2009 Investigator Responsibilities guidance). Delegation of a task never transfers regulatory accountability — the investigator who signed the [[form-fda-1572-statement-of-investigator|Form FDA 1572]] remains responsible for supervision and for the trial's conduct. See [[subinvestigator-and-delegation]].
2. **Obligation transfer (sponsor side).** A sponsor may transfer any or all sponsor *obligations*, in writing, only to a contract research organization — a legal person that thereby becomes "subject to the same regulatory action as a sponsor" (21 CFR 312.52(b)). Any obligation not described in the writing is deemed not transferred (312.52(a)). Software cannot be subject to FDA regulatory action, so software can never be a transferee. See [[cro]], [[transfer-of-regulatory-obligations-toro]], and [[legal-thesis-3123-vs-31252]].
3. **Role collapse (the sponsor-investigator).** One individual may lawfully hold both roles simultaneously: the [[sponsor-investigator]] of 21 CFR 312.3(b) "both initiates and conducts" the investigation and carries *both* full obligation sets. Nothing is transferred; nothing is delegated away; one person is accountable for everything. This is the operative structure of every investigator-initiated trial and the OSSICRO core user.

## Role matrix

| Role | Page | Primary authority | Non-delegable floor (minimum that stays with this party) |
|---|---|---|---|
| Sponsor | [[sponsor]] | 21 CFR 312.50-312.59; 312.32-312.33; ICH E6(R3) Annex 1 §3 | Ultimate accountability for the IND, participant safety, data integrity; safety-report causality/expectedness judgments; the 312.56(d) discontinuation decision; Form FDA 1571 attestation |
| Investigator | [[investigator]] | 21 CFR 312.60-312.69; Parts 50, 54, 56 | Personal conduct/supervision; the informed-consent event; SAE assessment to sponsor; the 1572 signature and its Field 9 commitments |
| Sponsor-investigator | [[sponsor-investigator]] | 21 CFR 312.3(b) (both sets apply) | The union of both floors above, held by one individual |
| Subinvestigator / delegated staff | [[subinvestigator-and-delegation]] | 21 CFR 312.3(b); ICH E6(R3) Annex 1 §2; FDA 2009 guidance | Performs delegated tasks under investigator supervision; holds no independent regulatory accountability |
| CRO | [[cro]] | 21 CFR 312.3(b), 312.52 | The only lawful transferee of sponsor obligations; must be a legal entity; assumes enforcement exposure for each assumed obligation |
| Micro-CRO (OSSICRO accountable layer) | [[micro-cro-accountable-layer]] | 21 CFR 312.52 (as a CRO) | Holds enumerated transferred obligations via a written [[transfer-of-regulatory-obligations-toro|TORO]]; never holds investigator conduct duties (those are not transferable) |
| IRB / IEC | [[irb-iec]] | 21 CFR Part 56; 45 CFR 46 | The approval judgment itself (56.111 criteria); initial and continuing review |
| DSMB / DMC | [[dsmb-dmc]] | FDA 2006 DMC guidance (2024 draft update) | Independent review of accumulating safety/efficacy data; advisory recommendations to the sponsor |
| Pharmacovigilance / safety function | [[pharmacovigilance-safety]] | 21 CFR 312.32; ICH E2A | Intake/coding/narrative drafting are delegable; the triggering judgments are not (they belong to the medical monitor/sponsor) |
| Medical monitor | [[medical-monitor]] | 21 CFR 312.32; ICH E6(R3) | Seriousness, causality, expectedness determinations; continue/modify/stop safety judgment |
| Biostatistician | [[biostatistician]] | ICH E9 / E9(R1) | Statistical sign-off on the SAP and analyses |
| Clinical monitor / CRA | [[clinical-monitor-cra]] | 21 CFR 312.53(d), 312.56(a); ICH E6(R3) Annex 1 §3 | Qualified-monitor judgment on findings and deviations; visit scheduling/reporting mechanics are automatable |
| Pharma partner | [[pharma-partner-sponsor]] | 21 CFR 312.50 et seq. (Mode A); IIS support agreements (Mode B) | Its own sponsor obligations (Mode A); the decision to supply drug (Mode B / expanded access) |
| FDA | [[fda-as-counterparty]] | FDCA; 21 CFR 312.40, 312.42 | Safe-to-proceed, clinical hold, inspection — the regulator is a counterparty, never a party OSSICRO acts for |
| QPPV / QP (EU analogue) | [[qualified-person-qppv-eu]] | EU CTR 536/2014; GVP Module I | Named accountable humans for pharmacovigilance and IMP release in the EU frame |

## The non-delegable floor

The recurring floor across the matrix, consolidated in the master gating matrix at [[non-delegable-functions-and-gates]]:

- **Informed consent** — the consent *event* with each subject (21 CFR Part 50; [[informed-consent-document-vs-event]]).
- **IRB review and approval** — the committee's ethics judgment (21 CFR 56.111; [[irb-submission-and-approval]]).
- **Safety judgments** — seriousness, causality, expectedness; the 7-/15-day report trigger (21 CFR 312.32, 312.64(b); [[safety-reporting-lifecycle]]).
- **Legal attestations** — signatures on [[form-fda-1571-ind-cover|Form FDA 1571]], [[form-fda-1572-statement-of-investigator|Form FDA 1572]], and [[form-fda-3454-3455-financial-disclosure|Forms FDA 3454/3455]].
- **Submission to FDA** — every filing is an explicit human-authorized act.
- **Supervision and conduct** — the investigator's personal conduct/supervision commitment; not transferable to any entity, let alone software.
- **Statistical sign-off** — the accountable analysis judgment (ICH E9).
- **The manufacturer's decision to supply** investigational product (expanded access; FDCA §561A; [[expanded-access-workflow]]).

> [!warning] Non-delegable
> No function on the floor above may be performed, owned, or signed by OSSICRO software. OSSICRO drafts complete documentation for qualified human review; it never replaces human-in-the-loop judgment, IRB/ethics review, DSMB oversight, or medical/safety decisions. Every generated artifact routes to a named, qualified human at a gate before any accountable act occurs.

> [!interpretive] OSSICRO position
> The matrix column "non-delegable floor" states black-letter law. The complementary claim — that everything *outside* the floor (drafting, completeness checking, routing, deadline computation, version control, assembly of submission packages) is lawfully automatable as coordination labor — is the OSSICRO thesis, defended at [[legal-thesis-3123-vs-31252]] and operationalized in the [[non-delegable-functions-and-gates]] gating matrix and the [[completeness-ledger]].

## Reading order

For a clinician new to research: [[investigator]] → [[sponsor-investigator]] → [[subinvestigator-and-delegation]] → [[irb-iec]]. For a regulatory reviewer evaluating the OSSICRO design: [[sponsor]] → [[cro]] → [[micro-cro-accountable-layer]] → [[non-delegable-functions-and-gates]].

## Related

- [[sponsor]]
- [[investigator]]
- [[sponsor-investigator]]
- [[subinvestigator-and-delegation]]
- [[cro]]
- [[micro-cro-accountable-layer]]
- [[irb-iec]]
- [[dsmb-dmc]]
- [[non-delegable-functions-and-gates]]
- [[legal-thesis-3123-vs-31252]]
- [[two-modes-site-vs-sponsor-investigator]]
- [[glossary]]

## Sources

- [21 CFR 312.3 — Definitions](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-A/section-312.3)
- [21 CFR 312 Subpart D — Responsibilities of Sponsors and Investigators](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D)
- [21 CFR 312.52 — Transfer of obligations to a contract research organization](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.52)
- [ICH E6(R3) Step 4 Final Guideline (2025-01-06)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [FDA — E6(R3) Good Clinical Practice guidance page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e6r3-good-clinical-practice-gcp)
- [FDA Guidance — Investigator Responsibilities: Protecting the Rights, Safety, and Welfare of Study Subjects (2009)](https://www.fda.gov/media/77765/download)
