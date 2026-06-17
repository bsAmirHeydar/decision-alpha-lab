# M0001 Fast Final-Only Runtime

## Purpose

The EA no longer recomputes nodes, events, audit states, distribution statistics,
or redraws all chart objects on every closed bar by default.

The default research mode is now:

```text
InpRuntimeVisuals = false
```

In this mode the EA only appends new closed bars to the in-memory live stream.
It computes the node/random LogRTV research result once, at `OnDeinit`, after the
backtest/expert run completes.

## Why this is faster

The expensive path was:

```text
every new bar -> detect all nodes -> recompute all events -> recompute audit states -> delete/redraw chart objects
```

That path is now disabled unless `InpRuntimeVisuals=true`.

## Warmup behavior

`InpWarmupHistoricalBars` still seeds older closed bars before the analysis
period. Final reports filter node events by `analysis_start`, so warmup data can
build historical node memory without contaminating the research sample.

## Timer

The millisecond timer is disabled by default:

```text
DAL_M0001_TIMER_MS = 0
```

The stream appends new closed bars from `OnTick`, which is sufficient for
Strategy Tester and removes redundant timer checks.

## .venv

No `.venv` directory is required for the MQL-native branch. `.venv/` and `venv/`
are ignored in `.gitignore`; remove local virtual environments manually if they
exist in your working tree.

## Version

`M0001_LiveVisualLab.mq5` version: `1.57`.
