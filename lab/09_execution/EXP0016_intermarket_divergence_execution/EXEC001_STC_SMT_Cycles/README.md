# EXEC001 STC SMT Cycles

This folder contains the locked specification and implementation blueprint for the **STC SMT Cycles** strategy.

The strategy is an execution model for two-index SMT divergence. It trades only the two configured symbols, it is independent of the chart symbol, and it must not use information from outside the current STC trading day for signal decisions.

The documents in this folder are intentionally layered. The goal is to make the strategy reusable, auditable, and implementable without hiding logic inside one large EA file.

## Current status

Status: **Locked specification, ready for research/paper engine implementation**.

The strategy rules have been normalized from the source SRS and then refined through owner clarification passes. The remaining implementation work is no longer conceptual; it is engineering: build the cycle engine, SMT detector, confirmation scheduler, trade simulator, live/paper executor, journals, and drawings exactly according to the locked rules.

## Document map

- `00_strategy_document_map.md` explains how to read the documentation set.
- `01_source_srs_extraction.md` keeps the source SRS extraction and protects traceability.
- `02_normalized_strategy_spec.md` is the main human-readable strategy specification.
- `03_cycle_calendar.md` defines the STC trading day, M cycles, W cycles, gaps, and check-candle anchoring.
- `04_smt_divergence_rules.md` defines W reference selection, hunt detection, SMT divergence, confirmation, ambiguity handling, and signal identity.
- `05_execution_and_risk.md` defines entry, stop, target, risk sizing, volume, broker limits, hedging, partial close, hard close, fees, and outcomes.
- `06_mql5_architecture_plan.md` defines the modular MQL5 architecture.
- `07_test_plan.md` defines deterministic test cases before live use.
- `08_open_questions.md` should remain nearly empty; it now contains only optional future knobs, not core unresolved rules.
- `09_owner_decisions_pass_1.md` records the first owner clarification pass.
- `10_owner_decisions_pass_2.md` records the second owner clarification pass.
- `11_algorithm_layers.md` breaks the entire strategy into independent algorithms.
- `12_state_machines.md` defines the strategy state machines.
- `13_data_model_and_journals.md` defines records, keys, CSV outputs, and persistence.
- `14_backtest_live_runtime.md` defines the backtest runtime and live/paper runtime.
- `15_visualization_contract.md` defines chart drawings and audit overlays.
- `16_implementation_checklist.md` converts the spec into build phases.

## Locked one-line strategy definition

STC SMT Cycles detects, confirms, and executes SMT divergence between two configured index symbols inside the current STC trading day. The system compares each symbol against its own W-cycle reference levels. If exactly one symbol hunts a valid previous W high or low and the divergence remains valid at the close of the configured check candle, the strategy trades the clean non-hunted symbol, with the stop placed on the selected reference W of the traded symbol and the target computed as a Final Reward R-multiple.

## Core locked rules

1. Time is New York time.
2. The STC trading day starts at 20:00 New York and ends at 15:30 New York on the following calendar day.
3. At 15:30 New York all STC positions are hard-closed and state is reset.
4. M gaps are no-detection and no-entry zones.
5. Open positions are still managed during gaps.
6. M1 is 20:00-02:00, M2 is 03:00-09:00, and M3 is 09:30-15:30.
7. Each M has four W cycles.
8. W1 never creates signals.
9. W2 can compare only against W1.
10. W3 can compare only against W2 and W1.
11. W4 can compare only against W3, W2, and W1.
12. A W never compares against itself.
13. Each symbol has its own W high and W low.
14. The comparison is structural, not shared-price.
15. Hunt is touch-only.
16. Equality counts as touch: high >= reference high and low <= reference low.
17. No tolerance is used.
18. High-side SMT is a sell setup.
19. Low-side SMT is a buy setup.
20. The trade is opened on the clean symbol that did not hunt.
21. If buy and sell confirm in the same check candle, the event is discarded and no trade is allowed.
22. If multiple valid references exist, the selected reference is the one that creates the largest stop distance on the clean traded symbol.
23. Final Reward is an R-multiple. Final Reward 10 means 10R.
24. TP is calculated without transaction costs.
25. Spread and commission are used for reporting and net analysis.
26. Maximum three opened trades are allowed per M across both symbols.
27. Hedging OFF locks direction only inside the current M.
28. Opposite direction trades are allowed in later M cycles even when Hedging is OFF.
29. Partial close happens at the end of W4 for M1 and M2.
30. M3 partial is disabled because the hard close at 15:30 has priority.
31. Missed partial and missed hard close must be recovered at the first opportunity.
32. The EA manages only its own magic-number positions.
33. Duplicate EA instances for the same strategy and symbol pair must be blocked.


## Current engineering level: Level 05

The current code level builds the legal previous-W reference matrix and audits raw touch-only high/low hunts for every closed check candle. It still does not produce SMT candidates, confirmations, signals, paper trades, or live orders.
