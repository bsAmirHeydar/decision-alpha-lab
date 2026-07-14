---
title: No Autonomous Promotion
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- doctrine
---

# Thesis

Models and agents may compile evidence but only a governed human committee can authorize promotion.

## Architectural design

### Separation of duties

Research agents create artifacts; statistical and model-risk agents challenge them; human authorities sign promotion.

### Immutable dossier

Promotion binds exact data, code, feature, treatment, model, calibration, policy, and runtime hashes.

### Revocation

Any material integrity, drift, security, or operational failure can revoke admission without rewriting history.

## Machine contracts

- `promotion_dossier`
- `reviewer_signatures`
- `authority_matrix`
- `revocation_record`
- `effective_horizon`

## Validation and evidence

- No signer is the sole producer of the candidate.
- All required challenges are resolved or explicitly waived by authorized roles.
- Expired or revoked admission prevents runtime activation.

## Failure modes and mandatory response

- **Agent attempts to sign:** Hard deny and log a security incident.
- **Unsigned waiver:** Gate remains blocked.
- **Artifact changes after review:** Invalidate signatures and restart review.

## UCEE handoff

All outputs bind to exact upstream context, feature, data-role, treatment-universe, and economics hashes. Promotion and runtime authority remain in UCEE I12–I18.

## Related notes

- [[Multi_Agent_Authority_Matrix]]
- [[Model_Risk_Committee]]
