# PHASE06 HOTFIX 004 — Drawing Visibility Checklist

## Compile Check

- `EXP0017_CG_Visual_Ledger_Anatomy.mq5` compiles.
- No missing include errors.
- No object-property compile errors.

## Input Check

These must be true for a full visual audit:

```text
InpEnableDrawing = true
InpForceAllVisualObjectsOn = true
InpDrawOnBothInputSymbolCharts = true
InpOpenMissingInputSymbolCharts = true
InpShowChartPanel = false
InpPrintSummaryOnNewClosedCandle = false
```

## Chart Check

- Symbol A chart is open.
- Symbol B chart is open.
- Both charts have enough M1 history.
- Object list contains `EXP0017_P06_` objects.

## Object Check

For at least one signal, expect:

```text
origin_to_destination_*_shadow
origin_to_destination_*
origin_marker_*
destination_marker_*
origin_vertical_*
destination_vertical_*
confirmation_close_vertical_*
reference_guide_*
current_extreme_guide_*
visual_label_*
```

## If Only Text Still Appears

Check these possibilities:

1. Old EA input settings are loaded from a saved `.set` file.
2. `InpForceAllVisualObjectsOn` is false.
3. Object List is filtered and hiding non-text objects.
4. Drawing objects are behind another indicator object layer.
5. M1 history is incomplete and extreme timestamps fall back to compressed times.
6. The current state is not confirmed/invalidated yet and only older labels remain.

The fastest reset is:

```text
Remove EA from both charts.
Delete all EXP0017_P06_* objects from Object List.
Attach the EA again.
Keep InpForceAllVisualObjectsOn = true.
```
