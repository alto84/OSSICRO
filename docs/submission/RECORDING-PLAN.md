# OSSICRO — 3-minute demo recording plan (turnkey)

Deadline: **Mon Jul 13, 9:00 PM ET**. The video is used in Stage 1 (Demo = 30%)
**and** replayed in the Stage 2 final round — so this one recording is the whole
show. Target: 2:50–3:00, "genuinely cool to watch."

## Before you hit record
- Close every other window; single monitor if possible; hide the bookmark bar.
- Screen recorder: Loom or QuickTime (Mac) / Xbox Game Bar (Win). 1080p.
- Have the server running: `python app/server.py`. Two browser tabs ready:
  **Tab A** = `http://127.0.0.1:8765/` (dashboard), **Tab B** = `http://127.0.0.1:8765/microcro`.
- In Tab A, pre-create a case and load the sample so "Generate" is one click away
  (or start fresh if you want to show the intake — your call; fresh is more honest,
  pre-loaded is faster).
- Do one dry run. One or two takes is fine; don't over-polish.

## The five beats (with the voiceover)

**1 · The user and the wall — 0:00–0:18** · *Talking head or a slide, then the dashboard.*
> "Dr. Jordan Rivera is a neurologist. Her patient has refractory epilepsy and could benefit from an investigational drug — but there's no open trial. To treat that one patient legally, she'd have to become an FDA sponsor-investigator and produce grade-A regulatory documentation: months of work, tens of thousands in CRO fees. Most physicians just give up."

**2 · What it is — 0:18–0:38** · *Tab A, dashboard at localhost:8765.*
> "OSSICRO is open-source software that assembles, checks, and coordinates that entire burden — for single-patient expanded access, FDA Form 3926. I built it this week with Claude Code. Here's the real thing, running."

**3 · The working flow — 0:38–1:20** · *Exact clicks, in order:* **Start a case → Load example case → Save & continue →** type your name + **Commit profile → Generate documents.** The 8 drafts and the ledger appear (the button now reads *Regenerate documents*); open the **Form 3926 PDF.** *(The commit is a nice governance beat — a named human commits the input of record before anything is drafted.)*
> "From the patient's intake, OSSICRO generates the eight documents the FDA needs — every field stamped back to its source. A named clinician commits the confirmed data first; nothing is drafted from an unconfirmed input. This is the completeness ledger: green, amber, red — each item mapped to the exact regulation that governs it. And here's the filled Form 3926, as a real PDF."

**4 · The wow beat — governance in code — 1:20–2:15** · *Switch to Tab B (`/microcro`).*
> "But generating documents isn't the hard part. This is. A solo physician can't hold every regulatory obligation, so some can transfer to a small accountable entity — a micro-CRO. OSSICRO knows which obligations can move…"
*(toggle two transferable obligations to "Transfer to CRO")*
> "…and which never can. Watch."
*(click "Try to transfer to CRO" on **Obtaining the subject's informed consent**)*
> "When I try to transfer informed consent, OSSICRO refuses — because under 21 CFR Part 50, that's a non-delegable human act. The AI drafts everything a physician needs, and refuses to do the things only a human may. It enforces the legal line in code."
*(click "Draft the TORO →" to show the clean, cited instrument)*

**5 · Built with Claude Code, built to last — 2:15–3:00** · *Quick cuts: the passing test run, the repo, the wiki.*
> "Underneath: 25 engine modules, 593 passing tests, a 131-page regulatory wiki, every claim cited to a primary FDA source — verified, not hallucinated. I used Claude Code to build it and to run adversarial multi-agent reviews against it, catching regulatory errors a single pass would miss. MIT-licensed, one command to run, working today. OSSICRO gives every physician with the right patient a compliant path — without a CRO in the room."

## Submission checklist (do these, in order)
1. Record → export the video (≤3:00).
2. Upload to **YouTube (unlisted is fine) or Loom**; make sure the link is **public/viewable**.
3. Confirm the repo is public: `https://github.com/alto84/OSSICRO` (it is). Push any final commits.
4. Written description: paste from `docs/submission/SUMMARY.md` (~165 words).
5. Submit at **`https://cerebralvalley.ai/e/built-with-claude-life-sciences/hackathon/submit`** with: video link + repo link + description. **Before Mon Jul 13, 9:00 PM ET.**
6. (Optional) Post in the Discord `#questions` if anything about the form is unclear.
