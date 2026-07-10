# Phase 13 Python Engine Architecture

## Input layer

- Phase 10 model-ready dataset;
- Phase 11 fixed fold plan;
- Phase 12.5 readiness summary.

## Feature layer

Train-only encoder:

- numerical train means and scales;
- categorical vocabularies learned on train only;
- unknown-category handling;
- sparse feature dictionaries.

## Model layer

- hierarchical bucket baseline;
- median threshold baseline;
- deterministic sparse logistic SGD;
- deterministic sparse ridge SGD;
- fixed convex ensemble.

## Evaluation layer

Classification:

- log loss;
- Brier score;
- accuracy;
- balanced accuracy;
- precision and recall;
- calibration intercept/slope;
- expected calibration error.

Regression:

- MAE;
- RMSE;
- R-squared;
- Pearson correlation;
- sign accuracy.

## Evidence layer

- fold comparison;
- prediction ledger;
- calibration bins;
- coefficient importance;
- leaderboard;
- fold stability;
- leakage audit;
- model cards;
- HTML report;
- experiment registry.
