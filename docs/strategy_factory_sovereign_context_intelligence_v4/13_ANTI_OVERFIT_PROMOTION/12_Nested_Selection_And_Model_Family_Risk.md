---
title: Nested Selection and Model-Family Risk
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

Account for selection across hyperparameters, features, treatments, model families, representations, objectives, seeds and ensemble choices.

# Protocol

- Outer folds estimate the entire selection procedure.
- Inner folds choose all preprocessing, features, thresholds, calibration, model family and treatment policy.
- Trial/exposure universe includes invalid, failed, pruned and manually inspected candidates.
- Family-level search budgets are predeclared.
- Locked-final is opened once under signed rules.

# Model-family risk

Report the probability that the selected family is a transient winner, rank instability across outer folds, family complexity penalties, and performance of the selection algorithm—not only the chosen model.

# Required challenges

PBO/CSCV, deflated performance, family ablation, compute-matched baselines, random-family controls and prospective confirmation.
