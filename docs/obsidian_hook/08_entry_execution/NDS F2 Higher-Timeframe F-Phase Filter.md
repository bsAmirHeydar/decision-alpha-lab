# NDS F2 Higher-Timeframe F-Phase Filter

## Contract

```text
HTF bullish F → Buy only (when bullish qualifying counts are the sole qualifying direction)
HTF bearish qualifying F counts only → Sell only
both directions qualify → ambiguous / no entry
no qualifying count → no entry
```

Default higher timeframe: `H1`.

Every canonical HTF F1 root is evaluated as a separate count. Hook/ND veto is local to the count that owns the Hook boundary; an unrelated scale or sequence cannot close the entire gate. The snapshot uses closed HTF bars and refreshes once per new HTF bar.

Pending orders that no longer match the gate are cancelled by default. Open positions are not force-closed.

## Inputs

```text
InpF2BTUseHigherTimeframeFPhaseFilter = true
InpF2BTHigherTimeframe = PERIOD_H1
InpF2BTUseHigherTimeframeF1ToF2ConfirmationWindow = true
InpF2BTCancelPendingWhenHigherTimeframeDisallows = true
```

## Authority

- [[../../nds_entry_architecture/f2_waist_break_point2_limit/13_higher_timeframe_f_phase_direction_filter|Full higher-timeframe filter contract]]
- [[NDS F2 Higher-Timeframe F1-to-F2 Confirmation Window]]
- [[NDS F2 Canonical Frequency Recovery and Multi-Count HTF Gate]]
