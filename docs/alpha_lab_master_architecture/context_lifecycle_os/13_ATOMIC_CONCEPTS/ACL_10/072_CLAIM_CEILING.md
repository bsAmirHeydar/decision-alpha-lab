---
title: Claim Ceiling
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-10, promotion]
---
# Claim Ceiling

**Definition.** Claim Ceiling is a bounded ACL-10 concept in deterministic promotion-state evaluation.

**Invariant.** It preserves source identity, UNKNOWN semantics, baseline and diagnostic isolation, and all execution and capital denials.

**Failure.** Missing, ambiguous, unregistered or mutated material fails closed.

**Non-claim.** This concept does not prove alpha, execute promotion, generate runtime, submit an order or activate capital.

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
