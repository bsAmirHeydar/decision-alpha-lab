---
title: Incremental Value Attribution
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- core-production
---

# Purpose

Measure where value is created relative to manual and simple baselines.

## Capability tier

**Core Production**

## System design

### Attribution axes

Eligibility/selection, entry mechanism, treatment, exit/trail, timing, risk tier, portfolio interaction, and residual.

### Paired design

Compare decisions on the same occurrence and economic scenarios.

### Prospective attribution

Expected and observed incremental value are reconciled.

### Negative value

Avoided losses, missed opportunities, abstention cost, and operational burden are included.

## Input contracts

- `BaselineDecisions`
- `CandidateDecisions`
- `OutcomeCube`

## Output contracts

- `AttributionReport`
- `OpportunityLevelDeltas`
- `ResidualAnalysis`

## Measurement framework

- Incremental net utility.
- Attribution stability.
- Manual agreement.
- Residual size.

## Adversarial questions

- Does attribution double-count interactions?
- Are only selected trades paired?
- Does avoided loss ignore missed upside?

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

- [[Complexity_Must_Earn_Its_Right]]
