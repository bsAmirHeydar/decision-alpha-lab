# 01 — Scope and Inputs

## Objective

Add Hook visualization and diagnostics to the same central expert that already displays Rally / F-counting.

The existing Rally behavior must remain untouched.

## Display Family Input

Recommended input enum:

```text
NDS_DISPLAY_RALLY_ONLY
NDS_DISPLAY_HOOK_ONLY
NDS_DISPLAY_RALLY_AND_HOOK
```

## Suggested User Inputs

```text
InpNDSDisplayFamily
InpHookShowPositive
InpHookShowNegative
InpHookShowXSequence
InpHookShowYSequence
InpHookShowClosure
InpHookShowHookType
InpHookShowND
InpHookShowOppositeExtreme
InpHookShowDeathBoundary
InpHookShowDebugLabels
InpHookMaxSequencesToDraw
InpHookMaxBarsToScan
InpHookMinL
InpHookMaxNodesPerSequence
```

## Default Behavior

The default should preserve existing behavior:

```text
InpNDSDisplayFamily = NDS_DISPLAY_RALLY_ONLY
```

This ensures that adding Hook code does not change the existing F-counting / Rally display.

## Display Modes

### Rally Only

Use the current F-counting logic exactly as it is.

No Hook code should change the Rally calculation path.

### Hook Only

Draw CycleHook / Hook objects and diagnostics.

Do not draw Rally/F-counting labels unless they are explicitly needed for Hook debug.

### Rally and Hook

Draw both layers.

Object names must be namespaced to avoid overwriting existing Rally chart objects.

## Object Namespace

Suggested object prefixes:

```text
NDS_RALLY_
NDS_HOOK_
NDS_HOOK_X_
NDS_HOOK_Y_
NDS_HOOK_TYPE_
NDS_HOOK_ND_
NDS_HOOK_DEATH_
```

## First Implementation Goal

The first implementation should be visual and audit-only.

No trading behavior.
