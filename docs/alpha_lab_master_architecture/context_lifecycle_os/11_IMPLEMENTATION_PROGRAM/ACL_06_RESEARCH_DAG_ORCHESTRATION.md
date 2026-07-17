---
title: ACL-06 — Research DAG Orchestration
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, context-lifecycle, acl-06]
---

# ACL-06 — Research DAG Orchestration

## Accepted ACL-05 dependency contract

ACL-06 starts only from a validated `ACL05_TO_ACL06` handoff. It must resolve the exact frozen Batch definition, semantic Batch manifest, freeze receipt, candidate/search freeze digests, dataset/label sets, split, environment, budget, content-addressed object index, event ledger and provenance graph. Every referenced digest must resolve within the received generated ACL-05 root.

The handoff grants exactly these next actions:

- `PLAN_RESEARCH_DAG`
- `REGISTER_TASK_CONTRACTS`
- `EXECUTE_BOUNDED_RESEARCH`

It forbids Batch mutation, setup-behavior mutation, diagnostic candidate promotion, alpha inference from the freeze itself, execution authorization and capital activation. ACL-06 cannot regenerate ACL-04 candidates, alter data cuts, change labels, refit split boundaries or expand budgets. Material changes return to ACL-05 and create a new Batch.

## Responsibility boundary

ACL-06 owns deterministic task planning, task registry contracts, dependency ordering, bounded execution, idempotent retries, task-level evidence, failure propagation and research-result packaging. It does not own Batch identity, validation promotion, trading permission or capital decisions.

## Minimum intake checks

- `handoff_type == ACL05_TO_ACL06`;
- Batch state is `FROZEN` and mutation is false;
- output manifest and Batch receipt are byte-valid;
- CAS objects resolve by exact SHA-256 bytes;
- diagnostic and research lanes are distinct;
- environment and budget capabilities are enforced;
- event/provenance chains are complete;
- no order, capital, secret or network authority is present.

## Required ACL-06 outputs

ACL-06 must produce a closed research DAG, registered task contracts, deterministic cache keys, execution receipts, bounded resource accounting, failure evidence, result artifacts, lineage to the frozen Batch and a non-promotional handoff to ACL-07 Unified Validation Gate.

## Claim ceiling

Planning or executing a research DAG does not prove alpha, production readiness, live parity or capital authorization.

## Related

- [[ACL_05_IMMUTABLE_BATCH_AND_STORE]]
- [[BATCH_DAG_ORCHESTRATOR]]
- [[TASK_REGISTRY_AND_CONTRACT]]
