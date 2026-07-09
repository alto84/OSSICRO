---
title: "Close-Out Visit Report"
doc_id: "close-out-visit-report"
category: "monitoring"
governing_citations: ["ICH E6(R3) 3.11"]
owner: "cro"
receiver: "sponsor"
gate: "none"
status: template
updated: 2026-07-09
---

# Close-Out Visit Report — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [ICH E6(R3) §3.11](https://www.ich.org/page/efficacy-guidelines) (monitoring; §3.11.4 monitoring reports). Related obligations verified at close-out: [21 CFR 312.59](https://www.law.cornell.edu/cfr/text/21/312.59) (disposition of unused drug), [21 CFR 312.62(c)](https://www.law.cornell.edu/cfr/text/21/312.62) (investigator record retention), [21 CFR 312.66](https://www.law.cornell.edu/cfr/text/21/312.66) (final report to the IRB). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** The close-out visit (COV) report documents the final monitoring visit at a site after the last subject completes: reconciliation of investigational product and data, resolution or disposition of all outstanding items, and confirmation that the site understands its record-retention and IRB-notification obligations. It is the record that the site was closed in an orderly, GCP-compliant manner.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing.

## Template

### CLOSE-OUT VISIT REPORT

| | |
|---|---|
| **Protocol number / title** | {{protocol_number}} / {{protocol_title}} |
| **Site number / name** | {{site_number}} / {{site_name}} |
| **Principal investigator** | {{investigator_name}} |
| **Visit date(s)** | {{visit_date}} |
| **Visit mode** | {{visit_mode}} |
| **Monitor (author)** | {{monitor_name}}, {{monitor_title}} |
| **Report date** | {{report_date}} |
| **Reason for close-out** | {{closeout_reason}} [INSTRUCTION: study completed / site completed enrollment and follow-up / early termination (state cause).] |

#### 1. Final site status

| Metric | Value |
|---|---|
| Subjects screened / enrolled | {{subjects_screened}} / {{subjects_enrolled}} |
| Subjects completed / withdrawn | {{subjects_completed}} / {{subjects_withdrawn}} |
| Date of last subject's last visit | {{last_subject_last_visit}} |

#### 2. Reconciliation summary

{{reconciliation_summary}}

[INSTRUCTION: Address each area with an explicit closed/open status.]

| Area | Status | Detail |
|---|---|---|
| Investigational product: all IP reconciled (received = dispensed + returned + destroyed); final reconciliation/destruction record complete per 21 CFR 312.59 | {{ip_reconciliation_status}} | [[03-documents/ip-final-reconciliation-destruction]] |
| Data: all eCRF pages complete; all queries resolved; outstanding SDV per plan completed | {{data_reconciliation_status}} | |
| Safety: all AEs/SAEs reported and reconciled; no open safety follow-up owed by the site | {{safety_reconciliation_status}} | |
| Protocol deviations: log final and reconciled against sponsor records | {{deviation_reconciliation_status}} | |
| Financial disclosure: updated disclosures collected (covering 1 year post-study per 21 CFR 54.4(b)) commitment confirmed | {{financial_disclosure_status}} | |
| ISF / regulatory binder: complete, final versions filed, ready for archival | {{isf_status}} | |
| Biological samples / equipment: returned or dispositioned per protocol and CTA | {{samples_equipment_status}} | |

#### 3. Site obligations confirmed at close-out

| Obligation | Confirmed (Y/N) | Detail |
|---|---|---|
| Record retention: {{retention_period}} per 21 CFR 312.62(c) (2 years after marketing approval, or 2 years after investigation discontinued and FDA notified); site instructed not to destroy or relocate records without sponsor notice | {{retention_confirmed}} | Archive location: {{archive_location}} |
| Final report to IRB per 21 CFR 312.66 | {{irb_final_report_status}} | [[03-documents/final-irb-notification-of-completion]] |
| Site contact for post-closure queries identified | {{post_closure_contact}} | |

#### 4. Outstanding items

{{outstanding_items}}

| # | Item | Owner | Resolution path | Target date |
|---|---|---|---|---|
| 1 | {{outstanding_item_1}} | {{outstanding_owner_1}} | {{outstanding_resolution_1}} | {{outstanding_due_1}} |

[INSTRUCTION: A site should not be closed with open critical items. If any item remains open, state why closure proceeds anyway and who tracks the item to resolution post-closure. If none, state "No outstanding items; site closed clean."]

#### 5. Close-out determination

{{closeout_determination}}

