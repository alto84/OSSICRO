# QA Review — PATIENT reviewer — patient advocate

**Model:** Fable 5 | claude-fable-5  
**Verdict:** The legal armor around the patient is genuinely strong — non-delegable consent, code-enforced privacy gating, three-valued matching — but the patient's lived interests (readability, injury compensation, n-of-1 re-identification, visibility into their own matching) are under-specified relative to the polish of the citations.

## Strengths
- The consent document-vs-event bright line is stated correctly and repeatedly (informed-consent-form.md, patient.md): OSSICRO drafts the ICF but the consent conversation, comprehension judgment, and voluntariness assessment stay with a qualified human on the delegation log. This is the single most important patient protection and it is handled without hedging.
- The three-valued eligibility contract with the explicit rule 'indeterminate is never silently coerced to not-met' (matching-eligibility-adjudication.md) directly encodes the patient-advocacy asymmetry: a false exclusion silently costs a patient access, so the system asks instead of rejecting. The safety-asymmetry defense is stated in the patient's favor, in writing.
- hipaa-and-privacy-gating.md gets the law right and then deliberately exceeds it: the preparatory-review/enrollment boundary is code-enforced with 'no administrative override,' local-first, minimum-necessary, with an audit log. The operational table (phase / lawful basis / PHI movement / gate evidence) is exactly the transparency a privacy advocate wants.
- patient.md correctly captures the subtle 164.524(a)(2)(iii) nuance — the patient's right of access to research records can be suspended during the trial only if they agreed at consent, and is reinstated at completion. Most systems miss this entirely.
- Matching rationale is auditable, not a black-box score: per-criterion citations to both the trial's exact eligibility text and the patient datum, and the machine never emits a bare eligible/ineligible. The investigator owns the call under 312.60.

## Findings
### [HIGH] wiki/05-ossicro-system/hipaa-and-privacy-gating.md
**Issue:** The flagship n-of-1 scenario breaks the page's own privacy model and the page never says so. For one physician + one patient + one rare condition, 'de-identified' data is effectively re-identifiable (small-cell problem: a Safe Harbor dataset of n=1 with a rare epilepsy phenotype identifies the patient), yet the page treats §164.514(b) de-identification as the compliant currency for anything leaving the covered entity. Worse, the core workflow requires the physician to approach a manufacturer ('my patient needs this drug' — expanded-access intake, single-patient site inquiry) BEFORE any authorization exists, and neither this page nor the fulcrum table has a row for that pre-authorization external disclosure about an identifiable single patient.

**Recommendation:** {f.get('recommendation','')}

### [HIGH] wiki/05-ossicro-system/matching-eligibility-adjudication.md
**Issue:** The 'indeterminate is never coerced to not-met' protection only exists at the adjudication stage. The retrieve stage applies hard binary filters on structured facets (condition, age/sex, geography, recruitment status) and a semantic ranker — a trial dropped at retrieval never reaches adjudication and the patient silently loses access with no ledger entry, no question routed to the clinician, and no trace. Geography is the worst offender: a filter excludes trials the patient would happily travel for. The page's own stated failure mode ('a patient silently loses access') is thus still live one stage earlier, and the recall commitment is deferred to a benchmarks page rather than being a contract on this page.

**Recommendation:** {f.get('recommendation','')}

### [HIGH] wiki/03-documents/informed-consent-form.md
**Issue:** Section 8 claims the engine will 'validate against 56.111/50.20 (no exculpatory language, understandable language)' — but 'understandable language' validation is completely unspecified for a system that AUTO-DRAFTS consent forms from Investigator's Brochure risk data. IB risk sections are written for regulators at graduate reading level; piping them into an ICF is the mechanism most likely to produce a legally-complete, humanly-incomprehensible consent form. No readability target (e.g., 6th-8th grade standard used by most IRBs), no health-literacy check, no plain-language transformation step, and translation for limited-English-proficiency patients gets one clause about the 46.117 short form with no workflow.

**Recommendation:** {f.get('recommendation','')}

### [MEDIUM] wiki/06-personas/patient.md
**Issue:** The persona page covers payment-to-subjects but is silent on the question that actually matters to a patient injured in an early-phase trial: research-injury compensation. 50.25(a)(6) requires the ICF to disclose whether compensation and medical treatment for injury are available — and in OSSICRO's core Mode B scenario the honest answer is likely 'none': a solo sponsor-investigator has no sponsor injury fund, and clinical malpractice insurance typically excludes research. The wiki's patient page should confront this rather than let the apparatus imply big-sponsor protections exist in the n-of-1 case.

