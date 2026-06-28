# LEVEL 13 — EXEC001 STC SMT Visualization / Audit Drawing

This patch adds chart-side visualization for the EXEC001 STC SMT Cycles paper execution stack.

It draws audit objects only. It does not place orders, modify signals, or change paper outcomes.

## Main file

`mql5/Experts/IntermarketDivergenceExecution/IMDEXEC001_STC_SMT_Cycles.mq5`

## New module

`mql5/Include/IntermarketDivergenceExecution/STC/DAL_STC_Drawing.mqh`

## New output

`dal/stc/EXEC001_STC_SMT_Cycles/stc_level13_drawing_audit.csv`

## New inputs

- `InpWriteDrawingAudit`
- `InpDrawingRefreshSeconds`
- `InpDrawingHistoryChecks`
- `InpDrawingHistoryWLevels`
- `InpDrawingClearOnDeinit`
- `InpDrawingObjectPrefix`

## Objects

The renderer draws:

- STC M zones.
- W boundaries.
- current check candle.
- 15:30 NY hard close.
- W high/low levels for the active chart symbol when the chart is Symbol1 or Symbol2.
- paper entry guide text.
- SL/TP guide lines.
- W4 partial markers.
- ambiguity markers.
- dashboard labels.

## Safety

Level 13 is still no-order. Auto trade remains disabled.
