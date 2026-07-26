---
type: strategy-factory-document
status: canonical
title: "Explainability, Ablation, and Failure Analysis"
tags:
  - strategy-factory
---

# Explainability, Ablation, and Failure Analysis

Explanation is used to debug and constrain models, not to manufacture narratives for every prediction.

## Global analysis

Permutation importance, coefficient stability, SHAP for supported challengers, partial dependence with caution, feature-group ablation, and fold-to-fold sign consistency. Explanations are computed OOS where possible.

## Failure cohorts

Analyze false positives, missed tails, high-MAE winners, cost-sensitive trades, feed disagreements, and model/rule disagreements. Each cohort can create a new hypothesis but cannot alter the tested version retroactively.

## Sanity checks

Label shuffle, feature time shift, random feature injection, and impossible-feature tests should collapse performance. If not, the pipeline likely leaks or selection is flawed.

