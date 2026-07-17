---
title: V4-34 Sovereign Distributed Compute
status: accepted-reference
version: 1.0.0
created: '2026-07-13'
updated: '2026-07-17'
capability_tier: core-production-architecture
phase: SAED_V4_34
tags:
  - saed-v4
  - implementation
  - sovereign-compute
---
# Phase V4-34: Sovereign Distributed Compute

## Mission

Build a deterministic, additive and independently reproducible reference architecture for distributing research workloads across sovereign compute domains while preserving data residency, artifact immutability, complete budget accounting, fail-closed recovery and the UCEE authority boundary.

## Entry gates

V4-33 certificate and handoff hashes are mandatory. The compute constitution, jurisdiction registry, node identities, runtime-image hashes, data roles, artifact identities, known-time cutoff, workload DAG, compute budgets, exposure budgets and review budgets are frozen before planning begins.

## Architecture

The implementation contains nine closed planes: constitutional control, sovereign inventory, artifact identity, workload compilation, deterministic partitioning, topological scheduling, synthetic execution, checkpoint/recovery, and evidence/governance. Cross-domain messages are limited to aggregate, receipt, checkpoint-digest and evidence classes. Raw rows, credentials, private keys and account data are forbidden.

## Deterministic pipeline

1. Verify immutable V4-33 certificate and handoff.
2. Freeze a research-only compute constitution.
3. Freeze sovereign domains and independently operated nodes.
4. Validate node identity, runtime-image identity and known-time attestations.
5. Freeze default-deny network routes and immutable artifacts.
6. Compile the workload specification into an acyclic task DAG.
7. Enforce CPU, GPU, memory, scratch, network, cost, attempt, wall-clock and exposure budgets.
8. Partition tasks using deterministic capability/locality hashing.
9. Generate a locality proof and a topological wave schedule.
10. Execute the synthetic deterministic reference and emit hash-chained receipts.
11. Persist immutable checkpoints and inject declared synthetic faults.
12. Recover within the same sovereign domain and preserve the baseline.
13. Build resource, cost, network and exposure ledgers.
14. Redact telemetry and build complete distributed provenance.
15. Perform human, security, model-risk and fault-tolerance reviews.
16. Issue a reference-only certificate and bounded V4-35 handoff.

## Fail-closed semantics

Unknown fields, missing identities, future-known attestations, unapproved nodes, mutable artifacts, raw-data routes, unbounded resources, cyclic dependencies, unsatisfied locality, insufficient recovery capacity, incomplete exposure accounting or authority escalation reject the run. There is no permissive fallback.

## Acceptance gates

- Forty closed artifact/schema pairs.
- Exact deterministic replay and input-order invariance.
- Zero raw-data cross-domain movement.
- Complete task, network, cost, resource and exposure ledgers.
- Synthetic fault recovery without cross-domain migration.
- Evidence quorum across independent domains.
- Zero UCEE or central-engine mutation.
- Explicit separation of static evidence from real cluster, hardware, network, MetaEditor and broker evidence.

## Non-goals and claim ceiling

The accepted claim is limited to a synthetic deterministic reference. This phase does not claim a real distributed cluster, confidential compute, hardware attestation, network isolation, consensus protocol, production scheduler, runtime parity, broker qualification, prospective success, real alpha or production authorization.

## Handoff

V4-35 receives immutable compute, model, dependency and evidence identities as inputs for Model Risk and Supply Chain. No authority is transferred.
