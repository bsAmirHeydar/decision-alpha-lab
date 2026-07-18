---
title: Policy Engine and Allowed Next Actions
status: accepted-reference
version: 2.0.0
updated: 2026-07-18
tags: [acl-os, acl-09, control-plane]
---
# Policy Engine and Allowed Next Actions

ACL-09 binds separate memory and planner policies. Only governed admission and non-executing proposal compilation are permitted.

## Control invariant
Unknown identity, incompatible policy, budget breach, poisoning or hidden authority fails closed. All outputs are content-addressed, attributable and replayable.

## Related
- [[ACL09_MEMORY_AND_ACTIVE_PLANNER_RUNTIME]]
- [[ACL09_EVENT_LEDGER]]
