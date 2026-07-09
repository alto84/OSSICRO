---
title: "Study Budget with Fair-Market-Value Basis"
doc_id: "study-budget-fmv"
category: "contracts"
governing_citations: ["42 CFR 403.904 (Open Payments context)", "ICH E6(R3) Annex 1 (Sponsor)"]
owner: "sponsor-investigator"
receiver: "sponsor"
gate: "none"
status: template
updated: 2026-07-09
---

# Study Budget with Fair-Market-Value Basis — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [42 CFR 403.904](https://www.law.cornell.edu/cfr/text/42/403.904) (Open Payments — research payments by applicable manufacturers to covered recipients are reportable, so the budget must be structured and documented for accurate reporting); [ICH E6(R3)](https://www.ich.org/page/efficacy-guidelines) Annex 1 (Sponsor — financial aspects of the trial should be documented in an agreement between the sponsor and the investigator/institution). Documenting a fair-market-value (FMV) basis is also the standard compliance safeguard against remuneration that could implicate the federal Anti-Kickback Statute (42 U.S.C. § 1320a-7b(b)) — that analysis belongs to counsel, not to this template. This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** The study budget itemizes every payment the sponsor will make to the site for conducting the protocol — per-subject procedure costs, fixed startup fees, and invoiceable items — and records the FMV methodology behind each figure. It is negotiated during startup and attached as an exhibit to the [[clinical-trial-agreement]].

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing. Every dollar figure must trace to a stated FMV basis; a budget line without a basis is incomplete. Counsel and the institution's clinical-trials office review before execution.

## Template

### STUDY BUDGET — Exhibit A to Clinical Trial Agreement

**Protocol No.:** {{protocol_number}}
**Protocol Title:** {{protocol_title}}
**Site:** {{site_name}}
**Budget Version:** {{budget_version}} — {{budget_date}}
**Currency:** {{currency}}
**Payee (legal entity and tax ID on file):** {{payee_entity}}

[INSTRUCTION: The payee should be the contracting entity (institution or practice), not the investigator personally, unless the CTA expressly provides otherwise. Personal payments to physicians change the Open Payments reporting character and raise additional compliance review.]

#### 1. Per-Subject Budget (procedure grid)

{{budget_lines}}

