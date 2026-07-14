---
title: Compute Fabric and Schedulers
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Execute reproducible CPU/GPU workloads at institutional scale with quotas, priorities, isolation, and cost evidence.

## Capability tier

**Core Production**

## System design

### Job graph

Data materialization, pretraining, tuning, calibration, evaluation, export, and challenge tasks form a dependency DAG.

### Resource classes

CPU high-memory, single GPU, multi-GPU, distributed, and secure production build pools.

### Scheduling

Fair-share, project quotas, preemption rules, retry policy, locality, and deadline classes.

### Cost accounting

Every artifact records compute time, energy proxy, cloud/on-prem cost, and failed-job waste.

## Input contracts

- `JobDAG`
- `EnvironmentDigest`
- `ResourceRequest`

## Output contracts

- `JobEvidence`
- `ComputeCostReport`
- `SchedulerLedger`

## Measurement framework

- Queue time.
- Utilization.
- Cost per accepted candidate.
- Retry and preemption rate.
- Reproducibility across pools.

## Adversarial questions

- Can researchers bypass quotas?
- Does hardware change alter numerical results?
- Are failed expensive trials hidden from program economics?

## Mandatory controls

1. Exact upstream hashes and data roles are recorded.
2. Candidate and failure ledgers are complete.
3. Costs, capacity, missingness, censoring, and support are explicit.
4. Validation uses chronological, cluster-aware, purged folds.
5. Advanced outputs cannot bypass manual policy, hard risk, portfolio, or UCEE promotion.
6. Any runtime handoff requires deterministic export, parity, latency, fallback, and revocation evidence.

## Acceptance boundary

Passing research metrics is necessary but never sufficient. The component remains non-authoritative until its evidence is admitted through UCEE I12, compiled by I14, challenged prospectively under I15, bounded by I17, and qualified under I18.

## Related notes

- [[Distributed_Training_And_Parallelism]]
