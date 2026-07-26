---
title: Prospective Paper Challenge
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- core-production
---

# Purpose

Freeze the full candidate before an untouched forward period and record every opportunity, decision, cost, fill, mismatch, and incident.

## Capability tier

**Core Production**

## System design

### Freeze

Context, features, treatment universe, model, calibration, thresholds, policy, costs, risk, runtime, and monitoring.

### No tuning

No retraining, threshold changes, treatment changes, cherry-picking, or result-dependent exclusions.

### Reconciliation

Expected and observed contexts, decisions, orders/no-send requests, fills, costs, and outcomes.

### Decision

Promote, extend challenge, recalibrate through a new version, reject, or retire.

## Input contracts

- `FrozenRuntimeBundle`
- `PaperPlan`
- `LiveLikeTelemetry`

## Output contracts

- `ProspectiveReport`
- `ReconciliationLedger`
- `ChallengeDecision`

## Measurement framework

- Opportunity count.
- Decision agreement.
- Expected/observed utility.
- Cost and fill deltas.
- Incident rate.

## Adversarial questions

- Was the paper period watched and then restarted?
- Were missing trades omitted?
- Did runtime and research diverge?

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

- [[Release_And_Production_Qualification]]
