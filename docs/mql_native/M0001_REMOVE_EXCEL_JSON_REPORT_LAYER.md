# M0001 Remove Excel/JSON Report Layer

## Decision

Excel/JSON report generation has been removed from the native MQL layer.

MQL is now kept focused on:

```text
visual validation
node state machine
touch/hunt/consume behavior on chart
```

The following report-related items were removed:

```text
InpWriteExcelReport
InpWriteJsonReport
InpExcelReportUseFullHistorySnapshot
InpJsonReportUseFullHistorySnapshot
InpWriteReportProbe
Excel/JSON writer helpers
report sync script
report folder artifacts
```

CSV validation journal support remains as the lightweight legacy logger, but the
active validation path is visual-first.

## Version

`M0001_LiveVisualLab.mq5` version: `1.39`.
