# M0001 Candle-Gated Runtime

Version: 1.59

M0001 is still an Expert Advisor, so MetaTrader wakes it through `OnTick()`. The research engine itself is not tick-based.

## Runtime behavior

```text
intra-candle tick -> return immediately
new candle opens -> append the previous closed candle once
OnDeinit -> compute full final state once
```

The timer is disabled by default:

```text
DAL_M0001_TIMER_MS = 0
```

If a timer is enabled later, it must pass through the same candle gate.

## Fast default

The optimized default is:

```text
InpRuntimeVisuals = false
InpDrawFinalVisuals = true
InpKeepVisualsOnDeinit = true
```

This keeps runtime light while restoring final chart drawings. During the run the EA appends closed candles only. At shutdown, the same final computed state is used for both:

- `DAL_M0001_FINAL_NODES` / `DAL_M0001_FINAL_RANDOM`
- final node, zone, revisit, state, and optional RTV/event drawings

## Visual replay mode

For step-by-step visual debugging:

```text
InpRuntimeVisuals = true
```

This recomputes and redraws on each newly closed candle only. It never runs heavy logic on intra-candle ticks, but it is intentionally slower than final-only mode.

## Semantics unchanged

The candle gate does not change:

- structural-node definition,
- `active_from = node_index + L`,
- territory formula,
- HUNT priority,
- exit-gap confirmation,
- TOUCH/HUNT consumption modes,
- revisit memory,
- revisited-live extreme reset,
- RTV/logRTV,
- matched random baseline.
