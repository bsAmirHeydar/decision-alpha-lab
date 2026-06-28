# 08 - Remaining Open Questions Before Implementation

The strategy-level questions from the SRS have been resolved by owner clarification passes 1 and 2.

This file now tracks only non-blocking engineering decisions that can be implemented as defaults or inputs without changing the strategy logic.

## Resolved strategy decisions

- Equality counts as touch.
- No tolerance is applied.
- Check candles are anchored from 20:00 New York.
- No entry is allowed from a check candle closing at or after active M end.
- Multiple references resolve to the one producing the largest stop distance for the clean/traded symbol.
- Simultaneous buy and sell in the same check candle are forgotten for execution.
- Entry OFF signals are audit-only and cannot be entered later.
- Offline-at-entry signals are not entered later.
- Failed order attempts consume the signal but do not increase the M trade counter.
- Hedging/direction lock applies only within each M.
- Each M can open at most three trades across both symbols combined.
- Volume above broker max may be split into multiple broker-valid orders.
- Contract Size is a shared fallback input.
- TP is calculated without costs; costs are reporting/net-analysis fields.
- SL/TP same-candle ambiguity is reported as AMBIGUOUS.
- Both symbols must have complete enough data.
- Restart reconstruction uses current-day candles, persistent state, and strategy-owned positions.
- Duplicate executable instances must be blocked.
- Symbol1 and Symbol2 are both data and execution symbols in this STC version.
- EA manages only its own magic-number positions.

## Non-blocking engineering items

These can be implemented with documented defaults:

1. Exact required data-coverage threshold for a W/check window.
2. CSV schemas for cycle audit, divergence audit, trade journal, and state audit.
3. Exact chart object styling for drawing.
4. Exact retry interval default for hard-close retry.
5. Exact behavior when requested live volume cannot be fully split because of broker constraints.
