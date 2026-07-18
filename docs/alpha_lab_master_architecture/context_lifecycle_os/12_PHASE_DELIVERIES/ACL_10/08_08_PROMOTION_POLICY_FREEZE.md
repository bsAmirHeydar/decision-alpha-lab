---
title: ACL-10 — 08 Promotion Policy Freeze
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-10, promotion]
---
# ACL-10 — 08 Promotion Policy Freeze

This artifact records the ACL-10 engineering decision for **08 Promotion Policy Freeze**. It binds exact ACL-09 evidence to a closed promotion-state evaluation while preserving all authority denials.

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
