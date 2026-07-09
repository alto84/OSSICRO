---
title: "Form FDA 1572 — Statement of Investigator"
section: "03-documents"
status: confirmed
governing_authority:
  - "21 CFR 312.53(c)"
  - "Form FDA 1572, OMB No. 0910-0014"
tags: [fda-form/1572, cfr/312, role/investigator, role/sponsor-investigator, lifecycle/activation, ossicro/gating, status/confirmed]
aliases: ["1572", "Statement of Investigator"]
updated: 2026-07-09
---

# Form FDA 1572 — Statement of Investigator

> [!authority] Governing authority
> 21 CFR 312.53(c) (sponsor must obtain a signed 1572 before permitting an investigator to begin); Form FDA 1572 (OMB No. 0910-0014, 4/25 edition). Status: **Confirmed**.

Form FDA 1572 is the clinical investigator's signed, binding commitment to conduct an investigation under the protocol and in compliance with 21 CFR Part 312. The form's header states the black-letter rule directly: **"No investigator may participate in an investigation until he/she provides the sponsor with a completed, signed Statement of Investigator, Form FDA 1572 (21 CFR 312.53(c))."** The sponsor obtains it under [21 CFR 312.53(c)(1)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.53), retains it in the [TMF/regulatory binder](regulatory-binder-isf-index.md), and incorporates the information into the [IND](ind-application-312-23.md); completed 1572s with attachments satisfy Field 15 items 6b–d of the [Form FDA 1571](form-fda-1571-ind-cover.md). Investigators do **not** send the 1572 to FDA directly — they forward it to the sponsor.

In the [sponsor-investigator](../01-roles-responsibilities/sponsor-investigator.md) model the same physician signs the 1571 as sponsor and the 1572 as investigator; the two obligation sets collapse into one person but neither signature is waived by the overlap.

OSSICRO auto-populates the 1572 from the investigator's CV, site data, IRB record, and protocol identifiers, validates every required field, and produces a signature-ready draft. The commitment signature is non-delegable (see gate).

## Field map (Form FDA 1572, 4/25 edition)

| Field | Content | Note |
|-------|---------|------|
| 1 | Name and address of the clinical investigator | The named accountable human |
| 2 | Education, training, and experience qualifying the investigator as an expert — **Curriculum Vitae** or **Other Statement of Qualifications** (select one) | Supports the sponsor's § 312.53(a) selection duty and § 312.53(c)(2) CV collection |
| 3 | Name/address of each medical school, hospital, or research facility where the investigation will be conducted | Continuation page permitted |
| 4 | Name/address of any clinical laboratory facilities to be used | Continuation page permitted |
| 5 | Name/address of the **IRB** responsible for review and approval | Ties the site to a registered [IRB (Part 56)](../01-roles-responsibilities/irb-iec.md) |
| 6 | Names of subinvestigators (enter "None" if not applicable) | The on-form anchor for the [delegation-of-authority log](delegation-of-authority-log.md) |
| 7 | Name and code number of the protocol(s) in the IND | Links the 1572 to the specific [protocol](clinical-protocol-and-synopsis.md) |
| 8 | Clinical protocol information (select one): a **Phase 1** general outline (duration, maximum subjects) **or** a **Phase 2/3** protocol outline (subject numbers, controls, clinical uses, subject characteristics, observations/tests, duration, CRFs) | Phase-dependent content |
| 9 | **Commitments** (the binding attestations — see below) | Not a fill-in field; the signature adopts them |
| 10 | Date (mm/dd/yyyy) | |
| 11 | **Signature of investigator** | The commitment. See gate. |

### Field 9 — the commitments the signature adopts
By signing, the investigator commits to each of the following (verbatim substance from the form):

