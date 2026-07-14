---
title: Point-in-Time Feature Store V3
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v3
---

# Mission

Serve exact fold-local and runtime-equivalent features while preventing latest-value joins, role leakage, and schema drift.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Versioned platform manifest.
- Identity and evidence role.
- Immutable upstream artifacts.

## Output contracts

- Hash-bound platform artifact or service state.
- Health, lineage, and failure evidence.

## Algorithmic design

- Feature views bind code hash, input hash, fit role, valid time, and system time.
- Offline/online parity contract.
- Materialization by immutable snapshot.


## Data and known-time semantics

- Role-aware storage and access.
- Known-time semantics preserved.
- No mutable overwrite of evidence.

## Anti-overfit and model-risk controls

- Least privilege.
- Independent audit.
- No platform shortcut may bypass scientific or UCEE gates.

## Measurement system

- Feature freshness.
- Offline-online parity.
- Missingness.
- Schema compatibility.

## Scalability and operating model

- Horizontal stateless workers where possible.
- Content-addressed caching.
- Cell and campaign quotas.
- Isolation by namespace and evidence role.

## Adversarial failure modes

- Training uses corrected features unavailable live.
- Online default differs from offline.
- Feature reuse crosses roles.

## UCEE integration

- Feeds UCEE contracts but cannot modify Context truth, promotion, risk, portfolio, or live authorization.

## Required tests and evidence

- Failure injection.
- Restart/replay.
- Permission mutation.
- Hash/compatibility mismatch.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Platform_Reference_Architecture]]
- [[Context_Cell_Fleet_Control_Plane]]
