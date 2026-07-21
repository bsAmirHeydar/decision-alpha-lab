# EXP0017 Phase 06 Hotfix005 — Historical Visual Backfill Patch

This patch upgrades Phase 06 so visual divergence drawings are not limited to events occurring after the EA is attached.

## Install

```powershell
Expand-Archive -Force ".\decision-alpha-lab-exp0017-phase06-hotfix005-historical-visual-backfill-patch.zip" ".\"
Remove-Item ".\decision-alpha-lab-exp0017-phase06-hotfix005-historical-visual-backfill-patch.zip"
```

## Compile Target

```text
mql5/Experts/IntermarketDivergenceExecution/EXP0017_CG_Visual_Ledger_Anatomy.mq5
```

## Main New Inputs

- `InpEnableHistoricalVisualBackfill = true`
- `InpHistoricalBackfillLookbackTradingDays = 2`
- `InpHistoricalBackfillMaxClosedCandles = 600`
- `InpHistoricalBackfillWriteLedger = false`
- `InpHistoricalBackfillPrintSummary = true`
- `InpKeepFirstVisualForSameSignalId = true`

## Design Intent

The EA scans historical closed candles from oldest to newest, rebuilds the same anatomy stack at each closed-candle observation point, and draws prior confirmed or invalidated states on both input-symbol charts.

## Non-Goals

No trade execution, risk, target, outcome study, ranking, AI, or strategy mutation is added.
