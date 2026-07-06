# Phase 33 — Timeframe-Change Runtime Redraw State Guard

## Purpose

This phase fixes a runtime redraw failure observed after repeatedly switching chart timeframes while the central FlagCounting Phoenix expert is attached.

The visible symptom is that Hook drawings may stop updating after several timeframe changes. The root cause is not Hook geometry and not the semantic arc renderer. The failure is a runtime lifecycle issue around chart identity, history synchronization, and the `InpRedrawOnNewBarOnly` throttle.

## Problem

The expert uses a new-bar throttle to avoid expensive full recalculation on every tick:

```text
InpRedrawOnNewBarOnly = true
```

Before this phase, the throttle updated `g_fp_last_bar_time` before knowing whether the full run actually completed.

That is dangerous during timeframe changes because MetaTrader may briefly have incomplete or unsynchronized history for the newly selected timeframe. In that window, the first run can fail at the timebase layer:

```text
FP_LoadCanonicalRates
-> timebase not ready / not enough closed bars / strict timebase failure
```

If the throttle already recorded the current bar time before the failed run, later ticks inside the same candle no longer trigger a retry. The chart can then remain empty or stale until a new candle appears, which looks like Hook drawings stopped updating.

## Correct Doctrine

A bar-time throttle may only be advanced after a successful full run.

```text
failed run  => keep retry eligibility alive
successful run => commit current bar time as last rendered bar
```

This is a runtime contract, not a Hook-structure contract.

## New Runtime State

The expert now tracks explicit run health:

```text
g_fp_last_run_ok
g_fp_force_redraw
g_fp_last_run_status
```

### Failed run

When a run fails due to license state, timebase failure, insufficient closed bars, or missing scales, the expert marks:

```text
g_fp_last_run_ok = false
g_fp_force_redraw = true
```

This keeps retry eligibility alive even if the bar time has not changed.

### Successful run

Only after all stages complete does the expert mark:

```text
g_fp_last_run_ok = true
g_fp_force_redraw = false
g_fp_last_bar_time = iTime(_Symbol, _Period, 0)
```

Therefore the throttle now represents the last successfully rendered bar, not the last attempted bar.

## Timer Retry

The previous timer only performed license upkeep. This phase lets the timer retry failed runtime runs without waiting for a new candle.

New inputs:

```text
InpRuntimeRetryFailedRunsOnTimer = true
InpRuntimeRetryTimerSeconds = 2
InpRuntimePrintRedrawState = false
```

The timer now performs two recovery actions:

1. If chart identity changed, clean relevant objects, reset runtime redraw state, and run.
2. If the previous run failed or a forced redraw is pending, retry the run.

The timer does not continuously recalculate a healthy chart. When the last run succeeded and the current bar has not changed, it remains idle.

## Chart-Change Handling

The existing identity guard is kept:

```text
symbol + period
```

On chart identity changes, the expert still performs hard cleanup of:

```text
InpObjectPrefix
DAL_HOOK_*
Hook Phase 01-10 prefixes
```

Then it resets the runtime redraw state and runs again.

## Why This Fix Is Correct

The fix separates three states that were previously conflated:

```text
1. chart identity changed
2. run attempted
3. run successfully rendered
```

Only state 3 is allowed to update the new-bar throttle.

This prevents the expert from freezing after a failed first run on a newly selected timeframe.

## What This Phase Does Not Change

This phase does not change:

- Hook sequence logic
- Hook origin survival rules
- Hook after Hook validity
- Hook after opposing F3 validity
- F1/F2/F3 logic
- Zone logic
- order execution
- broker behavior
- risk sizing
- paper trading logic

It only changes runtime redraw eligibility and retry behavior.

## Debug Procedure

For diagnostics, enable:

```text
InpRuntimePrintRedrawState = true
InpPrintTimebaseSanity = true
InpPrintFailureSummaries = true
```

Then switch timeframes repeatedly.

Expected behavior:

```text
FP_RUNTIME_REDRAW status=FAILED ...
```

may appear briefly while history is not ready, followed by:

```text
FP_RUNTIME_REDRAW status=OK reason=RUN_COMPLETED ...
```

without waiting for a new candle.

## Acceptance Criteria

- Repeated timeframe switching should not leave stale Hook drawings.
- Failed first run after chart change should be retried by timer.
- `g_fp_last_bar_time` should only represent a successful completed render.
- Healthy charts should not be recalculated continuously when `InpRedrawOnNewBarOnly=true`.
- Hook objects should still be cleaned on init, deinit, chart change, recompile, parameter change, and template application according to existing inputs.
