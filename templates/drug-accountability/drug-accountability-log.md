---
title: "Investigational Product Accountability Log"
doc_id: "drug-accountability-log"
category: "drug-accountability"
governing_citations: ["21 CFR 312.62(a)", "21 CFR 312.61"]
owner: "investigator"
receiver: "site-file"
gate: "none"
status: template
updated: 2026-07-09
---

# Investigational Product Accountability Log — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 312.62(a)](https://www.law.cornell.edu/cfr/text/21/312.62) (investigator recordkeeping — disposition of drug, including dates, quantity, and use by subjects) and [21 CFR 312.61](https://www.law.cornell.edu/cfr/text/21/312.61) (control of the investigational drug — administration only under the investigator's or a subinvestigator's personal supervision; no supply to unauthorized persons). Essential-record status per [ICH E6(R3) Appendix C](https://www.ich.org/page/efficacy-guidelines). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs each entry.

**Purpose.** The investigator's continuous, subject-level record of the disposition of investigational product (IP) at the site — every unit received, dispensed, returned, and remaining — maintained from first receipt through final reconciliation. It is the primary evidence that IP was administered only to enrolled subjects under authorized supervision (21 CFR 312.61) and that adequate disposition records exist (21 CFR 312.62(a)).

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing. Each dispensing/return entry line is completed contemporaneously and initialed by the person performing the transaction; corrections are single-line strikethrough, initialed and dated — never obliterated (ALCOA+; ICH E6(R3) §4 data-integrity principles).

## Template

### Section 1 — Study and Site Identification

| Field | Value |
|---|---|
| Protocol number | {{protocol_number}} |
| Protocol title | {{protocol_title}} |
| IND number | {{ind_number}} |
| Investigational product (name/code) | {{drug_name}} |
| Dosage form / strength | {{dosage_form}} / {{dose_strength}} |
| Unit of accountability | {{unit_of_measure}} [INSTRUCTION: e.g., tablets, vials, kits, syringes — one consistent unit per log] |
| Principal investigator | {{investigator_name}} |
| Site name / number | {{site_name}} / {{site_number}} |
| IP storage location | {{storage_location}} [INSTRUCTION: identify the secured, access-limited location — e.g., locked investigational pharmacy cabinet — consistent with 21 CFR 312.61 control requirements] |
| Required storage conditions | {{storage_conditions}} |
| Log initiated (date) | {{log_start_date}} |

[INSTRUCTION: Maintain ONE log per product per protocol. For multi-lot studies, either use one log with a lot-number column (as below) or a separate page per lot; state the convention here and do not mix conventions.]

### Section 2 — Lot / Batch Inventory Summary

[INSTRUCTION: One row per lot received at the site. Source each row from the corresponding Drug Shipment Receipt and Temperature Log entry.]

| Lot / batch number | Expiry / retest date | Date received | Quantity received ({{unit_of_measure}}) | Shipment record reference |
|---|---|---|---|---|
| {{lot_numbers}} | {{lot_expiry_date}} | {{lot_receipt_date}} | {{lot_quantity_received}} | {{shipment_record_ref}} |

### Section 3 — Dispensing and Return Entries

[INSTRUCTION: Complete one line per transaction, in chronological order, at the time of the transaction. Every dispensation must be to an enrolled subject identified by study code only — no names, no MRNs (subject confidentiality; the code list is a separate confidential record). The "Running balance" column must equal the prior balance minus quantity dispensed plus quantity returned; any line that breaks the arithmetic requires a documented explanation in Section 4.]

| Date | Subject ID | Visit | Lot number | Qty dispensed | Qty returned by subject | Running balance | Dispensed/received by (initials) | Verified by (initials) |
|---|---|---|---|---|---|---|---|---|
| {{dispensing_entries}} | | | | | | | | |

[INSTRUCTION: {{dispensing_entries}} expands to one row per transaction from the study record. "Returned by subject" captures unused IP brought back at subsequent visits (compliance check); record the count actually returned, not the expected count.]

### Section 4 — Discrepancies and Comments

[INSTRUCTION: Record any count discrepancy, damaged/lost unit, temperature-excursion quarantine affecting usable stock, or deviation from the dispensing plan. Each entry: date, description, resolution, initials. Cross-reference the Protocol Deviation Log where a deviation was filed.]

| Date | Description of discrepancy / event | Resolution / corrective action | Deviation log ref (if any) | Initials |
|---|---|---|---|---|
| {{discrepancy_date}} | {{discrepancy_description}} | {{discrepancy_resolution}} | {{deviation_ref}} | {{discrepancy_initials}} |

