---
title: Model Risk Scorecard
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- core-production
---

# Purpose

Quantify scientific, data, operational, security, and governance risk separately from model performance.

## Capability tier

**Core Production**

## System design

### Scientific risk

Selection, multiplicity, causal assumptions, instability, and unexplained complexity.

### Data risk

Lineage, missingness, vintage, support, and feed dependence.

### Operational risk

Latency, parity, restart, fallback, broker, and monitoring.

### Security risk

Supply chain, signatures, dependencies, secrets, and model tampering.

### Governance risk

Concentration of authority, undocumented waivers, and review independence.

## Input contracts

- `AllEvidenceBundles`
- `ModelCard`
- `OperationalTests`

## Output contracts

- `ModelRiskScorecard`
- `ResidualRisk`
- `RequiredMitigations`

## Measurement framework

- Risk by domain.
- Residual risk after controls.
- Change from champion.
- Risk-adjusted incremental value.

## Adversarial questions

- Can strong returns override critical risk?
- Are risk scores self-assessed by the producing agent?
- Are waivers expiring and signed?

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

- [[Model_Risk_Committee]]
