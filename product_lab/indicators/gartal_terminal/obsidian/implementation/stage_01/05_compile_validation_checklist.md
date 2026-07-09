# Stage 01 — Compile Validation Checklist

## Pre-compile file placement

Copy or keep these files under MetaTrader's indicator source tree:

```text
MQL5/Indicators/GartalTerminal/GartalTerminal.mq5
MQL5/Indicators/GartalTerminal/include/*.mqh
```

If compiling from the repo directly through an IDE mapping, preserve the relative include structure.

## Compile checks

- [ ] `GartalTerminal.mq5` opens in MetaEditor.
- [ ] All include files resolve from `include/`.
- [ ] No undefined identifiers.
- [ ] No string-normalization compile errors.
- [ ] No duplicate global variable names.
- [ ] No missing function signatures.
- [ ] Indicator compiles with zero fatal errors.

## Runtime checks on chart

- [ ] Indicator attaches to a chart.
- [ ] Dashboard shell appears.
- [ ] Source status shows `SAMPLE`.
- [ ] Broker GMT appears in the header.
- [ ] Sample events appear in event rows.
- [ ] Vertical lines appear at sample event times.
- [ ] Bottom timeline shell appears.
- [ ] Removing the indicator clears `GT_` objects if cleanup input is enabled.

## Known Stage 01 limitations

- Forex Factory parser is not implemented.
- Dashboard buttons are not active.
- The luxury UI is not final.
- Timeline projection is not screen-space mapped yet.
- Cache fallback exists but is not the main test path.
