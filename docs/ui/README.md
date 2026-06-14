# Quant Lab UI

The UI is a Research Operating System for Decision Alpha Lab.

It is not a chart-only dashboard. It is designed to make every research object traceable:

```text
Observation → Hypothesis → Metric → Experiment → Analysis → Validation → Production → Monitoring
```

The first supported visual adapter is `M0001 — Relative Territory Volatility`.

## Principles

1. Python owns market logic.
2. React only renders typed visualization contracts.
3. Every document, metric, experiment, and run must be discoverable.
4. Chart overlays, tables, and inspectors must stay synchronized.
5. The default visual state is quiet; hover and selection reveal detail.
