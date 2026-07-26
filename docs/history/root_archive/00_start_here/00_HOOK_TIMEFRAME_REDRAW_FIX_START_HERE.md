# Hook Timeframe Redraw Fix — Start Here

This patch fixes a runtime redraw lifecycle issue in the central FlagCounting Phoenix expert.

Observed symptom:

```text
After switching chart timeframes several times, Hook drawings may stop updating.
```

Root cause:

```text
The new-bar redraw throttle could commit the current bar time before a full run successfully completed.
```

If the first run after a timeframe change failed because the new timeframe history was not ready, the expert could skip retries inside the same candle.

Fix:

```text
Only successful runs commit last-rendered bar time.
Failed runs keep force-redraw/retry state alive.
The timer retries failed runs without waiting for a new candle.
```

Read:

```text
docs/nds_hook_architecture/45_phase33_timeframe_change_redraw_state_guard.md
```

Obsidian:

```text
docs/obsidian_hook/03_architecture/Phase_33_Timeframe_Change_Redraw_State_Guard.md
```
