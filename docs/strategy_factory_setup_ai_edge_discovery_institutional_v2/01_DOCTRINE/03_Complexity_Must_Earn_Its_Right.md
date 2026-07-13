---
title: Complexity Must Earn Its Right
status: canonical
version: 2.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v2
- doctrine
---

# Thesis

Model complexity is a capital allocation decision and must earn incremental, stable, cost-adjusted value over simpler baselines.

## Architectural design

### Baseline ladder

Skip-all, manual policy, unconditional treatment means, regularized linear models, calibrated trees, ranking baselines, and only then deep challengers.

### Complexity budget

Each increase in parameters, latency, data dependence, or operational surface consumes an explicit complexity budget.

### Incremental attribution

Selection, treatment, timing, risk, and residual uplift are estimated against the same manual baseline and folds.

## Machine contracts

- `baseline_manifest`
- `complexity_budget`
- `incremental_value_report`
- `latency_budget`
- `operational_risk_score`

## Validation and evidence

- Advanced model uplift remains positive after multiplicity correction.
- Ablations show which component produced the uplift.
- Fallback to the simpler model is deterministic and tested.

## Failure modes and mandatory response

- **Marginal uplift disappears under costs:** Reject or demote the challenger.
- **Latency budget exceeded:** Keep research-only or simplify.
- **Operational burden exceeds expected value:** Prefer the simpler production model.

## UCEE handoff

All outputs bind to exact upstream context, feature, data-role, treatment-universe, and economics hashes. Promotion and runtime authority remain in UCEE I12–I18.

## Related notes

- [[Model_Ladder_And_Champion_Challenger]]
- [[Incremental_Value_Attribution]]
