# EXP0017 — Cycle Group Intermarket Divergence EA

## Purpose

`EXP0017_cycle_group_intermarket_divergence` defines a fresh, independent MQL5 expert specification for detecting and trading intermarket divergence between two symbols using configurable time-based cycle groups.

This experiment is intentionally separated from earlier experts and earlier strategy stacks. It does not inherit the STC/M/W-cycle execution model, Flag logic, NDS logic, astrology modules, or previous IntermarketDivergenceExecution runtime.

The model is based on a simple structural rule:

> If one symbol hunts a previous cycle high/low and the other symbol does not, a divergence is formed after the chart timeframe candle closes.

## Core identity

| Field | Value |
|---|---|
| Experiment ID | EXP0017 |
| Expert concept | CG Intermarket Divergence EA |
| Runtime surface | MQL5 Expert Advisor |
| Strategy family | Intermarket divergence / SMT-like divergence |
| Time model | New York trading day, 18:00 to 17:00 |
| Cycle model | Multiple cycle groups from 3m to 720m |
| Default pair | SPXUSD / NDXUSD |
| Entry symbol | Symbol that did not hunt |
| Stop reference | Divergence reference level on clean symbol |
| Target | End time of current cycle |
| Risk | 1% of equity |
| Data retention | Same trading day only |

## Document map

1. [`01_strategy_spec.md`](01_strategy_spec.md) — full strategy doctrine.
2. [`02_cycle_group_calendar.md`](02_cycle_group_calendar.md) — cycle group construction from 18:00 New York.
3. [`03_divergence_detection_rules.md`](03_divergence_detection_rules.md) — high/low hunt and divergence formation.
4. [`04_inputs_contract.md`](04_inputs_contract.md) — complete input schema for symbols, timezone, trade/draw/color per CG.
5. [`05_drawing_contract.md`](05_drawing_contract.md) — hunter-symbol drawing rules.
6. [`06_execution_and_risk_contract.md`](06_execution_and_risk_contract.md) — entry, stop, target, position sizing, risk.
7. [`07_mql5_modular_architecture.md`](07_mql5_modular_architecture.md) — proposed modular MQL5 file breakdown.
8. [`08_state_and_data_model.md`](08_state_and_data_model.md) — runtime state, event keys, memory boundaries.
9. [`09_test_plan.md`](09_test_plan.md) — validation matrix and manual checks.
10. [`10_open_questions.md`](10_open_questions.md) — deliberate unresolved decisions before code.

## Non-goals

This project deliberately does **not** implement:

- previous STC M/W-cycle logic;
- previous EXP0015 CSV experiment engine;
- previous EXP0016 auto-entry stack;
- multi-day reference scanning;
- close-break hunt requirements;
- tolerance-based equal-high/equal-low interpretation;
- astrology timing;
- Flag / Hook / NDS structural logic.

## Implementation posture

The MQL5 expert should be built as a modular framework, not a one-off script. The EA file should remain an orchestration layer. The following domains should be isolated:

```text
Time conversion
Cycle group calendar
Symbol OHLC access
Cycle reference level builder
Hunt detector
Divergence detector
Signal registry
Drawing manager
Risk and volume manager
Trade router
Daily reset manager
Audit logger
```

## Phase 14 raw execution backtest

The first modular order-producing profile is documented at:

- [[phase14_raw_execution_backtest/PHASE14_INDEX]]

This owner-approved backtest profile uses closed-candle market entry, selectable protected/hunter execution leg, confirmation-candle stop, and ATR target. It consumes the Hotfix011 signal authority without changing divergence detection. Every divergence anatomy has one hard, non-retryable execution entitlement even when it is observed on multiple lower-timeframe candles.

- [[phase14_raw_execution_backtest/PHASE14_ONE_SHOT_SIGNAL_EXECUTION_CONTRACT]]

