# EXEC001 - STC SMT Cycles

## Purpose

This folder documents the STC Expert Advisor strategy from the provided SRS PDF as a layered, implementation-ready English specification.

The source describes an Expert Advisor that trades an SMT divergence strategy between two indices. It is chart-symbol independent, uses only `Symbol1` and `Symbol2` inputs for analysis and trade management, uses New York time, and resets all strategy state at the end of the STC trading day.

## Current status

| Layer | Status |
| --- | --- |
| Source PDF read-through | Done |
| English extraction | Done |
| Normalized strategy spec | Done |
| Cycle model | Done with explicit ambiguity notes |
| SMT divergence model | Done with explicit ambiguity notes |
| Execution/risk model | Done |
| MQL5 implementation architecture | Proposed |
| Test plan | Proposed |
| Code implementation | Not started |

## Read these files in order

1. [`01_source_srs_extraction.md`](./01_source_srs_extraction.md)
2. [`02_normalized_strategy_spec.md`](./02_normalized_strategy_spec.md)
3. [`03_cycle_calendar.md`](./03_cycle_calendar.md)
4. [`04_smt_divergence_rules.md`](./04_smt_divergence_rules.md)
5. [`05_execution_and_risk.md`](./05_execution_and_risk.md)
6. [`06_mql5_architecture_plan.md`](./06_mql5_architecture_plan.md)
7. [`07_test_plan.md`](./07_test_plan.md)
8. [`08_open_questions.md`](./08_open_questions.md)

## Core summary

The EA should:

- Run once on any chart, independent of the chart symbol and chart timeframe.
- Analyze and trade only two configured symbols.
- Use New York time for all strategy windows.
- Manage DST automatically, while the user supplies only the broker UTC offset.
- Treat one STC trading day as New York 20:00 to New York 15:30 next day.
- Close all open trades and reset all state at 15:30 New York.
- Detect SMT divergence when only one of the two symbols hunts a prior W high or low within the same M cycle.
- Treat a hunt as touch only; candle close is not required for the hunt itself.
- Wait for the selected check candle to close before entry.
- Enter immediately after the check candle close if the divergence still exists.
- Prevent repeated entries from the same divergence.
- Limit entries to 3 trades per M cycle.
- Support optional hedging and optional partial close.
- Set stop-loss exactly on the referenced W high/low, with no buffer.
- Calculate size from risk percent, equity, and contract size.
- Set take-profit from final reward and never modify it after entry.

## Implementation warning

The PDF contains one important ambiguity in the W comparison matrix. The text says the current W is never compared with itself and is compared only with previous W cycles in the same M. However, the printed rule matrix includes pairings that can be read more than one way. The implementation should not start until the rule direction is confirmed in [`08_open_questions.md`](./08_open_questions.md).
