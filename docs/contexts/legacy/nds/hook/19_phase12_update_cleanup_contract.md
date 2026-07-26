# NDS Hook Phase 12 — Update Cleanup Contract

## Purpose

When the expert updates, the previous Hook drawings must not remain on the chart. The chart must represent the current calculation pass only.

## Change

Phase 07 cleanup is now extended from P01..P07 to the full Hook overlay namespace P01..P10.

A common prefix cleanup was also added:

- `InpHookPhase07CleanCommonHookPrefix`
- `InpHookPhase07CommonHookObjectPrefix = "DAL_HOOK_"`

This deletes stale objects from older Hook phases or previous prefixes before the current pass redraws.

New cleanup toggles:

- `InpHookPhase07CleanP08Objects`
- `InpHookPhase07CleanP09Objects`
- `InpHookPhase07CleanP10Objects`

All are enabled by default.

Phase 07 now also stores the cleanup prefixes for:

- Phase 08 audit objects / future objects
- Phase 09 smoke-test panel objects
- Phase 10 freeze / contract objects

## Runtime behavior

On each update pass, before the Hook phases draw again:

1. Phase 07 deletes existing Hook objects by the common `DAL_HOOK_` prefix.
2. Phase 07 deletes P01..P10 objects by their specific prefixes.
3. The selected view profile is applied.
3. Phase 01..Phase 06 redraw the current Hook structures.
4. Audit/smoke/freeze phases run against the current pass.

This prevents stale labels, panels, and objects from previous calculations from being visually mixed with the new Hook state.

## Default

`InpHookPhase07CleanBeforeApply = true` remains the default in the official schematic view.

So the official view is now:

- clean before draw
- compact schematic profile
- capped structure count
- no old Hook overlays left behind
