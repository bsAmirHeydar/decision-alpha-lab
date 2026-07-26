---
id: AIEOS2-858AEAEE00C7
title: "Alpha Lab Repository Contract"
type: standard
status: active
domain: engineering
version: 2.0.0
created: 2026-07-10
updated: 2026-07-10
tags:
  - ai-engineering
  - alpha-lab
  - engineering
---
# Alpha Lab Repository Contract

## Repository Topology

| Path | Owner / Purpose | Prohibited Use |
|---|---|---|
| `docs/` | Philosophy, architecture, policy, knowledge | Runtime state and generated datasets |
| `lab/01_observation/` | Observable facts and raw anomalies | Conclusions or production rules |
| `lab/02_hypotheses/` | Falsifiable mechanism statements | Untracked code patches |
| `lab/03_experiments/` | Reproducible experiment packets | Live capital authority |
| `lab/04_analysis/` | Exploratory and explanatory analysis | Production promotion by implication |
| `lab/05_validation/` | OOS, robustness, stress, benchmark evidence | New untested features |
| `lab/06_production/` | Approved signals/models/contracts | Experimental logic |
| `lab/07_monitoring/` | Drift, incidents, health, retirement evidence | Hidden strategy changes |
| `lab/08_archive/` | Rejected/retired knowledge | Active imports or runtime dependency |
| `lab/09_execution/` | Broker adapters, MQL5 execution, logs | Research truth or model training |
| `lab/10_infrastructure/` | CI, config, data utilities, tests | Domain decisions without specs |
| `registry/` | Canonical IDs and status indices | Duplicated unversioned truth |
| `data/` | Data contracts and controlled data pointers | Secrets or undocumented generated files |

## Ownership Rules

- Every mutable state has one owning module.
- Renderers do not own domain state.
- Adapters do not redefine domain semantics.
- Execution consumes approved decision contracts; it does not invent research logic.
- Generated outputs are never edited manually as source truth.
- Cache directories are disposable and reproducible.

## Dependency Direction

```text
Domain doctrine
  → specifications/contracts
    → pure algorithm/core state
      → signals/scenarios
        → persistence/observability
          → adapters/renderers/execution
```

Dependencies may point downward only. Execution must not become a hidden source of domain truth.

## File Placement Decision

Before adding a file, answer:

1. Is it source, generated, evidence, configuration, or documentation?
2. What stage owns it?
3. Is it deterministic and reproducible?
4. Who may mutate it?
5. What is its retention/retirement rule?
