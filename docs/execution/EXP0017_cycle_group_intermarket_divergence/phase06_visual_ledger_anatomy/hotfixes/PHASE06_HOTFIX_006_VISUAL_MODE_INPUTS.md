# EXP0017 Phase 06 Hotfix006 — Minimal Line-Only Visual Mode

## New / Changed Inputs

```mql5
input ECGVVisualMode InpVisualMode = CGV_VISUAL_MODE_MINIMAL_LINES_ONLY;
input bool InpSuppressAllTextObjects = true;
input bool InpDeleteTextObjectsWhenSuppressed = true;
input bool InpForceAllVisualObjectsOn = false;
input bool InpDrawTextLabel = false;
input bool InpDrawInvalidatedDoubleHunts = false;
input int  InpHistoricalBackfillMaxClosedCandles = 350;
input int  InpMaxHistoricalVisualDraws = 250;
```

## Visual Modes

### `CGV_VISUAL_MODE_MINIMAL_LINES_ONLY`
Only origin-to-destination divergence legs are drawn. This is the default.

### `CGV_VISUAL_MODE_LINES_AND_MARKERS`
Draws origin-to-destination legs plus origin and destination markers. Text remains off.

### `CGV_VISUAL_MODE_STRUCTURAL_LINES`
Draws origin-to-destination legs plus vertical timing lines. Text remains off.

### `CGV_VISUAL_MODE_FULL_AUDIT`
Draws the full audit package: markers, verticals, reference guides, current-extreme guides, clean guides, labels, and invalidated states. This mode is intentionally not the default because it can flood the chart.

## Recommended Current Settings

For your current chart-review stage:

```text
InpVisualMode = CGV_VISUAL_MODE_MINIMAL_LINES_ONLY
InpSuppressAllTextObjects = true
InpDeleteTextObjectsWhenSuppressed = true
InpShowChartPanel = false
InpPrintSummaryOnNewClosedCandle = false
InpDrawInvalidatedDoubleHunts = false
InpEnableHistoricalVisualBackfill = true
InpDrawOnBothInputSymbolCharts = true
```