### Section 5 — Authorized Personnel

[INSTRUCTION: Only staff delegated IP dispensing/accountability duties on the Delegation of Authority Log may make entries. List them here; initials in Sections 3-4 must match the Site Signature and Initials Log.]

| Name | Role | Initials | Delegation effective date |
|---|---|---|---|
| {{authorized_staff_name}} | {{authorized_staff_role}} | {{authorized_staff_initials}} | {{delegation_date}} |

### Section 6 — Investigator Review

I have reviewed this accountability log and confirm that the investigational product was used only in accordance with the protocol and was administered only to subjects under my personal supervision or that of a subinvestigator responsible to me (21 CFR 312.61), and that this record adequately documents the disposition of the drug (21 CFR 312.62(a)).

| | |
|---|---|
| Investigator signature | ______________________ [INSTRUCTION: wet-ink or Part 11-compliant e-signature by the named investigator; not delegable to unlisted staff] |
| Name | {{investigator_name}} |
| Date | {{review_date}} |

[INSTRUCTION: On study termination, suspension, discontinuation, or completion, close this log and carry the final per-lot balances into the IP Final Reconciliation and Destruction Record (21 CFR 312.62(a) return/disposition obligation; disposition per 21 CFR 312.59). If the IP is a controlled substance, additionally satisfy 21 CFR 312.69 storage requirements and DEA recordkeeping.]

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{protocol_number}} | study.protocol.number | 21 CFR 312.62(a) |
| {{protocol_title}} | study.protocol.title | 21 CFR 312.62(a) |
| {{ind_number}} | study.ind.number | 21 CFR 312.62(a) |
| {{drug_name}} | study.product.name | 21 CFR 312.62(a) |
| {{dosage_form}} | study.product.dosage_form | 21 CFR 312.62(a) |
| {{dose_strength}} | study.product.strength | 21 CFR 312.62(a) |
| {{unit_of_measure}} | study.product.accountability_unit | 21 CFR 312.62(a) |
| {{investigator_name}} | site.investigator.name | 21 CFR 312.61 |
| {{site_name}} | site.name | ICH E6(R3) Appendix C |
| {{site_number}} | site.number | ICH E6(R3) Appendix C |
| {{storage_location}} | site.ip_storage.location | 21 CFR 312.61 |
| {{storage_conditions}} | study.product.storage_conditions | 21 CFR 312.62(a) |
| {{log_start_date}} | site.ip_log.start_date | 21 CFR 312.62(a) |
| {{lot_numbers}} | study.product.lots[].number | 21 CFR 312.62(a) |
| {{lot_expiry_date}} | study.product.lots[].expiry | 21 CFR 312.62(a) |
| {{lot_receipt_date}} | site.shipments[].received_date | 21 CFR 312.62(a) |
| {{lot_quantity_received}} | site.shipments[].quantity | 21 CFR 312.62(a) |
| {{shipment_record_ref}} | site.shipments[].record_id | 21 CFR 312.57 |
| {{dispensing_entries}} | site.ip_log.transactions[] | 21 CFR 312.62(a) |
| {{discrepancy_date}} | site.ip_log.discrepancies[].date | 21 CFR 312.62(a) |
| {{discrepancy_description}} | site.ip_log.discrepancies[].description | 21 CFR 312.62(a) |
| {{discrepancy_resolution}} | site.ip_log.discrepancies[].resolution | 21 CFR 312.62(a) |
| {{deviation_ref}} | site.deviations[].id | 21 CFR 312.66 |
| {{discrepancy_initials}} | site.ip_log.discrepancies[].recorded_by | ICH E6(R3) §4 |
| {{authorized_staff_name}} | site.staff[].name | ICH E6(R3) 2.7 |
| {{authorized_staff_role}} | site.staff[].role | ICH E6(R3) 2.7 |
| {{authorized_staff_initials}} | site.staff[].initials | ICH E6(R3) Appendix C |
| {{delegation_date}} | site.staff[].delegation_effective | ICH E6(R3) 2.7 |
| {{review_date}} | site.ip_log.investigator_review_date | 21 CFR 312.62(a) |

## Related

[[03-documents/drug-accountability-log]] · [[03-documents/drug-shipment-receipt-temperature-log]] · [[03-documents/ip-final-reconciliation-destruction]] · [[03-documents/delegation-of-authority-log]] · [[03-documents/site-signature-initial-log]] · [[03-documents/protocol-deviation-log]]
