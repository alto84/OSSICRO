---
title: "HIPAA and Privacy Gating — The Matching/Enrollment Fulcrum"
section: "05-ossicro-system"
status: mixed
governing_authority:
  - "45 CFR 164.512(i) (uses and disclosures for research)"
  - "45 CFR 164.508 (authorization)"
  - "45 CFR 164.514(b), 164.514(e) (de-identification; limited data set)"
  - "45 CFR 164.502(b) (minimum necessary)"
tags: [ossicro/gating, ossicro/matching, entity/covered-entity, lifecycle/feasibility, status/confirmed, status/interpretive]
aliases: ["HIPAA Gating", "Privacy Gating", "Preparatory to Research"]
updated: 2026-07-09
---

# HIPAA and Privacy Gating — The Matching/Enrollment Fulcrum

> [!authority] Governing authority
> The HIPAA Privacy Rule, [45 CFR Part 164 Subpart E](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E): [§164.512(i)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.512) (research uses/disclosures, including reviews preparatory to research and IRB/Privacy Board waiver), [§164.508](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.508) (authorization), [§164.514](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.514) (de-identification; limited data set), [§164.502(b)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.502) (minimum necessary). All binding rules. Status: **Mixed** — the legal boundaries are confirmed; the code-enforced state-machine design is interpretive.

HIPAA is the fulcrum on which OSSICRO's entire matching workflow balances. A clinician searching for a trial that fits a specific patient is *using protected health information (PHI)*, and the lawful basis for that use changes categorically at one moment: the transition from **looking** (feasibility/matching) to **enrolling** (research use of PHI about an identified subject). OSSICRO's position is that this boundary must be enforced in code — a logged state transition, not a policy document — which is the subject of the companion page [[privacy-state-machine]]. This page states the law that boundary implements.

## The three lawful bases, in order of use

### 1. Reviews preparatory to research — 45 CFR 164.512(i)(1)(ii)

A covered entity may use or disclose PHI for reviews **preparatory to research** without patient authorization if it obtains from the researcher representations that:

- the use or disclosure is sought **solely to review PHI as necessary to prepare a research protocol or for similar purposes preparatory to research** — which includes assessing feasibility and identifying prospective research participants;
- **no PHI is removed from the covered entity** by the researcher in the course of the review; and
- the PHI for which access is sought is **necessary for the research purposes**.

This is the cleanest lawful basis for OSSICRO's trial-matching step, and it dictates architecture. When the treating clinician (a workforce member of the covered entity) uses OSSICRO to screen a patient or a panel against candidate programs ([[patient-trial-matching]], [[matching-engine]], [[smart-on-fhir-integration]]), the review is preparatory to research and lawful **provided PHI does not leave the covered entity**. Hence the local-first design: chart data is read inside the covered-entity boundary, matching runs there ([[offline-local-deployment]]), reads are ephemeral and audited, and only the *representations log* — not the PHI — persists as the compliance record. The minimum-necessary standard (§164.502(b)) applies throughout: the matcher reads the data elements eligibility adjudication needs, not the whole chart.

Two confirmed limits of this basis deserve emphasis, because they are commonly misunderstood:

- **Preparatory review authorizes identification, not recruitment contact by outsiders.** A researcher who is not a workforce member of the covered entity may identify prospective participants under this provision but may not record or remove identifiers, and contact of prospective subjects generally proceeds through the treating provider or under a separate lawful basis (e.g., a partial waiver of authorization for recruitment granted by an IRB/Privacy Board). In OSSICRO's core scenario the enrolling clinician *is* the treating provider, which keeps the contact question inside the treatment relationship — but the system must not export candidate lists across the covered-entity boundary.
- **Preparatory review never covers the research itself.** The moment PHI is used *as research data* about an enrolled (or enrolling) subject, this basis is exhausted.

### 2. Authorization — 45 CFR 164.508

Enrollment's default lawful basis is a signed, research-specific authorization. A valid authorization contains the core elements and required statements of [§164.508(c)](https://www.law.cornell.edu/cfr/text/45/164.508): a specific and meaningful description of the information to be used or disclosed, the persons authorized to use/disclose and to receive it, a description of each purpose, an expiration date or event (research authorizations may state "end of the research study" or "none"), the individual's signature and date, and statements of the right to revoke, of redisclosure risk, and of conditioning rules. Research authorizations are routinely combined with the informed consent document ([[informed-consent-form]]) — a compound authorization permitted for research under §164.508(b)(3)(i) — and OSSICRO drafts them together, with the consent *event* remaining the non-delegable human act ([[informed-consent-document-vs-event]]).

### 3. IRB / Privacy Board waiver — 45 CFR 164.512(i)(1)(i)

