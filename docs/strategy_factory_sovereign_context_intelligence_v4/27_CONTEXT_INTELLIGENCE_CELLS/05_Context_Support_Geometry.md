---
title: Context Support Geometry
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v4
---

# Mission

Model where a Context-treatment decision is empirically supported and where the system must abstain, simplify, or fall back.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Context representations.
- Treatment assignments.
- Fold and evidence roles.

## Output contracts

- Support map.
- Coverage and overlap diagnostics.
- Per-candidate support state.

## Algorithmic design

- Combine density-ratio estimation, nearest-neighbor coverage, one-class classifiers, energy scores, ensemble disagreement, and treatment propensity overlap.
- Model support hierarchically by context version, symbol, session, regime, payoff profile, entry mechanism, and broker economics.
- Define support states: in-support, sparse, extrapolative, contradictory, OOD, unknown.
- Calibrate thresholds only on allowed calibration roles.

## Formal objective and constraints

```text
admit(x,a) = 1[support_state(x,a)=IN_SUPPORT and overlap(x,a)>=tau and calibration_valid]
```

## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- No threshold tuning on locked or prospective outcomes.
- High model confidence cannot override low support.
- Transfer priors are discounted by recipient support.

## Measurement system

- Coverage.
- Selective risk.
- Sparse-bucket utility.
- False in-support rate.
- OOD containment rate.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- Embedding distance is treated as universal support.
- Rare profitable bucket is promoted without overlap.
- Support changes after final inspection.

## UCEE integration

- None declared.

## Required tests and evidence

- Synthetic holes.
- Leave-symbol-out OOD.
- Regime-drop.
- Adversarial near-neighbor with contradictory lifecycle.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Selective_Prediction_And_Set_Valued_Action]]
- [[Causal_Overlap_And_Positivity_Engine]]
