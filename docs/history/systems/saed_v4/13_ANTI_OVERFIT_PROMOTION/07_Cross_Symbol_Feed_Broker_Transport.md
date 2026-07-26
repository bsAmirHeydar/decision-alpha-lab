---
title: Cross-Symbol, Feed and Broker Transport
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Test whether edge behavior survives changes in market, data feed, symbol specification, and execution venue.

## Capability tier

**Core Production**

## System design

### Symbol transport

Related and unrelated markets test mechanism breadth and false universality.

### Feed transport

Quote differences, gaps, timestamps, and bar construction are preserved.

### Broker transport

Spread, stops level, volume steps, sessions, rejects, and fill policies vary.

### Decision

Transport failure may constrain the admission domain rather than reject a genuinely local edge.

## Input contracts

- `DomainDatasets`
- `BrokerProfiles`
- `FeedLineage`

## Output contracts

- `TransportReport`
- `DomainRestrictions`
- `CalibrationRequirements`

## Measurement framework

- Transported utility.
- Calibration shift.
- Execution mismatch.
- Admission-domain coverage.

## Adversarial questions

- Is a local symbol effect being called universal?
- Does feed normalization conceal fragile timing?
- Does broker selection create survivorship bias?

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

- [[Causal_Transport_And_Domain_Shift]]
