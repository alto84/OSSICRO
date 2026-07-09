---
title: "Drug Shipment Receipt and Temperature Log"
doc_id: "drug-shipment-receipt-temperature-log"
category: "drug-accountability"
governing_citations: ["21 CFR 312.57", "ICH E6(R3) Appendix C"]
owner: "investigator"
receiver: "site-file"
gate: "none"
status: template
updated: 2026-07-09
---

# Drug Shipment Receipt and Temperature Log — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 312.57](https://www.law.cornell.edu/cfr/text/21/312.57) (records of receipt, shipment, or other disposition of the investigational drug — name of recipient, quantity, date, batch or code marks) and [ICH E6(R3) Appendix C](https://www.ich.org/page/efficacy-guidelines) (essential records — documentation of IP shipment, receipt, and storage conditions). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** The site-side record that each investigational product (IP) shipment arrived intact, in the stated quantity and lot, and within its required storage conditions — plus the continuing storage-temperature record and the handling of any excursion. Together with the sponsor's 312.57 shipping records, it establishes the chain of custody and condition of every unit before it enters the Accountability Log.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing. Complete Section 2 at the moment of receipt, before releasing product to usable stock. Any shipment with a suspected excursion or count/condition problem goes to QUARANTINE (Section 4) — not to stock — until the sponsor disposition is documented.

## Template

### Section 1 — Study and Site Identification

| Field | Value |
|---|---|
| Protocol number | {{protocol_number}} |
| Investigational product (name/code) | {{drug_name}} |
| Principal investigator | {{investigator_name}} |
| Site name / number | {{site_name}} / {{site_number}} |
| Required storage conditions | {{storage_conditions}} [INSTRUCTION: state the labeled range, e.g., 2-8 °C refrigerated, 15-25 °C controlled room temperature] |
| Storage location / equipment ID | {{storage_location}} / {{storage_equipment_id}} |
| Temperature monitoring device(s) | {{monitoring_device_id}} [INSTRUCTION: identify device and calibration status; retain calibration certificates in the site file] |

### Section 2 — Shipment Receipt Record

[INSTRUCTION: One block per shipment. Inspect BEFORE signing the courier receipt where practicable. Download/read the in-transit temperature monitor before releasing product.]

| Field | Value |
|---|---|
| Shipment / consignment number | {{shipment_number}} |
| Date shipped (per sponsor/depot) | {{ship_date}} |
| Date and time received | {{shipment_date}} {{receipt_time}} |
| Courier / carrier | {{courier_name}} |
| Lot / batch number(s) | {{lot_number}} |
| Expiry / retest date(s) | {{lot_expiry_date}} |
| Quantity per packing list | {{quantity_expected}} |
| Quantity counted on receipt | {{quantity}} |
| Count matches packing list? | {{count_match_yn}} [INSTRUCTION: if No, quarantine and notify sponsor/CTM same day; record in Section 4] |
| Physical condition acceptable? | {{condition_acceptable_yn}} [INSTRUCTION: check for damage, leakage, broken seals, label integrity] |
| In-transit temperature monitor ID | {{transit_monitor_id}} |
| In-transit monitor reading / alarm status | {{transit_monitor_reading}} |
| In-transit excursion indicated? | {{temperature_excursions}} [INSTRUCTION: Yes/No. If Yes — QUARANTINE the shipment, complete Section 4, and do not dispense until the sponsor issues a written disposition] |
| Acknowledgment of receipt sent to sponsor (date/method) | {{receipt_ack_date}} / {{receipt_ack_method}} |
| Received by (name, initials) | {{received_by_name}} ({{received_by_initials}}) [INSTRUCTION: must be staff delegated IP duties on the Delegation of Authority Log] |
| Placed into storage (date/time, location) | {{stocked_datetime}}, {{storage_location}} |

### Section 3 — Ongoing Storage Temperature Log

[INSTRUCTION: Record per site SOP — continuous logger with periodic verification, or manual min/max readings each business day. Record actual values, not just "OK." Reset min/max after each reading if using a min/max thermometer.]

| Date | Time | Current temp | Min since last reading | Max since last reading | Within range ({{storage_conditions}})? | Initials |
|---|---|---|---|---|---|---|
| {{temp_log_date}} | {{temp_log_time}} | {{temp_current}} | {{temp_min}} | {{temp_max}} | {{temp_in_range_yn}} | {{temp_log_initials}} |

### Section 4 — Temperature Excursion / Quarantine Record

[INSTRUCTION: One block per excursion or receipt problem — in-transit or in-storage. The affected product is physically segregated and marked QUARANTINE — DO NOT DISPENSE until sponsor disposition is received in writing. The usability decision belongs to the sponsor (product stability data holder), not the site.]

