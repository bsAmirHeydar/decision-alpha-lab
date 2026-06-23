# M0007 — F1 Flag Counting MQL5 Module

This folder contains the reusable MQL5 include files for the M0007 adaptive F1 counter.

## Folder rule

The project root already identifies the lab, so the MQL folders only use the M-series module name.

Correct locations:

```text
mql5/Experts/M0007_FlagCountingF1/
mql5/Include/M0007_FlagCountingF1/
```

## Files

- `DAL_M0007_F1_Types.mqh`
- `DAL_M0007_F1_NodeDetector.mqh`
- `DAL_M0007_F1_Detector.mqh`
- `DAL_M0007_F1_Renderer.mqh`

## Include contract

The Expert Advisor imports the module like this:

```mql5
#include <M0007_FlagCountingF1/DAL_M0007_F1_Types.mqh>
#include <M0007_FlagCountingF1/DAL_M0007_F1_Detector.mqh>
#include <M0007_FlagCountingF1/DAL_M0007_F1_Renderer.mqh>
```

## Scope

M0007 is visual/audit-only. It counts and draws F1 structures. It does not place orders.
