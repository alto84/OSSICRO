---
title: "Delegation-of-Authority Log — Task Delegation, Training Evidence, and Signature Log"
section: "03-documents"
status: confirmed
governing_authority:
  - "21 CFR 312.53(c); 21 CFR 312.60; 21 CFR 312.62(a)"
  - "ICH E6(R3) Section 2 (investigator) and Appendix C (essential records)"
  - "ICH E6(R2) 4.1.5, 8.3.24 (signature sheet)"
tags: [role/investigator, role/sponsor-investigator, cfr/312, gcp/e6r3, lifecycle/activation, lifecycle/conduct, ossicro/engine, status/confirmed]
aliases: ["delegation log", "DOA log", "task-delegation log", "delegation of authority", "signature sheet"]
updated: 2026-07-09
---

# Delegation-of-Authority Log — Task Delegation, Training Evidence, and Signature Log

> [!authority] Governing authority
> 21 CFR 312.53(c) (investigator qualification/commitment package), 312.60 (investigator conduct per protocol and supervision), 312.62(a) (case-history/records); ICH E6(R3) §2 (investigator responsibilities — adequate supervision of delegated tasks) and Appendix C (essential records); ICH E6(R2) §4.1.5 and §8.3.24 (the signature-and-delegation sheet). Status: **Confirmed** — the delegation log is an essential record and the delegation/supervision duties are black-letter GCP; the boundary of what may be delegated is fixed by regulation, not by OSSICRO.

The **delegation-of-authority (DOA) log** — equivalently the task-delegation log or signature/initials sheet — is the essential record documenting which trial-related tasks the [[investigator]] (or [[sponsor-investigator]]) has delegated to which qualified individuals, evidenced by each person's role, delegated tasks, training qualification, sample signature/initials, and the dates over which the delegation was in effect. It is the **accountability spine** of site conduct: it lets a monitor, auditor, or FDA inspector reconstruct who was authorized to do what, when, and on whose supervision. ICH E6(R3) §2 requires the investigator to maintain adequate supervision of any individual to whom trial-related duties are delegated; the DOA log is the auditable evidence of that supervision.

Delegation of a **task** never transfers the investigator's **accountability**. This is the investigator-side analogue of the [[transfer-of-regulatory-obligations-toro|312.52]] firewall on the sponsor side: tasks move, responsibility does not, and software is never on the log as an accountable delegate.

## Function and evidentiary role

The DOA log discharges three functions simultaneously:

1. **Authorization** — it is the investigator's written statement that a named, qualified person is permitted to perform specific study tasks. A task performed by someone not on the log (for the relevant dates) is a finding.
2. **Qualification linkage** — each delegated task is tied to the delegate's evidenced qualification: a current CV, medical/professional license where required, and study-specific and GCP training. The log points to the [[regulatory-binder-isf-index|ISF]] records that prove competence.
3. **Attribution / handwriting key** — the sample signature and initials let a reviewer attribute every source-document and CRF entry to an authorized person (an ALCOA++ *attributable* requirement; see [[part-11-and-ai-credibility]] and the [[draft-provenance-model]]).

## Required data fields

A complete DOA log carries, per delegate, at minimum:

| Field | Content | Why |
|-------|---------|-----|
| **Name** | Full legal name of the delegate | Identity |
| **Role** | Sub-investigator, study coordinator, pharmacist, nurse, etc. | Scope framing |
| **Delegated tasks** | Specific tasks (often a coded task list: consent process support, eligibility data entry, drug accountability, AE collection, etc.) — **not** the non-delegable acts | Authorization scope |
| **Signature and initials sample** | Handwritten (or Part-11 e-signature) exemplar | Attribution key |
| **Start date** | Date delegation became effective | Temporal bound |
| **End date** | Date delegation ended (if applicable) | Temporal bound |
| **Investigator authorization** | PI signature and date authorizing each delegation | The supervision evidence |
| **Training/qualification reference** | Pointer to CV, license, GCP and protocol training in the ISF | Qualification linkage |

The log is version-controlled and dated; changes (a new staff member, a departure, a scope change) are captured contemporaneously, not reconstructed. Under E6(R3), qualification and delegation records must be kept current as staff change ([[conduct-tmf-checklist]]).

## What can and cannot be delegated

