# Phase 37 — Strict Valid Hook View Owner

The strict valid Hook view guard is applied after Hook view-profile overrides and release-profile overrides, so no later profile can accidentally turn raw Hook drawing back on.

Runtime effect:

```text
InpHookPhase02ShowOnlyValidHooks = true
→ suppress raw/core hook renderer
→ suppress Phase 01/03/04/05/06 visual layers
→ cleanup stale Hook prefixes
→ redraw Phase 02 valid families only
```

Opposing-F3 validity is bounded to the first Hook after the F3.
