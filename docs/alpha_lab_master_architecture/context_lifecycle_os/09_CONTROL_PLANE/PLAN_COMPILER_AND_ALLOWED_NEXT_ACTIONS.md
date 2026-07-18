---
title: Plan Compiler and Allowed Next Actions
status: accepted-reference
version: 2.0.0
updated: 2026-07-18
tags: [acl-os, acl-09, control-plane]
---
# Plan Compiler and Allowed Next Actions

ACL-09 provides the first reference Plan Compiler: it converts governed UNKNOWN evidence into closed-registry proposals, applies deterministic priority and budget caps, and exposes proposals without scheduling or execution authority.

## Control invariant
Unknown identity, incompatible policy, budget breach, poisoning or hidden authority fails closed. All outputs are content-addressed, attributable and replayable.

## Related
- [[ACL09_MEMORY_AND_ACTIVE_PLANNER_RUNTIME]]
- [[ACL09_EVENT_LEDGER]]
