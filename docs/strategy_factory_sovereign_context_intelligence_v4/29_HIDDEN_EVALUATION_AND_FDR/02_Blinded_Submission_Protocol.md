---
title: Blinded Submission Protocol
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v4
---

# Mission

Freeze and submit model, preprocessing, policy, treatment lattice, calibration, and metric plan as a single immutable candidate.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Candidate artifacts.
- Metric and gate declaration.
- Environment lock.

## Output contracts

- Submission ID.
- Receipt and eligibility state.

## Algorithmic design

- Package deterministic code, model, feature order, preprocessing, calibration, candidate universe, fallback, and environment.
- Compute content hash and sign by research owner and independent reviewer.
- Evaluation service rejects partial or incompatible bundles.


## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- No post-submission patch.
- Any correction creates a new submission and spends budget.
- Submission must include simple baseline comparison.

## Measurement system

- Rejected partial bundles.
- Resubmission count.
- Environment reproducibility.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Model submitted without exact preprocessing.
- Threshold changed after score.
- Baseline omitted.

## UCEE integration

- None declared.

## Required tests and evidence

- Missing artifact.
- Signature mismatch.
- Incompatible schema.
- Nondeterministic output.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Immutable_Runtime_Compiler]]
- [[Hidden_Evaluation_Service_Architecture]]
