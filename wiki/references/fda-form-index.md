---
title: "FDA Form Index"
section: "references"
status: confirmed
governing_authority:
  - "21 CFR 312.23(a)(1) (Form 1571); 21 CFR 312.53(c) (Form 1572); 21 CFR Part 54 (Forms 3454/3455); 21 CFR 312.32 (Form 3500A); 21 CFR 312.310 (Form 3926); 42 U.S.C. 282(j)(5)(B) (Form 3674)"
tags: [status/confirmed, fda-form/1571, fda-form/1572, fda-form/3454, fda-form/3455, fda-form/3500a, fda-form/3926, fda-form/3674, ossicro/gating]
aliases: ["FDA forms", "form index", "OMB numbers"]
updated: 2026-07-09
---

# FDA Form Index

> [!authority] Governing authority
> Each form below is the OMB-cleared instrument implementing a specific regulatory or statutory requirement (cited per row). The forms themselves are U.S. Government works — public domain, freely reproducible. Status: **Confirmed**.

This is the master index of the FDA forms in OSSICRO's scope: what each form is, the regulation or statute it implements, its OMB control number, where to download the current edition, and which wiki page explains it in depth. Two operational warnings apply to every row. First, **edition currency**: FDA revises form editions on OMB renewal cycles; the engine's generate pass must fetch or verify the current edition rather than trusting a cached copy (the local snapshots under `sources/fda-form/` are authoring-time evidence, not the live form). Second, **routing**: several forms are commonly mis-addressed — the 1572 goes to the *sponsor*, never directly to FDA; the 3454/3455 accompany the *marketing application*, not the IND.

## The core form set

