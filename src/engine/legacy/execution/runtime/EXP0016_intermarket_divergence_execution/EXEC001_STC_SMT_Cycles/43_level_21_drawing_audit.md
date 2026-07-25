# Level 21 — Drawing Audit Hardening + HardClose Warning Fix

Level 21 does not change STC signal logic, paper simulation, real auto entry, real partial close, or real hard close behavior.

It hardens the visual audit layer so the chart can be used as a practical verification surface for the locked STC rules:

- STC day projection from 20:00 New York to 15:30 New York.
- M1/M2/M3 active windows.
- 02:00–03:00 and 09:00–09:30 no-detection/no-entry gaps.
- 15:30 New York hard-close boundary and post-close zone.
- W1/W2/W3/W4 boundaries and W1 no-signal reminder.
- Closed W high/low levels for the active chart symbol only.
- Recent check-candle boxes for the active chart symbol only.
- Final check candles marked as audited but no-entry.
- Raw high/low hunt markers per legal previous-W reference.
- BOTH-hunted no-SMT markers.
- Clean-symbol SMT markers.
- Selected reference line used as the protective stop source.
- Paper entry line, SL line, TP line, partial marker, hard-close-if-open marker, and outcome marker.

The drawing layer is still audit-only. It does not mutate runtime execution state and does not send orders.

## Chart symbol rule

If the EA is attached to `Symbol1` or `Symbol2`, price-specific layers are drawn on that chart.

If the EA is attached to another symbol, time zones and the dashboard can still be drawn, but price-specific W/SMT layers are suppressed because the price scale is unrelated.

## Visual replay state

The chart replay uses a scratch paper state for visualization so drawing historical plans does not mutate real runtime counters or direction locks.

The operational engine remains governed by the actual signal registry, paper entry, auto-entry, partial, hard-close, and persistence modules.

## HardClose warning fix

The compile warning in `DAL_STC_HardClose.mqh` was caused by assigning `SYMBOL_SPREAD`, returned as an integer/long, into a double variable without an explicit cast.

Level 21 adds the explicit cast:

```mql5
(double)SymbolInfoInteger(audit.trade_symbol, SYMBOL_SPREAD)
```

This is a warning-only cleanup; hard-close accounting logic is unchanged.

## Acceptance checklist

1. Compile `IMDEXEC001_STC_SMT_Cycles.mq5`.
2. Confirm there are no errors and the previous hard-close cast warning is gone.
3. Attach to `Symbol1` or `Symbol2` in Paper Live mode.
4. Confirm the dashboard says `DAL STC LEVEL21`.
5. Confirm M zones, gaps, W boundaries, current check, W levels, check boxes, raw hunts, SMT plan, SL/TP and outcome markers are visible when data exists.
6. Confirm attaching to a non-pair chart suppresses price-specific layers and shows the warning label.
