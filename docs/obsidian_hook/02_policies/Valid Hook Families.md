# Valid Hook Families

Production-valid Hook families are restricted to:

1. Hook After Hook
2. Hook After Opposing F3

Hook After Hook requires exact node continuity:

```text
previous_hook.resolve_node_id == current_hook.origin_node_id
```

Hook After Opposing F3 requires an opposite completed/locked F3 before the Hook start.

`InpHookPhase02ShowOnlyValidHooks=true` hides unqualified Hook-like structures from the Phase 02 semantic view.
