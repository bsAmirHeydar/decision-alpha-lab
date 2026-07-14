---
title: Model Card and System Card
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Document not only model metrics but the full decision system, dependencies, support, failure modes, and intended authority.

## Capability tier

**Core Production**

## System design

### Model card

Task, data, architecture, features, calibration, uncertainty, support, performance, limitations, and export.

### System card

Context, treatment lattice, policy graph, risk, portfolio, runtime, broker, monitoring, human controls, and incidents.

### Domain restrictions

Markets, symbols, sessions, contexts, profiles, brokers, and horizons.

### Change history

Every material change maps to new evidence and compatibility review.

## Input contracts

- `ModelArtifacts`
- `PolicyGraph`
- `RuntimeBundle`

## Output contracts

- `ModelCard`
- `SystemCard`
- `RestrictionManifest`

## Measurement framework

- Card completeness.
- Consistency with registry.
- Known limitations.
- Change traceability.

## Adversarial questions

- Does a model card omit policy-level failure?
- Are restrictions enforceable in runtime?
- Is a generic disclaimer substituting for evidence?

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

- [[Model_Risk_Scorecard]]
