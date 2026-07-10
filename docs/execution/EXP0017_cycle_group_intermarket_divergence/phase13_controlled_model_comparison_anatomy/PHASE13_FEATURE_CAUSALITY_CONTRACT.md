# Phase 13 Feature Causality Contract

## Allowed raw information

Only information known at or before confirmation is eligible:

- cycle-group identity and duration;
- current/reference cycle indices and reference age;
- direction and side;
- hunter, clean, and role identity;
- confirmation-time hour/session;
- stop-reference distance available at confirmation.

## Explicitly forbidden

- all forward outcome windows;
- MFE and MAE;
- labels;
- full-day range and ratios derived from it when the range uses future bars;
- Phase 09 full-history ranking enrichments;
- shortlist membership;
- any field whose value depends on later candles.

## Derived features

Permitted derived features are computed from allowed fields only:

- log cycle duration;
- reference age;
- direction/side codes;
- cyclical time-of-day encoding;
- log stop distance;
- train-only categorical one-hot encoding.

The denylist is emitted into `phase13_leakage_audit.csv` for each run.
