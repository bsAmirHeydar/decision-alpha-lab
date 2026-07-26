---
title: "Repository and Module Map"
tags:
  - strategy-factory
  - implementation-roadmap
  - alpha-lab
status: canonical
doc_version: 1.0.0
---

# Repository and Module Map

```text
lab/11_strategy_factory/
├── python/strategy_factory/
│   ├── contracts/
│   ├── identity/
│   ├── plugins/
│   ├── compiler/
│   ├── adapters/
│   ├── context/
│   ├── features/
│   ├── candidates/
│   ├── simulation/
│   ├── costs/
│   ├── labels/
│   ├── statistics/
│   ├── nulls/
│   ├── validation/
│   ├── anti_overfit/
│   ├── models/
│   ├── registry/
│   ├── decision/
│   ├── portfolio/
│   ├── risk/
│   ├── paper/
│   ├── execution/
│   ├── monitoring/
│   ├── artifacts/
│   ├── reporting/
│   └── cli/
├── mql5/Include/AlphaLab/StrategyFactory/
│   ├── Contracts/
│   ├── Context/
│   ├── Features/
│   ├── Decision/
│   ├── Risk/
│   ├── Paper/
│   ├── Broker/
│   └── Telemetry/
├── schemas/
├── examples/
├── fixtures/
├── tests/
├── benchmarks/
└── implementation_program/
```

## Boundary Rule

No strategy-specific market meaning may be imported into the stable kernel. A module containing `hook`, `f3`, `smt`, `daye`, `ict`, or `astro` belongs in a plugin package or experiment adapter, not in the core runtime.
