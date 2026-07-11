---
title: "Runtime Invariants"
---

# Runtime Invariants

The following rules are not optional implementation preferences. They are platform invariants.

## Authority Invariants

1. Host inputs cannot create broker authority.
2. Run mode cannot create broker authority.
3. Model confidence cannot create broker authority.
4. Only a future execution adapter behind the risk engine may hold broker authority.
5. Phase 02 binds an explicit no-send boundary.

## Causality Invariants

1. Event time must not exceed known time.
2. Known time must not exceed confirmation time.
3. Feature known time must not exceed snapshot time.
4. Snapshot identity must be derived after all features are frozen.
5. Rejected events may not silently become candidates later.

## Runtime Invariants

1. Required ports are bound before initialization.
2. Services initialize before the runtime becomes READY.
3. Services start before the runtime becomes RUNNING.
4. Services stop in reverse registration order.
5. Runtime work per cycle is bounded by `max_events_per_cycle`.
6. Audit capacity is fixed after initialization.
7. Duplicate service IDs are forbidden.
8. Illegal lifecycle transitions are rejected.

## Host Invariants

1. The Host is a composition root only.
2. The Host contains no anatomy vocabulary.
3. The Host contains no entry, stop, exit, model or risk logic.
4. The Host delegates ticks and timer callbacks.
5. Strategy-specific composition is introduced through a registry later, not through an expanding conditional block.

## Error Invariants

In strict mode, contract violations fail closed. In permissive research mode, a row may be rejected, but rejection counters and audit records remain mandatory. No error path may silently manufacture default market facts.
