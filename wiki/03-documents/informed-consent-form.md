---
title: "Informed Consent Form (21 CFR 50.25; Common Rule Key Information; eConsent)"
section: "03-documents"
status: mixed
governing_authority:
  - "21 CFR 50.20, 50.25, 50.27 (FDA informed consent)"
  - "45 CFR 46.116, 46.117 (Common Rule informed consent + key information)"
  - "21 CFR 312.60 (investigator duty to obtain consent)"
  - "FDA/OHRP Use of Electronic Informed Consent Q&A (2016)"
  - "21 CFR Part 11 (electronic signatures)"
tags: [cfr/50, cfr/11, cfr/312, lifecycle/activation, lifecycle/conduct, role/investigator, ossicro/gating, status/confirmed, status/interpretive]
aliases: ["ICF", "informed consent", "informed consent form", "consent form", "eConsent", "50.25"]
updated: 2026-07-09
---

# Informed Consent Form (21 CFR 50.25; Common Rule Key Information; eConsent)

> [!authority] Governing authority
> **21 CFR 50.20** (general requirements), **21 CFR 50.25** (elements — basic + additional), **21 CFR 50.27** (documentation); **45 CFR 46.116** (Common Rule elements + **key-information** summary), **45 CFR 46.117** (documentation); **21 CFR 312.60** (no subject enrolled without legally effective consent); **FDA/OHRP 2016 eConsent Q&A**; **21 CFR Part 11** for the electronic signature. Status: **Mixed** — the consent **elements** are confirmed black-letter; the document-vs-event boundary is a confirmed legal distinction OSSICRO foregrounds; eConsent mechanics and OSSICRO's authoring role are flagged interpretive.

The **informed consent form (ICF)** is the written document that records the information a prospective subject must receive and the subject's (or legally authorized representative's) voluntary agreement to participate. It is distinct from **informed consent itself**, which is a **process** — the human conversation in which a qualified person gives the subject the opportunity to consider participation, answers questions, and confirms voluntary, uncoerced, competent agreement. OSSICRO drafts, version-controls, and completeness-checks the **document**; it must never conduct or substitute for the **event**. This bright line is the single most important gate in the system ([[informed-consent-document-vs-event]], [[non-delegable-functions-and-gates]]).

> [!warning] Non-delegable
> Obtaining informed consent is a **non-delegable subject-facing human act**. 21 CFR 312.60 forbids an [[investigator]] from involving a human as a subject unless **legally effective informed consent** is obtained; 21 CFR 50.20 requires that consent be sought under circumstances that give the subject sufficient opportunity to decide **without coercion or undue influence**. OSSICRO generates and maintains the ICF and can drive an eConsent presentation flow, but the consent **conversation, comprehension confirmation, and the qualified person's judgment that consent is valid** stay with a human on the delegation-of-authority log ([[delegation-of-authority-log]]). No AI action satisfies the consent requirement.

## 1. General requirements — 21 CFR 50.20

Except as provided in 50.23 (emergency) and 50.24 (planned emergency research), no investigator may involve a human as a subject unless the investigator has obtained the legally effective informed consent of the subject or the subject's **legally authorized representative (LAR)**. Consent must be:

- sought only under circumstances giving the prospective subject sufficient **opportunity to consider** whether to participate and **minimizing the possibility of coercion or undue influence**;
- in **language understandable** to the subject or the representative;
- free of **exculpatory language** through which the subject waives or appears to waive any legal rights or releases the investigator, sponsor, institution, or agents from liability for negligence.

## 2. Basic elements — 21 CFR 50.25(a)

The ICF must contain each of the eight basic elements (FDA numbering; the Common Rule at 45 CFR 46.116(b) is harmonized):

