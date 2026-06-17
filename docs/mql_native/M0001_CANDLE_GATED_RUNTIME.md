# M0001 Candle-Gated Runtime

Version: 1.58

This update keeps the research engine candle-based rather than tick-based.

## What changed

- `OnTick()` no longer runs append, node detection, event computation, audit-state computation, or chart redraw on every tick.
- A candle clock tracks the current open candle time.
- The EA returns immediately while the current candle is unchanged.
- Work is triggered only when a new candle opens, which means the previous candle has closed.
- The timer remains disabled by default, but if it is enabled in the future it uses the same candle gate.

## What did not change

The research semantics are unchanged:

- structural-node definition
- `active_from = node_index + L`
- territory formula
- touch / exit-gap confirmation
- HUNT / TOUCH consumption semantics
- revisit semantics
- RTV and logRTV definition
- random baseline comparison
- final-only node/random reporting

## Why this matters

MetaTrader Expert Advisors receive `OnTick()` events, but this version uses them only as a lightweight notification source. No heavy research logic runs intra-candle.

The runtime behavior is now:

```text
intra-candle tick -> return immediately
new candle opens -> append previous closed candle once
shutdown -> compute final node/random statistics once
```
