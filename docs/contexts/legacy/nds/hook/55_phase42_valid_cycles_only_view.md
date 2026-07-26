# Phase 42 — Valid Cycles Only View

## Problem

A valid-only Hook view must not become a noisy structural-Hook view. The previous fallback policy allowed the renderer to fall back to structural Hook candidates when no valid Hook family was selected. That helped debugging, but it made production mode ambiguous: the user could enable valid-only and still see many non-valid Hook labels.

## Doctrine

`ShowOnlyValidHooks` means:

```text
valid cycles only
valid sequence labels only
valid node labels only
```

The renderer must show only origin groups selected by the Hook validity layer.

## Valid production families

The valid Hook-cycle families are:

1. **Immediate Hook After Opposing F3**
2. **Hook After Hook**

For Hook-after-Hook, Hook-2 is the valid Hook. Hook-1 may be shown only as the parent companion required for structural readability.

## Selection contract

The renderer is allowed to draw:

- the arc/envelope of selected valid Hook origin groups;
- the X-node labels of selected valid Hook origin groups;
- the sequence labels of selected valid Hook origin groups;
- the parent companion origin group when selected through a Hook-after-Hook child.

The renderer is not allowed to draw:

- unqualified standalone Hook candidates;
- Phase 01 raw nodes;
- Phase 03-06 diagnostic overlays;
- stale Hook objects from previous runs;
- structural fallback hooks in production mode.

## Fallback policy

Structural fallback is debug-only:

```text
InpHookPhase02ValidOnlyFallbackToStructural = false
```

If this input is manually set to `true`, the chart is no longer strict production valid-only. It is a debug view used to diagnose why the valid-family selector returned no candidates.

## Expected behavior

If no valid Hook family exists in the current window, strict valid-only mode draws nothing. This is correct. A blind chart in strict valid-only mode means no valid Hook was found, not that the renderer should invent structural fallbacks.
