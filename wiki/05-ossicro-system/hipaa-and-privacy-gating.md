---
title: "HIPAA and Privacy Gating — The Matching/Enrollment Fulcrum"
section: "05-ossicro-system"
status: mixed
governing_authority:
  - "45 CFR 164.512(i) (uses and disclosures for research)"
  - "45 CFR 164.508 (authorization; revocation and reliance)"
  - "45 CFR 164.506(c) (treatment disclosures)"
  - "45 CFR 164.514(b), 164.514(e) (de-identification; limited data set)"
  - "45 CFR 164.502(b) (minimum necessary)"
tags: [ossicro/gating, ossicro/matching, entity/covered-entity, lifecycle/feasibility, lifecycle/expanded-access, status/confirmed, status/interpretive]
aliases: ["HIPAA Gating", "Privacy Gating", "Preparatory to Research"]
updated: 2026-07-09
---

# HIPAA and Privacy Gating — The Matching/Enrollment Fulcrum

> [!authority] Governing authority
> The HIPAA Privacy Rule, [45 CFR Part 164 Subpart E](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E): [§164.512(i)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.512) (research uses/disclosures, including reviews preparatory to research and IRB/Privacy Board waiver), [§164.508](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.508) (authorization; revocation), [§164.506(c)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.506) (treatment disclosures), [§164.514](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.514) (de-identification; limited data set), [§164.502(b)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.502) (minimum necessary). All binding rules. Status: **Mixed** — the legal boundaries are confirmed; the code-enforced state-machine design is interpretive.

HIPAA is the fulcrum on which OSSICRO's entire matching workflow balances. A clinician searching for a trial that fits a specific patient is *using protected health information (PHI)*, and the lawful basis for that use changes categorically at one moment: the transition from **looking** (feasibility/matching) to **enrolling** (research use of PHI about an identified subject). OSSICRO's position is that this boundary must be enforced in code — a logged state transition, not a policy document — which is the subject of the companion page [[privacy-state-machine]]. This page states the law that boundary implements, including the boundary case the flagship scenario actually presents: one physician, one patient, one rare condition.

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

