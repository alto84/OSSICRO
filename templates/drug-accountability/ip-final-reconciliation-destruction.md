---
title: "IP Final Reconciliation and Destruction Record"
doc_id: "ip-final-reconciliation-destruction"
category: "drug-accountability"
governing_citations: ["21 CFR 312.59"]
owner: "investigator"
receiver: "sponsor"
gate: "none"
status: template
updated: 2026-07-09
---

# IP Final Reconciliation and Destruction Record — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 312.59](https://www.law.cornell.edu/cfr/text/21/312.59) (disposition of unused supply — the sponsor shall assure the return of all unused supplies from each discontinued or terminated investigator, or may authorize alternative disposition provided it does not expose humans to risks from the drug; written records of disposition are maintained per [21 CFR 312.57(b)](https://www.law.cornell.edu/cfr/text/21/312.57)). Investigator-side return/disposition obligation: [21 CFR 312.62(a)](https://www.law.cornell.edu/cfr/text/21/312.62). This is a DRAFT template; OSSICRO fills it from the closed Accountability Log, a qualified human verifies the counts and signs.

**Purpose.** The close-out document that reconciles all investigational product (IP) ever received at the site against everything dispensed, returned, and destroyed — lot by lot, to a zero or fully-explained balance — and records the sponsor-authorized final disposition (return to sponsor/depot or documented destruction). Completed at study termination, suspension, discontinuation, or completion, before site close-out is finalized.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing. The arithmetic in Section 2 must close for every lot: Received = Dispensed + Returned-to-sponsor + Destroyed + Other-disposition. Any residual difference is a discrepancy requiring a written explanation in Section 3. On-site destruction requires the sponsor's prior written authorization (21 CFR 312.59) — attach it.

## Template

### Section 1 — Study and Site Identification

| Field | Value |
|---|---|
| Protocol number / title | {{protocol_number}} / {{protocol_title}} |
| IND number | {{ind_number}} |
| Investigational product (name/code) | {{drug_name}} |
| Unit of accountability | {{unit_of_measure}} |
| Principal investigator | {{investigator_name}} |
| Site name / number | {{site_name}} / {{site_number}} |
| Sponsor / sponsor-investigator | {{sponsor_name}} |
| Reason for reconciliation | {{closeout_reason}} [INSTRUCTION: completion / termination / suspension / discontinuation / investigator withdrawal] |
| Date of final reconciliation | {{reconciliation_date}} |

### Section 2 — Final Reconciliation by Lot

[INSTRUCTION: One row per lot, {{quantities_reconciled}} expanding from the closed Accountability Log and shipment records. "Returned by subjects" is unused IP returned at visits (already inside "Dispensed" — shown for compliance visibility, not added to the balance equation). Balance check per lot: A − B − C − D − E must equal 0.]

| Lot / batch | (A) Total received | Dispensed to subjects | Returned by subjects (unused) | (B) Used/consumed (dispensed − returned) | (C) Returned to sponsor/depot | (D) Destroyed | (E) Other disposition | Balance (A−B−C−D−E) |
|---|---|---|---|---|---|---|---|---|
| {{quantities_reconciled}} | | | | | | | | |

| Totals across all lots | Received: {{total_received}} | Used: {{total_used}} | Returned to sponsor: {{total_returned}} | Destroyed: {{total_destroyed}} | Other: {{total_other}} | Net balance: {{net_balance}} |
|---|---|---|---|---|---|---|

### Section 3 — Discrepancies

[INSTRUCTION: Required for any lot whose balance is non-zero — lost, broken, spilled, quarantined-then-rejected units, count errors. Each entry names the lot, quantity, cause, and resolution; cross-reference the Accountability Log Section 4 entry and any protocol deviation.]

| Lot | Quantity | Explanation | Supporting record reference | Resolved (Y/N) |
|---|---|---|---|---|
| {{discrepancy_lot}} | {{discrepancy_quantity}} | {{discrepancy_explanation}} | {{discrepancy_record_ref}} | {{discrepancy_resolved_yn}} |

