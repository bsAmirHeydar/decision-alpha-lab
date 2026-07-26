# M0001 Fast Final-Only Runtime

Version: 1.59

The fast default keeps the research loop light while preserving the final chart drawings.

## Default inputs

```text
InpRuntimeVisuals = false
InpDrawFinalVisuals = true
InpKeepVisualsOnDeinit = true
```

## What happens during the run

On each intra-candle tick:

```text
return
```

When a new candle opens:

```text
append previous closed candle once
```

No heavy full-history recomputation happens during the run when `InpRuntimeVisuals=false`.

## What happens at shutdown

`OnDeinit` computes the complete state once:

```text
bars -> structural nodes -> M0001 events -> audit states
```

The same computed arrays are used for:

1. final `DAL_M0001_FINAL_NODES` report,
2. final `DAL_M0001_FINAL_RANDOM` report,
3. final restored chart drawings.

This avoids duplicate logic and prevents drift between the final report and the chart.

## What is restored visually

- structural node arrows,
- local node price labels,
- live/revisited/consumed zones,
- true revisit labels,
- pending/live/revisited/consumed state labels,
- consumed markers,
- optional event boxes through `InpShowEvents`,
- optional final RTV labels through `InpShowRTV`,
- optional extreme audit links through `InpShowExtremes`,
- final summary label.

Objects are kept after test finish when:

```text
InpKeepVisualsOnDeinit = true
```

## What did not change

This optimization does not change the research semantics:

- confirmed L-rule node definition,
- active-from timing,
- territory formula,
- frozen event geometry,
- strict exit-gap confirmation,
- HUNT priority,
- TOUCH/HUNT consumption,
- revisit IDs,
- revisited-live extreme reset,
- RTV/logRTV sample construction,
- matched random baseline.
