---
title: Missing-View-Robust Multimodal Fusion
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v3
---

# Mission

Fuse price, structure, temporal, intermarket, execution, and Context views while preserving missingness and view-specific support.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Per-view embeddings.
- View availability and quality masks.

## Output contracts

- Fused embedding.
- View contribution and missing-view directive.

## Algorithmic design

- Per-view encoders and calibration.
- Gated attention or product/mixture of experts with explicit masks.
- Modality dropout during training.
- Fallback to valid subset only when subset support was trained and certified.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- Missing view never imputed as valid zero.
- View quality cannot be inferred from outcome.
- Critical view absence forces abstention.

## Measurement system

- Performance by missing pattern.
- Calibration.
- View dominance.
- Fallback coverage.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- One powerful view suppresses others.
- Training always complete but runtime missing.
- View mask itself leaks regime outcome.

## UCEE integration

- None declared.

## Required tests and evidence

- Every missing combination.
- Corrupt view.
- View permutation.
- Critical-view drop.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Multi_View_Multimodal_Fusion]]
- [[Context_Abstention_And_Fallback_Ladder]]
