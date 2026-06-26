# M0007 — F1 Flag Counting MQL5 Module

This folder contains the reusable MQL5 include files for the M0007 adaptive F1 counter.

## Folder rule

The project root already identifies the lab, so the MQL folders only use the M-series module name.

Correct locations:

```text
mql5/Experts/M0007/
mql5/Include/M0007/
```

## Files

- `DAL_M0007F1Types.mqh`
- `DAL_M0007F1NodeDetector.mqh`
- `DAL_M0007F1Detector.mqh`
- `DAL_M0007F1Renderer.mqh`

## Include contract

The Expert Advisor imports the module like this:

```mql5
#include <M0007/DAL_M0007F1Types.mqh>
#include <M0007/DAL_M0007F1Detector.mqh>
#include <M0007/DAL_M0007F1Renderer.mqh>
```

## Scope

M0007 is visual/audit-only. It counts and draws F1 structures. It does not place orders.

## v1.04 clean schematic-only renderer

The renderer now draws only the requested clean F1 grammar on the chart:

```text
Start -> straight Leg 1 -> end of Leg 1
end of Leg 1 -> smooth curved correction through W -> end of Leg 2
```

Removed from the default chart output:

```text
Previous High / Previous Low horizontal guide lines
protected waist horizontal line
R12 horizontal line
H2/L2 confirmation horizontal line
internal trigger vertical line
confirmation vertical line
invalidation vertical line
compact H1/W/H2/N1/R12/N2 audit labels
status panel text
```

The visual layer is intentionally clean and conceptual. It does not change the detector state. The detector still uses the full topology:

```text
bullish: H1 -> W -> H2 -> N1 -> R12 -> N2
bearish: L1 -> W -> L2 -> N1 -> R12 -> N2
```

## Display inputs

`M0007_FlagCountingF1.mq5` exposes these visual inputs:

```text
InpShowTextLabels  = true   // Start, Leg 1, Correction, Pullback / Correction, Leg 2
InpShowBadge       = true   // BULLISH F1 / BEARISH F1
InpShowStatusPanel = false  // keep false for clean chart output
```

`InpRedrawOnNewBar` remains enabled by default so the visual audit updates during replay/testing without running the detector on every tick. It redraws only when a new bar appears.
