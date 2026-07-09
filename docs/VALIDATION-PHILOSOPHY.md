# OSSICRO — Validation Philosophy: Concept over Rules

# OSSICRO Validation Philosophy

**Version 1.0 — 2026-07-09.** This document is dated and versioned because the boundary it draws moves as model capability and regulatory practice move. It is a perpetual work in progress by design, following the precedent of Anthropic's Constitution, which frames itself the same way.

## 1. The default is concept-based judgment

OSSICRO validates generated documents the way Anthropic aligns Claude: a small, named set of hard constraints, and judgment against stated principles everywhere else. Anthropic states the preference directly — "We generally favor cultivating good values and judgment over strict rules and decision procedures" — and gives the reason: a mix of good judgment and a minimal set of well-understood rules generalizes better than rules imposed as unexplained constraints.

The mechanism behind the preference matters more than the preference itself. A deterministic rule encodes a *proxy* for a goal, frozen at the capability level and writing norms of the day it was written. As models improve, a frozen proxy decays three ways at once:

1. **It under-fires.** New failure modes and new phrasings the rule-writer never saw pass clean. A 2024 mannerism list does not catch 2026 mannerisms.
2. **It over-fires.** The model becomes capable of the correct judgment call, but the rule still forces the cruder behavior, producing false positives that erode reviewer trust. Regulatory register legitimately uses "shall", formal passives, and verbatim defined-term repetition that naive style rules punish.
3. **It becomes gameable.** A generation pass optimizing against a fixed surface pattern routes around the pattern while violating the intent. A rule that checks for the string "50.25(a)(4)" trains the generator to paste the string, not to disclose the risks.

A principle stated at the level of intent — "this consent form must disclose reasonably foreseeable risks substantively, in language the subject population can understand" — does not decay. The same principle text produces better application as the reviewing model's judgment improves, because the principle names the target rather than a proxy for it. Capability growth directly improves principle application; it does nothing for a frozen rule. This is why concept-based review is OSSICRO's default: it is the only validation posture that gets better for free.

There is a second, subtler cost of rule-heavy validation that Anthropic documents from its own training experience: narrow mechanical rules do not stay narrow. A system optimized to pass a phrase-scanner learns box-ticking as its operating posture — "did I avoid the forbidden words" instead of "would a payer or regulator reading this find it credible and complete." The rule corrupts the objective, not just the coverage.

## 2. The hard-rule test

The default reverses only when a check passes the test Anthropic's Constitution states for its own hard constraints. A deterministic rule beats judgment when at least one of three conditions holds:

1. **The cost of error is severe or irreversible enough that predictability and evaluability become critical.** A hallucinated citation in a filing is a sanctionable event; a missed statutory deadline forecloses the patient's access.
2. **Judgment is known to be insufficiently robust at the tail.** Calendar arithmetic against a regulation is a case where an AI "judgment" would be strictly worse than a computation, always.
3. **Any flexibility creates an exploitable incentive.** A gate that can be argued around will be argued around; the firmness is itself the protection.

Importance alone does not earn a bright line. Anthropic's sharpest data point here is that honesty — its most load-bearing value — is deliberately *not* a hard constraint, because honesty requires contextual calibration a rigid rule would mangle. OSSICRO applies the same discipline: "this check feels high-stakes" is not an argument for determinism. Only the three conditions are.

## 3. OSSICRO's hard rules (the closed list)

Each entry is here because the target itself is discrete — fact-shaped or legally non-delegable — not because rules are inherently safer.

| Hard rule | Why it qualifies |
|---|---|
| Verbatim-lock SHA-256 checks and the template-diff invariant | Byte identity is a fact. This is the architectural guarantee of containment. |
| Statutory clocks: 7/15-day IND safety reports (21 CFR 312.32(c)), 30-day IND wait (312.40(b)(1)), 60-day annual report window (312.33) | Calendar arithmetic against a regulation. Condition 1 and 2. |
| The non-delegable gates (`gates.py`): named-human sign-off, causality determination, consent, attestation; `finalize()` refuses ungated advancement | Black-letter law — software cannot hold a sponsor obligation under 21 CFR 312.52, and firmness is protective against "just this once" erosion. Conditions 1 and 3. This is the exact analogue of Anthropic's hard-constraint list, and it is the product's legal thesis, not a limitation to outgrow. |
| Citation presence and traceability: a rule without a citation does not ship; every generated span carries provenance or is marked inferred | Whether a citation exists and resolves is checkable fact. |
| Ledger mechanics: required-document roster, required-field presence, green/amber/red tri-state, no gated document green without a recorded sign-off | Presence/absence is fact; the tri-state is the auditable spine. |
| Cross-document identity comparison on canonical structured fields, after normalization | Two documents asserting different IND numbers is a fact conflict; resolution routes to a human. |
| Exculpatory consent constructions ("you waive", "you release", "the sponsor shall not be liable"), cited to 21 CFR 50.20 | A cited regulatory prohibition — fact-shaped, correct to enforce deterministically forever. |
| Chat-transcript residue ("as an AI", "I hope this helps", chatbot openers) | Categorically never legitimate in a regulatory filing regardless of how writing norms evolve. Drafting-process leakage detection, not style opinion. |
| Part 11 audit trail: model, version, input hash, timestamp, reviewer identity per AI contribution | The accountability substrate for everything else, including the concept layer. |

