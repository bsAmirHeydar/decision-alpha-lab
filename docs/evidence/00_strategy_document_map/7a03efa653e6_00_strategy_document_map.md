# 00 - Strategy Document Map

This document explains the documentation layers for EXEC001 STC SMT Cycles.

## Why this strategy is documented in layers

STC is not only a signal rule. It is a full execution model that combines time, cycles, two-symbol SMT, confirmation candles, risk sizing, partial management, hard close, restart recovery, and duplicate-instance safety.

A single README would become ambiguous. Therefore the strategy is split into layers:

1. Source traceability.
2. Normalized strategy rules.
3. Time and cycle model.
4. SMT divergence model.
5. Execution and risk model.
6. Engineering architecture.
7. Test plan.
8. Persistence and journals.
9. Visualization.
10. Implementation checklist.

Each layer should be implementable and testable by itself.

## Reading order

Start with `02_normalized_strategy_spec.md` to understand the full strategy. Then read `03_cycle_calendar.md` and `04_smt_divergence_rules.md` because most logic errors will happen in time and divergence detection. Then read `05_execution_and_risk.md` before any trading logic is implemented.

The implementation team should use:

- `11_algorithm_layers.md` for exact algorithm decomposition.
- `12_state_machines.md` for state transitions.
- `13_data_model_and_journals.md` for persistence and CSV schemas.
- `14_backtest_live_runtime.md` for runtime behavior.
- `16_implementation_checklist.md` for build order.

## Source hierarchy

When documents seem to conflict, use this priority:

1. Owner decisions pass 2.
2. Owner decisions pass 1.
3. Normalized locked spec.
4. Source SRS extraction.
5. Architecture suggestions.
6. Optional future research notes.

## What is locked

The strategy logic is locked enough to build a research/paper engine. The code should not ask new conceptual questions about drawing, basic direction, W references, touch definition, entry symbol, final reward, daily reset, partial, or hedging scope. Those are now locked.

## What can still be configured as research knobs

Some rules can be exposed as inputs for research without changing the canonical default:

- Check candle timeframe.
- Risk percent.
- Final Reward.
- Spread and commission reporting mode.
- Data source.
- Drawing on/off.
- Research vs paper vs auto-trade runtime mode.

The canonical strategy default must remain unchanged unless explicitly versioned.
