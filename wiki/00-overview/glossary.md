---
title: "Glossary — OSSICRO Controlled Vocabulary"
section: "00-overview"
status: mixed
governing_authority:
  - "21 CFR 312.3(b) (definitions)"
  - "21 CFR 312.32(a) (safety-reporting definitions)"
  - "21 CFR Parts 11, 50, 54, 56"
  - "45 CFR 46; 45 CFR 160.103, 164.512(i)"
  - "ICH E6(R3) Glossary; ICH E2A; ICH E8(R1); ICH E9(R1)"
tags: [cfr/312, cfr/11, cfr/50, cfr/54, cfr/56, ich/e6r3, ich/e2a, ich/e8r1, ich/e9, status/confirmed, status/interpretive]
aliases: [Controlled Vocabulary, Definitions]
updated: 2026-07-09
---

# Glossary — OSSICRO Controlled Vocabulary

> [!authority] Governing authority
> Definitions are drawn from 21 CFR 312.3(b) and 312.32(a), 21 CFR Parts 11/50/54/56, 45 CFR 46 and 45 CFR Parts 160/164 (HIPAA), and the ICH E6(R3)/E2A/E8(R1)/E9(R1) glossaries. Status: **Mixed** — regulatory definitions are confirmed and cited to their source; OSSICRO-coined terms are explicitly marked *(OSSICRO term — interpretive)*.

This page is the controlled vocabulary for the entire wiki. Every term used with regulatory weight elsewhere in the corpus resolves here to a single definition with its citation. Where a term has both a regulatory definition and a colloquial usage, the regulatory definition controls. Terms coined by OSSICRO (micro-CRO, Mode A/Mode B, completeness ledger) carry no regulatory force and are labelled interpretive; see [[confirmed-vs-interpretive]] for the calibration standard.

> [!warning] Non-delegable
> A definition never transfers an obligation. Several terms below (informed consent, IRB approval, causality, sponsor attestation) name functions that must be performed by a qualified human or legally accountable entity regardless of what software drafts, checks, or routes. The master list is [[non-delegable-functions-and-gates]].

## A

