---
title: Causal Transport and Domain Shift
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- governed-challenger
---

# Purpose

Assess whether treatment relationships transport across time, symbols, feeds, brokers, and regimes.

## Capability tier

**Governed Challenger**

## System design

### Transport variables

Market, symbol, session, volatility, liquidity, broker, feed, context version, and regime.

### Reweighting

Importance weighting and doubly robust transport are used only when overlap is adequate.

### Invariant mechanisms

Search for stable conditional relationships, not universal invariance assumptions.

### Target-domain calibration

A new domain requires calibration and prospective evidence even when a causal model transports.

## Input contracts

- `SourceDomainData`
- `TargetDomainCovariates`
- `TransportAssumptions`

## Output contracts

- `TransportedPolicyValue`
- `OverlapWarning`
- `DomainAdmission`

## Measurement framework

- Target-domain policy value.
- Overlap and weight concentration.
- Mechanism stability.
- Cross-domain calibration.

## Adversarial questions

- Does source-domain success rely on unavailable features?
- Are transport weights extreme?
- Is a broker difference treated as harmless covariate shift?

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

- [[Cross_Symbol_Feed_Broker_Transport]]
