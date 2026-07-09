---
title: "Investigator's Brochure"
doc_id: "investigators-brochure"
category: "ind-application"
governing_citations: ["21 CFR 312.23(a)(5)", "21 CFR 312.55", "ICH E6(R3) Appendix A"]
owner: "sponsor"
receiver: "investigator"
gate: "none"
status: template
updated: 2026-07-09
---

# Investigator's Brochure  — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 312.23(a)(5)](https://www.law.cornell.edu/cfr/text/21/312.23) (IB content within the IND); [21 CFR 312.55](https://www.law.cornell.edu/cfr/text/21/312.55) (sponsor duty to furnish and update the IB); [ICH E6(R3) Appendix A](https://www.ich.org/page/efficacy-guidelines) (Investigator's Brochure structure and content). This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** The Investigator's Brochure (IB) is the compilation of the clinical and nonclinical data on the investigational product relevant to its study in humans. It is how the sponsor discharges its 21 CFR 312.55 duty to inform each investigator, it is a required component of the IND (21 CFR 312.23(a)(5)), and it is the **reference safety information (RSI)** against which expectedness is judged for [[ind-safety-report-7-15-day|IND safety reporting]] and against which [[informed-consent-form-part50|informed-consent]] risk disclosures are checked.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing. For a lawfully marketed drug studied in a new use, the current FDA-approved package insert may substitute for a from-scratch IB where it adequately conveys the 312.23(a)(5) content (21 CFR 312.55(a); 312.23(a)(5)(ii)) — see the marketed-drug note.

## Template

**INVESTIGATOR'S BROCHURE**

- **Investigational product:** {{drug_name}}
- **Edition / version:** {{edition}}
- **Edition date:** {{edition_date}}
- **Sponsor:** {{sponsor_name}}
- **Confidentiality:** This document contains confidential information of the sponsor. It is provided for the use of investigators and their study teams and IRB/IEC and must not be disclosed without sponsor authorization.
- **Supersedes:** {{prior_edition}}   [INSTRUCTION: Reference the prior edition/date this IB replaces; write "Not applicable — first edition" for the initial IB.]

[INSTRUCTION: Structure below follows ICH E6(R3) Appendix A and maps each section to the required content of 21 CFR 312.23(a)(5). Where full data volumes exist, summarize here and cross-reference the source reports; tabular integrated summaries are preferred over raw data.]

### 1. Summary
{{ib_summary}}
[INSTRUCTION: A concise summary highlighting the significant physical, chemical, pharmaceutical, pharmacological, toxicological, pharmacokinetic, metabolic, and clinical information available that is relevant to the stage of clinical development.]

### 2. Introduction
{{ib_introduction}}
[INSTRUCTION: The chemical/generic name of the drug substance, active ingredients, pharmacological class and expected position within it, the rationale for the research, and the anticipated prophylactic, therapeutic, or diagnostic indication(s). State the general approach to evaluating the drug.]

### 3. Physical, chemical, and pharmaceutical properties and formulation
{{ib_physical_chemical}}
[INSTRUCTION: Describe the drug substance (structural formula if known), and the formulation, including excipients where relevant to safety, and storage/handling instructions.]

### 4. Nonclinical studies

#### 4.1 Nonclinical pharmacology
{{ib_nonclinical_pharmacology}}

#### 4.2 Pharmacokinetics and product metabolism in animals
{{ib_animal_pk}}

