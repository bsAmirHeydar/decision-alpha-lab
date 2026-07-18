---
title: Event Ledger and Idempotency
status: accepted-reference
version: 2.0.0
updated: 2026-07-18
tags: [acl-os, acl-09, control-plane]
---
# Event Ledger and Idempotency

ACL-09 proves append-only memory snapshots and idempotent re-ingestion. Exact prior fingerprints link to existing entries; prior proposal fingerprints suppress repeated research.

## Control invariant
Unknown identity, incompatible policy, budget breach, poisoning or hidden authority fails closed. All outputs are content-addressed, attributable and replayable.

## Related
- [[ACL09_MEMORY_AND_ACTIVE_PLANNER_RUNTIME]]
- [[ACL09_EVENT_LEDGER]]
