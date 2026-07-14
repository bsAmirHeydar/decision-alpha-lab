---
title: "Paper Reconciliation Ledger"
tags: [exp0019, fp-i15, concept]
status: canonical
---
# Paper Reconciliation Ledger

The append-only event chain for plan, quota, order, fill, position, and risk evidence.

## Invariants

- Identity is deterministic and versioned.
- The concept cannot mutate upstream signal evidence.
- Paper behavior remains separate from the unresolved live policy.
- All failures are reason-coded and auditable.
