# M0001 Live Past-Only Event Bridge Fix

## Problems

1. Strategy Tester could show nodes from future candles if the bridge exported a
   count-based historical window rather than a time-bounded window.
2. MQL repeatedly deleted and redrew objects on every timer, causing flicker and
   overload.
3. Python could hit `PermissionError [WinError 32]` while refreshing the MQL CSV
   adapter while MT5 was reading it.

## Fixes

- MQL exports candles using a time-bounded `CopyRates(start_time, end_time)` call.
- `end_time` is the last closed bar when `InpBridgeClosedBarsOnly=true`.
- MQL redraws only when Python publishes a new `request_id` in the status file.
- MQL file handles use share flags.
- Python writes the visual adapter through a temp file and retries on Windows file locks.

## Important inputs

```text
InpBridgeClosedBarsOnly = true
InpBridgeOnEveryTick = false
InpRedrawOnlyOnNewPythonResult = true
InpBridgeTimerConfigPulse = false
```

This is the closest live-safe visual mode: only information available up to the
current simulated closed candle is exported to Python.
