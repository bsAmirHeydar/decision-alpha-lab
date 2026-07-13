---
title: CI/CD and Qualification Pipelines
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- core-production
---

# Purpose

Automate tests and artifact promotion while preserving human authority and evidence-class distinctions.

## Capability tier

**Core Production**

## System design

### CI gates

Schemas, unit, property, leakage, reproducibility, static MQL5, security, and boundary checks.

### Qualification gates

Actual MetaEditor compile, Python/export/MQL5 parity, shadow/no-send, performance, soak, chaos, and authorization.

### Evidence classes

Static, fixture, simulated, paper, shadow, and actual evidence remain distinct.

### Release

Only signed immutable bundles may move between environments.

## Input contracts

- `SourceCommit`
- `EnvironmentDigest`
- `TestPlans`

## Output contracts

- `CIEvidence`
- `QualificationDossier`
- `ReleaseCandidate`

## Measurement framework

- Gate pass rate.
- Flaky test rate.
- Evidence completeness.
- Rollback success.

## Adversarial questions

- Can static validation be reported as actual compile?
- Can a failed gate be retried until lucky without ledger entry?
- Can CI sign promotion?

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
