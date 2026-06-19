# VAL_M0001_MQL_NATIVE

## Scope

Visual and journal validation for the native MQL5 implementation of M0001.

## Checklist

- [ ] L-rule high node confirms exactly at `i + L`.
- [ ] L-rule low node confirms exactly at `i + L`.
- [ ] Marker is drawn on pivot candle.
- [ ] Active-from line, when enabled, is drawn at `i + L`.
- [ ] Event scan does not start before active-from.
- [ ] RTV fields match the event window and before-window lengths.
- [ ] Strategy Tester visual state does not require Python.
