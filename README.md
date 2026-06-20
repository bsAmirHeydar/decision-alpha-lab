# Decision Alpha Lab

Decision Alpha Lab is a structural market research laboratory. Its purpose is not to fit indicators to past price, but to test whether price contains repeatable decision structure around confirmed market nodes.

The project has evolved into a strict research program built around three contracts:

1. **Structural nodes instead of fixed time windows** — the x-axis of the market is not a calendar window; it is a sequence of decision nodes, zones, revisits, breaks, hunts, and confirmed state changes.
2. **Live-known time instead of completed-sample ordering** — a regime may only influence a later decision after the candle/time at which it became knowable. Events that become known on the same candle are simultaneous, not sequential.
3. **Execution R instead of path-normalized R** — an R multiple is only tradable when a real initial risk model exists: zone edge, ATR stop, fixed R, trailing stop, or another explicit stop rule.

The current research focus is the transition from exploratory structural reports to live-valid, no-sample, candle-by-candle replay.

---

## Current research map

| ID | Name | Status | Current interpretation |
|---|---|---|---|
| H0001 | Structural highs/lows as decision nodes | Active | Structural nodes are treated as privileged market locations, not arbitrary prices. |
| H0002 | Node territory and revisit lifecycle | Active | Nodes have zones, activation, revisits, consumption, and termination. |
| H0004 | Branch regime memory | Rebuilt | Classic sample sequence is deprecated for live claims. Atomic no-sample known-time batches are the official contract. |
| H0005 | Directional memory and execution | Rebuilt | Classic path reports are exploratory only. Main reports must use raw-event, live-style, no-sample replay and explicit risk models. |

---

## Research layers

### Observations

Raw qualitative and empirical observations live in `lab/01_observation`.

### Hypotheses

Hypothesis documents live in `lab/02_hypotheses`. Each hypothesis must state the null, the live-validity contract, expected evidence, failure conditions, and what would make it tradable.

### Experiments and validations

Experiments and validation reports live in `lab/03_experiments`, `lab/04_analysis`, and `lab/05_validation`. Debug validators may exist, but a result is not considered official until it is promoted into the main report contract.

### Execution

Execution concepts are documented in `lab/09_execution` and implemented in MQL5 Expert Advisors. Execution claims must not rely on structural path R unless that structural distance is actually used as a real stop.

---

## Core live-validity rule

A report must answer this before being trusted:

> At this exact closed candle, what was actually knowable without using future data?

This means:

- no future-completed samples as decision sources,
- no outcome-sorted sample order for live regime sequencing,
- no fake transition between events that became known on the same candle,
- no regime-change exit before the regime change was itself knowable,
- no R multiple unless the risk denominator is a real execution risk.

---

## Important terminology

- **Classic sample report**: a report built from completed branch samples. Useful for discovery, not enough for live execution claims.
- **Causal batch report**: a report that groups sample labels by known candle and treats same-candle labels as simultaneous.
- **Atomic no-sample report**: a report that does not build M0002 branch samples at all. It replays raw M0001 events by known time.
- **Known-time batch**: all labels/events that become knowable on the same candle/time. These are simultaneous.
- **Ambiguous batch**: a known-time batch containing both reversal and continuation energy. It must not create a fake sequence.
- **Path-normalized R**: an R-like scale based on structural distance. It is not necessarily tradable.
- **Execution R**: R based on a real stop/risk model.

---

## Main documents

Start here:

- `docs/00_project_index.md`
- `docs/atomic_live_research_contract.md`
- `docs/research_lessons_and_failure_modes.md`
- `docs/reports/2026-06-20_h4_h5_gold_m10_report.md`
- `docs/articles/structural_regime_memory_without_samples.md`
- `docs/articles/reversal_vs_continuation_execution.md`
- `docs/process/release_application_protocol.md`
- `papers/001_atomic_live_regime_framework.md`

---

## Current engineering rule

New releases must use short application commands, clean their own release files, and avoid printing `git status` as part of the standard apply block.

Use this shape:

```powershell
Expand-Archive .\release_files.zip -DestinationPath . -Force
powershell -ExecutionPolicy Bypass -File .\install_release.ps1
Remove-Item .\release_files.zip -ErrorAction SilentlyContinue
Remove-Item .\release.patch -ErrorAction SilentlyContinue
Remove-Item .\install_release.ps1 -ErrorAction SilentlyContinue
```

Commit commands should list only project files, not release archives or installer scripts.
