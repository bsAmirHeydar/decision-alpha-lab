# Decision Alpha Lab — Strategy Factory V2

This is the standalone, expanded replacement for the original Strategy Factory patch. It contains the complete V1 anatomy-to-research platform plus the V2 ultra-modular and low-latency context-to-decision architecture.

## What V2 adds

- versioned plugin kernel and capability registry;
- startup-compiled immutable strategy plans;
- feature dependency DAG and cycle detection;
- incremental context recomputation with generation-aware TTL caching;
- fixed-order numeric feature vectors;
- precompiled bounded candidate templates;
- pre-resolved local model routes;
- calibration, multi-objective utility, explicit abstention, and deterministic fallback;
- idempotency and duplicate-decision protection;
- per-stage latency budgets and bounded telemetry;
- immutable generations and atomic hot swap;
- champion/challenger shadow serving architecture;
- MQL5 V2 contracts for context, plugins, decisions, latency, telemetry, and runtime gates;
- expanded anti-overfit, testing, migration, and operations documentation;
- V2 scaffolding, plan compilation, one-shot decision, and benchmark commands.

## Canonical entry points

- `docs/alpha_lab_master_architecture/strategy_factory_v2/00_start_here/00_STRATEGY_FACTORY_V2_MOC.md`
- `docs/alpha_lab_master_architecture/strategy_factory/00_start_here/00_STRATEGY_FACTORY_MOC.md` — original V1 deep research canon
- `lab/11_strategy_factory/python/strategy_factory/`
- `lab/11_strategy_factory/mql5/Include/AlphaLab/StrategyFactoryV2/`

## Core design

```text
Any Anatomy Engine
  -> Small Adapter
  -> Canonical Event
  -> Incremental Context DAG
  -> Compiled Candidate Templates
  -> Local Model Routes
  -> Utility Ranking + Abstention
  -> Decision Envelope
  -> Independent Hard Risk Gate
  -> Paper / Broker Adapter
```

The research lane remains exhaustive. The live lane is bounded, in-memory, version-pinned, and measurable.

## Important execution boundary

The patch does not introduce live order authority. The V2 MQL5 layer contains no `OrderSend`, `OrderCheck`, or `CTrade`. It is designed to connect to the repository's existing paper, broker-validation, lifecycle, risk, and promotion gates after the relevant strategy is approved.

## Verification performed for this artifact

- Python compileall: passed
- Combined V1 + V2 pytest suite: 45 passed
- V2 plan compilation: passed
- V2 reference decision: passed
- V2 reference benchmark: passed
- ZIP integrity: checked during packaging

Latency measurements from the reference environment are not guarantees for another machine, broker, model, or topology. V2 provides benchmark tooling and per-generation budgets so real targets can be measured correctly.
