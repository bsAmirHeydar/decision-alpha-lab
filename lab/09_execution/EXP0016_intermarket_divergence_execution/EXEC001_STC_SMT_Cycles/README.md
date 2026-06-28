# EXEC001 - STC SMT Cycles

This folder documents the STC SMT Cycles execution strategy extracted from the provided STC Expert Advisor SRS and the subsequent owner clarifications.

The strategy belongs to the intermarket divergence execution family. It is not a generic SMT detector; it is a specific cycle-based execution model using two symbols, New York time, M cycles, W cycles, touch-only SMT divergence, check-candle confirmation, risk-based sizing, final reward TP, optional partial close, and daily hard reset.

## Current implementation status

This folder is documentation-first. It is intended to lock the strategy contract before writing MQL5 code.

Status:

- Source SRS extracted: complete.
- Owner clarification pass 1: complete.
- Normalized executable spec: updated.
- M/W calendar: updated.
- SMT divergence rules: updated.
- Execution and risk rules: updated.
- Test plan: updated.
- Remaining questions: reduced to implementation-level details.

## Strategy summary

The EA analyzes exactly two configured symbols. The chart symbol is irrelevant. The two configured symbols are also the only symbols whose trades are managed by the strategy.

The STC trading day is defined in New York time. It begins at 20:00 New York and ends at 15:30 New York on the following calendar day. At 15:30 New York, all open trades are closed and all day state is reset.

The strategy divides the trading day into three parent M cycles. Each M contains four W cycles. W1 never produces a signal because there is no previous W inside the same M. W2 can compare only against W1. W3 can compare only against W1 and W2. W4 can compare only against W1, W2, and W3. A W never compares with itself.

A valid SMT divergence occurs when exactly one of the two symbols hunts the high or low of an eligible previous W reference in the same M, while the other symbol does not hunt its corresponding same-structure W reference. Hunt is touch-only. No candle close beyond the level is required.

The EA waits until the active check candle closes. If the divergence still exists at the check-candle close, the trade is entered immediately. If the clean symbol has also hunted the corresponding level before the check candle closes, the divergence is invalid and no trade is entered.

The trade is placed on the clean symbol, meaning the symbol that did not hunt. If Symbol1 hunts and Symbol2 does not, trade Symbol2. If Symbol2 hunts and Symbol1 does not, trade Symbol1.

High-side SMT divergence is a sell setup. Low-side SMT divergence is a buy setup.

Stop loss is placed on the high or low of the selected reference W of the trade symbol. No buffer is used. If multiple references are eligible, the selected reference is the closest eligible W by time, or the eligible reference producing the smaller stop distance if that option is enabled for testing.

Final Reward is an R-multiple. Final Reward = 10 means 10R TP.

## Document map

- `01_source_srs_extraction.md` - English extraction of the source PDF.
- `02_normalized_strategy_spec.md` - Executable strategy contract.
- `03_cycle_calendar.md` - New York trading day, M cycles, W cycles, gaps, and reset policy.
- `04_smt_divergence_rules.md` - Hunt, divergence, reference selection, confirmation, invalidation, and anti-duplicate rules.
- `05_execution_and_risk.md` - Entry, SL, TP, sizing, hedging, partial close, daily close, costs, and broker behavior.
- `06_mql5_architecture_plan.md` - Planned modular MQL5 structure.
- `07_test_plan.md` - Deterministic test scenarios.
- `08_open_questions.md` - Remaining questions after clarification pass 1.
- `09_owner_decisions_pass_1.md` - Locked decisions provided by the strategy owner.
