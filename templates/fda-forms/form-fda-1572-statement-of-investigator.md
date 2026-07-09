---
title: "Form FDA 1572 - Statement of Investigator"
doc_id: "form-fda-1572-statement-of-investigator"
category: "fda-forms"
governing_citations: ["21 CFR 312.53(c)(1)", "Form FDA 1572"]
owner: "investigator"
receiver: "sponsor"
gate: "1572-signature"
status: template
updated: 2026-07-09
---

# Form FDA 1572 - Statement of Investigator — TEMPLATE (DRAFT for qualified human review)

> [!authority] Governing authority
> [21 CFR 312.53(c)(1)](https://www.law.cornell.edu/cfr/text/21/312.53) (the sponsor shall obtain a completed and signed Statement of Investigator before permitting an investigator to begin participation) and [Form FDA 1572 itself (current OMB-approved version, FDA)](https://www.fda.gov/media/72981/download); FDA's [Form FDA 1572 FAQ guidance (2010)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/frequently-asked-questions-statement-investigator-form-fda-1572) resolves most completion questions. This is a DRAFT template; OSSICRO fills it, a qualified human reviews and signs.

**Purpose.** Form FDA 1572 is the investigator's personal, signed agreement with the sponsor to conduct a drug study under an IND in accordance with the protocol, 21 CFR Part 50 (informed consent), Part 56 (IRB), and the investigator obligations of Part 312 Subpart D. The sponsor must obtain it before the investigator begins; it is filed to the IND. In a sponsor-investigator (Mode B) study the same physician completes it as investigator.

**How to use.** Fill every {{placeholder}}; follow each [INSTRUCTION: ...] note; delete guidance text before finalizing. Values are transcribed onto the current OMB-approved Form FDA 1572; this markdown template is the structured worksheet, not the form of record. A new 1572 is required when a new investigator joins and should be updated (per the FDA FAQ) when key information on it changes — e.g., new IRB, new site address, protocol changes affecting listed items.

## Template

**STATEMENT OF INVESTIGATOR (Title 21, Code of Federal Regulations (CFR) Part 312)**

*(See instructions on reverse side. NOTE: No investigator may participate in an investigation until he/she provides the sponsor with a completed, signed Statement of Investigator, Form FDA 1572 — 21 CFR 312.53(c).)*

**1. Name and address of investigator**

{{investigator_name}}
{{investigator_address}}

**2. Education, training, and experience that qualifies the investigator as an expert in the clinical investigation of the drug for the use under investigation**

- [ ] Curriculum vitae attached — dated {{cv_date}}
- [ ] Other statement of qualifications attached

{{education_degrees}} [INSTRUCTION: List degrees (e.g., MD, PhD) and board certifications; one of the two boxes above must be checked and the corresponding document attached and kept current — 21 CFR 312.53(c)(2).]

**3. Name and address of any medical school, hospital, or other research facility where the clinical investigation(s) will be conducted**

{{site_name}}
{{site_address}}

[INSTRUCTION: List every location where study procedures on subjects will be performed, including satellite sites.]

**4. Name and address of any clinical laboratory facilities to be used in the study**

{{clinical_lab_name}}
{{clinical_lab_address}}

[INSTRUCTION: Include local labs, central labs, and any specialty labs (e.g., PK, biomarker). Pair each with its CLIA/CAP certification in the site file — see the laboratory-certification template.]

**5. Name and address of the Institutional Review Board (IRB) that is responsible for review and approval of the study(ies)**

{{irb_name}}
{{irb_address}}

**6. Names of the subinvestigators (e.g., research fellows, residents, associates) who will be assisting the investigator in the conduct of the investigation(s)**

{{subinvestigators}}

[INSTRUCTION: Per the FDA 1572 FAQ, list individuals who make a direct and significant contribution to the study data. Keep consistent with the delegation-of-authority log; do not list everyone on the delegation log — only those meeting the subinvestigator standard.]

**7. Name and code number, if any, of the protocol(s) in the IND for the study(ies) to be conducted by the investigator**

{{protocol_number}} — {{protocol_title}} (IND {{ind_number}})

**8. Attach the following clinical protocol information** [INSTRUCTION: Check the one that applies.]

- [ ] For Phase 1 investigations, a general outline of the planned investigation including the estimated duration of the study and the maximum number of subjects that will be involved. ({{phase}} = Phase 1)
- [ ] For Phase 2 or 3 investigations, an outline of the study protocol including an approximation of the number of subjects to be treated with the drug and the number to be employed as controls, if any; the clinical uses to be investigated; characteristics of subjects by age, sex, and condition; the kind of clinical observations and laboratory tests to be conducted; the estimated duration of the study; and copies or a description of case report forms to be used. ({{phase}} = Phase 2/3)

**9. Commitments** [INSTRUCTION: These appear on the form verbatim; the investigator's signature attests to all of them. Do not alter.]

> - I agree to conduct the study(ies) in accordance with the relevant, current protocol(s) and will only make changes in a protocol after notifying the sponsor, except when necessary to protect the safety, rights, or welfare of subjects.
> - I agree to personally conduct or supervise the described investigation(s).
> - I agree to inform any patients, or any persons used as controls, that the drugs are being used for investigational purposes and I will ensure that the requirements relating to obtaining informed consent in 21 CFR Part 50 and institutional review board (IRB) review and approval in 21 CFR Part 56 are met.
> - I agree to report to the sponsor adverse experiences that occur in the course of the investigation(s) in accordance with 21 CFR 312.64.
> - I have read and understand the information in the investigator's brochure, including the potential risks and side effects of the drug.
> - I agree to ensure that all associates, colleagues, and employees assisting in the conduct of the study(ies) are informed about their obligations in meeting the above commitments.
> - I agree to maintain adequate and accurate records in accordance with 21 CFR 312.62 and to make those records available for inspection in accordance with 21 CFR 312.68.
> - I will ensure that an IRB that complies with the requirements of 21 CFR Part 56 will be responsible for the initial and continuing review and approval of the clinical investigation. I also agree to promptly report to the IRB all changes in the research activity and all unanticipated problems involving risks to human subjects or others. Additionally, I will not make any changes in the research without IRB approval, except where necessary to eliminate apparent immediate hazards to human subjects.
> - I agree to comply with all other requirements regarding the obligations of clinical investigators and all other pertinent requirements in 21 CFR Part 312.

**10. Signature of investigator:** ______________________________ [INSTRUCTION: Wet or Part 11-compliant electronic signature of the named investigator only; not delegable to a coordinator or subinvestigator.]

**11. Date:** {{signature_date}}

> A willfully false statement is a criminal offense (U.S.C. Title 18, Sec. 1001).

> [!warning] Non-delegable
> Form FDA 1572 investigator signature is executed by the investigator (21 CFR 312.53(c)(1); Form FDA 1572). The signature is a personal, non-delegable commitment to conduct the study per the protocol, Part 50, and Part 56. OSSICRO fills the form; only the named investigator signs it. The engine cannot finalize this document without a recorded human sign-off.

## Fields

| placeholder | source (study-record path) | citation |
|---|---|---|
| {{investigator_name}} | investigator.name | 21 CFR 312.53(c)(1)(i); Form FDA 1572 item 1 |
| {{investigator_address}} | investigator.address | Form FDA 1572 item 1 |
| {{education_degrees}} | investigator.qualifications.degrees | 21 CFR 312.53(c)(2); item 2 |
| {{cv_date}} | investigator.qualifications.cv_date | 21 CFR 312.53(c)(2); item 2 |
| {{site_name}} | site.facility.name | 21 CFR 312.53(c)(1)(iii); item 3 |
| {{site_address}} | site.facility.address | Form FDA 1572 item 3 |
| {{clinical_lab_name}} | site.laboratories[].name | Form FDA 1572 item 4 |
| {{clinical_lab_address}} | site.laboratories[].address | Form FDA 1572 item 4 |
| {{irb_name}} | site.irb_of_record.name | 21 CFR 312.53(c)(1)(iii); item 5 |
| {{irb_address}} | site.irb_of_record.address | Form FDA 1572 item 5 |
| {{subinvestigators}} | site.subinvestigators[].name | 21 CFR 312.53(c)(1)(ii); item 6 |
| {{protocol_number}} | study.protocol.number | Form FDA 1572 item 7 |
| {{protocol_title}} | study.protocol.title | Form FDA 1572 item 7 |
| {{ind_number}} | ind.number | Form FDA 1572 item 7 |
| {{phase}} | study.phase | 21 CFR 312.53(c)(1)(iv)-(v); item 8 |
| {{signature_date}} | gates.1572-signature.discharge_date | Form FDA 1572 item 11 |

## Related

- [[form-fda-1572-statement-of-investigator]] (wiki document page)
- [[site-activation]]
- [[delegation-of-authority-log]]
- [[investigator]]
- [[sponsor-cro-site-coordination]]