### Section 4 — Final Disposition

| Field | Value |
|---|---|
| Disposition method | {{disposition_method}} [INSTRUCTION: "Return to sponsor/depot" or "On-site destruction" (or both, by lot). On-site destruction is permissible ONLY under the sponsor's written alternative-disposition authorization per 21 CFR 312.59 and must not expose humans to risks from the drug] |
| Sponsor authorization for disposition (reference, date) | {{sponsor_authorization_ref}} / {{sponsor_authorization_date}} [INSTRUCTION: attach the authorization letter/email to this record] |

**If returned to sponsor/depot:**

| Field | Value |
|---|---|
| Return shipment date / courier / tracking | {{return_ship_date}} / {{return_courier}} / {{return_tracking}} |
| Quantities and lots returned | {{return_quantities_by_lot}} |
| Return acknowledged by sponsor/depot (date, reference) | {{return_ack_date}} / {{return_ack_ref}} |

**If destroyed on site (or by authorized vendor):**

| Field | Value |
|---|---|
| Destruction date | {{destruction_date}} |
| Destruction method | {{destruction_method_detail}} [INSTRUCTION: per institutional/vendor SOP, e.g., incineration via licensed hazardous-pharmaceutical-waste contractor; cite the SOP or certificate] |
| Quantities and lots destroyed | {{destroyed_quantities_by_lot}} |
| Performed by (name, role) | {{destruction_performed_by}} / {{destruction_performer_role}} |
| Witnessed by (name, role) | {{witness_name}} / {{witness_role}} [INSTRUCTION: an independent second person witnesses and countersigns the destruction] |
| Destruction certificate reference (if vendor) | {{destruction_certificate_ref}} |

[INSTRUCTION: Controlled substances — DEA disposal requirements (21 CFR Part 1317) apply in addition to 312.59; do not destroy scheduled IP outside a DEA-compliant process. Storage/records obligations for controlled-substance IP: 21 CFR 312.69.]

### Section 5 — Attestations

**Investigator.** I certify that the quantities above are a true and complete accounting of all investigational product received at this site; that all unused supplies have been returned to the sponsor or otherwise dispositioned as authorized (21 CFR 312.62(a); 21 CFR 312.59); and that any discrepancy is explained in Section 3.

| | |
|---|---|
| Investigator signature | ______________________ |
| Name | {{investigator_name}} |
| Date | {{investigator_signoff_date}} |

**Destruction witness (if on-site destruction performed).**

| | |
|---|---|
| Witness signature | ______________________ |
| Name | {{witness_name}} |
| Date | {{witness_signoff_date}} |

**Sponsor / monitor verification.** Reconciliation reviewed against sponsor shipping records (21 CFR 312.57(b)); disposition records complete.

| | |
|---|---|
| Sponsor/monitor signature | ______________________ |
| Name / role | {{monitor_name}} / {{monitor_role}} |
| Date | {{monitor_signoff_date}} |

[INSTRUCTION: File the executed original in the investigator site file and provide a copy to the sponsor TMF. Retain per 21 CFR 312.62(c) — 2 years after approval of the marketing application, or 2 years after the investigation is discontinued and FDA notified.]

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{protocol_number}} | study.protocol.number | 21 CFR 312.59 |
| {{protocol_title}} | study.protocol.title | 21 CFR 312.59 |
| {{ind_number}} | study.ind.number | 21 CFR 312.59 |
| {{drug_name}} | study.product.name | 21 CFR 312.59 |
| {{unit_of_measure}} | study.product.accountability_unit | 21 CFR 312.57(b) |
| {{investigator_name}} | site.investigator.name | 21 CFR 312.62(a) |
| {{site_name}} | site.name | 21 CFR 312.59 |
| {{site_number}} | site.number | 21 CFR 312.59 |
| {{sponsor_name}} | study.sponsor.name | 21 CFR 312.59 |
| {{closeout_reason}} | site.closeout.reason | 21 CFR 312.62(a) |
| {{reconciliation_date}} | site.closeout.ip_reconciliation_date | 21 CFR 312.59 |
| {{quantities_reconciled}} | site.ip_log.final_reconciliation[] | 21 CFR 312.57(b) |
| {{total_received}} | site.ip_log.totals.received | 21 CFR 312.57(b) |
| {{total_used}} | site.ip_log.totals.used | 21 CFR 312.62(a) |
| {{total_returned}} | site.ip_log.totals.returned_to_sponsor | 21 CFR 312.59 |
| {{total_destroyed}} | site.ip_log.totals.destroyed | 21 CFR 312.59 |
| {{total_other}} | site.ip_log.totals.other_disposition | 21 CFR 312.59 |
| {{net_balance}} | site.ip_log.totals.net_balance | 21 CFR 312.57(b) |
| {{discrepancy_lot}} | site.ip_log.discrepancies[].lot | 21 CFR 312.57(b) |
| {{discrepancy_quantity}} | site.ip_log.discrepancies[].quantity | 21 CFR 312.57(b) |
| {{discrepancy_explanation}} | site.ip_log.discrepancies[].explanation | 21 CFR 312.57(b) |
| {{discrepancy_record_ref}} | site.ip_log.discrepancies[].record_ref | ICH E6(R3) Appendix C |
| {{discrepancy_resolved_yn}} | site.ip_log.discrepancies[].resolved | ICH E6(R3) Appendix C |
| {{disposition_method}} | site.closeout.ip_disposition_method | 21 CFR 312.59 |
| {{sponsor_authorization_ref}} | site.closeout.sponsor_authorization_ref | 21 CFR 312.59 |
| {{sponsor_authorization_date}} | site.closeout.sponsor_authorization_date | 21 CFR 312.59 |
| {{return_ship_date}} | site.closeout.return.ship_date | 21 CFR 312.59 |
| {{return_courier}} | site.closeout.return.courier | 21 CFR 312.57(b) |
| {{return_tracking}} | site.closeout.return.tracking | 21 CFR 312.57(b) |
| {{return_quantities_by_lot}} | site.closeout.return.quantities_by_lot | 21 CFR 312.57(b) |
| {{return_ack_date}} | site.closeout.return.ack_date | 21 CFR 312.57(b) |
| {{return_ack_ref}} | site.closeout.return.ack_ref | 21 CFR 312.57(b) |
| {{destruction_date}} | site.closeout.destruction.date | 21 CFR 312.59 |
| {{destruction_method_detail}} | site.closeout.destruction.method | 21 CFR 312.59 |
| {{destroyed_quantities_by_lot}} | site.closeout.destruction.quantities_by_lot | 21 CFR 312.57(b) |
| {{destruction_performed_by}} | site.closeout.destruction.performed_by | 21 CFR 312.59 |
| {{destruction_performer_role}} | site.closeout.destruction.performer_role | 21 CFR 312.59 |
| {{witness_name}} | site.closeout.destruction.witness_name | 21 CFR 312.59 |
| {{witness_role}} | site.closeout.destruction.witness_role | 21 CFR 312.59 |
| {{destruction_certificate_ref}} | site.closeout.destruction.certificate_ref | 21 CFR 312.59 |
| {{investigator_signoff_date}} | site.closeout.investigator_signoff_date | 21 CFR 312.62(a) |
| {{witness_signoff_date}} | site.closeout.destruction.witness_signoff_date | 21 CFR 312.59 |
| {{monitor_name}} | study.monitoring.monitor_name | 21 CFR 312.57(b) |
| {{monitor_role}} | study.monitoring.monitor_role | 21 CFR 312.57(b) |
| {{monitor_signoff_date}} | site.closeout.monitor_signoff_date | 21 CFR 312.57(b) |

## Related

[[03-documents/ip-final-reconciliation-destruction]] · [[03-documents/drug-accountability-log]] · [[03-documents/drug-shipment-receipt-temperature-log]] · [[03-documents/close-out-visit-report]] · [[03-documents/record-retention-and-archival-statement]]
