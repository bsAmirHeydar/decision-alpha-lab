# Hook Timeframe Change Debug Checklist

Use this when Hook drawings stop updating after switching timeframes.

## Inputs

Enable:

```text
InpRuntimePrintRedrawState = true
InpPrintTimebaseSanity = true
InpPrintFailureSummaries = true
```

Keep:

```text
InpRuntimeRetryFailedRunsOnTimer = true
InpRuntimeRetryTimerSeconds = 2
InpCleanObjectsOnChartChange = true
InpCleanObjectsOnInit = true
InpHookPhase07CleanBeforeApply = true
```

## Expected sequence

After switching timeframe:

```text
cleanup old objects
reset runtime redraw state
attempt run
if history not ready: mark failed and keep retry alive
timer retries
when history becomes ready: run completed and Hook view redraws
```

## Failure signs

A bad runtime state looks like:

```text
timebase failed once
last bar time already committed
no retry until next candle
Hook view stale or empty
```

Phase 33 prevents this by committing bar time only after a successful run.
