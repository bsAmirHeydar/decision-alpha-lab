---
title: Safe Action Projection
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- core-production
---

# Purpose

Ensure every learned or generated action remains inside treatment, risk, portfolio, and runtime constraints.

## Capability tier

**Core Production**

## System design

### Static projection

Action IDs outside the signed lattice are rejected.

### State projection

Only transitions valid from the current treatment state are allowed.

### Risk projection

AI cannot widen stop, increase authorized risk, or bypass kill/portfolio vetoes.

### Fallback

Invalid or low-support actions map deterministically to manual fallback, skip, or reject.

## Input contracts

- `ProposedAction`
- `TreatmentState`
- `AuthorityMatrix`

## Output contracts

- `ProjectedAction`
- `ProjectionReason`
- `FallbackDecision`

## Measurement framework

- Invalid-action attempt rate.
- Projection frequency.
- Fallback utility.
- Policy degradation under projection.

## Adversarial questions

- Does projection create an untested derived policy?
- Can repeated projections cause unsafe oscillation?
- Is model confidence preserved after action mutation?

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

- [[Manual_AI_Hybrid_Policy_Compilation]]
