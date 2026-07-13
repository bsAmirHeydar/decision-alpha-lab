---
type: strategy-factory-document
status: canonical
title: "Model Registry and Model Card"
tags:
  - strategy-factory
---

# Model Registry and Model Card

Every model artifact is immutable, versioned, and bound to exact schemas and folds.

## Registry fields

Model ID/version, strategy version, task, feature schema, candidate schema, label version, fold plan, training period, random seed, hyperparameters, metrics, calibration, artifact hash, runtime dependencies, owner, status, and retirement reason.

## Model card

Document intended use, prohibited use, training data, evaluation, failure modes, missing-feature behavior, drift indicators, decision threshold, explainability, and residual risks. A model without a complete card cannot enter paper execution.

## Compatibility

Inference checks feature names/order/types, strategy version, policy universe, and artifact hash. Mismatch means skip, never best-effort inference.

