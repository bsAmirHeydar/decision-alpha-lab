---
title: Stop Geometry Library
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Treat stop location as an invalidation contract with executable geometry, not as an arbitrary tuning parameter.

## Capability tier

**Core Production**

## System design

### Structural wide stop

Placed beyond context-level invalidation or protected reference with declared volatility and broker buffers.

### Trigger tight stop

Placed beyond the local activation structure and therefore highly execution-sensitive.

### Volatility-conditioned stop

Uses pre-known volatility state with bounded scaling and stable parameter neighborhoods.

### Composite stop

Combines structural and operational limits without allowing the model to widen risk after entry.

## Input contracts

- `StopAtom`
- `SymbolSpecification`
- `RiskPolicy`

## Output contracts

- `StopGeometry`
- `InvalidationReason`
- `StopSensitivityReport`

## Measurement framework

- Stop-hit hazard.
- MAE-to-stop distribution.
- Sensitivity to tick, spread, delay, and feed.
- Risk-normalized capital efficiency.

## Adversarial questions

- Is the stop optimized against future MAE?
- Does widening stop manufacture win rate?
- Can runtime normalize the stop differently from research?

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

- [[Execution_Realism_And_Broker_Constraints]]
