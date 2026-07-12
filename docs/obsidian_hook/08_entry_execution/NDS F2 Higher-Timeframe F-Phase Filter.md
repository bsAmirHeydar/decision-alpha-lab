# NDS F2 Higher-Timeframe F-Phase Filter

## Contract

```text
HTF bullish F → Buy only
HTF bearish F → Sell only
HTF Hook/ND or unresolved → no new entry
```

Default higher timeframe: `H1`.

The classifier uses closed higher-timeframe bars and the canonical Phoenix F1/F2/F3 plus Hook/ND engine. A Hook/ND context at or after the latest canonical F endpoint closes the gate. The snapshot is cached and rebuilt only on a new higher-timeframe bar.

Pending orders that no longer match the HTF gate are cancelled by default. Open positions are not closed by the filter; they keep their original SL and selected exit mode.

## Inputs

```text
InpF2BTUseHigherTimeframeFPhaseFilter = true
InpF2BTHigherTimeframe = PERIOD_H1
InpF2BTCancelPendingWhenHigherTimeframeDisallows = true
```

## Authority

- [[../../nds_entry_architecture/f2_waist_break_point2_limit/13_higher_timeframe_f_phase_direction_filter|Full higher-timeframe filter contract]]
- [[NDS F2 Waist-Break Point2 Limit Setup]]
- [[NDS F2 Dual Exit - Fixed F2 or F3 Retest]]
