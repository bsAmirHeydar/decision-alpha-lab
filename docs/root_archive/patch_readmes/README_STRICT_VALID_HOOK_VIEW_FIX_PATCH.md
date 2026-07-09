# Strict Valid Hook View Fix Patch

## Problem

`InpHookPhase02ShowOnlyValidHooks = true` could still appear to show all Hooks because the chart was not controlled by Phase 02 alone. Other render paths could still leave Hook objects visible:

1. the core/raw `FP_DrawAllWithReport(...)` Hook renderer, using `InpDrawHooks`
2. Phase 01 raw node drawing
3. Phase 03-06 diagnostic Hook overlays
4. stale objects from previous profiles or timeframe changes

There was also a semantic issue: the old `Hook After Opposing F3` rule treated any Hook after any previous opposing F3 as valid, so one historical F3 could accidentally validate too many later Hooks.

## Fix

Strict valid-only mode now means:

```text
Only Phase 02 valid Hook families may draw production Hook objects.
```

When `InpHookPhase02ShowOnlyValidHooks = true`, the expert suppresses raw/core Hook drawing and Phase 01/03/04/05/06 visual layers, deletes stale Hook objects, then lets Phase 02 redraw only valid families.

## Valid families

```text
1. Hook After Opposing F3
2. Hook After Hook
```

For `Hook After Hook`, the second Hook is the valid Hook. The first Hook is shown only as the immediate parent companion.

For `Hook After Opposing F3`, only the first valid Hook after each completed/locked opposing F3 is promoted. An old F3 no longer validates every later Hook.
