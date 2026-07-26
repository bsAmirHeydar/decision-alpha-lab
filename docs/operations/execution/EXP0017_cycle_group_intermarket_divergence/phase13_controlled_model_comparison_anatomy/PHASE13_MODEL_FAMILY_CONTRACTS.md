# Phase 13 Model Family Contracts

## Bucket baseline

Uses hierarchical train-window statistics. Preferred key is CG + direction + role, with fallback to broader train-only buckets and finally the global train mean.

## Threshold baseline

Selects one numeric feature and one train-window median threshold. The selected split maximizes an auditable train-only separation score subject to minimum side support.

## Logistic classifier

Predicts win probability from sparse causal features. It uses deterministic SGD, L2 regularization, bounded weights, and train-only encoding.

## Ridge R regression

Predicts primary R using the same causal feature surface. It uses deterministic SGD and L2 regularization.

## Constrained ensemble

Uses a fixed non-negative convex blend:

- bucket probability + logistic probability;
- bucket average R + ridge predicted R.

Weights sum to one and are not optimized on the test window.