> [!warning] Non-delegable
> The investigator may delegate specific study **tasks** to qualified individuals, but **cannot delegate the accountability** attached to the Form FDA 1572 commitments: overall **supervision** of the conduct of the trial, protection of the rights/safety/welfare of subjects, adherence to the protocol, and integrity of the data and records (21 CFR 312.60; ICH E6(R3) §2). Certain acts remain the investigator's personally or a qualified physician's: the **informed-consent event** as a human relationship (the [[informed-consent-document-vs-event|document is drafted, the event is owned]]), the **eligibility/medical-judgment** determinations, and the **medical care** decisions for participants. On the sponsor side of a [[sponsor-investigator]], the 1571/1572 legal attestations and the safety causality call are likewise non-delegable. OSSICRO never appears on the DOA log as a delegate: software is not a person to whom a regulated task can be delegated. It drafts and maintains the log; a qualified human authorizes every entry. See [[subinvestigator-and-delegation]] and [[non-delegable-functions-and-gates]].

The contrast with sponsor obligation transfer is exact and worth stating: a **sponsor** may transfer obligations, but only in writing to a legally accountable CRO **entity** (21 CFR 312.52; the [[transfer-of-regulatory-obligations-toro|TORO]] instrument), never to software; an **investigator** may delegate tasks to qualified **individuals** on the DOA log, never transferring the underlying accountability. Two different mechanisms, one shared principle: accountability stays with a named, qualified human or legal entity.

## Training evidence

Each delegation is only as valid as the delegate's qualification for the delegated task. The DOA log therefore links to, and is validated against, the training file:

- **CV** (current, signed, dated) evidencing relevant education/training/experience — 21 CFR 312.53(c)(2).
- **License/registration** where the task requires it (medical license for physician sub-investigators; pharmacist licensure for drug handling).
- **GCP training** (E6(R3) expectation) and **protocol-specific training** (evidenced, dated).
- **Task-specific competencies** where applicable (e.g., specimen handling, device operation).

OSSICRO cross-checks that every delegated task has a matching, current training/qualification record on file and raises a **red** [[completeness-ledger]] state naming the exact missing evidence where it does not — a delegate cannot be authorized for a task the record does not support.

## OSSICRO engine behavior
- **Generate:** produces the DOA-log template pre-populated with the site's roster, roles, and a coded task list derived from the protocol; produces the linked training-record index.
- **Check:** validates every delegated task maps to a current qualification/training record; flags a delegate with an authorized task but missing/expired CV, license, or training; flags source/CRF authorship by a person not on the active log for the relevant date; confirms start/end dates and PI authorization signatures are present.
- **Validate:** enforces that no non-delegable act (consent event, eligibility judgment, 1571/1572 attestation, safety causality) is ever entered as a delegated task — the engine rejects such an entry and routes to the non-delegable-functions gate. It never authorizes a delegation; the PI signs.

> [!interpretive] OSSICRO position
> The DOA log is where OSSICRO's attribution model meets the human-accountability floor most directly. Because every AI-drafted artifact is authored by software and reviewed/signed by a human, the DOA log's attribution discipline extends to the [[part-11-and-ai-credibility|Part-11 audit trail]]: an AI-generated draft is attributed to the model/version that produced it and to the human reviewer who accepted it — but the AI is never a *delegate* on the log and never a signer of a regulated act. The log documents human delegates; the audit trail documents machine authorship of drafts. Keeping these two attribution channels distinct is how OSSICRO stays a tool, not a transferee.

## Related
- [[subinvestigator-and-delegation]]
- [[investigator]]
- [[sponsor-investigator]]
- [[site-activation]]
- [[transfer-of-regulatory-obligations-toro]]
- [[informed-consent-document-vs-event]]
- [[regulatory-binder-isf-index]]
- [[conduct-tmf-checklist]]
- [[completeness-ledger]]
- [[part-11-and-ai-credibility]]
- [[non-delegable-functions-and-gates]]

## Sources
- [21 CFR 312.53 — Selecting investigators and monitors](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.53)
- [21 CFR 312.60 — General responsibilities of investigators](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.60)
- [21 CFR 312.62 — Investigator recordkeeping and record retention](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.62)
- [FDA — Investigator Responsibilities: Protecting the Rights, Safety, and Welfare of Study Subjects (2009)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/investigator-responsibilities-protecting-rights-safety-and-welfare-study-subjects)
- [ICH E6(R3) Good Clinical Practice — Step 4 Final Guideline (2025)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
