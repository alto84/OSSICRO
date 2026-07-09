# QA Review — PHARMA reviewer — clinical-operations / medical-affairs decision-maker

**Model:** Fable 5 | claude-fable-5  
**Verdict:** Regulatory scholarship a pharma compliance team would respect, but the acceptance model is optimistic where it matters: the door-in problem (no intake for unsolicited sites, AOI-gated IIS committees, institutional-counterparty preference) and the sponsor-side marginal costs of an n-of-1 site are underweighted, and the hash-chain dossier is pitched at a trust problem sponsors don't actually have — I would read the dossier with interest and still route the patient to an existing site or expanded access.

## Strengths
- Regulatory anatomy of the pharma interface is genuinely correct and unusually well-cited: Medical Affairs vs Clinical Development vs Commercial routing and the firewall, MSL constraints, 312.53(c)(1) 1572-before-drug-ships, Part 54 thresholds, §56.105 chair concurrence, LOA cross-reference under 312.305(b)(1), FDCA §561A non-compellable supply — these match how the inside of a pharma company actually works, which is rare in outside-built material.
- The three-route triage (individual-patient EA / site-add / S-I IIS) in single-patient-site-and-pharma-acceptance.md is the right decomposition, and the insistence that physician-side and manufacturer-side triage must agree on which route is live is an insight most site-facing tools miss entirely.
- Interpretive-vs-confirmed status labeling is disciplined and honest — the pages repeatedly flag their own weakest claims (dossier sufficiency 'interpretive and unproven at scale'), which is exactly the epistemic hygiene a sponsor's reviewer wants to see.
- Non-delegable gates are consistently and correctly drawn on the pharma side: supply decision, FMV/AKS judgment, funding decision, causality/expectedness — nothing in these five files pretends software can make pharma say yes.
- The money rails (AKS personal-services safe harbor conditions, Sunshine research-payment category with delayed publication, FMV-set-in-advance) are stated accurately and at the right level for a compliance conversation.

## Findings
### [HIGH] wiki/05-ossicro-system/verifiable-site-qualification-dossier.md
**Issue:** The hash-chained manifest solves a problem pharma does not have. As a sponsor quality/clin-ops decision-maker, my distrust of a new site is not 'the documents might be tampered with' — it is future operational conduct: coordinator bandwidth, protocol-deviation risk, data-entry quality over time, monitoring findings, inspection exposure. No sponsor QA function has an SOP for 'recompute a third party's SHA-256 chain,' and no pharma IT security policy lets a reviewer run a bundled 'dependency-free verification tool' from an unvetted open-source source inside the network. The page itself concedes the real wedge in its interpretive callout ('a complete, credentialed, internally-consistent package is what a sponsor's trust gate actually requires') — the crypto layer is garnish the buyer will never consume, yet it is positioned as the headline differentiator and the Micro-CRO 'moat.'

**Recommendation:** {f.get('recommendation','')}