**What revocation actually does — the reliance exception.** The right to revoke is real but bounded, and the patient-facing draft must say so plainly. Under [§164.508(b)(5)](https://www.law.cornell.edu/cfr/text/45/164.508) an individual may revoke a research authorization at any time, in writing, *except to the extent the covered entity has taken action in reliance on it* (§164.508(b)(5)(i)). Operationally: revocation stops new uses and disclosures of the patient's PHI for the research from the point of revocation forward; it does **not** claw back data already collected, used, or disclosed under the authorization, and study data already reported (to the sponsor, FDA, or in analyses needed to preserve the integrity of the research) is not withdrawn. The authorization itself must describe the exceptions to the right to revoke (§164.508(c)(2)(i)), and OSSICRO's drafted compound instrument — and the plain-language explanation on the [[patient]] persona page — states both halves: what revocation stops, and what it does not.

### 3. IRB / Privacy Board waiver — 45 CFR 164.512(i)(1)(i)

Where authorization is impracticable, an IRB or Privacy Board may waive or alter the authorization requirement upon the documented findings of [§164.512(i)(2)](https://www.law.cornell.edu/cfr/text/45/164.512): (A) the use/disclosure involves **no more than minimal risk to privacy**, based on (1) an adequate plan to protect identifiers, (2) an adequate plan to destroy identifiers at the earliest opportunity consistent with the research (absent a health/research justification or legal requirement to retain), and (3) adequate written assurances against reuse/redisclosure; (B) the research **could not practicably be conducted without the waiver**; and (C) it **could not practicably be conducted without access to the PHI**. The waiver documentation requirements of §164.512(i)(2)(i)-(v) (identification of the board, waiver date, findings, brief PHI description, review procedure, and signature of the chair or designee) define the record OSSICRO must hold in the TMF before the gate opens. Partial waivers for recruitment are the common real-world instrument for screening beyond the treating relationship.

## The n-of-1 boundary case — one physician, one patient, one rare condition

The flagship scenario ([[single-patient-site-enrollment]], [[expanded-access-workflow]]) stresses this framework at two points, and the system must treat both as first-class gates rather than edge cases.

**De-identification is presumptively unavailable at n=1.** Safe Harbor requires not only removal of the 18 identifier categories but also that the covered entity have *no actual knowledge* that the remaining information could be used, alone or in combination, to identify the individual ([§164.514(b)(2)(ii)](https://www.law.cornell.edu/cfr/text/45/164.514)). A dataset describing a single patient with a rare phenotype fails that second prong on its face — the small-cell problem: the combination of a rare condition, a clinical course, and any residual context is itself identifying, and the covered entity knows it. Expert Determination (§164.514(b)(1)) faces the same statistical reality. OSSICRO therefore does **not** treat §164.514(b) as available currency for single-patient or small-cohort exports; anything leaving the covered entity about the flagship patient is handled as identifiable PHI requiring one of the disclosure bases below. Cross-site analytics on de-identified data remain lawful only at cohort sizes where re-identification risk is genuinely very small.

**The manufacturer contact is a pre-authorization external disclosure and needs its own lawful basis.** The core workflow requires the treating physician to approach a manufacturer about a specific patient — the expanded-access intake, the single-patient site inquiry ([[single-patient-site-and-pharma-acceptance]], [[form-fda-3926-expanded-access]]) — typically *before* any research authorization exists. Preparatory review cannot cover this: PHI leaves the covered entity. Two lawful framings exist:

1. **Treatment disclosure — §164.506(c)(1).** A covered entity may use or disclose PHI *for its own treatment* activities without authorization, and individual-patient expanded access is by regulation a **treatment use** of an investigational drug (21 CFR 312.310). Disclosure to the manufacturer of the clinical information needed to obtain the drug for this patient's treatment fits that permission. Because the manufacturer is not a health care provider, the treatment exemption from minimum necessary (§164.502(b)(2)(i)) does not reach this disclosure — the minimum-necessary standard applies, and OSSICRO's drafted inquiry packet carries only what the acceptance decision requires. This framing is defensible but interpretive at the margin (marked as such); institutional privacy offices differ on it.
2. **Signed §164.508 authorization first.** The unambiguous path: obtain the patient's written authorization for the disclosure to the named manufacturer before the inquiry is sent.

OSSICRO's default is the conservative composite: the [[privacy-state-machine]] **blocks any outbound [[communication-hub]] message describing an identifiable patient** until the record contains either a signed §164.508 authorization covering that recipient or a documented treatment-disclosure determination under §164.506(c)(1) entered by the treating physician. The block is logged, and the fulcrum table below carries this phase explicitly.

## Supporting instruments

- **De-identification — §164.514(b).** Information de-identified under Safe Harbor (removal of the 18 identifier categories plus no actual knowledge of re-identifiability) or Expert Determination is not PHI, and OSSICRO's cross-site analytics and any shared eligibility datasets ride on this basis — **subject to the n=1 / small-cell limit stated above**. De-identification is performed inside the covered entity before anything leaves.
- **Limited data set + data use agreement — §164.514(e).** Where dates and geography are needed (e.g., feasibility statistics), a limited data set under a DUA meeting §164.514(e)(4) is the intermediate instrument.
- **Decedents — §164.512(i)(1)(iii).** Research on decedents' information proceeds on representations of death and necessity.
- **Common Rule interaction.** For HHS-supported research, 45 CFR 46 consent and IRB requirements run in parallel; HIPAA authorization and Common Rule consent are distinct instruments satisfied together ([[regulatory-landscape]], [[irb-submission-and-approval]]).

## The fulcrum, stated operationally

| Phase | Lawful basis | PHI movement | Gate evidence required |
|---|---|---|---|
| Matching / feasibility | §164.512(i)(1)(ii) preparatory review | None outside the covered entity; ephemeral audited reads; minimum necessary | Researcher representations recorded; audit log of reads |
| Manufacturer / sponsor inquiry about an identifiable patient (expanded-access intake, single-patient site inquiry) | §164.506(c)(1) treatment disclosure (expanded access is treatment use, 21 CFR 312.310) **or** §164.508 authorization naming the recipient | Minimum-necessary clinical summary to the named recipient only | Signed authorization, or documented treatment-disclosure determination by the treating physician; outbound message blocked until one exists |
| Recruitment contact | Treatment relationship, or partial waiver | None, or per waiver terms | Waiver documentation per §164.512(i)(2), if used |
| Enrollment / research use | §164.508 authorization **or** §164.512(i)(1)(i) full waiver | As authorized/waived, minimum necessary | Signed authorization in TMF, or documented waiver |
| Data sharing / analytics | §164.514(b) de-identification or §164.514(e) LDS+DUA | De-identified or limited data set only; **not available at n=1 / small cells** | De-identification determination or executed DUA |

> [!warning] Non-delegable
> Two human judgments anchor this page. The **IRB/Privacy Board waiver determination** (§164.512(i)(2)) is a board judgment OSSICRO assembles evidence for but never renders — the same non-delegable posture as IRB approval under 21 CFR 56 ([[non-delegable-functions-and-gates]], gate G2). And the **authorization signature** is the patient's own act, obtained in the consent conversation by a qualified human ([[informed-consent-document-vs-event]]). OSSICRO drafts the compound consent-authorization instrument and validates its required elements; it never obtains it. The **treatment-disclosure determination** for a manufacturer inquiry is likewise the treating physician's, not the system's.

> [!interpretive] OSSICRO position
> The Privacy Rule does not require that the preparatory→enrollment boundary be enforced by software; it requires the bases to be respected. OSSICRO's position is that in an AI-assisted matching system the boundary **must** be code-enforced to be credible: a hard, logged state transition ([[privacy-state-machine]]) that blocks any research use of PHI until the authorization or waiver record exists, and blocks any outbound message describing an identifiable patient until an authorization or documented treatment-disclosure basis exists, with no administrative override. This exceeds the regulatory floor deliberately — matching and the single-patient manufacturer inquiry are the highest-privacy-exposure surfaces of the system, and the mitigation for their highest-severity failure mode (silent PHI egress at scale, or an identifiable rare-disease patient exported under a "de-identified" label) is architectural, not procedural. See [[risks-and-limitations]].

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
- [[single-patient-site-enrollment]]
- [[single-patient-site-and-pharma-acceptance]]
- [[expanded-access-workflow]]
- [[form-fda-3926-expanded-access]]
- [[patient]]

## Sources

- [45 CFR 164.512 — Uses and disclosures for which an authorization or opportunity to agree or object is not required (eCFR)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.512)
- [45 CFR 164.508 — Uses and disclosures for which an authorization is required (eCFR)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.508)
- [45 CFR 164.506 — Uses and disclosures to carry out treatment, payment, or health care operations (eCFR)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.506)
- [45 CFR 164.514 — Other requirements relating to uses and disclosures of PHI (de-identification; limited data set) (eCFR)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.514)
- [45 CFR 164.502 — Uses and disclosures of PHI: general rules (minimum necessary) (eCFR)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.502)
- [21 CFR 312.310 — Individual patients (expanded access; treatment use) (eCFR)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-I/section-312.310)
- [HHS OCR: Research — HIPAA Privacy Rule guidance page](https://www.hhs.gov/hipaa/for-professionals/special-topics/research/index.html)
- [HHS OCR: Guidance on De-identification of PHI (Safe Harbor and Expert Determination)](https://www.hhs.gov/hipaa/for-professionals/special-topics/de-identification/index.html)
- [NIH: HIPAA Privacy Rule — Information for Researchers (Preparatory to Research)](https://privacyruleandresearch.nih.gov/)
- [45 CFR Part 46 — Protection of Human Subjects (Common Rule) (eCFR)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46)