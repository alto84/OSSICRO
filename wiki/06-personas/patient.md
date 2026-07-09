---
title: "Persona: Patient / Research Participant"
section: "06-personas"
status: mixed
governing_authority:
  - "21 CFR Part 50 (informed consent; Subpart D for children)"
  - "45 CFR 46.116 (Common Rule consent, incl. key-information summary)"
  - "45 CFR 164.508, 164.512(i), 164.514, 164.524 (HIPAA)"
  - "21 CFR Part 56 (IRB); 21 CFR 312 Subpart I (expanded access)"
  - "Belmont Report; Declaration of Helsinki (2024) para. 27"
tags: [entity/patient, cfr/50, cfr/56, lifecycle/expanded-access, ossicro/gating, status/mixed]
aliases: ["Patient Persona", "Research Participant", "Subject"]
updated: 2026-07-09
---

# Persona: Patient / Research Participant

> [!authority] Governing authority
> [21 CFR Part 50](https://www.law.cornell.edu/cfr/text/21/part-50) (informed consent, including Subpart D for children); [21 CFR Part 56](https://www.law.cornell.edu/cfr/text/21/part-56) (IRB protection); [45 CFR 46.116](https://www.ecfr.gov/current/title-45/part-46/section-46.116) (Common Rule consent for federally supported research); HIPAA at [45 CFR 164.508](https://www.ecfr.gov/current/title-45/section-164.508), [164.512(i)](https://www.ecfr.gov/current/title-45/section-164.512), [164.514](https://www.ecfr.gov/current/title-45/section-164.514), and [164.524](https://www.ecfr.gov/current/title-45/section-164.524); [21 CFR 312 Subpart I](https://www.law.cornell.edu/cfr/text/21/part-312/subpart-I) for treatment use; the [Belmont Report](https://www.hhs.gov/ohrp/regulations-and-policy/belmont-report/index.html) and [Declaration of Helsinki (2024)](https://www.wma.net/policies-post/wma-declaration-of-helsinki/) para. 27 as ethical framework. Status: **Mixed** — the protections are confirmed black-letter law; the patient-portal perspective and matching flow are OSSICRO **interpretive** design.

The patient owns nothing regulated and signs almost nothing — yet the entire apparatus described in this wiki exists to protect them. Their entry question is: *"Is there a trial or early-phase therapy for my condition, and can my doctor get me in?"* That framing carries a known hazard — it presents research as a treatment-access pathway from the first screen, which is the seed of **therapeutic misconception** — and this page confronts that hazard directly (see [[#The dual-role hazard: therapeutic misconception and the treating-physician sponsor-investigator|the dual-role section]]) rather than leaving it implicit. This page describes what the patient needs, what they see and sign, and the specific regulatory and ethical rights that protect them at every step.

## Perspective and needs

- **Access.** A candidate trial or investigational therapy matched to their actual clinical picture — the discovery problem [[patient-trial-matching]] and the [[matching-engine]] solve. For most patients in under-resourced settings, the practical barrier is not eligibility but the absence of a physician with a research office; see [[hcp-physician]].
- **Comprehension.** A consent process they can actually understand, in language understandable to them (21 CFR 50.20), with time to consider and no pressure — including a clear understanding that **research is not treatment**, even when the person offering it is their treating physician.
- **Privacy.** Confidence that looking for a trial does not broadcast their medical record, and that enrolling discloses only what they authorized.
- **Safety.** Independent review before ([[irb-iec|IRB]]), during ([[dsmb-dmc|DSMB]], [[safety-reporting-lifecycle|safety reporting]]), and a clear exit at any time without penalty.
- **Honesty about what happens if things go wrong.** A truthful, pre-consent answer to whether compensation and medical treatment for research injury exist (21 CFR 50.25(a)(6)) — especially in the sponsor-investigator configuration, where the honest answer may be that they do not.

## Rights the regulations confirm

### Informed consent — 21 CFR Part 50

[21 CFR 50.20](https://www.law.cornell.edu/cfr/text/21/50.20) sets the floor: no investigator may involve a human in FDA-regulated research without **legally effective informed consent**, obtained under circumstances that give the person **sufficient opportunity to consider** participation and that **minimize coercion or undue influence**; the information must be in **language understandable** to the subject; and no consent may include **exculpatory language** waiving legal rights or releasing the investigator, sponsor, or institution from liability for negligence.

[21 CFR 50.25(a)](https://www.law.cornell.edu/cfr/text/21/50.25) requires eight basic elements: (1) a statement that the study involves research, its purposes, duration, procedures, and identification of any experimental procedures; (2) reasonably foreseeable risks or discomforts; (3) benefits reasonably to be expected; (4) appropriate alternative procedures or treatments; (5) the extent of confidentiality, noting the possibility of FDA inspection of records; (6) for more-than-minimal-risk research, whether compensation and medical treatments are available if injury occurs; (7) whom to contact about the research, about research subjects' rights, and about research-related injury; (8) that participation is **voluntary**, refusal involves **no penalty or loss of benefits**, and the subject **may discontinue at any time** without penalty. [50.25(b)](https://www.law.cornell.edu/cfr/text/21/50.25) adds six additional elements when appropriate (unforeseeable risks including to embryo/fetus, investigator-initiated termination, additional costs, consequences and procedures of withdrawal, provision of significant new findings, and approximate number of subjects). For "applicable clinical trials," [50.25(c)](https://www.law.cornell.edu/cfr/text/21/50.25) requires the verbatim ClinicalTrials.gov statement (see [[clinicaltrials-gov-registration]]).

[21 CFR 50.27](https://www.law.cornell.edu/cfr/text/21/50.27) requires consent be **documented** by a written form approved by the IRB and signed and dated by the subject or the subject's legally authorized representative, with a **copy given** to the signer. Narrow exceptions exist only at [50.23](https://www.law.cornell.edu/cfr/text/21/50.23) (life-threatening emergency, individual) and [50.24](https://www.law.cornell.edu/cfr/text/21/50.24) (emergency research with community consultation), and for children, Subpart D ([50.50–50.56](https://www.law.cornell.edu/cfr/text/21/part-50/subpart-D)) adds parental permission and child assent requirements.

For federally supported research, the revised Common Rule additionally requires a concise **key-information summary** at the start of consent ([45 CFR 46.116(a)(5)(i)](https://www.ecfr.gov/current/title-45/part-46/section-46.116)). FDA proposed harmonizing 21 CFR Parts 50/56 with the revised Common Rule in a 2022 notice of proposed rulemaking; as of this page's update the harmonization had not been finalized — OSSICRO's [[informed-consent-form|ICF templates]] include the key-information section as best practice regardless, and this is flagged as an interpretive drafting choice, not a 21 CFR 50 mandate.

> [!warning] Non-delegable
> The **informed-consent event** — the conversation in which a qualified person explains the study, answers the patient's questions, and assures voluntariness — is a human act. OSSICRO drafts, version-controls, and completeness-checks the consent **document** (including [eConsent mechanics per the 2016 FDA/OHRP Q&A](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-electronic-informed-consent-clinical-investigations-questions-and-answers) and [[part-11-and-ai-credibility|Part 11]]); it never conducts the consent. See [[informed-consent-document-vs-event]].

### Privacy — HIPAA

The privacy fulcrum is the line between **looking** and **enrolling** (see [[hipaa-and-privacy-gating]] and the code-enforced [[privacy-state-machine]]):

- **Matching is a review preparatory to research** ([45 CFR 164.512(i)(1)(ii)](https://www.ecfr.gov/current/title-45/section-164.512)): the treating clinician may review PHI to identify candidate trials, provided the review is necessary to prepare for research and **no PHI is removed** from the covered entity. In OSSICRO, matching runs locally and de-identified; nothing about the patient leaves the clinical boundary at this stage.
- **Enrollment requires a signed authorization** ([164.508](https://www.ecfr.gov/current/title-45/section-164.508)) — with the core elements (description of the PHI, who may use/disclose, recipients, purpose, expiration, signature/date) and required statements (right to revoke, non-conditioning except as permitted for research, and redisclosure risk) — or an IRB/Privacy-Board **waiver** under [164.512(i)(1)(i)](https://www.ecfr.gov/current/title-45/section-164.512) meeting the waiver criteria.
- **De-identified data** ([164.514(b)](https://www.ecfr.gov/current/title-45/section-164.514)) and **limited data sets** under a data-use agreement ([164.514(e)](https://www.ecfr.gov/current/title-45/section-164.514)) are the compliant currencies for anything analytic.
- The patient's **right of access** to their records ([164.524](https://www.ecfr.gov/current/title-45/section-164.524)) may be temporarily suspended for research-generated records during the trial **only if** the patient agreed to that when consenting ([164.524(a)(2)(iii)](https://www.ecfr.gov/current/title-45/section-164.524)), and is reinstated at completion.

### Independent protection — IRB and DSMB

Before any patient is approached, an [[irb-iec|IRB]] must find the [21 CFR 56.111](https://www.law.cornell.edu/cfr/text/21/56.111) criteria satisfied: risks minimized and reasonable relative to benefits, **equitable subject selection** (56.111(a)(3)), adequate consent, data-safety monitoring where appropriate, and privacy/confidentiality protections. During conduct, serious adverse events flow investigator → sponsor → FDA/IRB ([21 CFR 312.64(b)](https://www.law.cornell.edu/cfr/text/21/312.64), [312.32](https://www.law.cornell.edu/cfr/text/21/312.32)), and for trials with a [[dsmb-dmc|DSMB]], an independent body reviews unblinded safety data. None of this requires patient action — it is the apparatus working for them.

### Payment, costs, and compensation for research injury

Payment to subjects is recruitment-adjacent, IRB-reviewed, and must not be coercive or unduly influential ([FDA information sheet, Payment and Reimbursement to Research Subjects](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/payment-and-reimbursement-research-subjects)). Any **additional costs** to the patient must be disclosed in consent (50.25(b)(3)).

**Compensation for research injury is a separate and harder question.** [21 CFR 50.25(a)(6)](https://www.law.cornell.edu/cfr/text/21/50.25) requires that, for research involving more than minimal risk, the ICF explain **whether** any compensation and **whether** any medical treatments are available if injury occurs — and if so, what they consist of or where further information may be obtained. The regulation requires an honest disclosure, not a compensation program. In OSSICRO's core Mode B scenario — a solo [[sponsor-investigator]] with no commercial sponsor behind them — the honest answer may well be that **no injury-compensation fund exists** and that the physician's clinical malpractice coverage typically **excludes research activities**. That answer must be determined and disclosed truthfully **before** consent, not discovered after an injury. Two consequences for OSSICRO's drafting apparatus:

- **Insurance/indemnification is a red-flag completeness-ledger item for Mode B.** The [[completeness-ledger]] treats an unanswered injury-compensation question as a blocking gap in the ICF package: the sponsor-investigator must affirmatively determine what coverage (if any) exists — institutional indemnification, a purchased clinical-trials liability policy, or nothing — and the ICF must state the answer plainly.
- **Expect the IRB to scrutinize element (6) hardest in exactly this configuration.** A single-physician sponsor-investigator study is where the gap between the apparatus of a trial and the protections of a large sponsor is widest; the [[irb-submission-and-approval|submission package]] should address it head-on rather than leave the board to discover it.

Note the interaction with 50.20: disclosing that no compensation is available is lawful; asking the subject to **waive** rights or release anyone from negligence liability is prohibited exculpatory language.

## What the patient sees and signs

| Artifact | Patient's action | Authority |
|---|---|---|
| [[informed-consent-form\|Informed-consent form]] | Reads, discusses, signs, keeps a copy | 21 CFR 50.25, 50.27 |
| HIPAA research authorization | Signs (or is covered by an IRB waiver) | 45 CFR 164.508 |
| Assent form (children) + parental permission | Child assents; parent(s) sign | 21 CFR 50.55 |
| Study visit schedule / participant materials | Receives | Protocol; IRB-approved materials |
| Significant new findings | Receives during trial when they may affect willingness to continue | 21 CFR 50.25(b)(5) |
| Expanded-access consent | Signs — treatment use still requires Part 50 consent and IRB review | 21 CFR 312.305(c); Part 50 |

The patient never sees the [[form-fda-1572-statement-of-investigator|1572]], the [[ind-application-312-23|IND]], or the [[transfer-of-regulatory-obligations-toro|TORO]] — those are the machinery that make the consent form they *do* see truthful.

## The three pathways, from the patient's chair

The [[the-three-pathways-triage|triage]] looks different from this seat: enrolling in an existing trial (Mode A) makes the patient a **research subject** with the full Part 50/56 apparatus; a [[sponsor-investigator]] study (Mode B) is the same from the patient's perspective; [[expanded-access-workflow|expanded access]] ([21 CFR 312.310](https://www.law.cornell.edu/cfr/text/21/312.310), [[form-fda-3926-expanded-access|Form 3926]]) is **treatment, not research** — the primary purpose is to treat them, the manufacturer must agree to supply, and there is no placebo and no research endpoint, but consent and IRB protections still apply. See [[single-patient-site-enrollment]] for the n-of-1 routes.

## The dual-role hazard: therapeutic misconception and the treating-physician sponsor-investigator

The Mode B n-of-1 configuration — a treating physician becomes a [[sponsor-investigator]] specifically so that their own identified patient can receive an investigational therapy — is the textbook setup for two related ethical failures, and the wiki names them here rather than leaving the IRB to discover them.

**Therapeutic misconception.** When research is entered through the door marked "can my doctor get me in," the patient is primed to understand the study as individualized treatment. It is not: a Mode B study is **research**, with a protocol, research procedures, and uncertainty that the intervention will help them at all — even when the study exists because of them. The first 50.25(a)(1) element ("a statement that the study involves research") does real work here, and OSSICRO's [[informed-consent-form|ICF templates]] for Mode B include **mandatory language explicitly distinguishing research from treatment**, in the key-information summary and again in the body, as a drafting requirement rather than boilerplate.

**Dual-role conflict of interest.** The person who initiated the study to treat this patient is, by default, also the person who conducts the consent conversation and judges its voluntariness. The Belmont Report's respect-for-persons principle and [Declaration of Helsinki (2024)](https://www.wma.net/policies-post/wma-declaration-of-helsinki/) para. 27 speak directly to this: where the potential participant is in a **dependent relationship** with the physician-researcher, particular caution is required, and consent should be sought by an appropriately qualified individual **independent of that relationship**. Design consequences OSSICRO builds into the Mode B package:

- **Independent consent discussant or consent monitor.** For Mode B n-of-1 cases, the [[irb-submission-and-approval|IRB submission]] should propose — and the ICF process should default to — a qualified individual other than the treating physician/sponsor-investigator conducting or witnessing the consent discussion. This is presented to the IRB as a designed mitigation, not left for the board to impose.
- **Role and funding disclosure in the ICF.** The ICF discloses that the treating physician is also the sponsor-investigator of the study, and discloses any funding source or financial interest, so the patient consents knowing the dual role exists. (Financial-disclosure machinery on the FDA side is Part 54; the patient-facing disclosure lives in the ICF.)
- **Equitable selection in an n-of-1 study.** [21 CFR 56.111(a)(3)](https://www.law.cornell.edu/cfr/text/21/56.111) requires the IRB to find subject selection equitable, taking into account the purposes of the research and the setting. A single-patient study built around a preselected patient does not evade this criterion; it changes what the IRB must weigh — why *this* patient, whether the design forecloses others similarly situated, and whether a treatment-use pathway ([[expanded-access-workflow|expanded access]]) is the more honest frame when the intent is purely therapeutic. OSSICRO's [[the-three-pathways-triage|triage]] asks that question before the Mode B machinery starts, and the submission package addresses 56.111(a)(3) explicitly for single-patient designs.

> [!warning] Non-delegable
> Judging voluntariness, resolving the dual-role conflict, and deciding whether expanded access is the more appropriate pathway are human and IRB judgments. OSSICRO surfaces the conflict, drafts the disclosures, and defaults the independent-discussant design in; it never adjudicates the ethics.

> [!interpretive] OSSICRO position
> The patient's portal perspective shows plain-language status, never medical advice, and never PHI in transit outside the covered-entity boundary before authorization. Matching output goes to the **HCP**, who owns the medical judgment — a deliberate design gate, not a legal mandate on the patient side. The reason raw match output is withheld from the patient is stated, not hidden: an unmediated list of investigational programs delivered to a seriously ill person invites therapeutic misconception and self-triage without clinical context. The gate is paternalism with a justification — and it comes with counterweights:
>
> - **Minimum transparency floor.** The portal shows *"your doctor received N candidate programs on [date]"*, an **expected-response window**, and — on request — a plain-language summary of why candidates were or were not pursued. The patient is never left watching a spinner with no recourse.
> - **Stated recourse.** The portal states plainly what the patient can do if they disagree or the physician does not act: seek a second opinion, self-search [ClinicalTrials.gov](https://clinicaltrials.gov) (which is public and theirs to use), or pursue a self-referral path to another investigator.
> - **Expectation management by design.** No status language implies likelihood of enrollment before IRB approval and the physician's clinical judgment — "candidate programs identified" is permitted; "a trial is available for you" is not. A **"no suitable option found" pathway is a designed outcome**, delivered with standard-of-care framing, not an empty state.
> - **Patient-facing copy is IRB-reviewable.** Portal status language shown to a prospective subject is recruitment-adjacent material; OSSICRO treats it as part of the IRB-reviewed package rather than unregulated UI text.

## What documentation protects the patient

Every protection above is only as real as its paper: the IRB approval letter gates enrollment ([[irb-submission-and-approval]]); the signed, versioned ICF evidences consent (retained in case histories per [21 CFR 312.62(b)](https://www.law.cornell.edu/cfr/text/21/312.62)); the [[delegation-of-authority-log]] evidences that whoever consented them was authorized and trained; [[ind-safety-report|IND safety reports]] evidence that emerging risks reached FDA and other investigators. Subject identity is **coded** in OSSICRO's logs, audit trails, and system-internal records — identities never appear there. Subject-facing legal instruments (the signed ICF, the HIPAA authorization) necessarily carry the patient's name and signature; those are stored under the case-history ([312.62(b)](https://www.law.cornell.edu/cfr/text/21/312.62)) and [[investigator-site-file|ISF]] controls, not in the system's generated-document stream. Complete documentation is patient protection — which is the mission.

## Related

- [[informed-consent-form]]
- [[informed-consent-document-vs-event]]
- [[hipaa-and-privacy-gating]]
- [[privacy-state-machine]]
- [[patient-trial-matching]]
- [[the-three-pathways-triage]]
- [[expanded-access-workflow]]
- [[single-patient-site-enrollment]]
- [[sponsor-investigator]]
- [[irb-submission-and-approval]]
- [[completeness-ledger]]
- [[irb-iec]]
- [[dsmb-dmc]]
- [[hcp-physician]]
- [[perspective-matrix]]

## Sources

- [21 CFR Part 50 — Protection of Human Subjects](https://www.law.cornell.edu/cfr/text/21/part-50)
- [21 CFR 50.25 — Elements of informed consent](https://www.law.cornell.edu/cfr/text/21/50.25)
- [21 CFR 50.27 — Documentation of informed consent](https://www.law.cornell.edu/cfr/text/21/50.27)
- [21 CFR 56.111 — Criteria for IRB approval of research](https://www.law.cornell.edu/cfr/text/21/56.111)
- [45 CFR 46.116 — General requirements for informed consent (Common Rule)](https://www.ecfr.gov/current/title-45/part-46/section-46.116)
- [45 CFR 164.508 — Uses and disclosures for which an authorization is required](https://www.ecfr.gov/current/title-45/section-164.508)
- [45 CFR 164.512 — Uses and disclosures for which authorization is not required (incl. research)](https://www.ecfr.gov/current/title-45/section-164.512)
- [45 CFR 164.524 — Access of individuals to protected health information](https://www.ecfr.gov/current/title-45/section-164.524)
- [HHS — HIPAA and Research](https://www.hhs.gov/hipaa/for-professionals/special-topics/research/index.html)
- [HHS OHRP — The Belmont Report](https://www.hhs.gov/ohrp/regulations-and-policy/belmont-report/index.html)
- [WMA — Declaration of Helsinki (2024 revision)](https://www.wma.net/policies-post/wma-declaration-of-helsinki/)
- [FDA — Use of Electronic Informed Consent: Questions and Answers (Dec 2016)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-electronic-informed-consent-clinical-investigations-questions-and-answers)
- [FDA — Payment and Reimbursement to Research Subjects (information sheet)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/payment-and-reimbursement-research-subjects)
- [FDA — Expanded Access to Investigational Drugs for Treatment Use: Q&A (guidance)](https://www.fda.gov/media/85675/download)