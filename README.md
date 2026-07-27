# Decision Alpha Lab

Decision Alpha Lab is an evidence-driven quantitative research and platform-engineering repository. It converts approved market concepts into deterministic, reviewable, replayable, testable and reversible software without allowing research artifacts or AI outputs to acquire execution authority implicitly.

## Current consolidation state

- UC-01 — Preserve and Baseline: **ACCEPTED**
- UC-02 — Authority and Standardization: **ACCEPTED**
- UC-03 — Physical Reorganization: **ACCEPTED**
- UC-04 — Semantic and Logic Unification: **IN PROGRESS**
  - UC04-W0 Foundation and Recovery: **ACCEPTED**
  - UC04-W1 Deterministic MQL5 Formatting Primitive: **AUTHORIZED**

Canonical program documentation:
`docs/architecture/master/01_UNIFIED_CONSOLIDATION_AND_PLATFORM_SEAL/`

## Engineering preflight

```text
python tools/engineering/run_engineering_policy.py .
python -m tools.consolidation.uc04w0.verify --repo-root .
```

## Authority boundary

The current stage grants no semantic retirement, deletion, order or capital authority. Candidate-specific logic-preservation evidence is mandatory before consumer cutover.
