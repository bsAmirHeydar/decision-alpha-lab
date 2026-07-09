# HOOK CANON STEP 7 — Post-F3 Recognition Code

This patch implements the documented post-F3 Hook recognition families in MQL5.

## Families

- `F3H_DIRECT_STRUCTURAL`
- `F3H_DIRECT_GEOMETRIC_80`
- `F3H_DELAYED_STRUCTURAL`
- `F3H_DELAYED_GEOMETRIC_80`

## Important constraint

The patch does not rebuild the Phase02 sequence engine. It classifies the post-F3 candidates that Phase02 already emits. Therefore geometric-80 detection is represented by Phase02 candidates with valid cycle geometry and at least the configured completion percentage.
