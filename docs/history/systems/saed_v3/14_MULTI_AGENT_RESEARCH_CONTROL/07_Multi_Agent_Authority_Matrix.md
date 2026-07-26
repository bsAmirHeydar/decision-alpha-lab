---
title: Multi-Agent Authority Matrix
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v3
- core-production
---

# Purpose

Encode least privilege and separation of duties for every human and agent role.

## Capability tier

**Core Production**

## System design

### Permissions

Read/write by artifact class and data role; run, block, request, review, sign, revoke, and deploy are distinct.

### Deny by default

Unlisted capabilities are denied.

### Two-person rules

Protected data access, critical waivers, promotion, authorization, and production rollback require independent roles.

### Audit

Every action carries actor, authority version, reason, inputs, and hash-chained event.

## Input contracts

- `RoleRegistry`
- `CapabilityMatrix`
- `IdentityAttestation`

## Output contracts

- `AuthorizationDecision`
- `AuthorityAudit`
- `ViolationIncident`

## Measurement framework

- Unauthorized attempts.
- Privilege breadth.
- Signer independence.
- Revocation latency.

## Adversarial questions

- Can a research agent write governance records?
- Can one person produce and approve?
- Are temporary permissions expiring?

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

- [[No_Autonomous_Promotion]]
