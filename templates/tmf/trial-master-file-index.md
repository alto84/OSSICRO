---
title: "Trial Master File Index"
doc_id: "trial-master-file-index"
category: "tmf"
governing_citations: ["ICH E6(R3) Appendix C", "21 CFR 312.57"]
owner: "sponsor-investigator"
receiver: "sponsor"
gate: "none"
status: template
updated: 2026-07-09
---

# Trial Master File Index — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [ICH E6(R3) Appendix C — Essential Records for the Conduct of a Clinical Trial](https://www.ich.org/page/efficacy-guidelines) (Step 4 final guideline, January 2025) and [21 CFR 312.57](https://www.law.cornell.edu/cfr/text/21/312.57) (sponsor recordkeeping: drug disposition, financial-interest records, and the §312.57(c) retention period). Sponsor record-access obligations under [21 CFR 312.58](https://www.law.cornell.edu/cfr/text/21/312.58) also apply. This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** The Trial Master File (TMF) index is the sponsor-side master filing plan for the essential records that demonstrate sponsor compliance with 21 CFR Part 312 Subpart D and ICH E6(R3), and that permit reconstruction of the trial's conduct. In a sponsor-investigator study the same person carries both filing obligations; this index covers the sponsor-role records, cross-referencing (not duplicating) the Investigator Site File where E6(R3) Appendix C files a record in both places.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing. For a single-site sponsor-investigator IND, decide up front whether the TMF and ISF are physically combined; if combined, complete the filing-location map so each Appendix C record still has exactly one declared original. Where an obligation has been transferred to a CRO under 21 CFR 312.52, the TORO defines who holds which records — reflect that in the "Held by" column.

## Template

**TRIAL MASTER FILE — INDEX**

| | |
|---|---|
| Study ID | {{study_id}} |
| Protocol number | {{protocol_number}} |
| Protocol title | {{protocol_title}} |
| IND number | {{ind_number}} |
| Sponsor-investigator | {{sponsor_investigator_name}} |
| Index version / date | {{index_version}} / {{version_date}} |
| TMF custodian | {{tmf_custodian}} |
| Format | {{tmf_format}} [INSTRUCTION: paper, eTMF platform name, or hybrid. If hybrid, each section below must state where its original lives.] |
| TMF/ISF structure | {{tmf_isf_structure}} [INSTRUCTION: "combined" (single binder set with role-tagged tabs) or "separate". If combined, retain the ISF index as the site-role filing plan and this index as the sponsor-role plan.] |

**Filing plan — sections**

{{index_sections}}

[INSTRUCTION: The table below is the reference section set for a sponsor-investigator IND TMF. Replace or extend as required; every sponsor-side essential record in ICH E6(R3) Appendix C must map to exactly one section. Mark empty-at-startup sections "Pending", not deleted.]