**Recommendation:** {f.get('recommendation','')}

### [MEDIUM] wiki/06-personas/patient.md
**Issue:** The patient is given transparency theater but no agency. The interpretive design gate routes all matching output to the HCP only ('never trial recommendations directly to the patient'), the portal shows only plain-language status lines, and there is no stated recourse if the physician sits on the candidate list, no timeline expectation, and no right to see the adjudication ledger for their own case — even though the patient can already search ClinicalTrials.gov themselves and the frontend advertises 'transparent trial & therapy matching' to them. Paternalism here needs either a justification or a counterweight.

**Recommendation:** {f.get('recommendation','')}

### [MEDIUM] frontend/index.html
**Issue:** The frontend is benefit-forward recruitment-toned copy aimed partly at patients ('Get patients into trials. Not stuck in paperwork.'; patient card: 'Is there a trial for me?') with zero therapeutic-misconception counterweight — nothing says early-phase trials may not benefit the participant, that most Phase 1/2 drugs fail, or that participation is voluntary. The footer disclaims medical advice but not benefit. And despite the detailed-plan promise that 'each persona gets a portal perspective in the frontend,' there is no patient view at all — the patient card's promises (transparent matching, plain-language documents) link to nothing; 'Get started' is an anchor scroll.

**Recommendation:** {f.get('recommendation','')}

### [MEDIUM] wiki/03-documents/informed-consent-form.md
**Issue:** Section 6 says OSSICRO can 'run comprehension checks' in the eConsent flow. An AI administering and scoring comprehension quizzes edges into the consent event itself — the 2016 FDA/OHRP Q&A permits interactive methods, but the judgment that the subject comprehends belongs to the qualified human. As written, a reader could conclude a passed machine quiz satisfies the comprehension requirement.

**Recommendation:** {f.get('recommendation','')}

### [LOW] wiki/05-ossicro-system/hipaa-and-privacy-gating.md
**Issue:** The patient's 'right to revoke' the authorization is named (here and in patient.md) but its real-world consequence is never explained anywhere in the assigned pages: after revocation the covered entity may still use/disclose data already collected in reliance on the authorization (§164.508(b)(5)(i)), and trial data already reported is not clawed back. A patient reading 'right to revoke' will assume more than the law delivers — that is a comprehension failure in the system's own transparency story.

**Recommendation:** {f.get('recommendation','')}

### [LOW] wiki/06-personas/patient.md
**Issue:** The claim 'subject identity is coded in every OSSICRO record (identities never appear in logs or generated documents)' is overbroad and self-contradicting: the ICF and the HIPAA authorization are generated documents that necessarily bear the patient's name and signature.

**Recommendation:** {f.get('recommendation','')}

### [LOW] wiki/05-ossicro-system/matching-eligibility-adjudication.md
**Issue:** Minimum-necessary is asserted ('the matcher reads the data elements eligibility adjudication needs, not the whole chart') but adjudicating hundreds of criteria across a recall-first candidate set approaches whole-chart access in practice, and real SMART-on-FHIR deployments typically grant broad resource scopes. The claim is a design intention presented as a property.

**Recommendation:** {f.get('recommendation','')}

## Must-fix
- Add the n-of-1 privacy reality to hipaa-and-privacy-gating.md: de-identification fails at n=1, and the pre-authorization pharma/manufacturer contact about a specific patient needs an explicit lawful basis and a state-machine gate before any outbound message.
- Specify the ICF readability/health-literacy check concretely (metric, ceiling, plain-language transformation of IB-derived risk text, translation workflow) — 'understandable language' cannot remain an unvalidated assertion in a system that auto-drafts consent forms.
- Close the retrieval-stage silent-exclusion gap: soft geography/preference facets, retrieval-coverage disclosure to the clinician, and a recall contract stated on the matching page itself.
- Tell the truth about research-injury compensation in sponsor-investigator mode (patient.md + ICF element 6) and add a therapeutic-misconception counterweight plus honest scoping of the nonexistent patient portal to frontend/index.html.