1. A statement that the study involves **research**, an explanation of its **purposes**, the **expected duration** of participation, a description of the **procedures**, and identification of any procedures that are **experimental**.
2. A description of any **reasonably foreseeable risks or discomforts** — consistent with the [[investigators-brochure|Investigator's Brochure]] risk section.
3. A description of any **benefits** to the subject or to others that may reasonably be expected.
4. A disclosure of appropriate **alternative** procedures or courses of treatment.
5. A statement describing the extent to which **confidentiality** of records will be maintained, and noting the possibility that **FDA may inspect** the records.
6. For research involving more than minimal risk, an explanation of whether **compensation** and **medical treatment for injury** are available.
7. An explanation of whom to **contact** for questions about the research and research subjects' rights, and whom to contact in the event of a **research-related injury**.
8. A statement that participation is **voluntary**, that refusal involves no penalty or loss of benefits, and that the subject may **discontinue at any time** without penalty or loss of benefits.

## 3. Additional elements — 21 CFR 50.25(b)

When appropriate, one or more of the additional elements must be provided, including: unforeseeable risks (including to an embryo/fetus); circumstances under which participation may be terminated by the investigator; additional costs to the subject; consequences of withdrawal and orderly-termination procedures; a statement that significant new findings will be provided; the approximate number of subjects; and — for applicable clinical trials — the mandatory **ClinicalTrials.gov statement** required by 21 CFR 50.25(c) (referencing 42 U.S.C. 282(j); see [[clinicaltrials-gov-registration]]).

## 4. Key-information summary — 45 CFR 46.116(a)(5)

Under the revised **Common Rule** (2018 requirements), consent must **begin with a concise and focused "key information"** presentation — the information a reasonable person would want in order to make an informed decision (purpose, voluntariness, risks, benefits, alternatives) — organized to **facilitate comprehension**, before the full detail. FDA has moved to harmonize (2022–2023 alignment activity under the Cures Act §3023); OSSICRO drafts the ICF with a **key-information front section** as the default so a single template satisfies both frameworks. Where a study is **both** FDA-regulated **and** HHS-supported, both 21 CFR 50 **and** 45 CFR 46 apply and the stricter requirement governs.

## 5. Documentation — 21 CFR 50.27 / 45 CFR 46.117

Informed consent must be **documented** by a written consent form approved by the [[irb-iec|IRB]] and **signed and dated** by the subject or the LAR at the time of consent; a copy is given to the person signing. FDA (50.27) generally requires the full written form; the Common Rule (46.117) permits a **short-form** written consent with an oral presentation and witness in defined circumstances. The signed form is filed in the subject's records and the [[regulatory-binder-isf-index|ISF]]; the fact and date of consent are recorded in the case history (21 CFR 312.62(b)).

## 6. Electronic informed consent (eConsent)

> [!interpretive] OSSICRO position — eConsent mechanics vs. the human event
> The **FDA/OHRP 2016 "Use of Electronic Informed Consent" Q&A** authorizes electronic delivery and electronic signature of consent, subject to: IRB review and approval of the eConsent **materials and process**; methods to promote and **confirm comprehension** (e.g., interactive elements, questions); confirmation of the **identity** of the signatory; subject **access to a copy**; and an electronic signature that satisfies **21 CFR Part 11** (unique attribution, authentication, non-repudiation, audit trail — [[part-11-and-ai-credibility]]). OSSICRO can present the eConsent flow, run comprehension checks, capture the Part-11-compliant e-signature, and file the executed record with an ALCOA++ audit trail. **What OSSICRO does not do:** replace the qualified person who conducts the consent discussion, answers questions in real time, and judges voluntariness and capacity. eConsent changes the medium, not the human requirement. Flagged interpretive; grounded in the 2016 guidance and Part 11.

## 7. Special populations

- **Children (Subpart D)** — 21 CFR 50.50–50.56 (and 45 CFR 46 Subpart D) impose additional protections and require, in addition to parental permission, the **assent** of the child where appropriate. Directly relevant where the enrolling clinician's population is pediatric; OSSICRO produces the parental-permission and age-appropriate assent documents as separate gated artifacts.
- **LAR / impaired capacity** — where the subject cannot consent, consent is obtained from a legally authorized representative per applicable law; OSSICRO surfaces this as a documented eligibility branch, not an automated determination.

## 8. The OSSICRO gate

The ICF is generated by the [[generate-check-validate-engine]]: **generate** the document from the [[clinical-protocol-and-synopsis|protocol synopsis]] and IB risk data (each span carrying a [[draft-provenance-model|provenance triple]] to its source and CFR citation); **check** all eight 50.25(a) elements plus applicable (b)/(c) additions and the key-information summary; **validate** against 56.111/50.20 (no exculpatory language, understandable language). The completed ICF then enters the [[irb-submission-package|IRB package]] for **approval**, and enrollment is gated on documented IRB approval **and** the executed, human-conducted consent event. Both the IRB approval and the consent event are non-automatable ([[completeness-ledger]] renders them as **amber** human-judgment gates).

## Related
- [[informed-consent-document-vs-event]]
- [[investigators-brochure]]
- [[clinical-protocol-and-synopsis]]
- [[irb-submission-package]]
- [[irb-iec]]
- [[investigator]]
- [[enrollment-and-consent]]
- [[delegation-of-authority-log]]
- [[regulatory-binder-isf-index]]
- [[clinicaltrials-gov-registration]]
- [[part-11-and-ai-credibility]]
- [[hipaa-and-privacy-gating]]
- [[patient]]
- [[generate-check-validate-engine]]
- [[draft-provenance-model]]
- [[non-delegable-functions-and-gates]]

## Sources
- [21 CFR 50.20 — General requirements for informed consent](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50/subpart-B/section-50.20)
- [21 CFR 50.25 — Elements of informed consent](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50/subpart-B/section-50.25)
- [21 CFR 50.27 — Documentation of informed consent](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50/subpart-B/section-50.27)
- [45 CFR 46.116 — General requirements for informed consent (Common Rule, incl. key information)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46/subpart-A/section-46.116)
- [45 CFR 46.117 — Documentation of informed consent](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46/subpart-A/section-46.117)
- [21 CFR 312.60 — General responsibilities of investigators](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-D/section-312.60)
- [FDA/OHRP (2016) — Use of Electronic Informed Consent: Questions and Answers](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-electronic-informed-consent-clinical-investigations-questions-and-answers)
- [21 CFR Part 11 — Electronic Records; Electronic Signatures](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11)
