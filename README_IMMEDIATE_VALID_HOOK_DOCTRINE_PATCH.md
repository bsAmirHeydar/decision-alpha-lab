# Immediate Valid Hook Doctrine Patch

This patch refines the Hook validity layer.

## Doctrine

A production-valid Hook is only one of two families:

- `IMMEDIATE_HOOK_AFTER_OPPOSING_F3`
- `HOOK_AFTER_HOOK`

The F3 rule is now strictly immediate: the first Hook after F3 owns the test. If that immediate Hook is opposite to F3, it becomes valid. If it is not opposite, the F3 validates no later Hook.

The Hook-after-Hook rule is exact node continuity:

```text
previous_hook.resolve_node_id == current_hook.origin_node_id
```

Direction is not an independent qualifier; the shared node owns the structural relationship.

## Scope

Hook Phase 02 validity annotation only. No F-counting, rally logic, execution, order sending, or risk sizing behavior is changed.
