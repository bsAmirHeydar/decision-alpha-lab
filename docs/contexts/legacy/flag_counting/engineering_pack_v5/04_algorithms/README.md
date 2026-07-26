# 04 Algorithms README

This package translates the contract into implementation modules.

## Files

- `MODULE_ARCHITECTURE.md`
- `NODE_ENGINE_ALGORITHM.md`
- `HOOK_BRANCH_ENGINE_ALGORITHM.md`
- `FLAG_BODY_ENGINE_ALGORITHM.md`
- `SEQUENCE_ENGINE_ALGORITHM.md`
- `F1_F2_F3_ALGORITHMS.md`
- `DEDUP_AUDIT_ALGORITHM.md`
- `PSEUDOCODE_REFERENCE.md`

## Implementation Strategy

Do not patch one giant detector function.

Implement modules in this order:

1. Node adapter.
2. Flag body builder.
3. Post-flag context tracker.
4. Hook branch engine.
5. F1 state machine.
6. F2 state machine with backfill.
7. F3 state machine with extension/lock.
8. Dedup/identity/audit.
9. Renderer.

## Rule

If a module needs renderer information to decide logic, the architecture is wrong.