### [HIGH] wiki/04-coordination/single-patient-site-and-pharma-acceptance.md
**Issue:** Route 2 (one-patient site added to the company's protocol) hand-waves the sponsor-side economics with 'expedited qualification rather than a full SQV where the sponsor's risk assessment permits.' OSSICRO software running at the site absorbs none of the sponsor's marginal costs: protocol-specific EDC account build and training, IRT/RTSM configuration and a new drug-supply shipping lane, scheduled IMVs for a one-subject site, indemnification/insurance amendment, addition to the sponsor's inspection footprint, and internal change control on an active protocol. Sponsors mid-enrollment routinely refuse site adds outright and steer the physician to an existing site or to expanded access — which is what actually happens. The page never ranks the three routes by realistic acceptance probability, so a physician-user will burn months pursuing the route pharma is least likely to grant.

**Recommendation:** {f.get('recommendation','')}

### [HIGH] wiki/02-lifecycle/iis-request-workflow.md
**Issue:** The IIS workflow is document-complete but acceptance-naive. Missing realities a Medical Affairs decision-maker lives with daily: (1) IIS programs publish areas-of-interest lists and decline most unsolicited concepts — strategic-fit rejection, not paperwork rejection, is the dominant failure mode, so a perfectly formatted synopsis outside the AOI is dead on arrival; (2) cycle time — committee review typically runs months, contracting months more, which collides fatally with the 'my patient needs this now' guiding scenario; (3) most companies will not contract with, or supply pre-approval investigational drug to, a solo private-practice physician — IIS agreements are signed with an institution's legal entity (indemnification, insurance, institutional oversight), and a physician with no institution is a structural non-starter the page never addresses. This is the single biggest adoption blocker for the solo-clinician premise on my side of the table.

**Recommendation:** {f.get('recommendation','')}

### [MEDIUM] wiki/04-coordination/pharma-partner-interface-iis.md
**Issue:** The interoperability section lists the CTMS/eTMF/EDC/IRT/safety-DB stack correctly, then quietly concedes there is no automated write-access and 'portal-shaped records' — which is not a defined thing. The unaddressed question my quality function will actually ask: if a site's regulatory documents live in OSSICRO, who stands behind OSSICRO's own Part 11 validation? Sponsors qualify vendors via audits (IQ/OQ/PQ evidence, SOPs, a legal entity to hold accountable). Open-source software self-hosted by the physician under review has no auditable vendor — and the dossier page's manifest even lists the Part 11 attestation signer as 'Deploying entity,' i.e., the same solo physician attesting to his own system's validation. That self-attestation fails sponsor QA on its face.

**Recommendation:** {f.get('recommendation','')}

### [MEDIUM] wiki/06-personas/pharma.md
**Issue:** The persona page names Clinical Development as the Mode A counterparty but assumes a landing pad that mostly doesn't exist: sponsors have no intake function for unsolicited inbound 'accept me as a site' requests from unknown physicians. Site identification runs outward through the sponsor's CRO feasibility machinery and site databases; a cold OSSICRO-armed inbound reaches, at best, a ClinicalTrials.gov central contact whose job is patient referral, not site adds. The 'acceptance workflow OSSICRO builds around' is flagged interpretive, but the page never tells the user the door may simply not open, or where the actual doors are.

**Recommendation:** {f.get('recommendation','')}

### [MEDIUM] wiki/04-coordination/single-patient-site-and-pharma-acceptance.md
**Issue:** Acceptance-gate item 6 ('a validated, Part 11-compliant document/data environment') overstates what a manufacturer requires for individual-patient expanded access — in practice EA physicians run on paper and institutional EMRs, and no expanded-access coordinator demands Part 11 validation evidence from a treating physician. Inflating the gate contradicts the page's own risk-proportionality argument and makes the 'minimal-but-compliant' package less minimal than the regulation or practice requires.

**Recommendation:** {f.get('recommendation','')}

### [LOW] wiki/02-lifecycle/iis-request-workflow.md
**Issue:** Sources list leans on secondary/vendor material for the money rails (IntuitionLabs blog, Advarra blog, Health Affairs brief) where primary authority exists and is cited elsewhere in the wiki; a pharma compliance reviewer discounts vendor-blog citations in a document that elsewhere holds itself to black-letter sourcing.

**Recommendation:** {f.get('recommendation','')}

## Must-fix
- single-patient-site-and-pharma-acceptance.md: add honest route ranking and the sponsor-side costs of Route 2 that OSSICRO cannot absorb (EDC/IRT build, monitoring visits, supply lane, indemnification, inspection footprint); document the standard sponsor counter-offer (existing site referral or expanded access).
- iis-request-workflow.md: address the solo-physician-without-institution contracting problem explicitly — most IIS programs contract only with institutional legal entities and will not supply investigational product to unaffiliated private-practice S-Is; specify whether the Micro-CRO is the answer and how.
- pharma-partner-interface-iis.md / verifiable-site-qualification-dossier.md: name the auditable entity behind OSSICRO's Part 11 validation (the Micro-CRO), because a solo physician self-attesting his own system's validation fails sponsor vendor-qualification on its face.
- verifiable-site-qualification-dossier.md: demote hash-chain verification from headline trust wedge to internal integrity feature; the sponsor-consumable wedge is completeness + citation mapping + credentialed signers in portal-native format, and the sponsor-side verification path must assume the reviewer runs no OSSICRO tooling.
