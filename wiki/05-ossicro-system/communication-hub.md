---
title: "Communication Hub: Role-Scoped Inter-Actor Comms & Oversight Routing"
section: "05-ossicro-system"
status: mixed
governing_authority:
  - "21 CFR Part 11 (electronic records/signatures; audit trail — §11.10(e))"
  - "HIPAA Privacy & Security Rules — 45 CFR 164.502(b)/164.514(d) (minimum necessary); 45 CFR 164.312 (technical safeguards)"
  - "21 CFR 312.32 / 312.64 (safety-report routing); 21 CFR 312.66 (investigator ↔ IRB assurance)"
  - "PhRMA Code; FDCA §502 (Medical-Affairs / Commercial firewall on off-label promotion)"
  - "ICH E6(R3) §5 (sponsor oversight; computerized-systems governance)"
tags: [ossicro/engine, ossicro/gating, cfr/11, cfr/312, usc/hipaa, gcp/e6r3, status/mixed]
aliases: ["Communication Hub", "Coordination Hub", "Messaging and Routing"]
updated: 2026-07-09
---

# Communication Hub: Role-Scoped Inter-Actor Comms & Oversight Routing

> [!authority] Governing authority
> [21 CFR Part 11](https://www.ecfr.gov/current/title-21/part-11) (e-records/e-signatures; time-stamped audit trail, §11.10(e)); HIPAA minimum-necessary [45 CFR 164.502(b)](https://www.ecfr.gov/current/title-45/section-164.502) and Security-Rule technical safeguards [45 CFR 164.312](https://www.ecfr.gov/current/title-45/section-164.312); safety routing [21 CFR 312.32](https://www.ecfr.gov/current/title-21/section-312.32) / [312.64](https://www.ecfr.gov/current/title-21/section-312.64); investigator–IRB assurance [21 CFR 312.66](https://www.ecfr.gov/current/title-21/section-312.66); the Medical-Affairs / Commercial firewall (PhRMA Code; [FDCA §502](https://www.govinfo.gov/content/pkg/USCODE-2022-title21/html/USCODE-2022-title21-chap9-subchapV-partA-sec352.htm)). Status: **Mixed** — the record, privacy, safety-timeline, and firewall obligations are black-letter (confirmed); the hub's role-scoping model and oversight-routing automation are interpretive design positions that carry, but never author, the underlying obligations.

The communication hub is OSSICRO's coordination spine: secure, role-scoped messaging and document exchange among the four entry-point actors — [[patient|Patient]], [[hcp-physician|HCP]], [[micro-cro|Micro-CRO]], and [[pharma|Pharma]] — with structured routing to the oversight bodies ([[irb-iec|IRB]], [[dsmb-dmc|DSMB]], [[fda-as-counterparty|FDA]]). It moves artifacts, tracks status, times deadlines, and writes an auditable log. It is a **carrier and a router**, not a decision-maker: no message the hub sends is an approval, a consent, a causality call, or a regulatory submission. Every such act remains a gated human function (see [[non-delegable-functions-and-gates]]).

## Design premise: routing is a compliance act

In an early-phase IND the *movement* of a document is itself regulated — who may receive what, on what timeline, under whose authority. A safety report has a 7- or 15-day clock and a fixed distribution list; an IRB submission must reach an IRB of record; a pharma interaction must reach Medical Affairs and not Commercial. The hub encodes these as **routing rules with citations**, so that "send" is constrained by the same authority map the [[generate-check-validate-engine]] uses. Mis-routing is a compliance failure, not a UX inconvenience — which is why routing is rule-driven and logged, not free-form.

## Role scoping and least privilege

Each actor sees only what their role and the current [[privacy-state-machine]] state permit. Scoping is enforced server-side (least privilege), consistent with HIPAA minimum-necessary ([45 CFR 164.502(b)](https://www.ecfr.gov/current/title-45/section-164.502), [164.514(d)](https://www.ecfr.gov/current/title-45/section-164.514)) and Security-Rule access controls ([45 CFR 164.312](https://www.ecfr.gov/current/title-45/section-164.312)).

| Actor | May originate | May receive | Hard scope limits |
|-------|---------------|-------------|-------------------|
| [[patient\|Patient]] | Questions to their own care team; consent-process acknowledgements | Study information, their own consent copy ([21 CFR 50.27](https://www.ecfr.gov/current/title-21/section-50.27)) | No access to other subjects; no regulatory-body channel |
| [[hcp-physician\|HCP / investigator]] | Site documents; queries to sponsor/Micro-CRO; SAE reports to sponsor ([312.64](https://www.ecfr.gov/current/title-21/section-312.64)); IRB submissions ([312.66](https://www.ecfr.gov/current/title-21/section-312.66)) | Protocol, IB, sponsor notices, IRB determinations | Cannot self-approve IRB or self-adjudicate causality |
| [[micro-cro\|Micro-CRO]] | Only obligations enumerated in an executed [[transfer-of-regulatory-obligations-toro\|TORO]] | Documents for its assumed functions | Never receives investigator-only conduct duties (non-transferable) |
| [[pharma\|Pharma]] | IIS/expanded-access intake; drug-supply authorization; safety-data exchange | Site-qualification dossier; safety data per agreement | Medical-Affairs-scoped; **no Commercial/Sales channel** |
| Oversight ([[irb-iec\|IRB]], [[dsmb-dmc\|DSMB]], [[fda-as-counterparty\|FDA]]) | Determinations, recommendations, correspondence | Submissions routed to them | Receive-and-decide; the hub never speaks for them |

> [!warning] Non-delegable
> The **Medical-Affairs / Commercial firewall** is a legal boundary, not a preference. A physician's inbound request for drug or funding routes to **Medical Affairs** (IIS/grants or medical information) and **never to a sales representative**; the exchange must stay non-promotional and documented (PhRMA Code; [FDCA §502](https://www.govinfo.gov/content/pkg/USCODE-2022-title21/html/USCODE-2022-title21-chap9-subchapV-partA-sec352.htm), off-label promotion). The hub encodes this as a routing constraint the pharma actor cannot override. See [[pharma-partner-interface-iis]] and [[pharma-partner-sponsor]].

## Oversight routing (confirmed obligations, automated timing only)

The hub encodes the canonical inter-entity arrows (the full map lives in [[inter-entity-document-flow-map]]):

- **Protocol / IB** → IRB, DSMB, monitors on version change.
- **Safety event** → the [[safety-clock-engine]] computes the [21 CFR 312.32](https://www.ecfr.gov/current/title-21/section-312.32) 7-day (fatal/life-threatening SUSAR) and 15-day (other serious, unexpected, suspected) clocks and pre-stages the distribution to **FDA + all participating investigators + IRB + DSMB**. The hub *tracks and escalates* the deadline; it **does not file** and **does not make the causality call**.
- **DSMB recommendation** → sponsor → (if adopted) IRB / protocol amendment. The recommendation is the committee's; the continue/modify/stop decision is the sponsor's.
- **IRB determination** → investigator + sponsor; enrollment stays gated until a documented approval is in the [[regulatory-binder-isf-index|TMF/ISF]].

> [!warning] Non-delegable
> The hub times, stages, and logs; it never authors or releases a regulated communication. **Causality/expectedness** ([21 CFR 312.32](https://www.ecfr.gov/current/title-21/section-312.32); ICH E2A) is the [[medical-monitor]]'s call; **IRB approval** ([21 CFR 56.111](https://www.ecfr.gov/current/title-21/section-56.111)) is the board's; **DSMB recommendations** are the committee's; **release of any submission to FDA** is an explicit human sign-off. Each is a gate the hub routes *to*, never *through*. See [[safety-reporting-workflow]] and [[dsmb-workflow]].

## Auditability (Part 11)

Every message and document transfer is an electronic record under [21 CFR Part 11](https://www.ecfr.gov/current/title-21/part-11): each carries a computer-generated, time-stamped, independent audit-trail entry (§11.10(e)) capturing sender, recipient(s), role scope, routing rule applied (with its citation), privacy-state at time of send, and content hash. Where a message effects a regulated action requiring signature, the hub captures a compliant e-signature (§11.50, §11.70, §11.100–11.300) rather than treating a bare "send" as an attestation. The communication log is thus part of the same ALCOA++ evidentiary spine as the [[data-model|document state machine]] and the [[verifiable-site-qualification-dossier]], and interoperates with sponsor stacks (CTMS/eTMF/site portals) on Part 11 conventions per ICH E6(R3) computerized-systems expectations.

## Status tracking and notifications

The hub surfaces a milestone/deadline view across counterparties (sponsor / IRB / DSMB / pharma / FDA) — the pharma-style regulatory tracker of [[architecture]] — and issues notifications on state changes (submission acknowledged, approval received, safety clock approaching, document expiring). Notifications are advisory prompts to act; they never auto-execute a gated action. Open items are reconciled against the [[completeness-ledger]] so that "what is outstanding, and who owns it" is always answerable.

## What the hub is not

- Not a consent channel — the [[informed-consent-document-vs-event|consent event]] is a human conversation, not a message.
- Not a submission portal to FDA on its own authority — release is a human sign-off.
- Not a promotional channel — the firewall forecloses that structurally.
- Not a PHI free-for-all — role scoping and the [[privacy-state-machine]] bound every payload to minimum-necessary and to the recorded privacy state.

## Related
- [[inter-entity-document-flow-map]]
- [[safety-reporting-workflow]]
- [[safety-clock-engine]]
- [[dsmb-workflow]]
- [[irb-review-workflow]]
- [[pharma-partner-interface-iis]]
- [[privacy-state-machine]]
- [[hipaa-and-privacy-gating]]
- [[part-11-and-ai-credibility]]
- [[completeness-ledger]]
- [[non-delegable-functions-and-gates]]
- [[patient-trial-matching]]

## Sources
- [21 CFR Part 11 — Electronic Records; Electronic Signatures (eCFR)](https://www.ecfr.gov/current/title-21/part-11)
- [45 CFR 164.502 — Uses and disclosures: general rules, minimum necessary (eCFR)](https://www.ecfr.gov/current/title-45/section-164.502)
- [45 CFR 164.312 — Security Rule technical safeguards (eCFR)](https://www.ecfr.gov/current/title-45/section-164.312)
- [21 CFR 312.32 — IND safety reporting (eCFR)](https://www.ecfr.gov/current/title-21/section-312.32)
- [21 CFR 312.64 — Investigator reporting to sponsor (eCFR)](https://www.ecfr.gov/current/title-21/section-312.64)
- [21 CFR 312.66 — Assurance of IRB review (eCFR)](https://www.ecfr.gov/current/title-21/section-312.66)
- [FDCA §502 (21 U.S.C. §352) — Misbranding / promotional constraints (govinfo)](https://www.govinfo.gov/content/pkg/USCODE-2022-title21/html/USCODE-2022-title21-chap9-subchapV-partA-sec352.htm)
- [ICH E6(R3) Good Clinical Practice — FDA guidance](https://www.fda.gov/media/169090/download)
