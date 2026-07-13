---
title: Abstention Is Alpha Protection
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- doctrine
---

# Thesis

The ability to refuse unsupported opportunities is part of the edge, not a defect.

## Architectural design

### Abstention sources

Low support, high epistemic uncertainty, missing views, model disagreement, unstable treatment rank, cost infeasibility, or policy conflict.

### Selective prediction

Coverage and conditional risk are jointly controlled; apparent performance cannot be improved by hiding abstention costs.

### Fallback hierarchy

Manual policy, simpler model, skip, or reject according to the signed policy graph.

## Machine contracts

- `abstention_reason`
- `coverage`
- `selective_risk`
- `fallback_action`
- `support_distance`

## Validation and evidence

- Coverage-risk curves are reported by time, symbol, regime, and profile.
- Abstention is included in opportunity-level economics.
- OOD and missing-view cases fail closed.

## Failure modes and mandatory response

- **Abstention omitted from reports:** Invalidate performance reporting.
- **Fallback outside support:** Reject runtime decision.
- **Coverage collapse in a regime:** Reduce, quarantine, or retrain through a new experiment.

## UCEE handoff

All outputs bind to exact upstream context, feature, data-role, treatment-universe, and economics hashes. Promotion and runtime authority remain in UCEE I12–I18.

## Related notes

- [[Conformal_Risk_Control]]
- [[OOD_Novelty_And_Support]]