Where authorization is impracticable, an IRB or Privacy Board may waive or alter the authorization requirement upon the documented findings of [§164.512(i)(2)](https://www.law.cornell.edu/cfr/text/45/164.512): (A) the use/disclosure involves **no more than minimal risk to privacy**, based on (1) an adequate plan to protect identifiers, (2) an adequate plan to destroy identifiers at the earliest opportunity consistent with the research (absent a health/research justification or legal requirement to retain), and (3) adequate written assurances against reuse/redisclosure; (B) the research **could not practicably be conducted without the waiver**; and (C) it **could not practicably be conducted without access to the PHI**. The waiver documentation requirements of §164.512(i)(2)(i)-(v) (identification of the board, waiver date, findings, brief PHI description, review procedure, and signature of the chair or designee) define the record OSSICRO must hold in the TMF before the gate opens. Partial waivers for recruitment are the common real-world instrument for screening beyond the treating relationship.

## Supporting instruments

- **De-identification — §164.514(b).** Information de-identified under Safe Harbor (removal of the 18 identifier categories plus no actual knowledge of re-identifiability) or Expert Determination is not PHI, and OSSICRO's cross-site analytics and any shared eligibility datasets ride on this basis. De-identification is performed inside the covered entity before anything leaves.
- **Limited data set + data use agreement — §164.514(e).** Where dates and geography are needed (e.g., feasibility statistics), a limited data set under a DUA meeting §164.514(e)(4) is the intermediate instrument.
- **Decedents — §164.512(i)(1)(iii).** Research on decedents' information proceeds on representations of death and necessity.
- **Common Rule interaction.** For HHS-supported research, 45 CFR 46 consent and IRB requirements run in parallel; HIPAA authorization and Common Rule consent are distinct instruments satisfied together ([[regulatory-landscape]], [[irb-submission-and-approval]]).

## The fulcrum, stated operationally

| Phase | Lawful basis | PHI movement | Gate evidence required |
|---|---|---|---|
| Matching / feasibility | §164.512(i)(1)(ii) preparatory review | None outside the covered entity; ephemeral audited reads; minimum necessary | Researcher representations recorded; audit log of reads |
| Recruitment contact | Treatment relationship, or partial waiver | None, or per waiver terms | Waiver documentation per §164.512(i)(2), if used |
| Enrollment / research use | §164.508 authorization **or** §164.512(i)(1)(i) full waiver | As authorized/waived, minimum necessary | Signed authorization in TMF, or documented waiver |
| Data sharing / analytics | §164.514(b) de-identification or §164.514(e) LDS+DUA | De-identified or limited data set only | De-identification determination or executed DUA |

> [!warning] Non-delegable
> Two human judgments anchor this page. The **IRB/Privacy Board waiver determination** (§164.512(i)(2)) is a board judgment OSSICRO assembles evidence for but never renders — the same non-delegable posture as IRB approval under 21 CFR 56 ([[non-delegable-functions-and-gates]], gate G2). And the **authorization signature** is the patient's own act, obtained in the consent conversation by a qualified human ([[informed-consent-document-vs-event]]). OSSICRO drafts the compound consent-authorization instrument and validates its required elements; it never obtains it.

> [!interpretive] OSSICRO position
> The Privacy Rule does not require that the preparatory→enrollment boundary be enforced by software; it requires the bases to be respected. OSSICRO's position is that in an AI-assisted matching system the boundary **must** be code-enforced to be credible: a hard, logged state transition ([[privacy-state-machine]]) that blocks any research use of PHI until the authorization or waiver record exists, with no administrative override. This exceeds the regulatory floor deliberately — matching is the highest-privacy-exposure surface of the system, and the mitigation for its highest-severity failure mode (silent PHI egress at scale) is architectural, not procedural. See [[risks-and-limitations]].

## Related

- [[privacy-state-machine]]
- [[patient-trial-matching]]
- [[matching-engine]]
- [[matching-eligibility-adjudication]]
- [[smart-on-fhir-integration]]
- [[offline-local-deployment]]
- [[feasibility-and-patient-matching]]
- [[informed-consent-document-vs-event]]
- [[informed-consent-form]]
- [[irb-review-workflow]]
- [[non-delegable-functions-and-gates]]
- [[communication-hub]]
- [[regulatory-landscape]]

## Sources

- [45 CFR 164.512 — Uses and disclosures for which an authorization or opportunity to agree or object is not required (eCFR)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.512)
- [45 CFR 164.508 — Uses and disclosures for which an authorization is required (eCFR)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.508)
- [45 CFR 164.514 — Other requirements relating to uses and disclosures of PHI (de-identification; limited data set) (eCFR)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.514)
- [45 CFR 164.502 — Uses and disclosures of PHI: general rules (minimum necessary) (eCFR)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.502)
- [HHS OCR: Research — HIPAA Privacy Rule guidance page](https://www.hhs.gov/hipaa/for-professionals/special-topics/research/index.html)
- [NIH: HIPAA Privacy Rule — Information for Researchers (Preparatory to Research)](https://privacyruleandresearch.nih.gov/)
- [45 CFR Part 46 — Protection of Human Subjects (Common Rule) (eCFR)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46)
