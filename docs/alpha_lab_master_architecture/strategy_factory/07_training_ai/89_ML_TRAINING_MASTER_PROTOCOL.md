---
type: strategy-factory-reference
status: canonical
title: "Machine-Learning Training Master Protocol"
tags:
  - strategy-factory
  - machine-learning
  - training
  - reference
---

# Machine-Learning Training Master Protocol

## Objective

The ML layer extracts conditional value from a deterministic anatomy and candidate universe. It does not replace the anatomy. The first goal is usually to decide whether to trade and which declared policy to use, not to predict raw future price from scratch.

## Dataset construction

The candidate-level table joins:

- event identity and market-event cluster;
- immutable decision-time features;
- candidate policy descriptors and geometry;
- outcome labels and label end time;
- source/feed/cost versions.

Candidates from the same event and cluster remain together in folds. Outcome columns are never features. Features with known times after the snapshot are rejected before training.

## Task hierarchy

### 1. Trade/skip meta-label

Estimate `P(net R > hurdle | event, context, candidate)` or a target-before-stop probability. This is the fastest useful model. Compare with always-trade and simple filters.

### 2. Expected-value regression

Predict net R, MFE, MAE, holding time, or cost. Use robust metrics and inspect residual tails. Expected-R models can rank policies but should not directly scale risk before calibration and live proof.

### 3. Candidate ranking

For each event, rank allowed entry/stop/exit candidates and include `skip`. Evaluate top-choice realized R and regret versus fixed policy. The historical oracle is an upper descriptive bound, not a valid model.

### 4. Survival / competing risk

Estimate time to fill, stop, target, expiry, or invalidation. Appropriate for time-cycle and management policies.

### 5. Sequence representation

Only after event-level models and sample requirements are met, add pre-event candle/order-flow sequences. The sequence ends exactly at decision time. Compare against summary-feature baselines.

## Baseline ladder

Every run includes:

1. never trade;
2. always trade fixed policy;
3. unconditional base probability/mean;
4. session/time-only;
5. anatomy-only;
6. one-feature threshold;
7. regularized logistic/ridge;
8. boosted-tree challenger;
9. ranker or sequence challenger.

A complex model that does not create stable economic uplift is rejected even if its predictive metric improves slightly.

## Preprocessing

All preprocessing is fit inside the training fold:

- numeric imputation and scaling;
- categorical vocabulary and encoding;
- rare-category grouping;
- feature selection;
- monotonic transformations;
- target balancing;
- calibration.

Persist the preprocessing artifact with the model. Live inference uses the exact transformation and rejects schema mismatch.

## Fold design

Use purged walk-forward by market-event cluster. For hyperparameters, use inner chronological validation or conservative fixed parameters. The outer test remains untouched. Candidate rows from one event cannot cross folds.

## Hyperparameter policy

Search spaces are bounded before the run and counted as trials. Start with defaults or small grids. Prefer regularization and shallow trees. Record every tested configuration, including failed jobs. Do not run broad AutoML on a small event dataset and report only the winner.

## Metrics

Classification:

- log loss
- Brier score
- calibration error/table
- ROC/PR only as secondary
- coverage and net R at threshold
- cluster-level economic uplift

Regression:

- MAE/MSE and rank correlation
- calibration of predicted versus realized R
- utility of top-ranked selections
- tail residual analysis

Ranking:

- top-1 and top-k net R
- regret versus oracle
- uplift versus fixed candidate
- policy concentration and stability

Always report fold-level metrics and economic outcome.

## Threshold selection

Thresholds are selected on training/validation using a declared utility:

```text
utility = expected net R
          - drawdown penalty
          - cost uncertainty penalty
          - turnover penalty
```

Hard constraints may require minimum clusters, calibration, or lower confidence bound. The outer test is used once to estimate the whole procedure.

## Calibration

Use reliability tables and Brier score. Platt scaling is suitable for smaller samples; isotonic requires more data. Calibration is fold-local. Live calibration drift is monitored. Poor calibration does not necessarily invalidate ranking, but it prohibits probability-proportional sizing.

## Model explainability

Use coefficients, permutation importance, group ablation, SHAP for supported models, and stability across folds. Look for impossible or suspicious drivers such as row order, post-event timestamps, missingness caused by future computation, or feed IDs that proxy period.

## Model packaging

A bundle contains:

- model artifact;
- preprocessing artifact;
- feature schema/order/types;
- model card;
- strategy/candidate/label/fold versions;
- decision threshold and fallback;
- artifact hash;
- runtime dependency versions;
- test vectors and expected predictions.

Deployment is atomic. A live runner loads the bundle read-only, validates hash, and runs test vectors before activation.

## Missing and out-of-distribution behavior

Each feature defines range and missing policy. Live observations outside trained support are flagged. The model may skip, use a simpler baseline, or enter review. It does not clip silently unless the transformation contract specifies clipping.

## Champion–challenger

The champion remains active while a challenger runs offline, then shadow, then paper. Compare disagreement cohorts. Promotion requires stable uplift, acceptable calibration, latency, and no new operational risk. A challenger can be superior statistically but rejected because it is too unstable or expensive.

## Online learning boundary

Live outcomes are collected in an evaluation store. Retraining is offline and follows the complete validation lifecycle. Contextual bandit exploration is a later controlled program with bounded actions and risk. No unrestricted online weight update occurs in the order path.

## LLM workflow

An LLM can:

- translate your setup explanation into a manifest and tests;
- inspect spreadsheets and map columns;
- find contradictory definitions;
- generate adapter scaffolds;
- propose nulls and ablations;
- analyze failure cohorts;
- write model cards and run reports.

The LLM cannot certify alpha, infer unavailable facts, or approve capital. All generated code remains untrusted until tests and review.

## Reference code

The supplied code includes transparent logistic and ridge models, purged walk-forward training, calibration tables, candidate ranking, model registry, and artifact contracts. Optional scikit-learn challengers may be added without changing the platform interfaces.