1. Conduct the study(ies) in accordance with the relevant, current protocol(s), and make changes only after notifying the sponsor **except when necessary to protect the safety, rights, or welfare of subjects**.
2. **Personally conduct or supervise** the described investigation(s).
3. Inform patients/controls that the drugs are being used for investigational purposes, and ensure that [informed consent (21 CFR Part 50)](informed-consent-form.md) and [IRB review/approval (21 CFR Part 56)](../01-roles-responsibilities/irb-iec.md) requirements are met.
4. Report adverse experiences to the sponsor in accordance with [21 CFR 312.64](ind-safety-report.md), and confirm having read and understood the [investigator's brochure](investigators-brochure.md), including potential risks and side effects.
5. Ensure that all associates, colleagues, and employees assisting in the study are informed of their obligations.
6. Maintain adequate and accurate records under 21 CFR 312.62 and make them available for inspection under 21 CFR 312.68.
7. Ensure that an IRB compliant with Part 56 conducts initial and continuing review; promptly report to the IRB all changes in research activity and all unanticipated problems involving risk to subjects or others; make no changes without IRB approval except to eliminate apparent immediate hazards.
8. Comply with all other requirements of 21 CFR Part 312.

The form carries the criminal-liability warning: **a willfully false statement is a criminal offense (18 U.S.C. § 1001).**

## Non-delegable gate

> [!warning] Non-delegable
> The Field 11 signature on Form FDA 1572 is the investigator's personal legal commitment to protocol adherence, informed consent, IRB compliance, safety reporting, supervision, and recordkeeping. It cannot be executed by software or by any person other than the investigator making the commitment. The obligations it adopts — personally conducting/supervising the investigation, obtaining consent, ensuring IRB review — are themselves non-delegable investigator duties (delegation of *tasks* to qualified [subinvestigators](../01-roles-responsibilities/subinvestigator-and-delegation.md) never transfers *accountability*). OSSICRO drafts and field-validates the 1572; the investigator reads, owns, and signs.

> [!interpretive] OSSICRO position
> OSSICRO's validate pass blocks a 1572 from "ready" status unless: Field 2 has an attached CV or qualifications statement; Field 5 names an IRB that resolves against a registered-IRB record; Field 7 protocol identifiers match the IND's protocol; and Field 8's phase selection matches the protocol's declared phase. In the sponsor-investigator configuration the engine additionally asserts that the Field 1 investigator equals the [1571](form-fda-1571-ind-cover.md) Field 2 sponsor. The routing rule that the completed form goes **to the sponsor, not to FDA**, is encoded as a workflow constraint so the engine never mis-addresses the artifact. See [compliance-mapping](../05-ossicro-system/compliance-mapping.md).

## Decentralized-trial note
Under the FDA decentralized-clinical-trials framework, local HCPs performing trial-related activities that are not investigational-drug-specific need not be listed on the 1572 as subinvestigators, provided the activities are within their normal practice and appropriately delegated; the regulatory *obligations* are unchanged by decentralization. OSSICRO surfaces this distinction when building Field 6 for a distributed site. (Status: **interpretive** application of the confirmed DCT guidance.)

## Related
- [[form-fda-1571-ind-cover]]
- [[investigator]]
- [[sponsor-investigator]]
- [[subinvestigator-and-delegation]]
- [[delegation-of-authority-log]]
- [[informed-consent-form]]
- [[irb-iec]]
- [[investigators-brochure]]
- [[ind-safety-report]]
- [[non-delegable-functions-and-gates]]

## Sources
- [21 CFR 312.53 — Selecting investigators and monitors](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.53)
- [21 CFR 312.62 — Investigator recordkeeping and record retention](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.62)
- [21 CFR 312.64 — Investigator reports](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.64)
- [FDA Form 1572 (Statement of Investigator)](https://www.fda.gov/media/72981/download) — local original: `../sources/fda-form/FDA_Form-1572.pdf`
- [FDA — Information Sheet: Statement of Investigator (Form FDA 1572)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/frequently-asked-questions-statement-investigator-form-fda-1572)
