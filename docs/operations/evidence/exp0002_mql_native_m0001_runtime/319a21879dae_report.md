# EXP0002 — MQL-native M0001 Runtime

## Objective

Move M0001 from a Python/MQL bridge into a pure MQL5 runtime while preserving the lab research workflow.

## Hypothesis

A native MQL5 implementation will produce faster, clearer, and more live-safe visual validation than an external Python bridge because the detector, event engine, tester timeline, and chart objects live in the same runtime.

## Validation Target

- L-rule nodes appear only after `L` right-side candles exist.
- Markers point to the true pivot candle.
- Event construction starts only from `active_from_index`.
- No future candles are available to the engine.
- Visual redraw is synchronous with MT5 tester time.
