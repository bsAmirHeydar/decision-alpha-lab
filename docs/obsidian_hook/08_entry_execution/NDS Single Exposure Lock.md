# NDS Single Exposure Lock

## Contract

```text
managed pending + managed position ≤ 1
```

The invariant is global for the Phase 52 magic number, not local to one chart.

## Enforcement

1. Count all pending orders and positions owned by the magic number.
2. Hold when one managed pending or position exists.
3. Acquire a terminal GlobalVariable compare-and-swap lock before submission.
4. Recount exposure while holding the lock.
5. Submit only if the second count is still zero.
6. Release the lock.

## Recovery

- position present → delete stray managed pending;
- duplicate pending → keep oldest and delete extras;
- multiple managed positions → fail closed for manual reconciliation;
- foreign position on the current symbol → block to avoid netting contamination.

## Ownership

Magic number is authoritative. Broker comments are descriptive metadata only.

## Related

- [[NDS Hook Limit Entry Contract]]
- [[NDS Hook Trade State Machine]]
- [[NDS Hook Trade Operator Checklist]]
