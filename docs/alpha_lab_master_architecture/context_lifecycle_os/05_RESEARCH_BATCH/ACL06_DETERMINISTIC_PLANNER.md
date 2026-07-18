---
title: ACL-06 Deterministic Planner
status: accepted-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-06]
---
# ACL-06 Deterministic Planner

## Purpose

The same Batch, request, registry and declared start time produce the same DAG identity and task identities. Wall-clock discovery is excluded from identity.

## Invariants

- ACL-05 Batch bytes and semantic digests remain unchanged.
- Unknown task types, fields, dependencies and capabilities fail closed.
- Research and diagnostic lanes remain explicit.
- Every output is attributable to a task receipt and immutable object.
- Order submission and capital activation are always false.

## Verification

Contract tests, hostile mutation tests, deterministic replay, budget tests, event-chain checks and clean-overlay validation are required. Passing them establishes only the stated reference claim ceiling.

## Related

[[ACL_06_RESEARCH_DAG_ORCHESTRATION]], [[BATCH_DAG_ORCHESTRATOR]], [[TASK_REGISTRY_AND_CONTRACT]]
