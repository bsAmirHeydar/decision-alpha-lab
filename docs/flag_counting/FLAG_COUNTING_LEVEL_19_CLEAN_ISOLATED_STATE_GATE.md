# Flag Counting Level 19 — Clean Isolated State Gate

## Purpose

This is a clean rebuild of Level 19 after rolling the project back to the pre-Level-19 state.

The new Level 19 is deliberately small, read-only, and isolated.

## Hard no-touch contract

Level 19 does **not** modify:

```text
FP_Renderer.mqh
FP_RenderRules.mqh
FP_RenderTypes.mqh
Node Engine
Hook / ND Engine
Flag Body
Internal Count
F1 / F2 / F3
Ownership / Canonicalization
Renderer curves
Renderer lines
Renderer labels
F / Hook / Node chart objects
RTV / zone chart objects
license logic
execution logic
```

## What it does

Level 19 reads already-produced engine/report outputs and creates one diagnostic snapshot:

```text
bars
scale_count
timebase status
node counts
hook counts
event counts
visible/hidden event counts
F1/F2/F3 counts
ND count
render report status
export report status
validation report status
latest visible event summary
latest visible hook summary
```

## Output CSV

```text
MQL5/Files/FlagCountingPhoenix/latest_state_gate_level19.csv
```

## Panel

The panel is **disabled by default**:

```text
InpLevel19StateGatePanelEnabled = false
```

If enabled manually, it uses a dedicated object prefix:

```text
DAL_L19_STATE_GATE_PANEL_
```

It does not use the renderer prefix:

```text
DAL_FCP_
```

So it does not clean, delete, move, or overwrite renderer objects.

## Inputs

```text
InpLevel19StateGateEnabled
InpLevel19StateGateExportCsv
InpLevel19StateGatePanelEnabled
InpLevel19StateGatePanelCleanOnInit
InpLevel19StateGatePanelCleanOnDeinit
InpLevel19StateGatePrintSummary
InpLevel19StateGateFolder
InpLevel19StateGateObjectPrefix
InpLevel19StateGatePanelCorner
InpLevel19StateGatePanelX
InpLevel19StateGatePanelY
InpLevel19StateGatePanelWidth
InpLevel19StateGatePanelFontSize
```

## Integration point

The EA runs Level 19 after Level 18/static QA and before the final summary print.

The layer only reads:

```text
rates
scales
events
hooks
detect result
timebase report
export report
render report
validation report
```

It does not write back into any of them.

## Why this version is safer

Previous Level 19 attempts grew into execution-like paper layers and responsive panel code. This clean rebuild avoids that path.

This version is a diagnostic state gate only.

Future phases must extend this layer without touching renderer files or existing structural engines.
