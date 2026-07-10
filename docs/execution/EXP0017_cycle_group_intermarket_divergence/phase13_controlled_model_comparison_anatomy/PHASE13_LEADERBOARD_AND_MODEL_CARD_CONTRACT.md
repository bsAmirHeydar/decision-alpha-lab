# Phase 13 Leaderboard and Model Card Contract

## Leaderboard

Classification ranks combine:

- log loss;
- Brier score;
- calibration error;
- balanced accuracy.

Regression ranks combine:

- RMSE;
- MAE;
- R-squared;
- sign accuracy.

Rank aggregation is descriptive and deterministic. It is not an execution gate.

## Model cards

Every model card records:

- task and purpose;
- feature boundary;
- training method;
- walk-forward validation basis;
- fold count;
- leaderboard position;
- known limitations;
- explicit lack of execution authority.
