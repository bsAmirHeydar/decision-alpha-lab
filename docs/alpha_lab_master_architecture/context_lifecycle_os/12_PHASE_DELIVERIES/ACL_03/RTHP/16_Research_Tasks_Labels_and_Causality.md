# RTHP Research Tasks, Labels, and Causality

## Separation of truth and outcome

RTHP Context truth ends at the confirmed occurrence and its factual lifecycle. Future return, MFE, MAE, exhaustion, duration, family strength, and reference-age effectiveness are research outcomes. They are not fields of Context truth and never become feature values merely because a task uses them as labels.

## Registered task families

The package declares 30 task references covering:

- reference exhaustion within 15, 30, and 60 minutes;
- reference exhaustion by active-cycle end;
- time to reference exhaustion;
- polarity-signed returns for Hunter and Protected roles;
- polarity-aligned direction for both roles;
- 60-minute MFE and MAE for both roles;
- family-relative strength;
- reference-age effectiveness;
- family-relative exhaustion strength.

## Role-local outcome construction

Hunter and Protected outcomes are constructed from role-local price paths. Prices of different instruments are not directly subtracted. Return and excursion calculations use the symbol assigned to the role, its own price basis, and its own tick-size normalization.

## Label maturity

Each label declares its maturity horizon, censoring behavior, feature eligibility, and selection segregation. A label is unavailable before its maturity time. Unmatured and incomplete paths are masked or censored; they are not set to zero or inferred.

## Leakage controls

- feature cut: `observation_cut_ms`;
- label-only ledgers are segregated from feature materialization;
- future perturbation leaves past hashes unchanged;
- overlapping horizons are clustered and purged by shared validation;
- source revisions append lineage rather than rewriting prior observations;
- final-test sealing remains owned by the shared engine.

## Discovery scope

The discovery contract allows versioned experiments over cycle definition, boundaries, pairing, family definition, lookback, reference age, confirmation timeframe, and factual validity horizon. Numeric ranges require explicit Search Authority. Entry, stop, target, position size, and capital allocation remain forbidden in Context discovery.
