---
title: Self-Supervised Context Pretraining
status: canonical
version: 3.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v3
---

# Mission

Learn reusable market and Context representations from unlabeled, decision-time-correct data before outcome-specific training.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Role-safe token streams.
- View masks.
- Pretraining curriculum.

## Output contracts

- Frozen encoder checkpoints.
- Representation evaluation dossier.

## Algorithmic design

- Masked span modeling, next-event prediction, temporal contrast, cross-view alignment, context transition prediction, regime discrimination, missingness reconstruction, and multi-horizon distribution prediction.
- Curriculum progresses from local path to cross-symbol/Context graph.
- Use negative samples that respect time and event dependence.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- No outcome or protected role in pretraining.
- Random/frozen encoder and from-scratch ablations.
- Checkpoint provenance and training corpus manifest.

## Measurement system

- Linear probe.
- Few-shot sample efficiency.
- Transfer uplift.
- Representation collapse.
- Leakage probes.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Pretraining corpus includes future evaluation.
- Contrastive negatives are trivially separable.
- Large encoder memorizes symbol/time IDs.

## UCEE integration

- None declared.

## Required tests and evidence

- Membership/contamination audit.
- Random-label probe.
- Temporal shuffle.
- Leave-domain-out transfer.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Multiresolution_Market_Tokenization]]
- [[Foundation_Model_Intake_V3]]
