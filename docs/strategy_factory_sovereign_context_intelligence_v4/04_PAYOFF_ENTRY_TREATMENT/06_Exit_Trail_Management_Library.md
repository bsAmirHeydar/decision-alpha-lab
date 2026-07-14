---
title: Exit, Trail and Management Library
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Represent exits and management as explicit state machines whose path dependence is replayable and parity-testable.

## Capability tier

**Core Production**

## System design

### Terminal exits

Fixed R, structural destination, opposite context, time stop, or explicit invalidation.

### Trailing families

Structural, volatility, swing, chandelier, state-dependent, and bounded learned trail variants.

### Partial management

Predeclared tranches, break-even rules, runner transitions, and cancellation conditions.

### No hidden optimization

Every state transition is generated from information available at that known time.

## Input contracts

- `PathEventStream`
- `ExitAtom`
- `TrailAtom`
- `ManagementAtom`

## Output contracts

- `TreatmentStateMachine`
- `ExitEvent`
- `TrailAudit`
- `ManagementOutcome`

## Measurement framework

- Capture ratio.
- Giveback ratio.
- Premature-exit rate.
- Path sensitivity.
- State-machine transition coverage.

## Adversarial questions

- Does OHLC ordering create fictional trail outcomes?
- Are break-even rules adjusted after results?
- Can partial exits alter risk beyond the policy contract?

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

- [[Path_Replay_And_Intrabar_Truth]]
