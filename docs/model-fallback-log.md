# Model Fallback Log

Principal directive: subagents should run on **Fable 5 (`claude-fable-5`)** for authoring/review and **Sonnet 5 (`claude-sonnet-5`)** for the academic sweep. Each subagent reports its actual model as its first output. Any fallback to **Opus 4.8 (`claude-opus-4-8`)** is logged here.

| Date | Phase | Requested | Reported | Fallback? |
|------|-------|-----------|----------|-----------|
| 2026-07-06 | (ideation) main session | Fable 5 | Opus 4.8 | YES — session kept on Opus 4.8 |
| 2026-07-06 | (ideation) Fable review of AE ideas | Fable 5 | Fable 5 | no |
| 2026-07-08 | virtual-CRO explore: site-activation agent | Fable 5 | Fable 5 | no |
| 2026-07-08 | virtual-CRO explore: trial-design agent | Fable 5 | Fable 5 | no |
| 2026-07-08 | virtual-CRO explore: physician-direct agent | Fable 5 | Fable 5 | no |
| 2026-07-08 | virtual-CRO explore: landscape agent | Fable 5 | **Opus 4.8** | **YES** |

Running tally will be appended as OSSICRO phases execute.

## OSSICRO Phase 1 (2026-07-08)
- 7 Fable regulatory/document briefs: all reported `claude-fable-5` (no fallback). [1 returned a probe placeholder - regenerated separately.]
- 3 Sonnet academic/institutional/publication sweeps: all reported `claude-sonnet-5` (no fallback).
- 1 Fable synthesis: reported `claude-fable-5` (no fallback).

## OSSICRO Phase 3 (2026-07-09)
- Wiki authoring (30 Fable cluster-agents): all reported `claude-fable-5` (no fallback); 129 pages, no probes.
- Engine builder (standalone Fable): reported `claude-fable-5`; TERMINATED by session rate-limit mid-write (had written 9/14 files); orchestrator completed the remaining 5 files by hand and verified (demo runs, 9/9 tests pass).
