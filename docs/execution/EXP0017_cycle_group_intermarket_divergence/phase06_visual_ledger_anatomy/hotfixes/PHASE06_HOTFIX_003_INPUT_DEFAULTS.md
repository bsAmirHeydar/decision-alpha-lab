# Phase 06 Hotfix003 — Input Defaults

## Main requested state

```text
all drawings = ON
chart comments = OFF
both input-symbol charts = ON
```

## Important visual defaults

```text
InpEnableDrawing = true
InpDrawOnBothInputSymbolCharts = true
InpOpenMissingInputSymbolCharts = true
InpShowChartPanel = false
InpPrintSummaryOnNewClosedCandle = false
```

## Drawing defaults

```text
InpDrawConfirmedTradeable = true
InpDrawInvalidatedDoubleHunts = true
InpDrawReferenceCycleAnchor = true
InpDrawConfirmationMarker = true
InpDrawTextLabel = true
InpDrawDivergenceOriginDestinationLine = true
InpDrawOriginMarker = true
InpDrawDestinationMarker = true
InpDrawOriginVertical = true
InpDrawDestinationVertical = true
InpDrawHunterReferenceGuide = true
InpDrawCleanReferenceGuide = true
InpDrawCleanStopReferenceGuide = true
InpDrawHunterCurrentExtremeGuide = true
InpDrawCleanComparisonLine = true
```

## Default origin and destination mode

```text
origin time = exact reference extreme from M1
origin price = symbol-local reference extreme

destination time = exact current-cycle extreme from M1
destination price = symbol-local current-cycle extreme
```

## Chart opening behavior

If one of the two input-symbol charts is not open, the EA may open it:

```text
InpOpenMissingInputSymbolCharts = true
```

The timeframe used for newly opened charts is controlled by:

```text
InpVisualChartTimeframe = PERIOD_CURRENT
```

## Ledger state

Ledger remains on:

```text
InpEnableLedger = true
```

The ledger is still not performance statistics. It is only raw signal audit memory.
