---
title: "Form FDA 1571 — Investigational New Drug Application (IND) Cover"
section: "03-documents"
status: confirmed
governing_authority:
  - "21 CFR 312.23(a)(1)"
  - "21 CFR 312.23(a)(1)(ix) (signature)"
  - "Form FDA 1571, OMB No. 0910-0014"
tags: [fda-form/1571, cfr/312, role/sponsor, role/sponsor-investigator, lifecycle/ind, ossicro/gating, status/confirmed]
aliases: ["1571", "IND cover sheet", "IND transmittal"]
updated: 2026-07-09
---

# Form FDA 1571 — Investigational New Drug Application (IND) Cover

> [!authority] Governing authority
> 21 CFR 312.23(a)(1) (IND cover sheet content); 21 CFR 312.23(a)(1)(ix) (signature requirement); Form FDA 1571 (OMB No. 0910-0014). Status: **Confirmed**.

Form FDA 1571 is the cover/transmittal sheet and binding commitment page for every Investigational New Drug Application. It is required by [21 CFR 312.23(a)(1)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.23) as the first item of the IND and identifies the sponsor, the drug, the phase(s) of investigation, and the contents of the application; its signature is the sponsor's legal attestation of the sponsor responsibilities enumerated in [Subpart D (§§ 312.50–312.59)](../01-roles-responsibilities/sponsor.md). The form is the outer envelope of the assembled [IND package](ind-application-312-23.md): everything else in the submission — general investigational plan, [investigator's brochure](investigators-brochure.md), [protocol](clinical-protocol-and-synopsis.md), CMC, pharmacology/toxicology, prior human experience — is content the 1571 transmits and the sponsor's signature vouches for. In the [sponsor-investigator](../01-roles-responsibilities/sponsor-investigator.md) model, a single physician signs both this form and every [Form FDA 1572](form-fda-1572-statement-of-investigator.md) for the study.

OSSICRO auto-populates the 1571 from structured study data and runs a completeness check against the § 312.23 content matrix, then hands a fully-drafted, field-validated form to the human sponsor for review and signature. It does not, and cannot, execute the signature — see the non-delegable gate below.

## Field map (per FDA 1571 instructions, 03/23 supplement)

The numbered fields correspond exactly to the boxes on the form. The load-bearing ones for OSSICRO's generate/check/validate passes:

| Field | Content | Authority / note |
|-------|---------|------------------|
| 1 | Select appropriate Center (CDER / CBER) | Routing; determines review division |
| 2 | **Name of sponsor** | 21 CFR 312.3(b). A sponsor-investigator both initiates and conducts the investigation and administers/dispenses the drug under their immediate direction. "For administrative reasons, only one individual should be designated as sponsor-investigator." |
| 3 | Date of submission | Must match the cover-letter date |
| 4–5 | Sponsor address and telephone | 21 CFR 312.23(a)(1)(i) |
| 6 | Name(s) of drug | Established name, trade name, dosage form, UNII |
| 7A / 7B | IND number (if assigned) / IND type | Research vs. Commercial; expanded-access INDs are marked **Research** (21 CFR 312.310, 312.315, 312.320) |
| 8A / 8B | Proposed indication; SNOMED CT disease term | Rare-disease / orphan-designation flag |
| 9 | Phase(s) of clinical investigation | 21 CFR 312.23(a)(1)(ii) |
| 10 | Cross-reference / letter of authorization | 21 CFR 312.22(d), 312.23(b) — right of reference to prior submissions |
| 11 | Serial number | Initial IND = "0000"; consecutive thereafter |
| 12A | Submission information (initial IND, protocol amendment, information amendment, IND safety report, annual report, DSUR, response to clinical hold, general correspondence) | Maps to §§ 312.30, 312.31, 312.32, 312.33, 312.41, 312.42 |
| 15 | **Contents of application** (items 1–12 checklist) | For a sponsor-investigator IND, items 2–4 may be briefly addressed in the cover letter; completed Form(s) 1572 satisfy items 6b–d |
| 16 | Contract Research Organizations | If a [CRO](../01-roles-responsibilities/cro.md) conducts the study, attach the name, address, and a **listing of obligations transferred** (21 CFR 312.23(a)(1)(viii)) — the on-form footprint of the [transfer of obligations (TORO)](transfer-of-regulatory-obligations-toro.md) |
| 17 | Person responsible for monitoring | 21 CFR 312.23(a)(1)(vi). "For Sponsor-Investigator INDs, the investigator has this responsibility." |
| 18 | Person responsible for safety review under § 312.32 | 21 CFR 312.23(a)(1)(vii). "For Sponsor-Investigator INDs, the investigator has this responsibility." |
| 19 | **Name of sponsor or sponsor's authorized representative** | For a sponsor-investigator IND, the sponsor-investigator is named and must sign |
| 24 | Date of signature | May differ from Field 3 |
| 25–27 | Countersigner (name/address/email) | Required only if the field-19 signatory has no U.S. residence or place of business (21 CFR 312.23(a)(1)(ix)) |
| 28 | **Signature of sponsor or authorized representative** | The attestation. See gate below. |

