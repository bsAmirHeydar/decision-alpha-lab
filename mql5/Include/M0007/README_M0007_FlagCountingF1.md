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

## Visual schematic overlay

The renderer now draws a clean F1 schematic on top of each detected event:

- one straight leg into `H1/L1`,
- one curve-like multi-segment shape from `H1/L1` through the waist region into `H2/L2`,
- one bold `F1` label near the second main extreme.

This schematic is intentionally visual and conceptual. It does not replace the mechanical F1 count. The detector still uses the full topology:

- bullish: `H1 -> W -> H2 -> N1 -> R12 -> N2`
- bearish: `L1 -> W -> L2 -> N1 -> R12 -> N2`

The schematic only makes the F1 shape readable on chart, matching the hand-drawn flag-counting concept.


## Current minimal overlay contract

The default chart output is intentionally minimal:

- the F1 path itself,
- one neutral `F1` label,
- `1` at the end of leg 1,
- `2` at the end of leg 2.

All other textual chart labels and audit guide lines are suppressed in the default renderer.
The numeric labels `1` and `2` appear only after the full F1 structure is completed and confirmed.
