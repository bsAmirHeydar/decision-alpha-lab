---
title: Security, Supply Chain and SBOM
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- core-production
---

# Purpose

Protect code, datasets, model weights, dependencies, builders, credentials, and runtime bundles from tampering and unreviewed supply-chain risk.

## Capability tier

**Core Production**

## System design

### Software supply chain

Pinned sources, signatures, SBOM, vulnerability scans, licenses, provenance, and reproducible builds.

### Model supply chain

Checkpoint provenance, training disclosure, license, checksum, malware/safe-tensor policy, and sandboxed intake.

### Secrets

Central vault, short-lived credentials, no secrets in artifacts, and scoped service identities.

### Response

Revocation, quarantine, dependency patch qualification, and descendant impact analysis.

## Input contracts

- `DependencyLock`
- `ModelIntake`
- `IdentityPolicy`

## Output contracts

- `SBOM`
- `SupplyChainAttestation`
- `SecurityIncidents`

## Measurement framework

- Unsigned artifact rate.
- Critical vulnerabilities.
- Secret exposure.
- Revocation time.
- Reproducible build rate.

## Adversarial questions

- Can an agent download arbitrary code or weights?
- Are pickle-like artifacts trusted?
- Does a dependency patch silently change results?

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

- [[Foundation_Model_Intake_Checklist]]