#### 4.3 Toxicology
{{pharm_tox_summary}}
[INSTRUCTION: Summarize the pharmacological and toxicological effects in animals (single-dose, repeat-dose, genotoxicity, carcinogenicity where available, reproductive toxicity, special toxicity), organized by species and study, in a form that lets the investigator make an unbiased risk assessment. This section carries the 21 CFR 312.23(a)(5)(ii) pharmacology/toxicology content and supports the sponsor's "reasonably safe to proceed" conclusion.]

### 5. Effects in humans
{{human_effects_summary}}
[INSTRUCTION: Summarize the known effects of the investigational product in humans — pharmacokinetics and metabolism; safety and efficacy from prior clinical studies; and marketing experience in countries where the drug has been marketed or withdrawn for safety/effectiveness reasons (21 CFR 312.23(a)(5)(ii)). Reprints of key published prior studies may be appended. For a first-in-human product, state that there is no prior human experience and point to the nonclinical basis.]

### 6. Summary of data and guidance for the investigator — risks, side effects, and special monitoring
{{ib_risk_and_guidance}}
[INSTRUCTION: This is the load-bearing risk section. Describe the possible risks and adverse reactions anticipated on the basis of prior experience with the drug and related drugs, and the precautions or special monitoring to be done as part of the investigational use (21 CFR 312.23(a)(5)(ii)). Provide guidance to the investigator on recognition and management of possible overdose and adverse reactions. This section functions as the Reference Safety Information (RSI) for expectedness determinations.]

> [!note] Marketed-drug substitution
> Where {{drug_name}} is a lawfully marketed drug studied for a new use under a sponsor-investigator IND, the current FDA-approved package insert (prescribing information) may be submitted in place of a from-scratch IB, provided it adequately conveys the pharmacology, toxicology, prior human experience, and risk information required by 21 CFR 312.23(a)(5). Attach the current label and add an IND-specific supplement covering any new-use risk the label does not address (21 CFR 312.55(a)).

> [!note] Ongoing update duty (21 CFR 312.55(b))
> The IB is not static. The sponsor must keep each participating investigator informed of new observations — particularly adverse effects and safe use — through revised editions or interim letters, and new safety information reportable under 21 CFR 312.32 must reach investigators. Review at least annually and revise as significant new information emerges (ICH E6(R3)). Whether a serious adverse reaction is "unexpected" relative to this IB — and therefore triggers an expedited [[ind-safety-report-7-15-day|IND safety report]] — is a medical judgment of the qualified [[medical-monitor]], not a determination OSSICRO makes.

## Fields
| placeholder | source (study-record path) | citation |
|---|---|---|
| {{drug_name}} | study.drug.name | 21 CFR 312.23(a)(5)(ii)(a) |
| {{edition}} | study.ib.edition | ICH E6(R3) App. A |
| {{edition_date}} | study.ib.edition_date | ICH E6(R3) App. A |
| {{sponsor_name}} | study.sponsor.name | 21 CFR 312.55(a) |
| {{prior_edition}} | study.ib.prior_edition | ICH E6(R3) App. A |
| {{ib_summary}} | study.ib.summary | ICH E6(R3) App. A |
| {{ib_introduction}} | study.ib.introduction | ICH E6(R3) App. A |
| {{ib_physical_chemical}} | study.ib.physical_chemical | 21 CFR 312.23(a)(5)(ii)(a) |
| {{ib_nonclinical_pharmacology}} | study.ib.nonclinical_pharmacology | 21 CFR 312.23(a)(5)(ii)(b) |
| {{ib_animal_pk}} | study.ib.animal_pk | 21 CFR 312.23(a)(5)(ii)(c) |
| {{pharm_tox_summary}} | study.ib.toxicology_summary | 21 CFR 312.23(a)(5)(ii)(b) |
| {{human_effects_summary}} | study.ib.human_effects_summary | 21 CFR 312.23(a)(5)(ii)(d)-(e) |
| {{ib_risk_and_guidance}} | study.ib.risk_and_guidance | 21 CFR 312.23(a)(5)(ii)(f) |

## Related
- [[investigators-brochure]]
- [[ind-application-312-23]]
- [[ind-introductory-statement]]
- [[informed-consent-form-part50]]
- [[safety-management-plan]]
- [[ind-safety-report-7-15-day]]
- [[ind-annual-report-312-33]]
- [[medical-monitor]]
- [[sponsor]]
- [[non-delegable-functions-and-gates]]
