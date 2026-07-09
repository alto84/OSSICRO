---
title: "Site Initiation Visit Report"
doc_id: "site-initiation-visit-report"
category: "monitoring"
governing_citations: ["21 CFR 312.53(b)", "ICH E6(R3) 3.11"]
owner: "cro"
receiver: "sponsor"
gate: "none"
status: template
updated: 2026-07-09
---

# Site Initiation Visit Report — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 312.53(b)](https://www.law.cornell.edu/cfr/text/21/312.53) (sponsor control of investigational drug shipment — the drug ships only to participating investigators, which in practice requires documented site readiness); [ICH E6(R3) §3.11](https://www.ich.org/page/efficacy-guidelines) (monitoring; §3.11.4 monitoring reports). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** The site initiation visit (SIV) report documents that, before screening begins, the site team was trained on the protocol and study procedures and that all regulatory prerequisites (IRB approval, signed 1572, executed agreements, IP logistics) were confirmed in place. It is the monitor's written record to the sponsor that the site was ready to enroll.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing.

## Template

### SITE INITIATION VISIT REPORT

| | |
|---|---|
| **Protocol number / title** | {{protocol_number}} / {{protocol_title}} |
| **Site number / name** | {{site_number}} / {{site_name}} |
| **Principal investigator** | {{investigator_name}} |
| **Visit date(s)** | {{visit_date}} |
| **Visit mode** | {{visit_mode}} [INSTRUCTION: on-site / remote (videoconference) / hybrid. If remote, state how document review was accomplished.] |
| **Monitor (author)** | {{monitor_name}}, {{monitor_title}} |
| **Report date** | {{report_date}} |

#### 1. Attendees

| Name | Role | Present for (topics/sections) |
|---|---|---|
| {{attendee_name_1}} | {{attendee_role_1}} | {{attendee_sections_1}} |

{{attendees}}

[INSTRUCTION: One row per attendee, including PI, sub-investigators, coordinators, pharmacist, and any sponsor/CRO personnel. Note any required staff absent and how make-up training will be documented.]

#### 2. Topics covered / training delivered

{{topics_covered}}

[INSTRUCTION: Mark each topic covered (Y/N/NA) and note the training material version. Standard SIV agenda:]

| Topic | Covered (Y/N/NA) | Version / notes |
|---|---|---|
| Protocol ({{protocol_version}}) — design, objectives, eligibility, visit schedule | | |
| Investigator's Brochure ({{ib_edition}}) — safety profile, expected AEs | | |
| Informed consent process and current IRB-approved ICF version | | |
| AE/SAE definitions, recording, and reporting pathway per 21 CFR 312.64(b) | | |
| Investigational product: storage, dispensing, accountability, returns | | |
| Randomization / blinding procedures (if applicable) | | |
| Source documentation and ALCOA++ expectations; eCRF completion | | |
| Delegation of authority; training documentation requirements | | |
| Protocol deviation identification and reporting | | |
| ISF / regulatory binder organization and maintenance | | |
| Monitoring plan overview: visit cadence, SDV scope, remote access | | |
| Record retention obligations (21 CFR 312.62(c)) | | |

#### 3. Regulatory readiness confirmations

| Item | Confirmed (Y/N) | Detail |
|---|---|---|
| IRB initial approval letter on file (protocol + ICF versions match) | {{irb_approval_confirmed}} | Approval date {{irb_approval_date}} |
| Form FDA 1572 signed by PI and on file | {{form_1572_confirmed}} | |
| Financial disclosure forms collected for all listed investigators | {{financial_disclosure_confirmed}} | |
| CVs, medical licenses, GCP training current for listed staff | {{staff_credentials_confirmed}} | |
| Lab certifications (CLIA/CAP) and normal ranges on file | {{lab_certification_confirmed}} | |
| Clinical trial agreement / budget executed | {{cta_confirmed}} | |
| IP received or shipment authorized; storage conditions verified | {{ip_logistics_confirmed}} | [INSTRUCTION: Under 21 CFR 312.53(b), drug may ship only to participating investigators; confirm no IP was shipped before readiness.] |
| Site authorized to begin screening | {{site_greenlight}} | Effective {{screening_start_date}} |

#### 4. Findings and observations

{{findings}}

[INSTRUCTION: Record anything observed at the SIV that requires attention — missing documents, equipment gaps, staffing concerns. If none, state "No findings."]