[INSTRUCTION: One paragraph: the monitor's conclusion that site close-out activities are complete (or complete-except-as-listed in §4), and the effective site closure date {{site_closure_date}}.]

#### 6. Monitor attestation and sponsor review

Prepared by (monitor): {{monitor_name}} ____________________ Date: ________

Reviewed by (sponsor / sponsor-investigator): {{sponsor_reviewer_name}} ____________________ Date: ________

[INSTRUCTION: ICH E6(R3) §3.11.4 requires the report be provided to the sponsor and reviewed. Signatures are human acts — OSSICRO drafts, humans sign.]

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{protocol_number}} | study.protocol.number | ICH E6(R3) 3.11.4 |
| {{protocol_title}} | study.protocol.title | ICH E6(R3) 3.11.4 |
| {{site_number}} | site.number | ICH E6(R3) 3.11.4 |
| {{site_name}} | site.name | ICH E6(R3) 3.11.4 |
| {{investigator_name}} | site.investigator.name | ICH E6(R3) 3.11.4 |
| {{visit_date}} | visit.cov.date | ICH E6(R3) 3.11.4 |
| {{visit_mode}} | visit.cov.mode | ICH E6(R3) 3.11.2 |
| {{monitor_name}} | visit.cov.monitor.name | ICH E6(R3) 3.11.4 |
| {{monitor_title}} | visit.cov.monitor.title | ICH E6(R3) 3.11.4 |
| {{report_date}} | visit.cov.report.date | ICH E6(R3) 3.11.4 |
| {{closeout_reason}} | site.closeout.reason | ICH E6(R3) 3.11.4 |
| {{subjects_screened}} | site.enrollment.screened | ICH E6(R3) 3.11.4 |
| {{subjects_enrolled}} | site.enrollment.enrolled | ICH E6(R3) 3.11.4 |
| {{subjects_completed}} | site.enrollment.completed | ICH E6(R3) 3.11.4 |
| {{subjects_withdrawn}} | site.enrollment.withdrawn | ICH E6(R3) 3.11.4 |
| {{last_subject_last_visit}} | site.enrollment.last_subject_last_visit | ICH E6(R3) 3.11.4 |
| {{reconciliation_summary}} | visit.cov.reconciliation_summary | ICH E6(R3) 3.11.4 |
| {{ip_reconciliation_status}} | site.closeout.ip_reconciliation.status | 21 CFR 312.59 |
| {{data_reconciliation_status}} | site.closeout.data_reconciliation.status | ICH E6(R3) 3.11.4 |
| {{safety_reconciliation_status}} | site.closeout.safety_reconciliation.status | 21 CFR 312.64(b) |
| {{deviation_reconciliation_status}} | site.closeout.deviation_reconciliation.status | ICH E6(R3) Appendix C |
| {{financial_disclosure_status}} | site.closeout.financial_disclosure.status | 21 CFR 54.4(b) |
| {{isf_status}} | site.closeout.isf.status | ICH E6(R3) Appendix C |
| {{samples_equipment_status}} | site.closeout.samples_equipment.status | ICH E6(R3) 3.11.4 |
| {{retention_period}} | study.records.retention_period | 21 CFR 312.62(c) |
| {{retention_confirmed}} | site.closeout.retention_confirmed | 21 CFR 312.62(c) |
| {{archive_location}} | site.closeout.archive_location | 21 CFR 312.62(c) |
| {{irb_final_report_status}} | site.closeout.irb_final_report.status | 21 CFR 312.66 |
| {{post_closure_contact}} | site.closeout.post_closure_contact | ICH E6(R3) 3.11.4 |
| {{outstanding_items}} | visit.cov.outstanding_items[] | ICH E6(R3) 3.11.4 |
| {{outstanding_item_1}} / {{outstanding_owner_1}} / {{outstanding_resolution_1}} / {{outstanding_due_1}} | visit.cov.outstanding_items[].text/.owner/.resolution/.due | ICH E6(R3) 3.11.4 |
| {{closeout_determination}} | visit.cov.determination | ICH E6(R3) 3.11.4 |
| {{site_closure_date}} | site.closeout.closure_date | ICH E6(R3) 3.11.4 |
| {{sponsor_reviewer_name}} | study.monitoring.report_reviewer.name | ICH E6(R3) 3.11.4 |

## Related

- [[03-documents/close-out-visit-report]]
- [[03-documents/risk-based-monitoring-plan]]
- [[03-documents/interim-monitoring-visit-report]]
- [[03-documents/ip-final-reconciliation-destruction]]
- [[03-documents/final-irb-notification-of-completion]]
- [[03-documents/record-retention-and-archival-statement]]
