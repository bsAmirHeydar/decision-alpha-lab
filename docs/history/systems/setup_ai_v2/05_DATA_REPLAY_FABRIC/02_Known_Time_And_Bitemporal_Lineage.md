---
title: Known-Time and Bitemporal Lineage
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- core-production
---

# Purpose

Guarantee that every feature, context, trigger, and decision uses only information available at the declared decision time.

## Capability tier

**Core Production**

## System design

### Knowledge time

Each datum carries when the system could first know it, not merely the economic time it describes.

### Lineage closure

Derived artifacts preserve the maximum knowledge time and all contributing source references.

### As-of joins

Cross-symbol, higher-timeframe, and external views use deterministic as-of semantics.

### Audit probes

Future-suffix mutation, delayed-arrival replay, and correction replay test temporal integrity.

## Input contracts

- `EventCursor`
- `FeatureDAG`
- `ContextOccurrence`

## Output contracts

- `KnownTimeCertificate`
- `LineageGraph`
- `LeakageIncident`

## Measurement framework

- Leakage probe pass rate.
- Late-arrival sensitivity.
- Lineage closure completeness.

## Adversarial questions

- Do revised macro values replace vintage values?
- Does higher-timeframe close use an unfinished bar?
- Are cross-symbol views synchronized by future timestamps?

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

- [[Data_Leakage_Sentinel]]