#### 5. Action items

| # | Action | Owner | Due date | Status |
|---|---|---|---|---|
| 1 | {{action_item_1}} | {{action_owner_1}} | {{action_due_1}} | Open |

{{action_items}}

[INSTRUCTION: Every open item must be tracked to closure at or before the first interim monitoring visit. Items blocking enrollment must be flagged and the site not activated until resolved.]

#### 6. Monitor attestation and sponsor review

Prepared by (monitor): {{monitor_name}} ____________________ Date: ________

Reviewed by (sponsor / sponsor-investigator): {{sponsor_reviewer_name}} ____________________ Date: ________

[INSTRUCTION: ICH E6(R3) §3.11.4 requires monitoring reports be provided to the sponsor in a timely manner and reviewed; document the review. Signature is a human act — OSSICRO drafts, humans sign.]

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{protocol_number}} | study.protocol.number | ICH E6(R3) 3.11.4 |
| {{protocol_title}} | study.protocol.title | ICH E6(R3) 3.11.4 |
| {{protocol_version}} | study.protocol.version | ICH E6(R3) 3.11.4 |
| {{site_number}} | site.number | ICH E6(R3) 3.11.4 |
| {{site_name}} | site.name | ICH E6(R3) 3.11.4 |
| {{investigator_name}} | site.investigator.name | 21 CFR 312.53(a) |
| {{visit_date}} | visit.siv.date | ICH E6(R3) 3.11.4 |
| {{visit_mode}} | visit.siv.mode | ICH E6(R3) 3.11.2 |
| {{monitor_name}} | visit.siv.monitor.name | ICH E6(R3) 3.11.4 |
| {{monitor_title}} | visit.siv.monitor.title | ICH E6(R3) 3.11.4 |
| {{report_date}} | visit.siv.report.date | ICH E6(R3) 3.11.4 |
| {{attendees}} | visit.siv.attendees[] | ICH E6(R3) 3.11.4 |
| {{attendee_name_1}} / {{attendee_role_1}} / {{attendee_sections_1}} | visit.siv.attendees[].name/.role/.sections | ICH E6(R3) 3.11.4 |
| {{topics_covered}} | visit.siv.topics_covered[] | ICH E6(R3) 3.11.4 |
| {{ib_edition}} | study.investigators_brochure.edition | 21 CFR 312.55 |
| {{irb_approval_confirmed}} | site.regulatory.irb_approval.on_file | 21 CFR 312.66; 21 CFR 56.109(e) |
| {{irb_approval_date}} | site.regulatory.irb_approval.date | 21 CFR 56.109(e) |
| {{form_1572_confirmed}} | site.regulatory.form_1572.on_file | 21 CFR 312.53(c)(1) |
| {{financial_disclosure_confirmed}} | site.regulatory.financial_disclosure.on_file | 21 CFR 54.4 |
| {{staff_credentials_confirmed}} | site.regulatory.staff_credentials.current | 21 CFR 312.53(c)(2) |
| {{lab_certification_confirmed}} | site.regulatory.lab_certification.on_file | 42 CFR Part 493 |
| {{cta_confirmed}} | site.contracts.cta.executed | ICH E6(R3) Annex 1 |
| {{ip_logistics_confirmed}} | site.ip.logistics.confirmed | 21 CFR 312.53(b) |
| {{site_greenlight}} | site.status.screening_authorized | 21 CFR 312.53(b) |
| {{screening_start_date}} | site.status.screening_start_date | 21 CFR 312.53(b) |
| {{findings}} | visit.siv.findings[] | ICH E6(R3) 3.11.4 |
| {{action_items}} | visit.siv.action_items[] | ICH E6(R3) 3.11.4 |
| {{action_item_1}} / {{action_owner_1}} / {{action_due_1}} | visit.siv.action_items[].text/.owner/.due | ICH E6(R3) 3.11.4 |
| {{sponsor_reviewer_name}} | study.monitoring.report_reviewer.name | ICH E6(R3) 3.11.4 |

## Related

- [[03-documents/site-initiation-visit-report]]
- [[03-documents/risk-based-monitoring-plan]]
- [[03-documents/interim-monitoring-visit-report]]
- [[03-documents/form-fda-1572-statement-of-investigator]]
- [[03-documents/irb-initial-approval-letter]]
- [[03-documents/delegation-of-authority-log]]
