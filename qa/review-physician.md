# QA Review — PHYSICIAN reviewer — enrolling community physician (primary user)

**Model:** Fable 5 | claude-fable-5  
**Verdict:** The regulatory map is the best I have ever seen aimed at a solo clinician and the non-delegable framing earns trust, but as a product it is a wiki plus a CLI plus a brochure: the four things that would actually stop me (IRB access, malpractice/research insurance, research billing compliance, and pharma saying yes) are absent or assumed away, and the frontend demonstrates no clinician flow at all.

## Strengths
- The non-delegable-duties table in wiki/06-personas/hcp-physician.md is honest in a way no vendor pitch ever is: it gives equal weight to what I keep (1572 Field 9, causality, 312.62 case histories, 312.68 inspection exposure) as to what it removes. That is exactly what builds trust with a physician who has been burned by 'we handle everything' CRO promises.
- The three-route table in single-patient-site-enrollment.md (expanded access vs one-patient site vs S-I IND, with speed/obligation-load/accountability columns) is precisely the triage decision I cannot make today without a regulatory consult. Making it legible in one table, with the warning that route selection is my judgment, is real value.
- The completeness ledger concept — red items ship with 'the exact resolving question' — is the single best UX idea here. 'Provide contact_phone (monitor, item 14) before filing' is how a checklist should talk to a busy clinician.
- Gates enforced in code (engine README: GateViolation on finalizing a gated document without recorded human sign-off, demo shows the engine refusing to sign a 1572) is a real implemented artifact, not a slide. The hard line is structural, not rhetorical.
- Citations are specific and correct at the level I can verify: 312.53(c) commitment package, 312.55(a) IB-before-start, 312.310(d) 15-working-day written follow-up for emergency use, Part 54 one-year post-study update commitment, drug release as the last act of activation per 312.53(b). The intimidation-points section (hcp-physician.md) shows the author actually understands why physicians don't enroll — fear of BIMO inspection is named, which almost nobody writing software for clinicians understands.

## Findings
### [HIGH] frontend/index.html
**Issue:** This is a static marketing landing page, not the 'pharma-corporate-style frontend demonstrating the clinician flow end-to-end' that PROGRAM.md success criterion 4 claims is done. There is no triage wizard, no intake form, no document view, no ledger wired to the engine — the 'Live example — actual engine output' ledger is hand-transcribed HTML, and 'Get started' scrolls to a persona card grid. As the primary user I can do exactly nothing with this page except click through to GitHub.

**Recommendation:** {f.get('recommendation','')}

### [HIGH] wiki/06-personas/hcp-physician.md
**Issue:** The intimidation-points list omits three prerequisites that stop a community physician before any document is drafted: (1) IRB access — a solo clinic has no institutional IRB; which central IRB reviews my protocol, at what fee ($2–5K+ initial review), on what timeline, and who contracts with them is nowhere in the physician-facing burden map; (2) malpractice/liability — my clinical malpractice policy almost certainly excludes research activity, and sponsor-investigator work is uninsurable without a specific rider; indemnification is not mentioned; (3) research billing compliance — Medicare coverage analysis, qualifying-trial determination, and the double-billing exposure that has produced real FCA settlements. Any one of these is a hard stop that a perfect paperwork package does not touch.

**Recommendation:** {f.get('recommendation','')}

### [HIGH] wiki/00-overview/guiding-scenario.md
**Issue:** Step 2→3 assumes away the binding constraint in one sentence: 'Assume the sponsor's protocol is open and willing to add a site.' For a community physician, getting pharma to return the call is the wall — PROGRAM.md itself names contract/budget negotiation as the dominant chokepoint, and a drafted CTA template does not resolve a bilateral negotiation with pharma legal that routinely takes months. The scenario that is supposed to be the spine of the architecture skips the step where the counterparty says yes.

**Recommendation:** {f.get('recommendation','')}

### [MEDIUM] wiki/06-personas/hcp-physician.md
**Issue:** Effort/reward is never quantified. 'The burden OSSICRO removes' lists categories but nowhere states what remains in physician-hours per route: GCP training (~8h), IRB back-and-forth, the SIV, 24/7 SAE availability once the drug is administered, monitoring visits, and — in Mode B — perpetual IND maintenance that is a standing part-time job even with perfect drafting. Barrier #5 is 'Time' and the page never answers it with a number. A physician deciding whether to do this needs the residual-hours estimate more than any other single datum.

