# Python Mirror Boundary

Python is the second-priority implementation because it performs work MQL5 should not perform in the live path: large joins, bootstraps, candidate search, walk-forward training, model comparison, and report generation.

## Mirror duties

- parse MQL5 artifacts;
- enforce the same validation rules;
- reproduce stable IDs;
- reject schema drift;
- expose immutable research objects;
- create training tables without changing event semantics;
- generate diagnostics and migration reports.

## Forbidden behavior

Python must not infer a missing event time, silently reorder simultaneous events, replace missing with zero without policy, regenerate an event using future bars, or assign a different ID to the same canonical MQL5 payload.

## Export back to MQL5

Later model exports will contain a fixed feature schema, normalization parameters, model coefficients/tree representation, thresholds, calibration, and artifact identity. MQL5 remains responsible for decision-time feature freshness and risk gating.
