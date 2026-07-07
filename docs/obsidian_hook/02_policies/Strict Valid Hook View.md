# Strict Valid Hook View

## Rule

When `InpHookPhase02ShowOnlyValidHooks = true`, the chart must show only valid Hook families.

Valid families:

- Hook After Opposing F3
- Hook After Hook

## Production owner

Only Phase 02 is allowed to own valid Hook production drawing.

Disabled in strict valid-only mode:

- core/raw Hook renderer
- Phase 01 raw nodes
- Phase 03-06 diagnostic overlays
- stale Hook objects from old profiles

## Parent companion rule

In Hook-after-Hook, the second Hook is valid. The first Hook is shown only because it is the required parent companion.