**Recommendation:** {f.get('recommendation','')}

### [MEDIUM] wiki/02-lifecycle/single-patient-site-enrollment.md
**Issue:** Route 3's medical-monitor problem is unaddressed: in an n-of-1 sponsor-investigator study I own causality/expectedness for 7/15-day IND safety reports on my own patient — a self-review conflict — and there is no coverage plan for when I am unreachable. Guiding-scenario Step 6 assigns causality to 'the medical monitor's judgment,' but in Route 3 the medical monitor is me. site-activation.md flags self-monitoring as 'the structural weak point' but the safety-judgment analog is silent in these files.

**Recommendation:** {f.get('recommendation','')}

### [MEDIUM] engine/README.md
**Issue:** The engine's generation is {{field}} substitution over a built-in template set (4 templates done; the 78-doc library is pending per PROGRAM.md). That is adequate for a 1572 but structurally incapable of drafting the documents where quality actually decides acceptance — a protocol-specific ICF risk section or an M11 protocol. The validate pass checks presence (e.g., '8 basic elements present'), not adequacy; a GREEN/AMBER ledger status could induce a physician to over-trust a document an IRB or sponsor will reject on substance. The 'drafts COMPLETE documentation' claim currently outruns the artifact.

**Recommendation:** {f.get('recommendation','')}

### [MEDIUM] wiki/02-lifecycle/single-patient-site-enrollment.md
**Issue:** The Route 2 wedge thesis — a verifiable dossier converts 'no track record' into sponsor acceptance — treats sponsor refusal as a trust/information problem. It is substantially an economics problem: per-site activation, monitoring, and safety-data-exchange costs for a one-patient site exceed its enrollment value on most sponsor models, and a beautiful dossier does not change that arithmetic. The page correctly flags the thesis interpretive, but still calls Route 2 'the cleanest route,' which will set physician expectations the market will break.

**Recommendation:** {f.get('recommendation','')}

### [LOW] wiki/06-personas/hcp-physician.md
**Issue:** 'Facilities adequate for the protocol (storage, labs — arranged, not necessarily owned)' hand-waves the operational reality: a community clinic typically has no temperature-monitored IP storage, no research pharmacy, no coordinator to populate the delegation log, and cannot execute early-phase assessment schedules (serial PK draws, central-lab kits, protocol imaging). Paperwork completeness does not confer conduct capability, and the pitch 'make me an accepted site' implies it.

**Recommendation:** {f.get('recommendation','')}

### [LOW] wiki/00-overview/guiding-scenario.md
**Issue:** Step 3 links 'live milestone tracker' to [[monitoring-plan]] — a monitoring plan (312.53(d)/E6(R3) sponsor oversight) is a different artifact from a startup milestone tracker; a physician following the link gets the wrong concept.

**Recommendation:** {f.get('recommendation','')}

## Must-fix
- Replace or relabel frontend/index.html: PROGRAM.md marks 'clinician flow end-to-end' done, but no clinician flow exists — build a minimal triage-to-ledger flow wired to real engine output, or mark the deliverable pending and remove 'Live example — actual engine output' from the static mock.
- Add the three absent physician-stoppers to the burden map (hcp-physician.md + site-activation.md): central-IRB access/cost/timeline for non-institutional sites, research liability insurance & indemnification, and Medicare/research billing compliance (coverage analysis).
- Rewrite guiding-scenario.md Step 2→3 to include the sponsor-acceptance negotiation instead of assuming it; the CTA/budget negotiation is the documented dominant chokepoint and cannot be presented as a drafted template.
- Add an honest per-route physician effort/cost table (setup hours, ongoing hours per month, out-of-pocket including IRB fees and micro-CRO pricing) — the tool's core pitch is burden reduction and it never quantifies the residual burden.
- Resolve the Route 3 medical-monitor self-review conflict explicitly: an n-of-1 sponsor-investigator cannot be the sole causality judge for their own patient with no coverage plan; specify the independent-monitor arrangement.
