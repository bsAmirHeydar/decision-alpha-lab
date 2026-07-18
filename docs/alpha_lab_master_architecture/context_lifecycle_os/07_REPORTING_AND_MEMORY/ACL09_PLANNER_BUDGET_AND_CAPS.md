---
title: ACL-09 Planner Budget and Caps
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-09, memory, planner]
---
# ACL-09 Planner Budget and Caps

Limits selected proposals and aggregate planning cost before any experiment can be authorized.

## Invariants

- Exact source identities and digests are preserved.
- UNKNOWN remains explicit and distinct from negative knowledge.
- Diagnostic and baseline evidence remain non-selectable.
- Generated artifacts are immutable and replayable.
- Research execution, promotion, order and capital authority remain false.

## Failure behavior

Missing identity, schema drift, poisoning, duplicate ambiguity, budget breach or authority escalation stops publication with an explicit reason code.

## Related

- [[ACL09_MEMORY_AND_ACTIVE_PLANNER_RUNTIME]]
- [[ACL09_ACL10_HANDOFF]]
