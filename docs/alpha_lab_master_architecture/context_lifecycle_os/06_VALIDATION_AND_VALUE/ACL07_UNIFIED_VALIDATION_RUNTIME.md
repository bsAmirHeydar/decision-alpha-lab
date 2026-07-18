---
title: Acl07 Unified Validation Runtime
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-07, validation]
---
# Acl07 Unified Validation Runtime

Defines the deterministic runtime that binds the immutable ACL-06 research evidence to a closed validation policy, executes the registered gates and issues non-promotional decisions.

## Responsibility boundary

ACL-07 consumes immutable evidence and issues non-promotional validation decisions. It cannot mutate the frozen Batch, research results, Setup behavior, diagnostic status, execution authority or capital authority.

## Invariants

- All identities and digests resolve exactly.
- Unknown required evidence fails eligibility.
- Diagnostic evidence remains segregated.
- Multiple-testing scope is the frozen candidate family.
- Generated outputs are immutable and replayable.
- No decision is an order, allocation or production authorization.

## Failure semantics

The component stops or emits an explicit FAIL/UNKNOWN reason code. It never fills missing evidence with optimistic defaults.

## Related

- [[ACL07_UNIFIED_VALIDATION_RUNTIME]]
- [[ACL07_DECISION_POLICY]]
- [[ACL07_ACL08_HANDOFF]]
