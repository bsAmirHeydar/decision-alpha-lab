# M0001 Live Visual Lab for MT5

This is the live/testing version of the MQL visual lab.

It does **not** wait for Python-exported CSV files. It computes the M0001 logic directly from the bars currently available to the MT5 chart or Strategy Tester.

```text
MT5/Strategy Tester chart bars
    ↓
MQL live L-rule node detector
    ↓
MQL live M0001 RTV engine
    ↓
nodes / territories / events / RTV labels / hunt markers on chart
```

## Main expert

```text
mql5/Experts/DecisionAlphaLab/M0001_LiveVisualLab.mq5
```

## Include modules

```text
mql5/Include/DecisionAlphaLab/M0001_Types.mqh
mql5/Include/DecisionAlphaLab/M0001_Math.mqh
mql5/Include/DecisionAlphaLab/M0001_LRuleNodes.mqh
mql5/Include/DecisionAlphaLab/M0001_RTVEngine.mqh
mql5/Include/DecisionAlphaLab/M0001_Drawer.mqh
```

## How it behaves

The expert is designed to feel like a live test:

1. It reads only bars currently available in MT5.
2. It confirms L-rule nodes only after `L` future bars are available.
3. It starts M0001 event tracking only after node confirmation.
4. It builds territory from live expansion.
5. It starts events by wick intersection with territory.
6. It computes inside/before log-range volatility.
7. It prints RTV labels directly on the chart.
8. It marks the exact first hunt candle.
9. It can show the currently open event as `LIVE RTV`.

## Important inputs

```text
InpL
InpZoneRatio
InpExitGap
InpConsumeOnTouch
InpLookbackBars
InpUseClosedBarsOnly
InpShowNodes
InpShowTerritories
InpShowEvents
InpShowRtvLabels
InpShowHunts
InpShowOpenEvent
InpMaxNodesToDraw
InpMaxEventsToDraw
```

## Live-safe mode

For clean testing keep:

```text
InpUseClosedBarsOnly = true
InpUpdateOnEveryTick = false
```

This means the expert updates on new closed bars, not every tick of a forming bar. This avoids repaint-like behavior.

For more active visual feedback:

```text
InpUseClosedBarsOnly = false
InpUpdateOnEveryTick = true
```

That mode is more visual but can change while the current bar is forming.

## Copy to terminal

From the project root, when the project is inside `MQL5\Shared Projects\decision-alpha-lab`:

```powershell
$mql5Root = Split-Path (Split-Path (Get-Location))

New-Item -ItemType Directory -Force "$mql5Root\Experts\DecisionAlphaLab"
New-Item -ItemType Directory -Force "$mql5Root\Include\DecisionAlphaLab"

Copy-Item .\mql5\Experts\DecisionAlphaLab\M0001_LiveVisualLab.mq5 "$mql5Root\Experts\DecisionAlphaLab\" -Force
Copy-Item .\mql5\Include\DecisionAlphaLab\M0001_*.mqh "$mql5Root\Include\DecisionAlphaLab\" -Force
```

Then compile:

```text
Experts/DecisionAlphaLab/M0001_LiveVisualLab.mq5
```

Attach it to a chart or run it in Strategy Tester visual mode.

## Difference from CSV Visual Lab

```text
M0001_VisualLab.mq5
  Reads Python CSV artifacts and draws them.

M0001_LiveVisualLab.mq5
  Computes M0001 directly inside MT5, bar by bar, like live testing.
```

Keep both. The CSV visualizer is for audit/reproducibility. The live visualizer is for fast market-native inspection.


## Compile compatibility note

The include files use plain MQL5 syntax and intentionally avoid C/C++ directives such as `#pragma once`.
Compile the expert from MetaEditor after copying both the `Experts/DecisionAlphaLab` and `Include/DecisionAlphaLab` folders.

## Debug Packages

The live visual lab now supports 12 audit packages controlled by `InpViewPreset`.

Read:

```text
docs/mql_live_visual_lab_debug_packages.md
```
