# Phase 33 — Timeframe Change Redraw State Guard

Phase 33 adds an explicit runtime redraw state machine to the central FlagCounting Phoenix expert.

Core fields:

```text
g_fp_last_run_ok
g_fp_force_redraw
g_fp_last_run_status
g_fp_last_bar_time
```

Before this phase, the new-bar throttle could advance before the run completed. If the first run after a timeframe change failed because history was not ready, subsequent ticks inside the same candle could skip retries.

After this phase:

```text
failed run => force redraw remains true
successful run => last bar time is committed
```

Timer recovery is enabled by:

```text
InpRuntimeRetryFailedRunsOnTimer = true
InpRuntimeRetryTimerSeconds = 2
```

The timer retries only when the previous run failed, a forced redraw is pending, or chart identity changed.