[INSTRUCTION: Expand {{budget_lines}} into a grid with one row per protocol-required procedure per visit, matching the protocol's schedule of activities exactly — no procedure in the budget that is not in the protocol, and no protocol-required procedure missing from the budget. Example structure:]

| Visit | Procedure | CPT/basis code | Unit cost | FMV source | Payable on |
|---|---|---|---|---|---|
| Screening | Informed consent discussion | — (staff time) | {{unit_cost}} | {{fmv_source}} | Verified eCRF entry |
| Screening | Physical exam | 99203 | {{unit_cost}} | {{fmv_source}} | Verified eCRF entry |
| Screening | Safety labs (CBC, CMP) | 85025 / 80053 | {{unit_cost}} | {{fmv_source}} | Verified eCRF entry |
| Cycle 1 Day 1 | IP administration and observation | — (staff time) | {{unit_cost}} | {{fmv_source}} | Verified eCRF entry |
| ... | ... | ... | ... | ... | ... |

**Total per completed subject:** {{per_subject_total}}
**Screen-failure reimbursement:** {{screen_fail_amount}} per screen failure, capped at {{screen_fail_cap}} screen failures. [INSTRUCTION: pay only for procedures actually performed before failure.]

#### 2. Fixed and Startup Fees (non-refundable unless stated)

| Item | Amount | FMV basis | Trigger |
|---|---|---|---|
| Site startup / regulatory preparation | {{startup_fee}} | {{fmv_source}} | CTA execution |
| IRB fees (initial / continuing / amendment) | Pass-through at cost | Invoice from IRB | IRB invoice |
| Pharmacy setup and close-out | {{pharmacy_fee}} | {{fmv_source}} | SIV complete / close-out complete |
| Records archival ({{retention_period}} retention per 21 CFR 312.62(c)) | {{archival_fee}} | {{fmv_source}} | Study close-out |
| Administrative overhead | {{overhead_percent}}% on {{overhead_base}} | Institutional published rate | Applied per payment |

#### 3. Invoiceable / Conditional Items

| Item | Amount | Condition |
|---|---|---|
| Unscheduled safety visit | {{unscheduled_visit_fee}} | Documented unscheduled visit |
| SAE reporting (per event, beyond first) | {{sae_fee}} | Submitted SAE report |
| Re-consent following amendment | {{reconsent_fee}} | IRB-approved amended ICF signed |
| Subject travel/parking reimbursement | Pass-through at cost, up to {{subject_travel_cap}} per visit | Receipts |

[INSTRUCTION: Subject reimbursement is repayment for actual expense, not compensation for participation; if subject stipends are used, list them separately, keep them consistent with the IRB-approved consent, and confirm the IRB reviewed the amounts (undue-influence review, 21 CFR 50.20).]

#### 4. Payment Terms

- Payment cadence: {{payment_cadence}} (e.g., quarterly, based on verified completed visits), net {{payment_net_days}} days.
- Holdback: {{holdback_percent}}% released at close-out after query resolution and IP reconciliation.
- No payment is contingent on study outcome, on enrollment of any particular patient, or on the volume or value of referrals.

#### 5. Fair-Market-Value Basis and Methodology

{{fmv_basis}}

[INSTRUCTION: Expand {{fmv_basis}} into a short memo covering: (a) benchmark sources used (e.g., current-year Medicare Physician Fee Schedule / Clinical Lab Fee Schedule rates for procedure costs; commercial FMV compilations or documented institutional charge masters for coordinator and PI time), with version/year for each; (b) hourly-rate build-up for PI, subinvestigator, and coordinator effort (rate × estimated minutes per activity), citing the salary survey or benchmark used; (c) geographic adjustment, if any; (d) a statement that rates were set in advance, in writing, at arm's length, and without regard to referrals; (e) who performed the FMV assessment and the date. This documentation is what makes the budget defensible in an Open Payments audit or AKS inquiry — keep the worksheets in the TMF.]

**Open Payments notice.** If the sponsor is an applicable manufacturer, research payments under this budget are reportable under 42 CFR 403.904, attributed to the study and to covered-recipient physicians named on the record; the parties agree to exchange the information reasonably needed for accurate reporting (study registration number {{nct_number}}, principal investigator NPI, payment aggregation).

#### 6. Approval

| Prepared by | Reviewed (site) | Reviewed (sponsor) |
|---|---|---|
| Name: {{preparer_name}} | Name: {{site_reviewer_name}} | Name: {{sponsor_reviewer_name}} |
| Date: ____________ | Date: ____________ | Date: ____________ |

[INSTRUCTION: The budget takes legal effect only as an executed exhibit to the CTA; signatures on the CTA govern. These review lines document human verification of the figures and FMV basis — a human act OSSICRO cannot perform.]

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{protocol_number}} | study.protocol.number | ICH E6(R3) Annex 1 |
| {{protocol_title}} | study.protocol.title | — |
| {{site_name}} | site.name | — |
| {{budget_version}} | contracts.budget.version | — |
| {{budget_date}} | contracts.budget.date | — |
| {{currency}} | contracts.budget.currency | — |
| {{payee_entity}} | contracts.budget.payee_entity | 42 CFR 403.904 (recipient identification) |
| {{budget_lines}} | contracts.budget.lines[] | ICH E6(R3) Annex 1 (financial aspects documented) |
| {{unit_cost}} | contracts.budget.lines[].unit_cost | — |
| {{fmv_source}} | contracts.budget.lines[].fmv_source | 42 CFR 403.904 context |
| {{per_subject_total}} | contracts.budget.per_subject_total | — |
| {{screen_fail_amount}} | contracts.budget.screen_fail_amount | — |
| {{screen_fail_cap}} | contracts.budget.screen_fail_cap | — |
| {{startup_fee}} | contracts.budget.startup_fee | — |
| {{pharmacy_fee}} | contracts.budget.pharmacy_fee | — |
| {{retention_period}} | closeout.retention_period | 21 CFR 312.62(c) |
| {{archival_fee}} | contracts.budget.archival_fee | — |
| {{overhead_percent}} | contracts.budget.overhead_percent | — |
| {{overhead_base}} | contracts.budget.overhead_base | — |
| {{unscheduled_visit_fee}} | contracts.budget.unscheduled_visit_fee | — |
| {{sae_fee}} | contracts.budget.sae_fee | — |
| {{reconsent_fee}} | contracts.budget.reconsent_fee | — |
| {{subject_travel_cap}} | contracts.budget.subject_travel_cap | 21 CFR 50.20 (IRB undue-influence review) |
| {{payment_cadence}} | contracts.budget.payment_cadence | — |
| {{payment_net_days}} | contracts.budget.payment_net_days | — |
| {{holdback_percent}} | contracts.budget.holdback_percent | — |
| {{fmv_basis}} | contracts.budget.fmv_basis | 42 CFR 403.904 context; AKS documentation practice |
| {{nct_number}} | registration.nct_number | 42 CFR 403.904 (research payment reporting) |
| {{preparer_name}} | contracts.budget.preparer_name | — |
| {{site_reviewer_name}} | contracts.budget.site_reviewer_name | — |
| {{sponsor_reviewer_name}} | contracts.budget.sponsor_reviewer_name | — |

## Related

- [[clinical-trial-agreement-and-budget]] — wiki document page
- [[clinical-trial-agreement]] — parent agreement (this budget is Exhibit A)
- [[site-activation]] — lifecycle stage gated by executed CTA + budget
- [[sponsor-cro-site-coordination]] — coordination context
