---
title: Run the Causal Treatment Program
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: canonical
tags:
  - saed-v4
  - runbook
  - operations
---

# Mission

Estimate treatment heterogeneity and policy value only inside defensible overlap and identification assumptions.

## Entry conditions

- Predeclared estimand.
- Occurrence clusters.
- Assignment and outcome data.

## Mandatory roles and separation of duties

- Causal scientist.
- Domain owner.
- Statistical adversary.
- Independent validator.

## Procedure

1. Document consistency, interference, ignorability, positivity, and transport assumptions.
2. Estimate cross-fitted propensities/outcomes.
3. Map overlap and ESS.
4. Run DR/R/forest and neural challengers.
5. Execute negative controls and hidden-confounder sensitivity.
6. Estimate policy value versus Skip/manual/fixed baselines.
7. Classify claim as causal, partially identified, or associative.

## Mandatory outputs

- Identification card.
- Overlap report.
- CATE and policy-value dossier.
- Sensitivity results.

## Stop and escalation conditions

- Structural non-overlap.
- Unresolved post-treatment feature.
- Extreme weight instability.
- Causal language unsupported.

## Evidence retained

- Nuisance models.
- Cross-fit folds.
- Influence values.
- Assumption signoff.

## Completion gate

The runbook is complete only when all required artifacts are content-addressed, all exposures and deviations are recorded, an independent reviewer signs the completion state, and the downstream UCEE gate accepts the exact immutable bundle rather than a narrative summary.

## Related notes

- [[Causal_Overlap_And_Positivity_Engine]]
- [[Orthogonal_Cross_Fitted_Policy_Value]]
