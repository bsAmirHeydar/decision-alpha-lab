# M0001 Reliable Excel Report Writing

## Fix

Excel report writing now creates missing folders before `FileOpen` and prints
success/failure messages to the Experts log.

## Inputs

```text
InpWriteExcelReport = true
InpExcelReportUseFullHistorySnapshot = true
```

`InpExcelReportUseFullHistorySnapshot=true` writes a report-only CopyRates snapshot
for full-history validation. It does not affect the live-stream engine or trading
logic.

This is useful when:

```text
InpUseLiveBarStream = true
InpWarmupHistoricalBars = 0
```

because the runtime stream can be empty at init while a full report is still
needed for research validation.

## Output

```text
DecisionAlphaLab\M0001\<symbol>_M0001_full_audit_report.xls
```

In Strategy Tester, MetaTrader writes files under the tester agent sandbox, not
always the normal terminal `MQL5\Files` folder.

## Version

`M0001_LiveVisualLab.mq5` version: `1.34`.
