---
title: Selectivity, Coverage, and Abstention Frontier
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v4
---

# Mission

Choose how often the system acts versus abstains by evaluating selective risk and economic utility across support and uncertainty thresholds.

## Why this component exists

- None declared.

## Authority and safety boundary

- This component may estimate, rank, simulate, challenge, or recommend only inside a declared research scope.
- It cannot create canonical Context truth, modify protected evidence roles, sign promotion, change portfolio risk, activate runtime generations, access live credentials, or place orders.
- Unsupported, stale, contradictory, OOD, hash-mismatched, uncalibrated, or incomplete paths resolve to **Skip**, **Abstain**, **Manual fallback**, **Reject**, or **Quarantine**.
- Every result is subordinate to UCEE I12 promotion admission, I13 authority/fallback, I14 immutable runtime, I17 portfolio/risk, and I18 release qualification.

## Input contracts

- Calibrated model outputs.
- Support/OOD state.
- Treatment utility distributions.

## Output contracts

- Coverage-risk-utility frontier.
- Frozen abstention policy.

## Algorithmic design

- Evaluate thresholds inside nested validation.
- Report coverage by Context, regime, symbol, profile, and entry mechanism.
- Prefer set-valued candidate output when rankings overlap.
- Use manual fallback only where its support and authority are valid.

## Formal objective and constraints

```text
select if LCB(U_best - U_skip) > 0 and support_valid and uncertainty <= τ
```

## Data and known-time semantics

- None declared.

## Anti-overfit and model-risk controls

- No final-test threshold tuning.
- Coverage cannot be increased by treating unsupported cases as low-confidence trades.
- Abstention has explicit opportunity-cost accounting.

## Measurement system

- Selective risk.
- Coverage.
- Net utility per opportunity.
- Fallback rate.
- Unsupported action rate.

## Scalability and operating model

- None declared.

## Adversarial failure modes

- High apparent precision at negligible coverage.
- Rare buckets silently excluded.
- Abstain counted as win.

## UCEE integration

- None declared.

## Required tests and evidence

- Threshold surface.
- Coverage floor.
- Group-wise calibration.
- Unknown-regime stress.

## Implementation slices

- None declared.

## Decision record

- None declared.

## Acceptance gate

The component is accepted only when its contracts are closed and versioned, all lineage and role boundaries are reconstructible, protected evaluation remains unexposed, negative and mutation tests pass, simpler baselines remain available, and an independent reviewer can reproduce the decision-equivalent result from immutable hashes.

## Related notes

- [[Conformal_Uncertainty_Abstention_Control]]
- [[Selective_Prediction_And_Set_Valued_Action]]
