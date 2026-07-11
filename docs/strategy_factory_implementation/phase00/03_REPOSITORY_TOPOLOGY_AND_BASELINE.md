---
title: "Repository Topology and Baseline"
tags: [strategy-factory, phase-00, repository-map]
status: canonical
---

# Repository Topology and Baseline

## Audited snapshot

The audited Git commit is:

```text
8a5472e6d5113386263a6665159c45e0d68c5876
```

The snapshot is materially earlier than the large multi-strategy repository discussed elsewhere. Its implemented topology is compact:

```text
docs/
registry/
lab/
├── 01_observation/
├── 02_hypotheses/
├── 03_experiments/
├── 04_analysis/
├── 05_validation/
├── 06_production/
├── 07_monitoring/
├── 08_archive/
├── 09_execution/
├── 10_infrastructure/
├── cache_data/
├── cache_nodes/
├── cache_metrics/
└── core/
    ├── CP0000_market_data/
    ├── CP0000_sample/
    └── CP0001_structural_nodes/
```

## Implemented path

The functional code path is:

```text
MetaTrader5 API
→ MT5Connector
→ MarketDataEngine
→ ParquetStore
→ LRuleNodeDetector
→ M0001RTV
→ Parquet metric artifacts
```

## Research path maturity

### Implemented

- MT5 connection and OHLC retrieval.
- Timeframe enumeration.
- Parquet market-data cache.
- Incremental data synchronization.
- MQL-style candle accessors.
- L-rule structural high/low extraction.
- Confirmed and provisional node logic.
- Node Parquet persistence.
- Revisit-aware relative territory volatility metric.
- Metric Parquet persistence.
- Research hypotheses and anatomy documentation.

### Partially implemented

- Experiment scaffolding.
- Registry structure.
- Validation directory.
- Production and monitoring directory ownership.
- Execution boundary folders.

### Not implemented in this snapshot

- Canonical event contracts.
- Feature snapshots and known-time provenance.
- Candidate entry/stop/exit generation.
- Shared outcome simulator.
- Shared cost models.
- Statistical report engine.
- Anti-overfit suite.
- Walk-forward model training.
- Model registry.
- Compiled decision runtime.
- Portfolio risk.
- Paper broker.
- MQL5 execution bridge.
- EXP0017, NDS, Daye, ICT, or Astro programs.

## Quantitative baseline

| Category | Count |
|---|---:|
| Total audited files | 103 |
| Documentation files | 37 |
| Python source files | 13 |
| Registry/config files | 11 |
| Generated/market-data artifacts | 20 |
| Ephemeral runtime artifacts | 4 |
| Empty files | 54 |

The high empty-file count is not automatically a defect. Many are intentional placeholders. It does mean that folder presence must not be interpreted as implemented capability.

## Git history signal

The latest commits demonstrate a coherent progression:

```text
Market-data connector
→ Market-data engine
→ Structural nodes
→ H0002 node territory hypothesis
→ M0001 relative territory volatility
```

This supports selecting CP0001/M0001 as the local foundation pilot.
