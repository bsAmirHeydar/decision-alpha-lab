---
title: Compute Budget and Cancellation
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-06]
---
# Compute Budget and Cancellation

## Accepted implementation

ACL-06 plans and charges every task against ACL-05 caps. The reference DAG remains below all caps and any first breach cancels publication.

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