### The commitments the signature attests
Printed below Field 17, the sponsor's signature commits — among other things — that clinical investigations will **not begin until 30 days after FDA receives the IND** (unless notified sooner), that an [IRB complying with Part 56](../01-roles-responsibilities/irb-iec.md) will review and approve each study, and that the investigation will be conducted in accordance with all other applicable regulatory requirements. The form carries the criminal-liability warning: **a willfully false statement is a criminal offense (18 U.S.C. § 1001).**

## Non-delegable gate

> [!warning] Non-delegable
> The Field 28 signature on Form FDA 1571 is the sponsor's personal legal attestation of the [Subpart D sponsor obligations](../01-roles-responsibilities/sponsor.md) and of the printed commitments (30-day wait, IRB compliance, GCP compliance). It cannot be delegated to software. OSSICRO drafts and validates the form to completeness; a qualified human sponsor (or, in the [dual-role model](../01-roles-responsibilities/sponsor-investigator.md), the sponsor-investigator) reads, owns, and signs it. Submission to FDA is likewise a human act (see [fda-as-counterparty](../01-roles-responsibilities/fda-as-counterparty.md)).

> [!interpretive] OSSICRO position
> OSSICRO treats the 1571 as a **generated-then-gated** artifact. The generate pass populates every field from the study data model; the check pass verifies each § 312.23 content item is present or accounted for (item 6 satisfied by attached 1572s, items 5/7/8/9 referenceable when the drug is supplied in final dosage form under a manufacturer's authorization); the validate pass blocks "ready-to-sign" status until Fields 2, 15, 17, 18, and 19 are internally consistent (e.g., in a sponsor-investigator IND, the same named individual appears in Fields 2, 17, 18, and 19). The signature block is rendered but never machine-completed. This mapping is recorded in [compliance-mapping](../05-ossicro-system/compliance-mapping.md) and enforced by the [non-delegable gate matrix](../05-ossicro-system/non-delegable-functions-and-gates.md).

## Relationship to companion forms

- **[Form FDA 1572](form-fda-1572-statement-of-investigator.md)** — attached to the IND; completed 1572(s) with CV satisfy Field 15, items 6b–d. Retained by the sponsor; investigators do **not** send it to FDA directly.
- **[Form FDA 3674](form-fda-3674-clinicaltrialsgov-certification.md)** — the ClinicalTrials.gov certification (Field 15, item 12) that must accompany the IND.
- **[Forms FDA 3454 / 3455](form-fda-3454-3455-financial-disclosure.md)** — financial-disclosure certification/disclosure; the underlying data is collected at IND stage (§ 312.53(c)(4)) but the forms are filed with the eventual marketing application.
- **[Form FDA 3926](form-fda-3926-expanded-access.md)** — a streamlined substitute cover for individual-patient expanded access that stands in for the 1571 (and 1572) under a § 312.10 waiver.

## Related
- [[ind-application-312-23]]
- [[form-fda-1572-statement-of-investigator]]
- [[form-fda-3674-clinicaltrialsgov-certification]]
- [[sponsor]]
- [[sponsor-investigator]]
- [[transfer-of-regulatory-obligations-toro]]
- [[non-delegable-functions-and-gates]]
- [[fda-as-counterparty]]
- [[pre-ind-and-ind-preparation]]

## Sources
- [21 CFR 312.23 — IND content and format](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.23)
- [21 CFR 312.3 — Definitions (sponsor, investigator, sponsor-investigator)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-A/section-312.3)
- [FDA Form 1571 (Investigational New Drug Application)](https://www.fda.gov/media/72335/download) — local original: `../sources/fda-form/FDA_Form-1571.pdf`
- [FDA Form 1571 Instructions (03/23 supplement)](https://www.fda.gov/media/72335/download) — local original: `../sources/fda-form/FDA_Form-1571-Instructions.pdf`
- [FDA — IND Application Procedures: Investigator's Responsibilities](https://www.fda.gov/drugs/investigational-new-drug-ind-application/ind-application-procedures-investigators-responsibilities)
