---
title: Multi-Model Stacking and Ensemble Governance
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- gap-closure
- canonical
---

# Objective

Combine diverse models only when diversity, calibration and protected incremental value exceed the selection and operational cost of ensembling.

# Allowed forms

- Deep ensembles for epistemic disagreement.
- Cross-fitted stacking on calibration/selection roles.
- Regime-gated experts with fallback.
- Median/trimmed distribution aggregation.
- Conservative lower-confidence-bound voting.

# Prohibitions

- Training a meta-learner on locked-final outcomes.
- Hidden candidate expansion through ensemble subset search.
- Averaging unsupported models into apparent confidence.
- Ensemble disagreement suppression.

# Required evidence

Component trial universe, diversity matrix, calibration, subgroup support, ablation, failure correlation, latency/export cost and decision-stability report.
