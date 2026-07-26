---
title: Structured Treatment Set Prediction
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production
tags:
  - saed-v4
  - 46_decision_focused_setup_synthesis
  - institutional-v4
---

# Mandate

Optimize the quality of bounded treatment decisions rather than generic forecast error, while preserving a finite approved action lattice and explicit skip/abstain options.

**This specification:** **Structured Treatment Set Prediction**.

The component exists to improve decision quality and scientific understanding while remaining subordinate to canonical Context truth, bounded Treatment DSL, protected evidence roles, UCEE promotion, hard risk, portfolio governance and production qualification.

## Institutional questions

- What exact uncertainty, mechanism, representation, decision or operational failure does this component address?
- Which claim is descriptive, predictive, causal, decision-theoretic or operational?
- Which support region and known-time boundary make the claim valid?
- Which simpler baseline would reveal that the added complexity has no economic value?
- Which independent evidence can reject the component before capital is exposed?
- Which failure must resolve to Skip, Abstain, Manual fallback, Quarantine or Reject?

## Input contracts

- treatment outcome cube
- utility vector
- constraints
- capacity curves
- uncertainty
- portfolio marginal contribution
- Exact Context ID and version, occurrence ID, known time, lifecycle state and required-view mask.
- Exact treatment-lattice version, cost/broker profile, evidence role, fold, environment and model-generation hashes.
- Explicit missingness, censoring, revision, clock and transport metadata.

## Output contracts

- Versioned output with support, calibration, uncertainty and novelty state.
- Claim class: descriptive, associational, causal, predictive, stress-only or operational.
- Decision contribution bounded to approved treatments, Skip, Abstain or Manual fallback.
- Evidence references and failure reasons sufficient for independent replay.
- No order, broker, risk-limit, portfolio-allocation, promotion or runtime-activation authority.

## Algorithmic stack

- decision-focused learning
- structured prediction
- set-valued selection
- differentiable optimization challengers
- multi-objective Pareto search
- minimax regret

The production path begins with the simplest defensible estimator. More complex methods enter only as governed challengers, and only after data sufficiency, support, calibration and transport tests are established.

## Formal objective

```text
maximize    protected lower-bound economic utility
subject to  known-time correctness
            declared support and overlap
            complete search/exposure accounting
            cost, capacity and execution realism
            calibration and selective coverage
            tail and drawdown constraints
            UCEE authority and runtime compatibility
            independent replication
```

Point-estimate backtest profit is never the optimization target by itself. Candidate ranking uses a vector of utility, tail risk, instability, complexity, capacity, uncertainty, evidence debt and operational burden.

## Data semantics

- Event time and knowledge time are distinct.
- Revisions never overwrite history.
- Treatment siblings share an opportunity cluster.
- Non-fill, cancellation, expiry and abstention remain observable outcomes.
- Protected final, prospective, shadow and live roles cannot be consumed by training or adaptive search.
- Synthetic paths are watermarked and cannot provide positive promotion evidence.

## Scientific controls

- no free-form actions
- utility decomposition
- simple-policy baseline
- constraint solver authority
- lower-bound selection
- action support audit
- Purged nested walk-forward with cluster-preserving splits.
- Complete trial, query, chart, narrative and agent-exposure ledger.
- Locked search space and hypothesis family before protected evaluation.
- Best-trade, best-period, best-symbol and best-regime removal.
- Delay, spread, slippage, feed, broker, capacity and correlation shocks.
- Independent rebuild and multi-lab replication for material capital tiers.

## Required baselines

1. Skip all.
2. Fixed approved treatment.
3. Manual policy.
4. Regularized linear or survival baseline.
5. Calibrated tree/ranker baseline.
6. Complexity-matched ablation.
7. Random/frozen representation control where applicable.

## Failure and fallback matrix

| Failure | Required response |
|---|---|
| Missing required view | Abstain or manual fallback |
| Outside support | Reject |
| Calibration stale | Quarantine |
| Hidden-evaluation budget exhausted | Stop research family |
| Critical red-team finding | Reject or redesign |
| Runtime parity mismatch | Do not compile/activate |
| Evidence lineage break | Invalidate dossier |
| Broker/capacity infeasible | Skip |

## Scalability design

- Stateless services read immutable artifacts and emit content-addressed results.
- Context-specific learning lives inside a Context Intelligence Cell; shared data, compute, evidence and runtime services remain centralized.
- Workloads are shardable by Context, occurrence cluster, treatment family, fold, model family and stress scenario.
- Expensive models are distilled only after protected uplift is established.
- Compute, storage, human-review and operational costs are attributed to every candidate.

## UCEE integration

- I01–I10 provide canonical truth, known-time features, datasets, folds and experiment identities.
- I11–I12 govern training, challenge and promotion.
- I13 compiles bounded manual/AI/hybrid policy with abstention and fallback.
- I14 requires immutable runtime and Python/export/MQL5 parity.
- I17 owns risk reservation, portfolio capacity and allocation.
- I18 owns release, authorization, recovery and production qualification.

## Acceptance evidence

- Closed contracts and schemas.
- Positive, negative, mutation, leakage and replay tests.
- Calibration and support report.
- Complexity and baseline uplift report.
- Search and exposure accounting.
- Independent challenge and replication.
- Runtime feasibility and fallback proof.
- Explicit unresolved limitations.

## Implementation slices

1. Freeze authority, inputs, outputs and claim class.
2. Implement deterministic baseline and golden fixtures.
3. Add representation or advanced learner as challenger.
4. Add red-team and transport tests before tuning expansion.
5. Register the complete search and exposure family.
6. Run hidden evaluation once within budget.
7. Produce signed evidence and model-risk dossier.
8. Hand off only through UCEE admission.

## Related architecture

- [[00_Home_V4]]
- [[Sovereign_Context_Intelligence_Reference_Architecture]]
- [[Ultimate_Anti_Overfit_Scientific_Constitution]]
- [[UCEE_I01_I18_Compatibility_V4]]