This list is closed and each entry is named with its justification, so reviewers can see at a glance which checks are deliberately rigid and why. Additions require passing the three-condition test in §2, in writing.

## 4. The boundary doctrine

**Fact-shaped properties get rules. Quality-shaped properties get judgment.** A citation exists or it does not; a deadline is met or missed; a hash matches or it does not; a gate has a recorded sign-off or it does not. Whether an SAE narrative is sufficient for a medical monitor, whether a consent form's risk disclosure is substantively adequate in lay language, whether a cover letter reads as professionally framed for its audience — these have no ground truth to string-match against, and the right answer is genuinely contextual.

Three corollaries govern the boundary:

**Never fake semantics with a string match.** When a check needs to know what prose *means*, there are exactly two honest options, in preference order: (a) restructure generation so the property becomes factual by construction — the 30-day-wait commitment as a verbatim template span verified by provenance, phase as a structured enum rendered into the form — because deterministic-by-construction beats both string-matching and AI judgment; or (b) hand the check to the concept reviewer with the citation as its principle. A substring match on "30 days" and "312.40" is judgment smuggled into a lexical proxy, and it inherits all three decay modes of §1.

**Label proxies as proxies.** Any pattern that stands in for a concept states, adjacent to the pattern, what concept it proxies. That is what lets a reviewer — human or model — recognize when the proxy has decayed and retire it, instead of the proxy silently going stale with no signal.

**Rules are data, not code.** Every validation rule carries `{citation, principle text, check strategy: deterministic | provenance | concept}`. A rule whose principle is stated as text can be executed deterministically where the property is factual and handed to the concept reviewer — with the same citation — where it is semantic. Regulatory changes then version the principle text rather than reworking matchers.

## 5. How the concept-based reviewer works

The reviewer is a Claude SDK agent applying Anthropic's own critique-and-revise pattern to OSSICRO's outputs. Constitutional AI works by having a model critique a draft against a sampled natural-language principle and revise in light of the critique; OSSICRO's review pass is the same loop at inference time:

- **Principles, not patterns.** Each concept check is a cited principle in text form — "21 CFR 50.25(a)(4): the ICF must disclose reasonably foreseeable risks; assess whether this draft does so substantively, in language the subject population can understand" — not a matcher. Voice review applies `docs/WRITING-PRINCIPLES.md` per document category.
- **Span-scoped jurisdiction.** The reviewer judges filled field values and generated spans. Verbatim-locked and fixed template prose are outside its jurisdiction by construction.
- **Structured, graded findings.** Each finding is `{field, span, principle cited, grade: deficient | adequate | advisory, quoted evidence, rationale, suggested rewrite}` — the same resolving-question format the ledger already uses.
- **Escalate-only coupling.** Concept findings can add reds or advisories to the ledger, enrich the human reviewer's critique packet, drive the flag-and-rewrite loop, and open a gate earlier. They can never clear: never red-to-green, never discharge a gate, never alter a deadline, never auto-resolve. Hard-fail authority stays with the deterministic layer and humans; the reviewer alone fails toward the human gate. "Green" means structurally complete *and* no unresolved concept deficiencies.
- **Structural independence.** The adversarial QC reviewer shares no working context with the drafting agents — it hunts internal contradictions, unsupported spans, stale versions, and missed conditional requirements as an outsider.
- **Full attribution.** Every concept-layer contribution is logged per the Part 11 scheme: model, version, input hash, finding, human disposition. This keeps the concept layer in a defensible tier under the FDA AI-credibility framing — low-influence context of use, because a named human still makes every decision, with the machine critique in front of them.

The property that justifies the whole design: when the underlying model improves, this reviewer improves with no rule rewrite, no re-labeling campaign, and no registry edit. The principle text stays; the application gets better.

## 6. Accountability for judgment checks

Judgment sacrifices some of what rules provide — up-front predictability, mechanical evaluability. Concept-based checks therefore carry their own accountability, different in kind but not lesser: per-document logged reasoning (auditable after the fact), human spot-check review on a sample, and a hindsight feedback loop — when a document fails downstream (payer rejection, IRB return, regulator flag) despite passing concept review, the failure feeds a rubric revision, recorded in the rubric's version history.

## 7. Revision

The hard-rule list (§3), the writing principles, and the per-category rubrics are versioned, dated artifacts. The example tiers that seed the concept reviewer are *expected* to go stale and be retired; that is their design, not their failure. Proposals to move a check across the rules/concepts boundary cite the three-condition test and are reviewed like any other regulatory-logic change.