| Sec. | Section | Contents (essential records) | Held by | Status |
|---|---|---|---|---|
| 1 | IND submissions | Form FDA 1571 (all serial submissions) with serial-number log; IND application content per 21 CFR 312.23; protocol amendments (312.30); information amendments (312.31); annual reports (312.33); withdrawal/completion notices (312.38) | {{section_holder}} | {{section_status}} |
| 2 | FDA correspondence | FDA acknowledgment letters (IND number assignment), clinical hold or comment letters, meeting requests/minutes, records of significant contacts | {{section_holder}} | {{section_status}} |
| 3 | Protocol | Final signed protocol, all amendments, version log | {{section_holder}} | {{section_status}} |
| 4 | Investigator's Brochure | All IB editions with distribution records (21 CFR 312.55) | {{section_holder}} | {{section_status}} |
| 5 | Investigator selection and qualification | Signed 1572(s), CVs/licenses, site feasibility/qualification records (21 CFR 312.53) | {{section_holder}} | {{section_status}} |
| 6 | Financial interests | Financial disclosure forms and supporting records — retained per 21 CFR 312.57(b) for 2 years after approval of the application [INSTRUCTION: 312.57(b) applies to the sponsor's Part 54 records for each participating investigator.] | {{section_holder}} | {{section_status}} |
| 7 | IRB | IRB approvals, approved consent versions, continuing-review approvals, IRB correspondence | {{section_holder}} | {{section_status}} |
| 8 | Agreements | Clinical trial agreement(s), TORO (21 CFR 312.52) if any obligations transferred, budget/FMV documentation, vendor agreements, insurance/indemnity documents | {{section_holder}} | {{section_status}} |
| 9 | Investigational product — sponsor records | Manufacturing/CMC references, IP disposition records showing receipt, shipment, and disposition of the drug (21 CFR 312.57(a)): dates, quantities, lot/batch numbers per shipment and recipient; labeling records (21 CFR 312.6) | {{section_holder}} | {{section_status}} |
| 10 | Safety | Safety management/pharmacovigilance plan; SAE reports received from investigator(s); IND safety reports filed (21 CFR 312.32) with distribution records; safety database outputs | {{section_holder}} | {{section_status}} |
| 11 | Monitoring | Risk-based monitoring plan; SIV, interim, and close-out visit reports; monitoring oversight and escalation records (21 CFR 312.50, 312.56(a)) | {{section_holder}} | {{section_status}} |
| 12 | DSMB / safety oversight | DSMB charter, meeting minutes and recommendations, sponsor responses | {{section_holder}} | {{section_status}} |
| 13 | Data management | Blank CRF/eCRF versions, data management plan, EDC validation/audit-trail documentation, database lock record | {{section_holder}} | {{section_status}} |
| 14 | Statistics | SAP versions with sign-off records, randomization documentation (if applicable), interim analysis outputs | {{section_holder}} | {{section_status}} |
| 15 | Registration and results | ClinicalTrials.gov registration record, updates, results submission, Form FDA 3674 copies | {{section_holder}} | {{section_status}} |
| 16 | Reports | Clinical study report (ICH E3); publications | {{section_holder}} | {{section_status}} |
| 17 | Close-out and retention | IP final reconciliation/destruction record (21 CFR 312.59), close-out visit report, record-retention and archival statement | {{section_holder}} | {{section_status}} |

**Filing-location map (combined TMF/ISF only)**

[INSTRUCTION: complete only if {{tmf_isf_structure}} = "combined". List each Appendix C record type filed in both sponsor and investigator files and declare the single original location.]

| Record type | Original filed in | Cross-reference |
|---|---|---|
| {{shared_record_type}} | {{original_location}} | {{cross_reference}} |

**Retention.** Sponsor records and reports required by Part 312 are retained for 2 years after a marketing application is approved for the drug for the indication under investigation, or, if not approved (or the application is discontinued), until 2 years after shipment and delivery of the drug for investigational use is discontinued and FDA has been so notified (21 CFR 312.57(c)). Retention custodian: {{retention_custodian}}; archive location: {{archive_location}}.

**Version history**

| Version | Date | Description of change | Updated by |
|---|---|---|---|
| {{index_version}} | {{version_date}} | {{change_description}} | {{updated_by}} |

Prepared by: {{preparer_name}}, {{preparer_role}} — Date: {{preparation_date}}
Reviewed by (sponsor-investigator): {{sponsor_investigator_name}} — Date: {{si_review_date}}

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{study_id}} | study_id | ICH E6(R3) Appendix C |
| {{protocol_number}} | protocol_number | ICH E6(R3) Appendix C |
| {{protocol_title}} | title | ICH E6(R3) Appendix C |
| {{ind_number}} | ind_number | 21 CFR 312.57 |
| {{sponsor_investigator_name}} | investigator.name | 21 CFR 312.3 (sponsor-investigator) |
| {{index_sections}} | tmf.index_sections | ICH E6(R3) Appendix C |
| {{index_version}} | tmf.index_version | ICH E6(R3) 4 (records management) |
| {{version_date}} | tmf.version_date | ICH E6(R3) 4 (records management) |
| {{tmf_custodian}} | tmf.custodian | ICH E6(R3) Annex 1 (Sponsor) |
| {{tmf_format}} | tmf.format | ICH E6(R3) 4.2 |
| {{tmf_isf_structure}} | tmf.isf_structure | ICH E6(R3) Appendix C |
| {{section_holder}} | tmf.sections[].holder | 21 CFR 312.52 (if transferred) |
| {{section_status}} | tmf.sections[].status | ICH E6(R3) Appendix C |
| {{shared_record_type}} | tmf.location_map[].record_type | ICH E6(R3) Appendix C |
| {{original_location}} | tmf.location_map[].original_location | ICH E6(R3) 4.2 |
| {{cross_reference}} | tmf.location_map[].cross_reference | ICH E6(R3) 4.2 |
| {{retention_custodian}} | tmf.retention.custodian | 21 CFR 312.57(c) |
| {{archive_location}} | tmf.retention.archive_location | 21 CFR 312.57(c) |
| {{change_description}} | tmf.versions[].change_description | ICH E6(R3) 4.2 |
| {{updated_by}} | tmf.versions[].updated_by | ICH E6(R3) 4.2 |
| {{preparer_name}} | tmf.preparer.name | ICH E6(R3) Annex 1 (Sponsor) |
| {{preparer_role}} | tmf.preparer.role | ICH E6(R3) Annex 1 (Sponsor) |
| {{preparation_date}} | tmf.preparation_date | ICH E6(R3) 4.2 |
| {{si_review_date}} | tmf.si_review_date | ICH E6(R3) Annex 1 (Sponsor) |

## Related

- [[03-documents/regulatory-binder-isf-index]] — wiki page covering the site-side/sponsor-side essential-records index pair
- [[03-documents/startup-tmf-checklist]], [[03-documents/conduct-tmf-checklist]], [[03-documents/closeout-tmf-checklist]] — phase-by-phase essential-records checklists
- [[02-lifecycle/record-retention-and-archival]] — retention obligations and archival workflow
- [[04-coordination/sponsor-cro-site-coordination]] — who holds which records when obligations are transferred
- Companion site-side index: `templates/tmf/regulatory-binder-isf-index.md` (doc_id `regulatory-binder-isf-index`)
