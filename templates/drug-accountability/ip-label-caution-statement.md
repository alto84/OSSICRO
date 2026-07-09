---
title: "Investigational Product Label - Caution Statement"
doc_id: "ip-label-caution-statement"
category: "drug-accountability"
governing_citations: ["21 CFR 312.6(a)"]
owner: "sponsor-investigator"
receiver: "site-file"
gate: "none"
status: template
updated: 2026-07-09
---

# Investigational Product Label - Caution Statement — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 312.6(a)](https://www.law.cornell.edu/cfr/text/21/312.6): the immediate package of an investigational new drug intended for human use shall bear a label with the statement "Caution: New Drug--Limited by Federal (or United States) law to investigational use." See also [21 CFR 312.6(b)](https://www.law.cornell.edu/cfr/text/21/312.6) (label or labeling may not bear any statement that is false or misleading and may not represent the drug as safe or effective for the investigated purposes). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and approves the label proof before printing.

**Purpose.** The label-content specification for the immediate package of the investigational product, centered on the exact caution statement 21 CFR 312.6(a) requires. It documents, for the site file, what the compliant label says and that each lot received bears it.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing. The caution statement text is fixed by regulation — reproduce it verbatim, including capitalization; do not paraphrase, translate away, or abbreviate it on the printed label.

## Template

### Section 1 — Product Identification

| Field | Value |
|---|---|
| Investigational product (name/code) | {{drug_name}} |
| Protocol number | {{protocol_number}} |
| IND number | {{ind_number}} |
| Sponsor / sponsor-investigator | {{sponsor_name}} |
| Label version / date | {{label_version}} / {{label_date}} |

### Section 2 — Required Caution Statement (verbatim)

> **{{caution_statement}}**

[INSTRUCTION: {{caution_statement}} must render exactly as:
"Caution: New Drug--Limited by Federal (or United States) law to investigational use."
This wording is prescribed by 21 CFR 312.6(a). The parenthetical "(or United States)" indicates the permitted alternative — the printed label uses either "Federal" or "United States", e.g., "Caution: New Drug--Limited by Federal law to investigational use." Do not substitute other wording. Exception: this statement is NOT required on drugs under a §561A expanded-access label per FDCA 561A(d) or where FDA has granted a labeling waiver under 21 CFR 312.10.]

### Section 3 — Immediate-Package Label Content

[INSTRUCTION: 312.6(a) mandates only the caution statement; the additional elements below are standard GCP/IMP labeling practice so the site can identify, store, and account for the product. Adjust for blinded studies — a blinded label must not unblind (no active/placebo distinction visible) and must carry identical text across arms.]

| Element | Content |
|---|---|
| Caution statement | {{caution_statement}} |
| Product name or blinded code | {{label_product_designation}} [INSTRUCTION: for blinded IP use the kit/bottle code, not the drug name] |
| Dosage form / strength (if not unblinding) | {{label_strength_line}} |
| Lot / batch or kit number | {{label_lot_line}} |
| Storage conditions | {{label_storage_line}} |
| Expiry / retest date (or reference to central system) | {{label_expiry_line}} |
| Protocol reference | {{label_protocol_line}} |
| Sponsor name and address | {{label_sponsor_line}} |
| Directions / "per protocol" statement | {{label_directions_line}} |
| "Keep out of reach of children" (if dispensed for home use) | {{label_children_line}} |

### Section 4 — Prohibited Content Check (21 CFR 312.6(b))

[INSTRUCTION: Confirm each item before approving the proof.]

- [ ] Label bears no statement that is false or misleading in any particular.
- [ ] Label does not represent that the drug is safe or effective for the purposes under investigation.
- [ ] No promotional claims, trade dress, or efficacy language.
- [ ] Blinding integrity preserved (if applicable).

### Section 5 — Approval and Site-File Verification

| | |
|---|---|
| Label proof approved by (sponsor/sponsor-investigator) | ______________________ |
| Name / role | {{label_approver_name}} / {{label_approver_role}} |
| Date | {{label_approval_date}} |
| Site verification: each received lot bears the required caution statement (checked at receipt) | {{site_verification_initials}} / {{site_verification_date}} [INSTRUCTION: performed with the shipment receipt inspection; any lot received without a compliant label is quarantined and the sponsor notified] |

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{drug_name}} | study.product.name | 21 CFR 312.6(a) |
| {{protocol_number}} | study.protocol.number | 21 CFR 312.6(a) |
| {{ind_number}} | study.ind.number | 21 CFR 312.6(a) |
| {{sponsor_name}} | study.sponsor.name | 21 CFR 312.6(a) |
| {{label_version}} | study.product.label.version | 21 CFR 312.6 |
| {{label_date}} | study.product.label.date | 21 CFR 312.6 |
| {{caution_statement}} | study.product.label.caution_statement | 21 CFR 312.6(a) |
| {{label_product_designation}} | study.product.label.designation | 21 CFR 312.6(b) |
| {{label_strength_line}} | study.product.label.strength_line | 21 CFR 312.6(b) |
| {{label_lot_line}} | study.product.label.lot_line | 21 CFR 312.57 |
| {{label_storage_line}} | study.product.storage_conditions | ICH E6(R3) Appendix C |
| {{label_expiry_line}} | study.product.label.expiry_line | ICH E6(R3) Appendix C |
| {{label_protocol_line}} | study.protocol.number | ICH E6(R3) Appendix C |
| {{label_sponsor_line}} | study.sponsor.address_block | 21 CFR 312.6 |
| {{label_directions_line}} | study.product.label.directions | 21 CFR 312.6(b) |
| {{label_children_line}} | study.product.label.children_warning | 21 CFR 312.6 |
| {{label_approver_name}} | study.product.label.approver_name | 21 CFR 312.6 |
| {{label_approver_role}} | study.product.label.approver_role | 21 CFR 312.6 |
| {{label_approval_date}} | study.product.label.approval_date | 21 CFR 312.6 |
| {{site_verification_initials}} | site.shipments[].label_check_by | 21 CFR 312.6(a) |
| {{site_verification_date}} | site.shipments[].label_check_date | 21 CFR 312.6(a) |

## Related

[[03-documents/ip-label-caution-statement]] · [[03-documents/drug-shipment-receipt-temperature-log]] · [[03-documents/drug-accountability-log]]
