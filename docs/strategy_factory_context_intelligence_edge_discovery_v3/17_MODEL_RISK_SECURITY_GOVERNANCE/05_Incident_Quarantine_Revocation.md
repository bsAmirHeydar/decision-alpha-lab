---
title: Incident, Quarantine and Revocation
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- core-production
---

# Purpose

Contain scientific, data, model, execution, security, and governance failures without rewriting historical evidence.

## Capability tier

**Core Production**

## System design

### Incident classes

Integrity, leakage, drift, calibration, execution, risk, portfolio, security, authorization, and operational.

### Immediate actions

Pause, reduce, quarantine context/model/generation, revoke authorization, or rollback.

### Forensics

Preserve telemetry, artifacts, environment, commands, broker state, and affected decisions.

### Resolution

Root cause, descendant impact, evidence repair, requalification, and lessons to failure memory.

## Input contracts

- `IncidentSignal`
- `ActiveGeneration`
- `AuthorityState`

## Output contracts

- `IncidentRecord`
- `ContainmentActions`
- `RevocationRecord`

## Measurement framework

- Detection and containment time.
- Affected decisions.
- Recurrence.
- Evidence preservation.

## Adversarial questions

- Can an incident be downgraded to protect performance reporting?
- Does rollback duplicate orders?
- Are revoked artifacts still cached?

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

- [[Monitoring_Assumption_Contract]]
