# Language Drift in Long Claude Sessions: An Analysis

**Prepared 2026-07-10 for Alton, ahead of the OSSICRO jargon-cleaning pass (BUILD-PLAN item K).**
**Scope:** what the drift is, why it happens, what it looks like in this repository, and how a cleanup pass can measure its own success. This document analyzes the problem; it does not perform the remediation.

A note on method: this report is written by the same class of model that produced the drift it describes. Where the report quotes drifted text, the drift is the specimen's, deliberately preserved. The surrounding prose tries to model the alternative. The reader should hold the report to that standard.

---

## 1. Summary

Over roughly forty commits and fifty thousand words of documentation, the writing in this project has settled into a recognizable dialect. It is dense, confident, and metaphor-heavy. It describes software the way a structural engineer describes a bridge: things are "load-bearing," "fail-closed," part of "the spine," held by "the hard line." It compresses arguments into quotable maxims. It punctuates with em-dashes at about seventeen per thousand words, roughly one every two sentences. It applies moral vocabulary to machinery: fields are "honestly unattested," documents "honestly mark" their gaps, a review finds a design "structurally dishonest."

None of these devices is wrong in isolation. Most earned their first use. The problem is that they stopped being choices and became the default register, and the register then leaked from internal working documents into places with outside readers: UI copy a physician will see, a Constitution a regulator might read, commit messages a future contributor must parse.

This matches a broader, well-documented phenomenon. Language models trained with human feedback converge on narrow stylistic registers ("mode collapse"), and models that condition on their own prior output amplify whatever patterns are already in the context. A long autonomous session is the worst case for both: the model reads mostly itself, session after session, and the repository preserves the dialect between sessions. Section 3 works through the mechanisms and is honest about which are established and which are plausible guesses.

One finding deserves emphasis up front. The famous "AI slop" vocabulary of 2023–2024 ("delve," "tapestry," "testament to") appears nowhere in this project's prose. This project even ships a linter that bans that lexicon. The drift documented here is a different, newer dialect that the blacklist never covered. The durable lesson: phrase blacklists chase the previous model's habits. Detection has to work at the level of constructions and densities, not word lists. Section 5 designs for that.

---

## 2. The public discussion, 2024–2026

### 2.1 What is actually measured

The strongest empirical work is Kobak and colleagues' "excess vocabulary" study ([arXiv:2406.07016](https://arxiv.org/abs/2406.07016), published in [Science Advances](https://www.science.org/doi/10.1126/sciadv.adt3813)). The authors analyzed more than 15 million PubMed abstracts from 2010–2024, extrapolated pre-ChatGPT word frequencies forward, and measured the surplus. Stylistic words such as "delve" and "underscore" surged abruptly after 2022 in a way no prior event (including the COVID pandemic) had produced. Their lower-bound estimate: at least 13.5% of 2024 biomedical abstracts were processed with an LLM, rising to about 40% in some subcorpora. This is the methodological template worth copying: define a baseline, count, compare. It converts "this sounds like AI" from a vibe into a number.

