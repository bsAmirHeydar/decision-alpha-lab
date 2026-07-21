# Hook Validity No-Draw Fix Patch

## Purpose

The previous practical valid-Hook filter could legitimately select zero hooks when the valid-family rules were too strict for the current chart window. Since the strict valid-only guard also disabled raw/core Hook renderers, the result was a blank Hook view.

This patch keeps the professional validity doctrine but adds explicit controls to prevent a blind chart:

- `InpHookPhase02ValidOnlyFallbackToStructural`
- `InpHookPhase02ValidF3RequireOppositeDirection`

## Default practical view

```text
InpHookPhase02ShowOnlyValidHooks = true
InpHookPhase02ValidOnlyFallbackToStructural = true
InpHookPhase02ValidF3RequireOppositeDirection = false
InpHookPhase02ValidOnlyRequireNearDeath = false
InpHookPhase02ValidF3RequireSameScale = false
```

## Strict research view

```text
InpHookPhase02ShowOnlyValidHooks = true
InpHookPhase02ValidOnlyFallbackToStructural = false
InpHookPhase02ValidF3RequireOppositeDirection = true
InpHookPhase02ValidOnlyRequireNearDeath = false
InpHookPhase02ValidF3RequireSameScale = false
```