- **Adverse event (AE)** — Any untoward medical occurrence associated with the use of a drug in humans, whether or not considered drug-related. *Citation:* [21 CFR 312.32(a)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32); ICH E2A §II.A. See [[safety-reporting-lifecycle]].
- **ALCOA+ / ALCOA++** — Data-integrity attribute set: Attributable, Legible, Contemporaneous, Original, Accurate, plus Complete, Consistent, Enduring, Available. *Citation:* ICH E6(R3) §4 (Data Governance); FDA Data Integrity and Compliance guidance (2018). *(Interpretive note:* "ALCOA++" is OSSICRO's house label for the E6(R3) attribute set plus explicit **traceability**, rendered in the [[draft-provenance-model]]; the regulation itself does not use the acronym.*)*
- **Anti-Kickback Statute (AKS)** — Federal criminal prohibition on remuneration to induce referrals of federal-health-program business; constrains trial budgets and IIS funding, which must be set at fair market value. *Citation:* [42 U.S.C. 1320a-7b(b)](https://www.law.cornell.edu/uscode/text/42/1320a-7b); safe harbors at 42 CFR 1001.952. See [[clinical-trial-agreement-and-budget]].
- **Annual report (IND)** — Brief report of the progress of the investigation submitted within 60 days of the IND anniversary date. *Citation:* [21 CFR 312.33](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.33). A DSUR (ICH E2F) is an accepted substitute. See [[ind-annual-report-dsur]].

## B

- **BIMO (Bioresearch Monitoring)** — FDA's inspection program for clinical investigators, sponsors, CROs, and IRBs; the enforcement surface behind every obligation in this wiki. *Citation:* FDA BIMO Compliance Programs (e.g., CP 7348.811 Clinical Investigators). See [[fda-as-counterparty]].

## C

- **Case report form (CRF)** — Printed or electronic document designed to record the protocol-required information to be reported to the sponsor on each trial participant. *Citation:* ICH E6(R3) Glossary. See [[conduct-and-monitoring]].
- **Clinical hold** — FDA order delaying a proposed investigation or suspending an ongoing one. *Citation:* [21 CFR 312.42](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-C/section-312.42). See [[ind-submission-and-30-day-clock]].
- **Clinical investigation** — Any experiment in which a drug is administered or dispensed to, or used involving, one or more human subjects, other than the use of a marketed drug in the course of medical practice. *Citation:* 21 CFR 312.3(b).
- **Clinical study report (CSR)** — The integrated full report of an individual study, per the ICH structure (synopsis, methods, results, appendices). *Citation:* [ICH E3](https://database.ich.org/sites/default/files/E3_Guideline.pdf) (FDA guidance 1996). See [[clinical-study-report]].
- **Common Rule** — The HHS regulation for protection of human subjects in federally conducted or supported research (2018 Requirements), harmonized-but-distinct from FDA Parts 50/56. *Citation:* [45 CFR 46 Subpart A](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46). See [[regulatory-landscape]].
- **Completeness ledger** *(OSSICRO term — interpretive)* — The per-package open-items contract: green (validated), amber (requires human judgment — a gate), red (missing data with the exact resolving question). OSSICRO's operating definition of "complete documentation." See [[completeness-ledger]].
- **Context of use (COU)** — The specific role and scope of an AI model in supporting a regulatory decision; the unit of risk assessment in FDA's AI credibility framework. *Citation:* FDA draft guidance, *Considerations for the Use of AI to Support Regulatory Decision-Making for Drug and Biological Products* ([90 FR, 2025-01-07](https://www.federalregister.gov/documents/2025/01/07/2024-31542/considerations-for-the-use-of-artificial-intelligence-to-support-regulatory-decision-making-for-drug); **draft** — comments closed 2025-04-07). See [[part-11-and-ai-credibility]].
- **Contract research organization (CRO)** — A person that assumes, as an independent contractor with the sponsor, one or more of the obligations of a sponsor. Transfer must be in writing; an assumed obligation makes the CRO subject to the same regulatory action as a sponsor. *Citation:* 21 CFR 312.3(b); [21 CFR 312.52](https://www.law.cornell.edu/cfr/text/21/312.52). See [[cro]], [[transfer-of-regulatory-obligations-toro]].
- **Critical-to-quality (CtQ) factors** — The attributes of a trial whose integrity is fundamental to participant protection and result reliability; the design-stage quality unit that E6(R3) risk-based quality management operationalizes. *Citation:* ICH E8(R1) §3; ICH E6(R3) §3 (Risk-Based Quality Management). See [[risk-based-monitoring-e6r3]].

## D

- **Data monitoring committee (DMC) / Data and safety monitoring board (DSMB)** — A group of individuals with pertinent expertise, independent of the sponsor and investigators, that reviews accumulating trial data and **recommends** (does not decide) continue/modify/stop to the sponsor. Required by regulation only for exception-from-informed-consent emergency research (21 CFR 50.24(a)(7)(iv)); otherwise guidance-driven. *Citation:* FDA guidance *Establishment and Operation of Clinical Trial Data Monitoring Committees* (2006); superseding [2024 draft](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-data-monitoring-committees-clinical-trials). See [[dsmb-dmc]], [[dsmb-charter]].
- **Delegation of authority log** — The investigator-maintained record of trial tasks delegated to qualified team members; delegation of tasks never transfers accountability. *Citation:* ICH E6(R3) §2.3; FDA guidance *Investigator Responsibilities* (2009). See [[delegation-of-authority-log]], [[subinvestigator-and-delegation]].
- **DSUR (Development Safety Update Report)** — The ICH-format annual safety report accepted by FDA in lieu of the 312.33 IND annual report. *Citation:* ICH E2F; 21 CFR 312.33. See [[ind-annual-report-dsur]].

## E

- **eConsent** — Electronic delivery, comprehension support, and signature capture for informed consent; permitted where 21 CFR 50.25/50.27 elements are met and the e-signature satisfies Part 11. Does not replace the human consent conversation. *Citation:* FDA/OHRP guidance, *Use of Electronic Informed Consent: Q&A* ([Dec 2016, final](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-electronic-informed-consent-clinical-investigations-questions-and-answers)). See [[informed-consent-document-vs-event]].
- **Electronic signature** — A computer-data compilation of symbols executed and adopted by an individual to be the legally binding equivalent of a handwritten signature. *Citation:* [21 CFR 11.3(b)(7)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11); §§11.50–11.300. See [[part-11-and-ai-credibility]].
- **Essential records** — The records (in whatever medium) that individually and collectively permit evaluation of the conduct of a trial and the quality of the data produced. E6(R3) deliberately shifted from "essential documents" (E6(R2) §8) to "essential records," applied risk-proportionately. *Citation:* [ICH E6(R3)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf) Appendix C. See [[document-catalog]].
- **Expanded access** — Use of an investigational drug for treatment (not research) of a patient with a serious or immediately life-threatening disease with no comparable or satisfactory alternative therapy; individual-patient (312.310, incl. emergency), intermediate-size (312.315), and treatment IND/protocol (312.320) categories. *Citation:* [21 CFR 312 Subpart I](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-I) (§§312.300–312.320); FDCA §561 (21 U.S.C. 360bbb). See [[expanded-access-workflow]], [[form-fda-3926-expanded-access]].

## F

- **Fair market value (FMV)** — The compensation standard for trial budgets and IIS support payments; the AKS-defensible basis for money flowing between pharma and a physician/site. *Citation:* 42 U.S.C. 1320a-7b(b); 42 CFR 1001.952(d) (personal-services safe harbor). See [[iis-request-workflow]], [[clinical-trial-agreement-and-budget]].
- **Form FDA 1571** — The IND cover sheet: the sponsor's identifying information, contents checklist, and signed commitments (30-day wait, IRB compliance, GCP conduct). Signature is a non-delegable sponsor attestation. *Citation:* 21 CFR 312.23(a)(1). See [[form-fda-1571-ind-cover]].
- **Form FDA 1572 (Statement of Investigator)** — The investigator's signed commitments to the sponsor (protocol adherence, consent, reporting per 312.64, IRB review); retained by the sponsor, not filed directly with FDA. *Citation:* 21 CFR 312.53(c)(1). See [[form-fda-1572-statement-of-investigator]].
- **Forms FDA 3454 / 3455** — Financial-disclosure certification (3454: no disclosable interests) or disclosure statement (3455: interests present) for each covered clinical investigator, submitted with a marketing application. *Citation:* [21 CFR Part 54](https://www.law.cornell.edu/cfr/text/21/part-54), esp. §§54.2, 54.4. See [[form-fda-3454-3455-financial-disclosure]].
- **Form FDA 3500A** — The MedWatch **mandatory** reporting form used for IND safety reports (ICSRs); distinct from the voluntary Form 3500. *Citation:* 21 CFR 312.32(c); ICH E2A/E2B(R3). See [[form-fda-3500a-medwatch]].
- **Form FDA 3674** — Certification of compliance with ClinicalTrials.gov requirements accompanying applications and submissions. *Citation:* 42 U.S.C. 282(j)(5)(B); FDAAA 801. See [[form-fda-3674-clinicaltrialsgov-certification]].
- **Form FDA 3926** — The streamlined individual-patient expanded-access IND application. *Citation:* 21 CFR 312.310; FDA guidance *Individual Patient Expanded Access Applications: Form FDA 3926*. See [[form-fda-3926-expanded-access]].

## G–I

- **Good clinical practice (GCP)** — The international ethical and scientific quality standard for designing, conducting, recording, and reporting trials involving human participants. *Citation:* ICH E6(R3) (FDA final guidance [2025-09-09](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e6r3-good-clinical-practice-gcp); no US compliance date set as of this writing). See [[regulatory-landscape]].
- **IND (Investigational New Drug application)** — The request for FDA authorization to administer an investigational drug to humans; the legal exemption from the premarket approval requirement for interstate shipment. *Citation:* [21 CFR Part 312](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312); 21 U.S.C. 355(i). See [[ind-application-312-23]].
- **IND safety report** — The sponsor's expedited notification to FDA and all participating investigators of qualifying safety findings: 15 calendar days for serious + unexpected suspected adverse reactions and qualifying findings; 7 calendar days for unexpected fatal or life-threatening suspected adverse reactions. *Citation:* 21 CFR 312.32(c)(1)–(c)(2). See [[ind-safety-report]], [[safety-report-timelines-7-15-day]].
- **Informed consent** — The **process** by which a subject voluntarily confirms willingness to participate, after being informed of all aspects relevant to the decision; documented per 50.27 but not reducible to the document. Consent may not be obtained by software. *Citation:* [21 CFR Part 50](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50), esp. §§50.20, 50.25, 50.27; 45 CFR 46.116 (key-information requirement). See [[informed-consent-document-vs-event]], [[informed-consent-form]].
- **Investigational new drug** — A new drug or biological drug used in a clinical investigation. *Citation:* 21 CFR 312.3(b).
- **Investigator** — The individual who actually conducts a clinical investigation, i.e., under whose immediate direction the drug is administered or dispensed to a subject; the responsible leader of an investigative team. Duties fixed at 21 CFR 312.60–312.69. *Citation:* 21 CFR 312.3(b). See [[investigator]].
- **Investigator-initiated study (IIS / IIT)** — Industry term (no CFR definition) for a study initiated and conducted by an investigator acting as sponsor-investigator, often with pharma support (drug and/or funding) routed through Medical Affairs. See [[iis-request-workflow]], [[pharma-partner-sponsor]].
- **Investigator site file (ISF)** — The investigator/institution's portion of the essential records, held at the site; complements the sponsor's TMF. *Citation:* ICH E6(R3) Appendix C. See [[regulatory-binder-isf-index]].
- **Investigator's brochure (IB)** — The compilation of clinical and nonclinical data relevant to the investigational drug that the sponsor must furnish to each investigator before the investigation begins. For a marketed drug, the package insert may substitute. *Citation:* 21 CFR 312.23(a)(5); [21 CFR 312.55(a)](https://www.law.cornell.edu/cfr/text/21/312.55). See [[investigators-brochure]].
- **IRB (Institutional Review Board) / IEC (Independent Ethics Committee)** — The board formally designated to review, approve, and conduct continuing review of research involving human subjects, applying the §56.111 (or §46.111) approval criteria. The approval determination is a non-delegable ethics judgment. *Citation:* [21 CFR Part 56](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56), esp. §56.102(g); 45 CFR 46; ICH E6(R3) Glossary (IEC). See [[irb-iec]], [[irb-review-workflow]].

## L–M

- **Letter of authorization (LOA)** — A manufacturer's written statement authorizing FDA to reference its IND/master file in support of another party's submission (e.g., an expanded-access IND or sponsor-investigator IND using the manufacturer's CMC data). *Citation:* 21 CFR 312.23(b) (right of reference); "right of reference or use" defined at 21 CFR 312.3(b). See [[expanded-access-coordination]].
- **Medical monitor** — The qualified physician responsible for trial-level medical safety judgment: seriousness, expectedness, causality, and the medical dimension of continue/modify/stop. Industry role, not a CFR-defined term; the underlying obligations sit at 21 CFR 312.32 and ICH E2A. See [[medical-monitor]].
- **Micro-CRO** *(OSSICRO term — interpretive)* — OSSICRO's thin, named, legally accountable human entity that assumes, via a written [[transfer-of-regulatory-obligations-toro|TORO]], only those sponsor obligations that 21 CFR 312.52 requires an accountable entity to hold when the sponsor-investigator cannot personally hold them. Never assumes investigator conduct obligations. See [[micro-cro-accountable-layer]].
- **Mode A / Mode B** *(OSSICRO terms — interpretive)* — Mode A: physician-as-site, enrolling into a pharma sponsor's protocol. Mode B: physician-as-sponsor-investigator holding their own IND. See [[two-modes-site-vs-sponsor-investigator]], [[the-three-pathways-triage]].
- **Monitor / monitoring** — The sponsor-selected, qualified person and the act of overseeing the progress of a clinical investigation to verify participant protection, protocol compliance, and data reliability; now risk-based under E6(R3). *Citation:* 21 CFR 312.53(d), 312.56(a); ICH E6(R3) §3 (monitoring). See [[clinical-monitor-cra]], [[monitoring-plan]].

## P–R

- **Part 11** — 21 CFR Part 11: the conditions under which electronic records and electronic signatures are trustworthy, reliable, and equivalent to paper records and handwritten signatures, including validation, audit trails (§11.10(e)), and access controls. *Citation:* [21 CFR Part 11](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11); FDA *Part 11 Scope and Application* guidance (2003). See [[part-11-and-ai-credibility]].
- **Preparatory to research (review preparatory to research)** — The HIPAA provision permitting a covered entity to use PHI, without authorization, to prepare a research protocol or assess feasibility, provided no PHI leaves the covered entity during the review. The lawful basis for OSSICRO's trial matching; enrollment requires authorization (164.508) or an IRB/Privacy Board waiver (164.512(i)(1)(i)). *Citation:* [45 CFR 164.512(i)(1)(ii)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.512). See [[hipaa-and-privacy-gating]], [[privacy-state-machine]].
- **Protected health information (PHI)** — Individually identifiable health information held or transmitted by a covered entity or business associate, in any form. *Citation:* [45 CFR 160.103](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-160/subpart-A/section-160.103).
- **Protocol amendment / information amendment** — Changes to protocols or new protocols require a protocol amendment (312.30); essential information not within the scope of a protocol or safety report is submitted as an information amendment (312.31). *Citation:* 21 CFR 312.30, 312.31. See [[annual-reporting-and-amendments]].

## S

- **Serious adverse event (SAE) / serious suspected adverse reaction** — An event that results in death, is life-threatening, requires or prolongs inpatient hospitalization, causes persistent or significant incapacity, is a congenital anomaly/birth defect, or is an important medical event per medical judgment. *Citation:* 21 CFR 312.32(a); ICH E2A §II.B. See [[safety-reporting-lifecycle]].
- **Single IRB (sIRB)** — The one IRB of record mandated for federally funded cooperative (multi-site) research in the US. FDA regulations permit but do not compel central IRB reliance for FDA-regulated studies. *Citation:* 45 CFR 46.114(b) (compliance date 2020-01-20); NIH sIRB policy (NOT-OD-16-094, effective 2018-01-25). See [[single-irb-mandate-and-central-irbs]].
- **Source data / source documents** — Original records (and certified copies) of clinical findings, observations, or other activities necessary for the reconstruction and evaluation of the trial. *Citation:* ICH E6(R3) Glossary. See [[conduct-and-monitoring]].
- **Sponsor** — The person (individual, company, institution, or organization) that takes responsibility for and initiates a clinical investigation, but does not actually conduct it. Duties fixed at 21 CFR 312.50–312.59. *Citation:* 21 CFR 312.3(b). See [[sponsor]].
- **Sponsor-investigator** — An **individual** who both initiates and conducts an investigation and under whose immediate direction the investigational drug is administered or dispensed. The term does not include any person other than an individual — no entity, and no software, can hold the role. Bears both the sponsor and the investigator obligation sets. *Citation:* 21 CFR 312.3(b); FDA draft guidance, *INDs Prepared and Submitted by Sponsor-Investigators* (May 2015, **draft**). See [[sponsor-investigator]], [[legal-thesis-3123-vs-31252]].
- **Subinvestigator** — Any individual member of the investigative team other than the investigator (its responsible leader) designated and supervised by the investigator to perform critical trial-related procedures or decisions. *Citation:* 21 CFR 312.3(b); Form FDA 1572 §6. See [[subinvestigator-and-delegation]].
- **Subject / participant** — A human who participates in an investigation, as recipient of the investigational drug or as a control. *Citation:* 21 CFR 312.3(b); "participant" is the E6(R3) usage.
- **SUSAR (suspected unexpected serious adverse reaction)** — ICH term (E2A) for the event class that triggers expedited reporting: a suspected adverse reaction that is both serious and unexpected. US operationalization: the 15-day IND safety report (7-day if fatal or life-threatening). *Citation:* ICH E2A; 21 CFR 312.32(c)(1)(i), (c)(2). See [[safety-report-timelines-7-15-day]].
- **Suspected adverse reaction** — An adverse event for which there is a **reasonable possibility** that the drug caused it — a lower causality standard than "adverse reaction." The determination is a qualified-physician judgment. *Citation:* 21 CFR 312.32(a) (as amended by 75 FR 59935, Sept 29, 2010).

## T–U

- **TORO (transfer of regulatory obligations)** — The written description, required by regulation, of each sponsor obligation transferred to a CRO; any obligation not described in writing is deemed **not** transferred. OSSICRO usage: the instrument by which the [[micro-cro-accountable-layer|micro-CRO]] assumes enumerated obligations. *Citation:* [21 CFR 312.52(a)–(b)](https://www.law.cornell.edu/cfr/text/21/312.52). See [[transfer-of-regulatory-obligations-toro]].
- **Trial master file (TMF)** — The sponsor-side collection of essential records permitting reconstruction and evaluation of trial conduct; with the ISF, the auditable evidentiary spine of the trial. *Citation:* ICH E6(R3) Appendix C; retention per 21 CFR 312.57(c), 312.62(c). See [[document-catalog]], [[record-retention-and-archival]].
- **Unanticipated problem** — The category of events (including certain adverse events) that investigators must report and IRBs must receive as "unanticipated problems involving risks to human subjects or others." *Citation:* 21 CFR 56.108(b)(1); 21 CFR 312.66. See [[irb-review-workflow]].
- **Unexpected (adverse event / suspected adverse reaction)** — Not listed in the investigator brochure at the observed specificity or severity (or, if no IB, not consistent with the risk information in the general investigational plan). *Citation:* 21 CFR 312.32(a).

> [!interpretive] OSSICRO position
> Terms marked *(OSSICRO term — interpretive)* — micro-CRO, Mode A/Mode B, completeness ledger, and the ALCOA++ house label — are design vocabulary, not regulatory categories. They are always mapped back to the confirmed authority they operationalize (312.52 for micro-CRO; 312.3(b)/312.52 for the mode split; E6(R3) Appendix C for the ledger) and must never be presented to a user as if FDA recognizes them.

## Related

- [[what-is-ossicro]]
- [[regulatory-landscape]]
- [[entity-map]]
- [[confirmed-vs-interpretive]]
- [[the-three-pathways-triage]]
- [[non-delegable-functions-and-gates]]
- [[document-catalog]]
- [[cfr-citation-map]]
- [[ich-guideline-map]]
- [[fda-form-index]]

## Sources

- [eCFR — 21 CFR Part 312 (definitions at §312.3)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312)
- [eCFR — 21 CFR 312.32 (IND safety reporting definitions)](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-D/part-312/subpart-B/section-312.32)
- [eCFR — 21 CFR Part 11](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-11) · [Part 50](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-50) · [Part 54](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-54) · [Part 56](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-A/part-56)
- [eCFR — 45 CFR Part 46 (Common Rule)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46)
- [eCFR — 45 CFR 164.512 (HIPAA research provisions)](https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164/subpart-E/section-164.512)
- [ICH E6(R3) Step 4 Final Guideline (2025-01-06, PDF)](https://database.ich.org/sites/default/files/ICH_E6%28R3%29_Step4_FinalGuideline_2025_0106.pdf)
- [FDA — E6(R3) Good Clinical Practice guidance page (Sept 2025)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e6r3-good-clinical-practice-gcp)
- [ICH Efficacy Guidelines (E2A, E2B, E2F, E3, E8, E9)](https://www.ich.org/page/efficacy-guidelines)
- [FDA — INDs Prepared and Submitted by Sponsor-Investigators (draft, 2015)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/investigational-new-drug-applications-prepared-and-submitted-sponsor-investigators)
- [FDA/OHRP — Use of Electronic Informed Consent: Q&A (final, Dec 2016)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/use-electronic-informed-consent-clinical-investigations-questions-and-answers)
- [Federal Register — FDA AI draft guidance (2025-01-07)](https://www.federalregister.gov/documents/2025/01/07/2024-31542/considerations-for-the-use-of-artificial-intelligence-to-support-regulatory-decision-making-for-drug)
