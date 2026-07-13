---
title: Data Leakage Sentinel
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- core-production
---

# Purpose

Continuously challenge temporal, cross-fold, feature, label, normalization, and research-exposure integrity.

## Capability tier

**Core Production**

## System design

### Static analysis

Inspect feature DAGs, joins, timestamps, preprocessing, target construction, and fold code.

### Dynamic probes

Future-suffix perturbation, time shifts, delayed arrivals, synthetic future markers, and role-access traps.

### Runtime parity

Compare known-time feature materialization across research and MQL5 paths.

### Authority

Can block a run or promotion gate; cannot repair evidence silently.

## Input contracts

- `FeatureCode`
- `LineageGraph`
- `AccessLogs`

## Output contracts

- `LeakageAudit`
- `BlockingIncidents`
- `RemediationRequirements`

## Measurement framework

- Probe coverage.
- Detected leakage incidents.
- False positives.
- Time to containment.

## Adversarial questions

- Can a model access outcome-derived caches?
- Is normalization fitted globally?
- Did an agent view protected rows?

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

- [[Known_Time_And_Bitemporal_Lineage]]