| Form | Title | OMB No. | Implements | Where it goes | OSSICRO page |
|---|---|---|---|---|---|
| **FDA 1571** | Investigational New Drug Application (cover sheet) | 0910-0014 | [21 CFR 312.23(a)(1)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.23) — required first element of every IND submission; the sponsor's signed commitment (30-day wait, IRB compliance, GCP) | FDA (tops every IND submission, initial and subsequent) | [[form-fda-1571-ind-cover]] |
| **FDA 1572** | Statement of Investigator | 0910-0014 | [21 CFR 312.53(c)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.53) — sponsor must obtain before an investigator participates | **Sponsor** (retained in TMF; contents feed the IND). Never filed directly with FDA | [[form-fda-1572-statement-of-investigator]] |
| **FDA 3454** | Certification: Financial Interests and Arrangements of Clinical Investigators | 0910-0396 | [21 CFR Part 54](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-54) (§ 54.4) — certifies *absence* of disclosable interests | FDA, with the **marketing application** (NDA/BLA); data collected at site activation per 21 CFR 312.53(c)(4) | [[form-fda-3454-3455-financial-disclosure]] |
| **FDA 3455** | Disclosure: Financial Interests and Arrangements of Clinical Investigators | 0910-0396 | 21 CFR Part 54 (§ 54.4) — *discloses* interests when present (per covered investigator) | FDA, with the marketing application | [[form-fda-3454-3455-financial-disclosure]] |
| **FDA 3500A** | MedWatch — Mandatory Reporting | 0910-0291 | [21 CFR 312.32](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32) IND safety reports (also mandatory postmarket reporting); content harmonized with ICH E2A/E2B(R3) | FDA (IND safety report to the reviewing division; 7-day/15-day clocks) | [[form-fda-3500a-medwatch]] |
| **FDA 3926** | Individual Patient Expanded Access — Investigational New Drug Application | 0910-0814 | [21 CFR 312.310](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-I/section-312.310); streamlined alternative to the full 1571 package for single-patient (incl. emergency) expanded access; Fields 10.a/10.b invoke 21 CFR 312.10 / 56.105 waivers | FDA (CDER/CBER) | [[form-fda-3926-expanded-access]] |
| **FDA 3674** | Certification of Compliance with ClinicalTrials.gov Requirements | 0910-0616 | [42 U.S.C. § 282(j)(5)(B)](https://www.law.cornell.edu/uscode/text/42/282) (PHS Act § 402(j), FDAAA 801); false certification is a prohibited act under 21 U.S.C. § 331(jj) | FDA, accompanying the IND/NDA/BLA submission types the statute lists | [[form-fda-3674-clinicaltrialsgov-certification]] |

## Download and instruction links

Current editions are always available from the [FDA IND Forms and Instructions hub](https://www.fda.gov/drugs/investigational-new-drug-ind-application/ind-forms-and-instructions) and the [FDA Forms database](https://www.fda.gov/about-fda/reports-manuals-forms/forms). Direct links and local authoring-time snapshots:

| Form | Direct download | Official instructions | Local original |
|---|---|---|---|
| FDA 1571 | [fda.gov/media/72335/download](https://www.fda.gov/media/72335/download) | Instructions supplement distributed with the form | `../sources/fda-form/FDA_Form-1571.pdf`, `FDA_Form-1571-Instructions.pdf` |
| FDA 1572 | [fda.gov/media/72981/download](https://www.fda.gov/media/72981/download) | [Instructions for Filling Out Form FDA 1572 (fda.gov/media/79326)](https://www.fda.gov/media/79326/download); [1572 FAQ information sheet](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/frequently-asked-questions-statement-investigator-form-fda-1572) | `../sources/fda-form/FDA_Form-1572.pdf` |
| FDA 3454 | [fda.gov/media/74190/download](https://www.fda.gov/media/74190/download) | [Financial Disclosure guidance (2013)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/financial-disclosure-clinical-investigators) | `../sources/fda-form/FDA_Form-3454.pdf` |
| FDA 3455 | [fda.gov/media/74191/download](https://www.fda.gov/media/74191/download) | Same guidance as 3454 | `../sources/fda-form/FDA_Form-3455.pdf` |
| FDA 3500A | [fda.gov/media/82728/download](https://www.fda.gov/media/82728/download) | Instructions distributed with the form; [MedWatch forms hub](https://www.fda.gov/safety/medical-product-safety-information/medwatch-forms-fda-safety-reporting) | `../sources/fda-form/FDA_Form-3500A.pdf`, `FDA_Form-3500A-Instructions.pdf` |
| FDA 3926 | Via the [Form 3926 guidance page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/individual-patient-expanded-access-applications-form-fda-3926) and the IND forms hub | [Individual Patient Expanded Access Applications: Form FDA 3926 (guidance, June 2016 / Oct 2017)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/individual-patient-expanded-access-applications-form-fda-3926) | `../sources/fda-form/fda_form_3926_individual_patient_expanded_access.pdf` |
| FDA 3674 | Via the [3674 certifications guidance page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/certifications-accompany-drug-biological-product-and-device-applicationssubmissions-compliance) and the FDA forms database | Same guidance (rev. June 2017) | `../sources/fda-form/FDA_Form-3674.pdf`, `FDA_Form-3674-Printer-Friendly.pdf` |

## Adjacent forms (context)

| Form | Title | OMB No. | Note |
|---|---|---|---|
| FDA 3500 | MedWatch — Voluntary Reporting (health professional) | 0910-0291 | Voluntary counterpart to the mandatory 3500A; not an IND safety-report instrument. Local: `../sources/fda-form/FDA_Form_3500_Voluntary_HCP.pdf` |
| FDA 3500B | MedWatch — Voluntary Reporting (consumer) | 0910-0291 | Consumer-friendly voluntary form. Local: `../sources/fda-form/FDA_Form_3500B_Consumer.pdf` |
| FDA 483 | Inspectional Observations | — (FDA-issued, not a submission form) | Issued *by* FDA investigators at the close of an inspection (e.g., BIMO); the site responds in writing. See [[fda-as-counterparty]]. Local: `../sources/fda-form/fda_form-483_blank.pdf` |

## Sponsor-investigator note

In the [[sponsor-investigator]] configuration one physician signs the **1571 as sponsor** and the **1572 as investigator**, collects their own financial-disclosure attestation (3454/3455 data), and certifies ClinicalTrials.gov compliance on the **3674**. The role collapse waives no signature and no form; it concentrates every attestation in one person — which is precisely why the engine's completeness checks ([[completeness-ledger]]) and the [[non-delegable-functions-and-gates|gating matrix]] treat the form set as a single coherent package whose internal identifiers (sponsor name, investigator name, protocol number, IND number) must be cross-document consistent.

> [!warning] Non-delegable
> Every signature on this page is a personal legal attestation carrying criminal exposure for willful falsity (18 U.S.C. § 1001, warned on the forms' face): the 1571 signature is the sponsor's acceptance of the full sponsor obligation set; the 1572 signature is the investigator's binding conduct commitments; the 3454/3455 are the investigator's financial attestations (and the sponsor's due-diligence certification); the 3926 physician signature adopts investigator obligations for the expanded-access use; the 3674 certifies statutory registration compliance. OSSICRO auto-populates, field-validates, and cross-checks each form and assembles the signature-ready draft; **a qualified human reads, owns, and signs — no form is ever auto-signed or auto-submitted.** Electronic signatures, where used, must satisfy 21 CFR Part 11 ([[part-11-and-ai-credibility]]).

> [!interpretive] OSSICRO position
> The validate pass encodes per-form field rules (see [[form-fda-1572-statement-of-investigator]] for the worked example), the routing constraints in the table above, and an edition-currency check that compares the generated form's edition date against the FDA forms database entry. OMB control numbers are the stable identifiers used in the engine's authority objects, because form edition dates rotate while control numbers persist across renewals. Expiration dates printed on form faces are deliberately not recorded here — they roll on OMB renewal and are exactly the kind of fact that must be read from the live form, not from a wiki.

## Related
- [[form-fda-1571-ind-cover]]
- [[form-fda-1572-statement-of-investigator]]
- [[form-fda-3454-3455-financial-disclosure]]
- [[form-fda-3500a-medwatch]]
- [[form-fda-3926-expanded-access]]
- [[form-fda-3674-clinicaltrialsgov-certification]]
- [[ind-application-312-23]]
- [[site-activation]]
- [[non-delegable-functions-and-gates]]
- [[generate-check-validate-engine]]
- [[cfr-citation-map]]

## Sources
- [FDA — IND Forms and Instructions](https://www.fda.gov/drugs/investigational-new-drug-ind-application/ind-forms-and-instructions)
- [FDA — Forms (agency-wide database)](https://www.fda.gov/about-fda/reports-manuals-forms/forms)
- [FDA — MedWatch Forms for FDA Safety Reporting](https://www.fda.gov/safety/medical-product-safety-information/medwatch-forms-fda-safety-reporting)
- [Instructions for Filling Out Form FDA 1572](https://www.fda.gov/media/79326/download)
- [FDA Guidance — Individual Patient Expanded Access Applications: Form FDA 3926](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/individual-patient-expanded-access-applications-form-fda-3926)
- [FDA Guidance — Certifications to Accompany Applications/Submissions (Form 3674)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/certifications-accompany-drug-biological-product-and-device-applicationssubmissions-compliance)
- [18 U.S.C. § 1001 — False statements](https://www.law.cornell.edu/uscode/text/18/1001)
- Local originals: `../sources/fda-form/` (19 documents; see `../sources/MANIFEST.md`)
