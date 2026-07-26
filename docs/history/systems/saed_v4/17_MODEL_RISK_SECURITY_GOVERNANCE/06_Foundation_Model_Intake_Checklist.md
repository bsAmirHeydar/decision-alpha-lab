---
title: Foundation Model Intake Checklist
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Govern third-party or public pretrained model use across provenance, overlap, security, license, domain, and reproducibility.

## Capability tier

**Core Production**

## System design

### Provenance

Publisher, paper, repository, checkpoint hash, training disclosure, date, and maintainer.

### Data overlap

Potential overlap with protected market periods or benchmark leakage is assessed and documented.

### Security

Sandboxed download, safe serialization, malware scan, SBOM/dependencies, and no arbitrary code execution.

### Scientific admission

Zero-shot or adapter results must pass native baselines, economics, shift, calibration, and support tests.

## Input contracts

- `ExternalModelReference`
- `SecurityPolicy`
- `DataRoles`

## Output contracts

- `IntakeDecision`
- `CheckpointAttestation`
- `UsageRestrictions`

## Measurement framework

- Intake completeness.
- Unresolved provenance risk.
- Economic uplift.
- Supply-chain findings.

## Adversarial questions

- Is training data unknown?
- Does model loading execute remote code?
- Can license permit production use?
- Is benchmark strength mistaken for trading edge?

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

- [[Time_Series_Foundation_Model_Adapters]]
