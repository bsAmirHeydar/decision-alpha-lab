# EXP0017 — Full Implementation Roadmap

This roadmap defines the professional implementation path for EXP0017. The project should not begin as a trading robot. It should begin as an anatomy engine that sees the market according to the Strategy Architect doctrine.

## Prime Rule

```text
See -> Measure -> Rank -> Decide -> Execute -> Analyze with AI
```

The robot must first reproduce the market anatomy: New York trading day, cycle groups, references, hunts, divergence, confirmation, invalidation, and signal persistence. Decision logic enters only after the statistical layer has produced evidence.

## Roadmap Table

| Phase | Name | Purpose | Output |
|---|---|---|---|
| Phase 00 | Master Doctrine and Strategy Constitution | Convert all Strategy Architect answers into immutable current-version doctrine. | Inspectable module + documentation + Obsidian notes |
| Phase 01 | Cycle Group Time Anatomy | Build New York trading-day logic, CG registry, current cycle, previous cycles, and chart display. | Inspectable module + documentation + Obsidian notes |
| Phase 02 | Symbol Pair Anatomy | Normalize SPXUSD and NDXUSD as separate self-referenced markets inside the same time field. | Inspectable module + documentation + Obsidian notes |
| Phase 03 | Reference Field Anatomy | Store all previous same-day cycle highs and lows per symbol, CG, and cycle. | Inspectable module + documentation + Obsidian notes |
| Phase 04 | Hunt Anatomy | Detect touch/break/equality hunts by high/low against each symbol’s own references. | Inspectable module + documentation + Obsidian notes |
| Phase 05 | Divergence Anatomy | Create buy/sell divergence states when one symbol hunts and the other does not. | Inspectable module + documentation + Obsidian notes |
| Phase 06 | Confirmation and Invalidation | Finalize signals only on candle close and invalidate double-hunt cases. | Inspectable module + documentation + Obsidian notes |
| Phase 07 | Visual Language and Drawing | Draw evidence lines, labels, and state panels so the robot’s vision can be audited. | Inspectable module + documentation + Obsidian notes |
| Phase 08 | Signal Ledger | Persist confirmed tradeable signals and supporting event fields to CSV/JSON/statistical memory. | Inspectable module + documentation + Obsidian notes |
| Phase 09 | Outcome Study Engine | Calculate cycle-end, multi-window, intraday max reward, MAE, MFE, R, pips, dollars, and normalized outcomes. | Inspectable module + documentation + Obsidian notes |
| Phase 10 | Statistical Report Engine | Report CG, direction, symbol role, session, overlap, signal density, win rate, expectancy, stop streaks, and outcome distributions. | Inspectable module + documentation + Obsidian notes |
| Phase 11 | Model-Ready Dataset | Transform the ledger into stable feature matrices for later ranking and model analysis. | Inspectable module + documentation + Obsidian notes |
| Phase 12 | Ranking and Comparison Layer | Rank families by win rate, expectancy, stop behavior, R outcome, pip outcome, and normalized movement. | Inspectable module + documentation + Obsidian notes |
| Phase 13 | Decision Promotion Gate | Allow the Strategy Architect to choose which statistical findings become versioned rules. | Inspectable module + documentation + Obsidian notes |
| Phase 14 | Raw Execution Layer | Implement doctrine-pure execution: clean-symbol trade, fixed risk, no base position limits, hedge allowed, immediate entry after confirmation. | Inspectable module + documentation + Obsidian notes |
| Phase 15 | Filtered Execution Layer | Implement only promoted constraints, filters, weights, and target variations from validated statistics. | Inspectable module + documentation + Obsidian notes |
| Phase 16 | AI Analyst Layer | Add AI analysis, ranking, comparison, language-aware reporting, warnings, and research recommendations without direct execution authority. | Inspectable module + documentation + Obsidian notes |

## Implementation Discipline

- Each phase must be independently testable.
- Each phase must expose state on chart, in logs, or in files.
- A later phase must not reimplement the contract of an earlier phase.
- No decision layer may contaminate the raw observation layer.
- No AI layer may mutate the current strategy without version promotion.
