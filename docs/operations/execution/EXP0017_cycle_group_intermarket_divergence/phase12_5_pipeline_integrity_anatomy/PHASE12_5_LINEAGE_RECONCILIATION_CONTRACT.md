# Phase 12.5 Lineage Reconciliation Contract

## Exact lineage

Exact lineage requires the child to represent the same identity population as the parent.

### Phase 07 → Phase 10

`outcome_id` and `signal_id` are exact. Phase 10 may mark rows excluded, but it must not silently drop their audit identity.

## Child-subset lineage

A child-subset relationship permits a valid selection from the parent but forbids invention.

### Phase 10 → Phase 11 predictions

Not every Phase 10 row must appear in OOS predictions. However, every prediction must point to a Phase 10 `sample_id` and `signal_id`.

### Fold plan → predictions/bucket validation

Every emitted fold ID must be declared in the fold plan.

## Measurements

Each relation records:

- parent unique keys;
- child unique keys;
- matched keys;
- missing parent keys;
- orphan child keys;
- parent coverage;
- child coverage;
- sample examples.

## Critical interpretation

An orphan downstream identity is more dangerous than an intentionally omitted upstream identity. It indicates stale files, mixed runs, or identity corruption.
