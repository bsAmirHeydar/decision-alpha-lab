# FlagCounting vNext MQL5 Module

This module is a clean implementation target for the v3 flag-counting specification. It intentionally does not depend on the older M0007/M0008 or old unified scanner code.

## Current implementation scope

- Multi-scale swing-node streams.
- Parallel F-counting sequences.
- F1 root body detection.
- F2 child detection from parent F1 internal 2.
- F3 child detection from parent F2 internal 2.
- F1 confirmation requires internal 1 and internal 2 before own Leg2 rebreak.
- F1 invalidation is own Waist break.
- F2 confirmation is own Leg2 extension/rebreak before Origin invalidation.
- F2 invalidation is own Origin break.
- F2 supports waist-break branch: `1 = Waist`, `2 = waist-breaking node`.
- F2 must be at least parent F1 size by default.
- F3 is terminal once its two-leg body is complete.
- Body-only renderer: Origin to Leg1 straight line; Leg1 to Waist to Leg2 curved body; tiny level and 1/2 labels.

## Files

- `FCN_Types.mqh` — enums, event model, nodes, config and string helpers.
- `FCN_NodeEngine.mqh` — swing-node detection and alternating-node compression.
- `FCN_Detector.mqh` — F1/F2/F3 multi-scale sequence detector.
- `FCN_Renderer.mqh` — chart rendering for accepted events.
- `FlagCountingVNextExperiment.mq5` — visual experiment expert.

## Expert

Compile:

`mql5/Experts/FlagCounting/FlagCountingVNextExperiment.mq5`

Recommended first-run inputs:

- `InpDrawOnlyConfirmed = false`
- `InpUseMultiScale = true`
- `InpSwingL1 = 2`
- `InpSwingL2 = 3`
- `InpSwingL3 = 5`
- `InpSwingL4 = 8`
- `InpSwingL5 = 13`
- `InpSwingL6 = 21`
- `InpMaxEventsToDraw = 350`
- `InpVerboseAuditLogs = false`

## Audit

The expert prints `FCN_SUMMARY` on every run. Enable `InpVerboseAuditLogs` to print each `FC_EVENT` with scale, sequence, level, direction, status, body points, internal labels, size and reason.

## Known next layer

ND/Hook partitioning is still the next explicit engine layer. This version keeps F detection and sequence registry independent so ND can be attached as a market partition layer instead of being mixed into renderer logic.
