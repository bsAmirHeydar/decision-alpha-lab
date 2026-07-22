# 08 - Open Questions

The core strategy is locked. The items below are not blockers for the research/paper implementation. They are optional engineering or research extensions.

## Optional future knobs

1. Whether to expose reference selection as a research input. Canonical default is largest stop distance on the clean traded symbol.
2. Whether to use lower-timeframe path reconstruction for ambiguous SL/TP candles. Canonical default is to mark them `AMBIGUOUS`.
3. Whether to support separate data symbols and execution symbols. Canonical STC uses Symbol1 and Symbol2 as both data and execution symbols.
4. Whether to support broker-specific commission models beyond simple net reporting.
5. Whether to export drawings as screenshots or only render them on chart.
6. Whether to add a calendar for holidays and early closes. Canonical default is no trade when data is missing or incomplete.
7. Whether to add auto-trade mode after research and paper modes are validated.

## No longer open

These are locked and should not be reopened during implementation unless the strategy version changes:

- Touch equality.
- No tolerance.
- W reference matrix.
- W1 no signal.
- New York time.
- Check candle anchoring from 20:00.
- No entry in M gaps.
- No entry on final check candle of M.
- Trade clean symbol.
- SL uses clean traded symbol reference W.
- Reference selection by largest stop.
- Final Reward as R-multiple.
- Hard close at 15:30.
- Partial at W4 end for M1/M2 only.
- M3 partial disabled.
- Entry OFF audit-only/no delayed entry.
- Offline at entry time means no delayed entry.
- Magic-number-only position management.
- Duplicate instance prevention.
