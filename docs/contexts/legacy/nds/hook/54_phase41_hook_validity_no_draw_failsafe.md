# Phase 41 — Hook Validity No-Draw Failsafe

## Problem

The practical valid-Hook model can be over-filtered when several strict conditions are enabled at the same time:

- valid-only view enabled
- only immediate post-F3 Hook accepted
- opposite F3 direction required
- same-scale F3 matching required
- semantic near-death readiness required
- raw/core Hook renderers suppressed

This can produce a blind chart: Hook counting succeeds, but no visible Hook is selected.

## Doctrine

Hook validity is a production filter, not a counting filter.

The engine must always be able to count Hook structures. The renderer may restrict what is visible, but during active research it must not hide all structural information unless the user explicitly asks for strict research mode.

## Practical Inputs

```text
InpHookPhase02ShowOnlyValidHooks = true
InpHookPhase02ValidOnlyFallbackToStructural = true
InpHookPhase02ValidF3RequireOppositeDirection = false
InpHookPhase02ValidOnlyRequireNearDeath = false
InpHookPhase02ValidF3RequireSameScale = false
```

## Strict Inputs

```text
InpHookPhase02ShowOnlyValidHooks = true
InpHookPhase02ValidOnlyFallbackToStructural = false
InpHookPhase02ValidF3RequireOppositeDirection = true
InpHookPhase02ValidOnlyRequireNearDeath = false
InpHookPhase02ValidF3RequireSameScale = false
```

## Implementation

If valid-only selection returns zero sequences and `valid_only_fallback_to_structural=true`, the renderer selects recent structural Hook sequences using the base draw filter. This is a fail-safe visual mode. It does not promote the fallback sequences into valid Hook families.

F3 direction strictness is now configurable. When `valid_f3_require_opposite_direction=false`, the immediate Hook after a completed/locked F3 can qualify regardless of direction. This is useful while the exact semantic direction mapping between F3 and Hook is still being stabilized.

## Rule

Do not let the chart become blind during Hook validity research.
