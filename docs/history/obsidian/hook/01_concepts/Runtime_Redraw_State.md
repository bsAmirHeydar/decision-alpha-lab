# Runtime Redraw State

Runtime redraw state is the expert-level lifecycle layer that decides whether the chart must be recalculated and redrawn.

It is separate from Hook logic.

The key rule is:

```text
Only a successful full run can advance the last-rendered bar timestamp.
```

A failed run must keep redraw eligibility alive. Otherwise a temporary timebase failure after a timeframe switch can freeze Hook visualization until the next candle.

Related:

- [[Phase_33_Timeframe_Change_Redraw_State_Guard]]
- [[Chart_Change_Must_Rebuild_Hook_View]]
- [[Hook_Timeframe_Change_Debug_Checklist]]