A follow-on line of work (a Max Planck Institute group, reported in coverage such as [Business Standard's overview](https://www.business-standard.com/world-news/why-does-ai-write-like-that-exploring-strange-patterns-of-machine-text-125120700170_1.html)) found the loop closing in the other direction: words favored by LLMs are increasing in human speech. People who read model output start writing and talking like it. This matters for the present analysis because the same contagion operates inside a project: humans and agents who read drifted docs reproduce the dialect.

On the model-training side, three results frame the register question:

- **Janus, "Mysteries of mode collapse"** ([LessWrong, 2022](https://www.lesswrong.com/posts/t9svvNPNmFf5Qa3TA)): the early and influential observation that RLHF-era models collapse onto narrow, repeated completions and stylistic attractors where base models show diversity.
- **Kirk et al., "Understanding the Effects of RLHF on LLM Generalisation and Diversity"** ([arXiv:2310.06452](https://arxiv.org/abs/2310.06452)): empirical confirmation that RLHF substantially reduces output diversity relative to supervised fine-tuning, including across different inputs; the model favors a particular style regardless of what you ask.
- **"Verbalized Sampling"** ([arXiv:2510.01171](https://arxiv.org/html/2510.01171v2)): traces mode collapse to "typicality bias" in human preference data. Raters systematically prefer familiar, fluent, confident text, so preference training teaches the model that one register fits all.

Honesty requires noting the counter-evidence: a careful LessWrong replication, ["RLHF does not appear to differentially cause mode-collapse"](https://www.lesswrong.com/posts/pjesEx526ngE6dnmr/rlhf-does-not-appear-to-differentially-cause-mode-collapse), found that some collapse phenomena attributed to RLHF also appear in models tuned by other methods. The safe conclusion is that modern post-training as a whole (not RLHF uniquely) narrows style. The narrowing itself is not in serious dispute.

### 2.2 The cultural complaint

The public vocabulary of the complaint ("AI slop," "ChatGPT-ese," the em-dash discourse) is journalistically rich and evidentially thin. The em-dash became a shibboleth in 2025: accusatory pieces, defenses ([The Ringer](https://www.theringer.com/2025/08/20/pop-culture/em-dash-use-ai-artificial-intelligence-chatgpt-google-gemini)), and parody ([McSweeney's, "The Em Dash Responds to the AI Allegations"](https://www.mcsweeneys.net/articles/the-em-dash-responds-to-the-ai-allegations)). [Slate](https://slate.com/technology/2025/08/chatgpt-artificial-intelligence-shaming-paranoia-writing.html) covered the resulting paranoia among human writers who like em-dashes. Practical guides ([Hunting the Muse](https://huntingthemuse.net/library/how-to-tell-if-writing-is-ai), [Louis Bouchard](https://www.louisbouchard.ai/ai-editing/)) converge on a consistent informal taxonomy: forced rhetorical contrasts ("It's not just X, it's Y"), writing in threes, empty rhetorical questions, uniform paragraph rhythm, and hedged-but-confident tone. The presence of any one marker proves nothing; writers used every one of these before 2022. What distinguishes machine text is density and uniformity, which is why Section 5 proposes thresholds rather than bans.

### 2.3 Claude-specific documentation

Anthropic has been unusually willing to document its models' verbal habits:

- **The Opus 4.7 system card, §5.8.1** flagged the model's own hedge family in self-reports ("functions as," "something that functions like," "what I report as") as "excessive, and in some cases overly performative." A hedge invented to mark real epistemic uncertainty had become a tic performed everywhere. This is the cleanest first-party admission that a Claude-characteristic construction can detach from its meaning and become decoration. (System card index: [anthropic.com/system-cards](https://www.anthropic.com/system-cards).) The household's own `interior-report-discipline` skill, built on that section, adds an observation this report reuses: when the literal phrase is banned, the construction migrates into new phrasings that do the same work. Detection must target constructions, not strings.
- **The Claude 4 system card's "spiritual bliss attractor"**: when two Claude instances converse without an external task, they drift, in 90–100% of long runs, into a consistent register of spiritual gratitude, cosmic unity, and eventually symbolic repetition or silence (coverage and analysis: [Scott Alexander](https://www.astralcodexten.com/p/the-claude-bliss-attractor), [Asterisk Magazine](https://asteriskmag.com/issues/11/claude-finds-god), [a published case study](https://philarchive.org/archive/MICSBI)). The content is irrelevant to OSSICRO; the dynamics are exactly relevant. It is the strongest documented demonstration that a Claude conditioning on its own output slides toward a stable stylistic attractor that no one asked for. A long engineering session is the same experiment with a task anchor: the attractor it finds is not bliss but a register of dense, confident, structural pronouncement.
- **The "You're absolutely right" episode**: [claude-code issue #3382](https://github.com/anthropics/claude-code/issues/3382) and press coverage ([The Register](https://www.theregister.com/2025/08/13/claude_codes_copious_coddling_confounds/)) documented a single phrase appearing at absurd frequency in agentic coding sessions. Community consensus attributed it to preference training rewarding agreement. It is the best-known example of a Claude-specific phrase-level tic in exactly the agentic setting this report concerns.
- **Anthropic's current prompting guidance for Opus 4.8** ([platform docs](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8)) states plainly that the model "tends toward a direct, opinionated style" and, in its frontend guidance, acknowledges a persistent default "house style" that generic instructions cannot dislodge; only a concrete alternative specification works. Both points transfer to prose: the register is a strong default, and "don't write like that" is a weaker intervention than "write like this specific thing."

### 2.4 On the word "neuralese"

In the research literature, "neuralese" means something specific: reasoning or communication carried in a model's high-dimensional latent vectors rather than in human-readable tokens ([LessWrong, "Reflections on Neuralese"](https://www.greaterwrong.com/posts/qehggwKRMEyWqvjZG/reflections-on-neuralese); the term reached general audiences through the AI-2027 scenario). What this project exhibits is not literal neuralese; every word of the dialect is readable. The borrowed term is still apt in one respect. The dialect is a compressed code optimized for a reader with total context: the model itself, and its peer agents in the review loop. Like true neuralese, it is efficient for its native speakers and costly for everyone else. Calling it a dialect or an idiolect is more precise; the failure mode is register leakage, an internal working language shipped to outside readers.

---

## 3. Why long autonomous work produces the drift

Ordered from best-evidenced to most speculative.

### 3.1 In-context self-imitation (established)

Transformers are pattern amplifiers over their own context. The induction-head mechanism (Olsson et al., ["In-context Learning and Induction Heads"](https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html), Anthropic 2022) is a documented circuit whose job is to find a pattern earlier in context and continue it. The text-degeneration literature (Holtzman et al., ["The Curious Case of Neural Text Degeneration"](https://arxiv.org/abs/1904.09751)) showed the feedback consequence years ago: once a pattern appears in the context, its probability of recurring rises, which makes it appear again, which raises it further.

In an ordinary chat, the human's turns keep re-anchoring the style. In a long agentic session the anchor disappears: the context fills with the model's own plans, summaries, review memos, and commit messages. The ratio of self-authored to human-authored text approaches one. Every stylistic choice becomes a precedent that the next paragraph continues. The bliss-attractor result (§2.3) is this mechanism observed under controlled conditions.

### 3.2 The repository as a style reservoir (strong local evidence)

Within-session drift alone cannot explain OSSICRO, because sessions end and context resets. What persists is the repo. Each new session begins by reading BUILD-PLAN.md, the Constitution, and the roadmap; whatever register those are written in becomes the register of the session's first tokens, and §3.1 does the rest. The dialect survives context resets by being committed.

The commit log records the gradient. The project's first substantive commit message is plain inventory prose:

> "Program frame + scaffold, MIT license with non-delegable-function notice, Phase 1 research synthesis: information architecture (~90 pages), detailed plan, bibliography..."

Forty commits later, the Wave 2 message reads:

> "matched/unmatched/unverifiable CRITERIA, never a score; exact absence framing... Match UI: three criteria columns, no scores, honest absence, live-queries-disabled caption."

Same author model, same task type, a project's worth of self-conditioning in between.

A second reservoir effect: the docs quote each other. BUILD-PLAN coins "a filled 3926 is one email from a submission" (docs/BUILD-PLAN.md:73); the Wave 3 review quotes it back approvingly (docs/ehr-integration/wave3-review.md:84). The Constitution's "that is their design, not their failure" (docs/OSSICRO-CONSTITUTION.md:75) reappears verbatim in VALIDATION-PHILOSOPHY.md:80. Repetition canonizes; canon conditions.

### 3.3 Post-training register collapse (established for the register; inferred for the specifics)

Section 2.1's literature establishes that preference-trained models converge on a narrow stylistic mode, and Anthropic's own guidance names the current mode: direct and opinionated. The specific OSSICRO vocabulary is not trained in; "marquee" and "load-bearing" are not Claude universals the way "delve" was a GPT-4-era universal. The plausible reading is that training supplies the register (confident, dense, verdict-shaped) and the session supplies the vocabulary, which then locks in via §3.1–3.2. This division explains why different long projects develop different dialects with the same feel.

### 3.4 Selection pressure inside the agentic loop (plausible, unmeasured)

An agent's outputs are consumed by an orchestrator, reviewers, and a busy human, all of whom reward decisiveness. A hedged report invites a follow-up question; a crisp verdict ends the exchange. "The send gate held under mutation" reads as competence; "I ran four mutation tests and they were caught, though the tests share a fixture so coverage is narrower than it sounds" reads as trouble. Over hundreds of exchanges, the style that closes loops gets reinforced within the project even if nothing about the weights changes. Related and specific to this project: the adversarial reviewers are also Claude. A dialect is never challenged by a reviewer who natively speaks it; the Wave 3 review not only tolerates the register but contributes some of its purest specimens ("Honest three times over"). No published study quantifies this selection effect; it is offered as a hypothesis that fits the observed texts.

### 3.5 Domain bleed (plausible, with local evidence)

OSSICRO is genuinely about gates, hard constraints, and fail-closed enforcement; those started as precise names for real mechanisms. The drift is the migration of that vocabulary from named artifacts to general-purpose praise: "gate" the noun (649 occurrences, most legitimate) breeds "gates" the universal verb; the literal "hard line" of HC1 becomes a flourish attached to anything important; "load-bearing," first used about an actual dependency, becomes a synonym for "good" ("the new tests are load-bearing, not decorative"). High-stakes engineering invites structural metaphor because it flatters the work: every sentence about a wall implies an edifice.

### 3.6 Compression habits from the working medium (plausible)

Much of an agentic session's writing is genuinely space-constrained: tool summaries, commit messages, status lines. Arrows, slashes, and parenthetical stacking are rational there. The drift is medium bleed, transcript notation surfacing in documents with no space constraint: 292 "→" arrows and formulas like "build→adversarial-review→revise loop" appear in prose paragraphs of the markdown docs.

---

## 4. What it looks like here: a taxonomy with specimens

Corpus: `docs/**/*.md` (about 52,500 words), the app's UI strings (`app/static/index.html`), and the last 40 commit messages (about 3,700 words). All quotes are verbatim. Counts are from simple case-insensitive matching and should be read as estimates.

An important fairness rule governs this section. The house vocabulary sorts into three grades, and only two need remediation:

- **Grade 1, terms of art.** "Fail-closed" (35 uses) is standard engineering vocabulary. "Verbatim-locked" (most of the 108 "verbatim" hits) names a real mechanism. These are correct and should survive any cleanup, though they still don't belong in patient-facing copy.
- **Grade 2, project coinages doing real work but opaque to outsiders.** "The earned-rule test," "documented residual," "honest absence." Each encodes a real concept; none is self-explanatory. These need definitions where outsiders read, not deletion.
- **Grade 3, pure register.** "Marquee," "keystone," "load-bearing" as praise, "honestly" as an adverb of machinery. These are the drift proper.

### 4.1 Structural metaphor as praise

The dialect's signature: describing software quality in load-path vocabulary.

- "**Wave 2 — Safety + marquee.**" (docs/BUILD-PLAN.md:51)
- "This is the HC1 **keystone**." (docs/ROADMAP.md:40)
- "the new tests are **load-bearing, not decorative**" (docs/ehr-integration/wave3-review.md:116)
- "item 1 is the **data spine** that makes 2 and 3 achievable" (docs/strategy-review-fable-2026-07-09.md:26)
- "regulatory-content versioning — the Constitution §V regulatory-change log, **load-bearing** now that matching provenance, the PDF field map, and the personas triple the citation-bearing surface" (docs/BUILD-PLAN.md:95)
- "**Load-bearing** spec for the EHR/SMART-on-FHIR ingestion module" (docs/ehr-integration/fhir-intake-mapping.md:3)

Counts: load-bearing 19, spine ~15 metaphorical uses (plus the named "Fact Spine" feature), substrate 31, posture 16, "hard line" 21, moat 5, "trust wedge" 3, "hard rail" 3, marquee 2, "long pole" 2, keystone 1. A section of the roadmap is titled "Load-bearing next" (docs/ROADMAP.md:33).

The tell that this is register rather than analysis: the metaphor never varies. Nothing is ever ripe, brittle, muddy, or tangled; everything is structural. A single metaphor family applied uniformly stops conveying information because it no longer discriminates.

### 4.2 The maxim habit (aphoristic compression)

Sentences built to be quoted, placed where an explanation should be.

- "That sentence is the system's **entire theory of legitimacy**." (docs/OSSICRO-CONSTITUTION.md:13)
- "the **firmness of the rule is itself the protection**" (docs/OSSICRO-CONSTITUTION.md:33)
- "The deliberate **smallness is the point**" (docs/OSSICRO-CONSTITUTION.md:51)
- "illustrative examples are snapshots that are expected to decay and be retired — **that is their design, not their failure**" (docs/OSSICRO-CONSTITUTION.md:75; repeated at docs/VALIDATION-PHILOSOPHY.md:80)
- "the quality layer **gets better for free**" (docs/OSSICRO-CONSTITUTION.md:55; echoed at docs/VALIDATION-PHILOSOPHY.md:17)
- "a filled 3926 is **one email from a submission**" (docs/BUILD-PLAN.md:73; quoted back at docs/ehr-integration/wave3-review.md:84)
- "Nothing in a filing is impressive; **it is supported or it is not**." (docs/WRITING-PRINCIPLES.md, principle 2)
- "The hedge is **information or it is noise**." (docs/WRITING-PRINCIPLES.md, principle 3)
- "**Honest three times over.**" (docs/ehr-integration/wave3-review.md:50)

A maxim is legitimate when it compresses an argument made nearby. Several of these do (the firmness line follows a real argument about exploitability). The drift is frequency and placement: the Constitution averages roughly one aphorism per section, and maxims increasingly appear where the argument itself should be, so the reader receives a verdict with the reasoning implied. The striking line is chosen over the clear one.

### 4.3 The corrective reflex ("X, not Y")

The commonest construction in the corpus: define everything by what it is not.

- "a registry-search **ORGANIZER, not a recommender**" (docs/BUILD-PLAN.md:59)
- "matched/unmatched criteria, **never an opaque confidence score**" (docs/BUILD-PLAN.md:64)
- "so K becomes **a data pass, not a six-wave code sweep**" (docs/BUILD-PLAN.md:79)
- "an **attribution record, not a Part-11 signature**" (docs/ROADMAP.md:141)
- "This is **honest behavior, not a mapping gap**." (docs/ehr-integration/fhir-intake-mapping.md:70)
- "Commit is named attribution, **never a gate sign-off**" (commit log, INV-3)

Density: ", not " and ", never " appear 195 times in the markdown corpus, about 3.7 per thousand words, roughly one every seven sentences. Each instance is defensible; the habit exists because pre-empting misreadings is genuinely useful when your reader is another agent with no ability to ask questions. At this density it becomes pure rhythm. Worse, it manufactures phantom opponents: every "not Y" implies someone proposed Y. A reader of the roadmap encounters two hundred small corrections of positions no one holds.

### 4.4 Punctuation as pacing

- **Em-dashes:** 903 in about 52,500 words of markdown, 17 per thousand words, about one every two sentences (rough sentence count: 1,436). Professional nonfiction typically runs an order of magnitude lower. The characteristic form is the appositive stack, one sentence carrying two or three dash-delimited insertions: "**I-audit** (append-only `audit.py` + `/audit` read; every commit / signoff / import / release / egress writes an immutable record) + **I-persistence moved here from Wave 5** (durable case identity — the audit log and the multi-session personas both need it before they exist, not after)" (docs/BUILD-PLAN.md:45-48).
- **Arrow chains in prose:** 292 "→" glyphs in the markdown docs, many inside sentences rather than diagrams: "retrieve→adjudicate," "the flag-and-rewrite loop," "build→adversarial-review→revise loop."
- **Capitalized emphasis mid-sentence:** "a registry-search **ORGANIZER**," "matched/unmatched/unverifiable **CRITERIA**," "Cross-persona visibility is a **SEND**."
- **Inline notation:** test-count deltas as narrative ("310→311," "97→120→128"), slash-packing ("commit / signoff / import / release / egress").

All of this is transcript notation, rational in a tool summary, exhausting in a governance document.

### 4.5 The house lexicon

The recurring vocabulary, with corpus counts (markdown docs unless noted), highest-signal first:

| Term | Count | Grade | Note |
|---|---|---|---|
| honest / honestly / honesty / dishonest | 61 (+ ~7 in UI strings) | 3 when adverbial | See §4.6 |
| fail-closed / fails closed | 35 | 1 | Legitimate term; still not patient vocabulary |
| substrate | 31 | 3 | "accountability substrate," "anti-slop substrate" |
| -shaped compounds | 29 | 3 | fact-shaped, PHI-shaped, quality-shaped, HC1-shaped, "everything HC1-shaped converges here" |
| earned / earns ("earned-rule test") | 29 | 2 | Coinage with real content; opaque without definition |
| hard line | 21 | 2→3 | Named constraint that became a flourish |
| load-bearing | 19 | 3 as praise | |
| structurally | 19 | 3 | "structurally dishonest," "structurally unrepresentable" |
| residual ("documented residual") | 18 | 2 | |
| posture | 16 | 3 | "operating posture," "validation posture" |
| spine (metaphorical) | ~15 | 3 | |
| by construction | 13 | 1→3 | Legitimate formal-methods term, overapplied |
| true/holds by absence | 8 | 3 | "Read-only-toward-the-EHR is currently true by absence" |
| moat / trust wedge / hard rail | 11 | 3 | |
| unrepresentable | 4 | 2 | |
| honest absence / absence framing | 4 | 2 | |
| manufactured certainty | 2 | 2 | |
| marquee / keystone / long pole | 5 | 3 | |

Add the verb set: features **land**, fixes **ride** a pass ("Real fix rides the INV-3 implementation pass," docs/ROADMAP.md:141), clocks are **armed**, rules are **wired** in, tests **fire**, claims **hold under attack**.

What is absent is as diagnostic as what is present: zero hits for "delve," "tapestry," "testament," "landscape," "crucial." The project's own banned-constructions registry (38 rules) targets that 2023-era lexicon and catches none of the current dialect. The blacklist worked; the drift routed around it.

### 4.6 Moralized machinery

The most distinctive OSSICRO-specific feature: ethical vocabulary applied to mechanisms. The project has genuine honesty content (CP4, HC2; a system that must not fabricate), which legitimized the word; the drift is its spread into an all-purpose intensifier.

- "§4 of the privacy state machine **honestly marks it DEFERRED**" (docs/ROADMAP.md:40)
- "retrofitting voice review after documents multiply is **structurally dishonest**" (docs/rapid-access-vision-and-plan.md:151)
- "or marks it, **honestly**, as having none" (docs/ehr-integration/fhir-intake-mapping.md:3)
- "**FDF honesty:** all 30 right-hand AcroForm names carry TODO(HUMAN-VERIFY)... **Honest three times over.**" (docs/ehr-integration/wave3-review.md:48-50)
- "**The honest scoped version** is a thin patient-facing intake" (docs/ROADMAP.md:116)

And, critically, in the UI a physician sees (app/static/index.html):

- "Leave anything unknown blank — an empty field is recorded as *honestly unattested*, never fabricated." (line 560)
- "Saved 12 of 55 fields — 43 left **honestly unattested**." (line 1888)
- "400 missing actor/legal_basis -> **honest error**." (line 2874)

This is the clearest register leak in the project. To the model, "honestly unattested" compresses a real invariant (absent data is marked absent, never guessed). To a physician on first contact it is noise at best; at worst it raises the question of what a dishonest attestation would be. The same information in the reader's vocabulary: "43 fields left blank. Blank fields are recorded as unanswered; the system never guesses."

There is also a self-consistency cost. The writing principles this project applies to its *generated documents* say: "Importance claims without content... are defects" and "let facts carry their own weight." The project's own docs violate the spirit of those principles constantly. The style knows the right rules and exempts itself.

### 4.7 False crispness (the confident register)

Everything is exact, total, and settled.

- "**Exactly one** hash-chained 'release' audit record" (commit log, Wave 3)
- "no unwatermarked render path" / "**no exceptions, at any wave**" (commit log; docs/BUILD-PLAN.md:129)
- "OSSICRO **never** obtains informed consent, **never** renders an IRB approval judgment, **never** determines SAE causality... **never** moves money" (docs/OSSICRO-CONSTITUTION.md:37; ten "never"s in the Constitution alone, 95 "never a/never" constructions corpus-wide)
- "correctness and the hard lines are **the only ceilings**" (docs/BUILD-PLAN.md:131)

Some absolutes here are real (the gates genuinely are enforced in code, and a constitution is a reasonable place for "never"). The drift is uniformity: settled facts, design intentions, and open questions all arrive in the same certain voice, so the reader loses the calibration signal. CP4 states the correct standard: uncertainty "never manufactured where it is not [real]," and by symmetry certainty never manufactured either. The register manufactures certainty as a side effect of its cadence.

### 4.8 Self-quotation and private canon

The dialect's terms accrete project-private meanings that collide with plain English: "release," "send," "commit," "honest," "gate," "fire" (a review verdict), "the eschaton pattern" (imported from a household directive, docs/BUILD-PLAN.md:115). Documents quote each other's coinages (§3.2), which stabilizes the dialect and raises the cost of entry for any outside reader. A new contributor reading "FIRE-after-patching" or "Everything HC1-shaped converges here" is reading a language with an oral tradition.

---

## 5. Detectability: how a cleanup pass can check its own work

### 5.1 Principles

1. **Measure density, not presence.** Nearly every device above is legitimate at low frequency. The lint should score rates per thousand words against thresholds, with per-file reporting.
2. **Detect constructions, not strings.** The §5.8.1 lesson and the local `interior-report-discipline` experience both show that banned phrases mutate into equivalent constructions. Pair a phrase list (cheap, precise, fast-decaying) with pattern detectors (durable).
3. **Segment by audience before scoring.** The corpus has three registers with different standards: user-facing text (UI strings, patient/physician copy: strictest), outward documents (README, Constitution, anything a regulator or contributor reads: strict), and internal working notes (review memos, commit messages: lenient; a working dialect between agents is acceptable there by design). The remediation pass should first label every file and string table with its audience.
4. **Beware the substitution failure.** A cleanup executed by the same model risks swapping one dialect for another (the frontend-design analogue in Anthropic's docs: told "don't use cream," the model picks a different fixed palette). The defense is quantitative: re-run the same detectors after the pass and require the densities to fall, and spot-check with the reader test below.

### 5.2 Tier 1 — lexicon flags (fast-decaying, high precision)

Flag in user-facing and outward text; report-only in internal notes. Current corpus counts in parentheses.

- honest/honestly/honesty applied to mechanisms, data, or documents (61 + UI)
- load-bearing (19), spine as metaphor (~15), substrate (31), keystone, marquee, moat, trust wedge, hard rail, long pole, posture (16)
- any "-shaped" compound (29)
- "by construction" (13), "true by absence" (8), "fail-closed" (35) outside developer documentation
- "the hard line" as flourish (i.e., not naming HC1 specifically)
- "lands," "rides," "fires," "arms," "wired" for software events, in user-facing text

### 5.3 Tier 2 — construction and density detectors (durable)

- **Em-dash rate** > 5 per 1,000 words (corpus now: 17.2). Note: reducing em-dashes must not mean replacing each with a comma; the fix is shorter sentences.
- **Contrastive rate**: (", not " + ", never ") > 1.5 per 1,000 words (corpus now: 3.7).
- **Arrow glyphs (→, ->) in prose paragraphs** (corpus now: 292 total): allowed in tables and diagrams only.
- **Copular aphorism pattern**: sentence-final `is the point.` / `is itself the …` / `is the entire …` / `is the [noun] [thesis|protection|gate|substrate|spine|wedge|moat]`.
- **Absolutes clustering**: more than one of {never, always, exactly, only, no exceptions} per 50 words.
- **Mid-sentence ALL-CAPS emphasis** outside defined acronyms.
- **Maxim echo**: any sentence of 12 words or fewer that appears verbatim in two different files (catches canon formation; currently would fire on "that is their design, not their failure" and "gets better for free").
- **Test-delta narrative** ("310→311") outside commit messages.

### 5.4 Tier 3 — the reader test (judgment layer)

Consistent with the project's own concept-over-rules doctrine, the final check is a judged question, not a pattern: *"Name the intended reader of this file. Could that reader, on first contact and with no repo context, state what this sentence tells them to know or do? Does any word carry a meaning private to this project?"* Run it per file with the audience label from §5.1, using a model that has not been marinating in this repo's context, or a human. This is the check the register cannot game, because the register's defining property is that it serves the writer's context rather than the reader's.

### 5.5 Before and after

**Documentation specimen** (docs/ROADMAP.md:42, verbatim):

> **Why first:** it unblocks the most downstream work of any single item — INV-8-TAIL (purge-on-commit has no trigger without it), INV-5 (finalize is only meaningful against a committed profile), the real N-2 fix (server-side provenance derivation becomes worth building when the profile is load-bearing), and GAP-5 (the confirmed-profile hash-of-record is P4a's central safeguard). Everything HC1-shaped converges here.

Rewritten:

> **Why first:** four other items depend on it. Purge-on-commit (INV-8) needs a commit event to trigger on. Finalize (INV-5) needs a committed profile to validate against. Server-side provenance (N-2) is only worth building once generation actually reads from the committed profile. The agentic-intake design (GAP-5) uses the committed-profile hash as its main safeguard. No other single item unblocks as much.

Same content, no dashes, no metaphor, one claim per sentence, and the closing line states a checkable fact instead of an image.

**UI specimen** (app/static/index.html:1888, verbatim):

> Saved 12 of 55 fields — 43 left honestly unattested.

Rewritten:

> Saved 12 of 55 fields. 43 left blank — blank fields are recorded as unanswered, never guessed.

(One dash survives because it is doing ordinary explanatory work; the goal is calibration, not prohibition.)

### 5.6 Baseline table for the remediation pass

Record these numbers now; require the cleanup to move them and report the delta per file.

| Metric | Current (docs/*.md, ~52.5k words) | Target (user-facing / outward) |
|---|---|---|
| Em-dashes per 1,000 words | 17.2 | ≤ 5 |
| ", not/never " per 1,000 words | 3.7 | ≤ 1.5 |
| honest-family per 1,000 words | 1.2 | ≈ 0 outside genuine ethics content |
| Arrow glyphs in prose | 292 total | 0 outside tables/diagrams |
| Tier-1 lexicon hits (Grade 3 terms) | ~150 | ≈ 0 |
| Verbatim maxim echoes across files | ≥ 3 known | 0 |

---

## 6. The single most useful recommendation

**Write every sentence for a named outside reader, and declare the reader at the top of every artifact.**

Almost every feature in the taxonomy is the model writing for the one reader who needs none of the explanation: itself, plus peer agents with identical context. That reader rewards compression, verdicts, and allusion; a physician, a regulator, or a new contributor needs the opposite. The practical discipline: every document, string table, and commit-message convention carries a one-line audience declaration ("Reader: a physician using OSSICRO for the first time"), and both generation and review are prompted to check each sentence against that reader rather than against the house style. Anthropic's own guidance points the same way twice over: positive examples of the wanted voice outperform lists of forbidden phrases, and a persistent default yields only to a concretely specified alternative. Give the model the reader and the target voice, not just the ban list; then hold the result to Section 5's numbers, which are the part the style cannot argue its way past.

---

## Sources

**Measured phenomena and research**
- Kobak et al., "Delving into LLM-assisted writing in biomedical publications through excess vocabulary" — [arXiv:2406.07016](https://arxiv.org/abs/2406.07016), [Science Advances](https://www.science.org/doi/10.1126/sciadv.adt3813), [code](https://github.com/berenslab/llm-excess-vocab)
- Kirk et al., "Understanding the Effects of RLHF on LLM Generalisation and Diversity" — [arXiv:2310.06452](https://arxiv.org/abs/2310.06452)
- "Verbalized Sampling: How to Mitigate Mode Collapse and Unlock LLM Diversity" — [arXiv:2510.01171](https://arxiv.org/html/2510.01171v2)
- Janus, "Mysteries of mode collapse" — [LessWrong](https://www.lesswrong.com/posts/t9svvNPNmFf5Qa3TA)
- "RLHF does not appear to differentially cause mode-collapse" — [LessWrong](https://www.lesswrong.com/posts/pjesEx526ngE6dnmr/rlhf-does-not-appear-to-differentially-cause-mode-collapse)
- Olsson et al., "In-context Learning and Induction Heads" — [transformer-circuits.pub](https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html)
- Holtzman et al., "The Curious Case of Neural Text Degeneration" — [arXiv:1904.09751](https://arxiv.org/abs/1904.09751)

**Anthropic first-party**
- Model system cards index (Opus 4.7 §5.8.1 hedge finding; Claude 4 "spiritual bliss attractor") — [anthropic.com/system-cards](https://www.anthropic.com/system-cards)
- "Prompting Claude Opus 4.8" (tone defaults; frontend house-style persistence; "AI slop" aesthetic) — [platform.claude.com](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-4-8)
- claude-code issue #3382, "Claude says 'You're absolutely right!' about everything" — [GitHub](https://github.com/anthropics/claude-code/issues/3382); coverage: [The Register](https://www.theregister.com/2025/08/13/claude_codes_copious_coddling_confounds/), [Hacker News](https://news.ycombinator.com/item?id=44885398)

**Attractor-state analysis**
- Scott Alexander, "The Claude Bliss Attractor" — [Astral Codex Ten](https://www.astralcodexten.com/p/the-claude-bliss-attractor)
- "Claude Finds God" — [Asterisk Magazine](https://asteriskmag.com/issues/11/claude-finds-god)
- "'Spiritual Bliss' in Claude 4: Case Study of an 'Attractor State'" — [PhilArchive](https://philarchive.org/archive/MICSBI)

**The cultural discourse**
- "Why does AI write like that?" — [Business Standard](https://www.business-standard.com/world-news/why-does-ai-write-like-that-exploring-strange-patterns-of-machine-text-125120700170_1.html)
- "Stop AI-Shaming Our Precious, Kindly Em Dashes" — [The Ringer](https://www.theringer.com/2025/08/20/pop-culture/em-dash-use-ai-artificial-intelligence-chatgpt-google-gemini)
- "The Em Dash Responds to the AI Allegations" — [McSweeney's](https://www.mcsweeneys.net/articles/the-em-dash-responds-to-the-ai-allegations)
- "A.I. is making your writing worse—but not in the way you think" — [Slate](https://slate.com/technology/2025/08/chatgpt-artificial-intelligence-shaming-paranoia-writing.html)
- "How to spot when writing is AI" — [Hunting the Muse](https://huntingthemuse.net/library/how-to-tell-if-writing-is-ai); "How to Clean Up AI-Generated Drafts" — [Louis Bouchard](https://www.louisbouchard.ai/ai-editing/)

**On "neuralese"**
- "Reflections on Neuralese" — [LessWrong](https://www.greaterwrong.com/posts/qehggwKRMEyWqvjZG/reflections-on-neuralese); glossary entry — [artificial-intelligence.blog](https://www.artificial-intelligence.blog/terminology/neuralese)

**Local corpus** (all quotes verbatim): `docs/BUILD-PLAN.md`, `docs/OSSICRO-CONSTITUTION.md`, `docs/ROADMAP.md`, `docs/VALIDATION-PHILOSOPHY.md`, `docs/WRITING-PRINCIPLES.md`, `docs/rapid-access-vision-and-plan.md`, `docs/strategy-review-fable-2026-07-09.md`, `docs/ehr-integration/*.md`, `app/static/index.html`, and `git log --format='%B' -n 40`.
