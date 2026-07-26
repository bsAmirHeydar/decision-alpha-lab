---
title: Causal and Execution Auditors
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Independently audit treatment-effect assumptions and executable economics before claims reach promotion.

## Capability tier

**Core Production**

## System design

### Causal auditor

Overlap, assignment mechanism, confounding, cross-fitting, sensitivity, and transport.

### Execution auditor

Bid/ask, fill, queue, slippage, partials, broker constraints, latency, and path ordering.

### Reconciliation

Compare simulator, historical behavior, paper, and shadow evidence.

### Blocking power

Either auditor can block unsupported causal or economic claims.

## Input contracts

- `CausalDossier`
- `OutcomeCube`
- `BrokerEvidence`

## Output contracts

- `AuditReports`
- `ClaimRestrictions`
- `BlockingFindings`

## Measurement framework

- Audit issue rate.
- Simulator/paper delta.
- Overlap quality.
- Cost-model error.

## Adversarial questions

- Are simulated treatments physically executable?
- Is historical policy confounded?
- Does net edge survive broker-specific conditions?

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

- [[Causal_Identification_And_Assumptions]]
