---
title: Batch DAG Orchestrator Boundary
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-06]
---
# Batch DAG Orchestrator Boundary

## Accepted implementation

ACL-06 now implements this boundary through a 54-task deterministic reference DAG, stable task contracts, acyclicity validation and atomic result publication.

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
