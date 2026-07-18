---
title: Cache, Idempotency and Replay
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-06]
---
# Cache, Idempotency and Replay

## Accepted implementation

ACL-06 cache keys bind task material and executor version. Reference replay verifies the run, DAG, result bundle, receipts, accounting, event chain, output manifest and handoff.

## Invariants

- The Batch cannot be mutated.
- The task graph is closed and acyclic.
- Retries are bounded and idempotent.
- Budget expansion is forbidden.
- Diagnostic evidence is non-selectable.
- Output remains non-executing and non-promotional.

## Verification

The phase includes unit, contract, negative-authority, deterministic replay, schema, registry and delivery tests. MetaEditor and live-market parity remain outside this phase.

## Related

[[ACL_06_RESEARCH_DAG_ORCHESTRATION]], [[ACL06_RESEARCH_DAG_RUNTIME]], [[ACL06_TASK_CONTRACT_STANDARD]]