| Field | Value |
|---|---|
| Excursion date(s)/time(s) detected | {{excursion_datetime}} |
| Affected lot(s) and quantity | {{excursion_lots}} / {{excursion_quantity}} |
| Excursion details (range reached, duration if known) | {{excursion_details}} |
| Product quarantined (date/time, by whom) | {{quarantine_datetime}} / {{quarantine_by}} |
| Sponsor/CTM notified (date/time, method, contact) | {{sponsor_notified_datetime}} / {{sponsor_notified_method}} / {{sponsor_contact}} |
| Sponsor disposition (release / return / destroy) and reference | {{sponsor_disposition}} / {{sponsor_disposition_ref}} [INSTRUCTION: attach the sponsor's written disposition to this log] |
| Disposition executed (date, by whom) | {{disposition_executed_date}} / {{disposition_executed_by}} |
| Root cause / corrective action (equipment excursions) | {{excursion_capa}} |

### Section 5 — Review

| | |
|---|---|
| Investigator or designee review signature | ______________________ |
| Name / role | {{reviewer_name}} / {{reviewer_role}} |
| Date | {{review_date}} |

[INSTRUCTION: Carry each released shipment's lot and quantity into Section 2 of the Investigational Product Accountability Log. Quarantined-then-rejected stock is excluded from usable balance and tracked to return/destruction in the IP Final Reconciliation and Destruction Record.]

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{protocol_number}} | study.protocol.number | ICH E6(R3) Appendix C |
| {{drug_name}} | study.product.name | 21 CFR 312.57 |
| {{investigator_name}} | site.investigator.name | 21 CFR 312.57 |
| {{site_name}} | site.name | ICH E6(R3) Appendix C |
| {{site_number}} | site.number | ICH E6(R3) Appendix C |
| {{storage_conditions}} | study.product.storage_conditions | ICH E6(R3) Appendix C |
| {{storage_location}} | site.ip_storage.location | ICH E6(R3) Appendix C |
| {{storage_equipment_id}} | site.ip_storage.equipment_id | ICH E6(R3) Appendix C |
| {{monitoring_device_id}} | site.ip_storage.monitor_id | ICH E6(R3) Appendix C |
| {{shipment_number}} | site.shipments[].consignment_number | 21 CFR 312.57 |
| {{ship_date}} | site.shipments[].ship_date | 21 CFR 312.57 |
| {{shipment_date}} | site.shipments[].received_date | 21 CFR 312.57 |
| {{receipt_time}} | site.shipments[].received_time | ICH E6(R3) Appendix C |
| {{courier_name}} | site.shipments[].courier | ICH E6(R3) Appendix C |
| {{lot_number}} | site.shipments[].lot_number | 21 CFR 312.57 |
| {{lot_expiry_date}} | study.product.lots[].expiry | ICH E6(R3) Appendix C |
| {{quantity_expected}} | site.shipments[].quantity_expected | 21 CFR 312.57 |
| {{quantity}} | site.shipments[].quantity | 21 CFR 312.57 |
| {{count_match_yn}} | site.shipments[].count_match | 21 CFR 312.57 |
| {{condition_acceptable_yn}} | site.shipments[].condition_ok | ICH E6(R3) Appendix C |
| {{transit_monitor_id}} | site.shipments[].transit_monitor_id | ICH E6(R3) Appendix C |
| {{transit_monitor_reading}} | site.shipments[].transit_monitor_reading | ICH E6(R3) Appendix C |
| {{temperature_excursions}} | site.shipments[].excursion_flag | ICH E6(R3) Appendix C |
| {{receipt_ack_date}} | site.shipments[].ack_date | 21 CFR 312.57 |
| {{receipt_ack_method}} | site.shipments[].ack_method | 21 CFR 312.57 |
| {{received_by_name}} | site.shipments[].received_by | ICH E6(R3) 2.7 |
| {{received_by_initials}} | site.staff[].initials | ICH E6(R3) Appendix C |
| {{stocked_datetime}} | site.shipments[].stocked_datetime | ICH E6(R3) Appendix C |
| {{temp_log_date}} | site.temperature_log[].date | ICH E6(R3) Appendix C |
| {{temp_log_time}} | site.temperature_log[].time | ICH E6(R3) Appendix C |
| {{temp_current}} | site.temperature_log[].current | ICH E6(R3) Appendix C |
| {{temp_min}} | site.temperature_log[].min | ICH E6(R3) Appendix C |
| {{temp_max}} | site.temperature_log[].max | ICH E6(R3) Appendix C |
| {{temp_in_range_yn}} | site.temperature_log[].in_range | ICH E6(R3) Appendix C |
| {{temp_log_initials}} | site.temperature_log[].recorded_by | ICH E6(R3) Appendix C |
| {{excursion_datetime}} | site.excursions[].detected_datetime | ICH E6(R3) Appendix C |
| {{excursion_lots}} | site.excursions[].lots | 21 CFR 312.57 |
| {{excursion_quantity}} | site.excursions[].quantity | 21 CFR 312.57 |
| {{excursion_details}} | site.excursions[].details | ICH E6(R3) Appendix C |
| {{quarantine_datetime}} | site.excursions[].quarantine_datetime | ICH E6(R3) Appendix C |
| {{quarantine_by}} | site.excursions[].quarantined_by | ICH E6(R3) Appendix C |
| {{sponsor_notified_datetime}} | site.excursions[].sponsor_notified | ICH E6(R3) Appendix C |
| {{sponsor_notified_method}} | site.excursions[].notify_method | ICH E6(R3) Appendix C |
| {{sponsor_contact}} | study.sponsor.ctm_contact | ICH E6(R3) Appendix C |
| {{sponsor_disposition}} | site.excursions[].disposition | ICH E6(R3) Appendix C |
| {{sponsor_disposition_ref}} | site.excursions[].disposition_ref | ICH E6(R3) Appendix C |
| {{disposition_executed_date}} | site.excursions[].executed_date | ICH E6(R3) Appendix C |
| {{disposition_executed_by}} | site.excursions[].executed_by | ICH E6(R3) Appendix C |
| {{excursion_capa}} | site.excursions[].capa | ICH E6(R3) Appendix C |
| {{reviewer_name}} | site.ip_log.reviewer_name | ICH E6(R3) Appendix C |
| {{reviewer_role}} | site.ip_log.reviewer_role | ICH E6(R3) Appendix C |
| {{review_date}} | site.ip_log.review_date | ICH E6(R3) Appendix C |

## Related

[[03-documents/drug-shipment-receipt-temperature-log]] · [[03-documents/drug-accountability-log]] · [[03-documents/ip-final-reconciliation-destruction]] · [[03-documents/delegation-of-authority-log]]
