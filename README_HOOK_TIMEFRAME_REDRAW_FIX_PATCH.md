# Hook Timeframe Redraw Fix Patch

## Summary

This patch fixes Hook drawings becoming stale after repeated timeframe changes.

The issue was runtime-state related, not Hook geometry related. The old redraw throttle could update `g_fp_last_bar_time` before the run succeeded. If the first run after a timeframe change failed because MT5 history was not ready, the expert could skip retries until the next candle.

## Code changes

Main file:

```text
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

Added runtime state:

```text
g_fp_last_run_ok
g_fp_force_redraw
g_fp_last_run_status
```

Added inputs:

```text
InpRuntimeRetryFailedRunsOnTimer = true
InpRuntimeRetryTimerSeconds = 2
InpRuntimePrintRedrawState = false
```

`FP_Run()` now returns success/failure and marks runtime state explicitly.

## Documentation

```text
docs/nds_hook_architecture/45_phase33_timeframe_change_redraw_state_guard.md
```

Obsidian notes:

```text
docs/obsidian_hook/01_concepts/Runtime_Redraw_State.md
docs/obsidian_hook/02_policies/Chart_Change_Must_Rebuild_Hook_View.md
docs/obsidian_hook/03_architecture/Phase_33_Timeframe_Change_Redraw_State_Guard.md
docs/obsidian_hook/04_debug/Hook_Timeframe_Change_Debug_Checklist.md
```

## Scope

This patch changes runtime redraw retry behavior only. It does not change Hook sequence logic, F logic, Zone logic, execution, broker behavior, or risk sizing.
