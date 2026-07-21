---
title: 08 Identity and Deduplication
status: accepted
version: 1.0.2
tags: [rthp, context, acl-02, english]
---

# 08 Identity and Deduplication

Occurrence identity is derived from Context ID, symbol-pair ID, cycle-definition version, relationship family, active and reference cycle identities, level side, hunter/protected roles, first-touch time, and synchronized confirmation time.

The same event ID is never appended twice. Restart, replay, or history reload must reconstruct the same ledger. Corrections are append-only and reference the event they supersede.

## Machine-readable authority

`lab/11_strategy_factory/contexts/CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1`


## ACL-03 generic identity aliases

The ACL-03 compiler requires three cross-context identity fields. RTHP binds them exactly: `anchor_time` to `confirmation_close_time`, `direction` to `relation_polarity`, and `subject_key` to `symbol_pair_id`. The original RTHP identity dimensions remain present, so replay and deduplication stay explicit.
