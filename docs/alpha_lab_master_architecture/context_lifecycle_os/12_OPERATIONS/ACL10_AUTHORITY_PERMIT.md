---
title: Acl10 Authority Permit
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-10, promotion]
---
# Acl10 Authority Permit

Binds the evaluation to one memory run and explicitly denies research execution, promotion execution, runtime generation, order submission, capital activation and self-approval.

## Invariants

- Exact source identities and digests are preserved.
- UNKNOWN remains explicit and blocks promotion.
- Baseline and diagnostic sources remain non-promotable.
- Promotion execution, runtime generation, order submission and capital activation remain false.
- Generated outputs are immutable and replayable.

## Failure behavior

Missing identity, schema drift, integrity mismatch, unregistered state, unregistered transition, missing evidence or authority escalation fails closed with a registered reason code.

## Related

- [[ACL10_PROMOTION_STATE_MACHINE_RUNTIME]]
- [[ACL10_ACL11_HANDOFF]]
