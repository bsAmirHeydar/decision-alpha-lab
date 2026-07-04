# NDS Hook Official Schematic Visual Cleanup

## Why

The raw multi-phase Hook overlay was technically correct for debugging, but visually too noisy for the official structural reading. The main pollution came from:

- projecting lifecycle thresholds all the way to `TimeCurrent()`
- stacking full debug labels from Phase 05 and Phase 06
- leaving the Phase 07 view profile on permissive modes such as `KEEP_INPUTS`
- drawing too many structures at once

## What changed

### 1) New official visual profile

A new Phase 07 view profile was added:

- `FP_HOOK_P07_VIEW_OFFICIAL_SCHEMATIC`

This profile draws a clean Hook schematic:

- Phase 02: origin + X nodes + X lines
- Phase 03: Y extremes + Y lines
- Phase 04: ND / death / X-close markers only
- Phase 05: compact Hook type anchor + compact type label
- Phase 06: compact quality anchor + compact quality label

It intentionally hides:

- Phase 02 labels
- Phase 03 labels and X-reference clutter
- Phase 04 threshold bands and lifecycle debug labels
- Phase 05 comparison lines and debug logic labels
- Phase 06 projection lines and debug logic labels

### 2) New clean defaults

The default Hook profile is now official schematic, with cleanup and tighter budgets:

- `InpHookPhase07ViewProfile = FP_HOOK_P07_VIEW_OFFICIAL_SCHEMATIC`
- `InpHookPhase07ShowLabels = false`
- `InpHookPhase07CleanBeforeApply = true`
- `InpHookPhase07MaxNodesToDraw = 120`
- `InpHookPhase07MaxSequencesToDraw = 12`

### 3) Threshold-line fix

Phase 04 threshold lines now stop at the latest relevant Hook evidence time instead of extending to `TimeCurrent()`. This removes the dense right-edge pile of `ORIGIN/DEATH`, `ND TH`, and `X CLOSE 50%`.

### 4) Compact labels

- Phase 05 labels are shortened to a compact Hook type form such as `HK A+ L5 #2911 0.87`
- Phase 06 labels are shortened to a compact quality form such as `Q XY+ E 0.87`

## Recommended usage

- For pure Hook reading: `InpNDSHookDisplayFamily = FP_NDS_HOOK_DISPLAY_HOOK_ONLY`
- For mixed review: `InpNDSHookDisplayFamily = FP_NDS_HOOK_DISPLAY_RALLY_AND_HOOK`
- For deep debugging only: switch Phase 07 to `FULL_DEBUG` or `KEEP_INPUTS`
