---
title: Path Replay and Intrabar Truth
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- core-production
---

# Purpose

Reconstruct the event path required for stops, limits, trails, partial fills, and competing event ordering.

## Capability tier

**Core Production**

## System design

### Resolution ladder

Tick, quote, lower-timeframe, and bar replay tiers are declared per treatment and evidence stage.

### Ordering policy

When resolution cannot order stop and target, the outcome is ambiguous, conservatively bounded, or excluded according to a frozen rule.

### Trail engine

Every trail activation, ratchet, giveback, and exit is replayed from the same event sequence used by runtime.

### Path compression

Research acceleration may cache state transitions but must remain hash-equivalent to canonical replay.

## Input contracts

- `ReplayManifest`
- `TreatmentStateMachine`
- `QuoteEvents`

## Output contracts

- `PathOutcome`
- `AmbiguityFlag`
- `TransitionLedger`

## Measurement framework

- Ambiguous-path rate.
- Replay/runtime parity.
- Trail transition coverage.
- Resolution sensitivity.

## Adversarial questions

- Does OHLC assume favorable event order?
- Are partial fills treated atomically?
- Does accelerated replay skip path-dependent states?

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

- [[Exit_Trail_Management_Library]]
