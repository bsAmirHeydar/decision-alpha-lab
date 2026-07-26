# Decision Alpha Lab Strategy Factory Patch

This additive patch installs the shared **Anatomy-to-Research-to-Execution
Strategy Factory**. It converts any approved market anatomy into one common
pipeline for:

- canonical event and known-time contracts;
- immutable feature snapshots;
- bounded entry/stop/exit candidate generation;
- causal path simulation and realistic cost accounting;
- standard statistics and conditional attribution;
- purged walk-forward validation;
- event-cluster bootstrap and dependence handling;
- false-discovery, reality-check, Deflated Sharpe, and PBO controls;
- rule baselines, meta-labeling, regression, and candidate ranking;
- model registry, model cards, calibration, champion/challenger, and drift;
- paper execution, hard risk gates, broker-adapter boundaries, reconciliation,
  incident response, promotion, and retirement;
- rapid scaffolding for future anatomy plugins.

## Main entry points

Documentation:

```text
docs/alpha_lab_master_architecture/strategy_factory/00_start_here/00_STRATEGY_FACTORY_MOC.md
```

Python engine:

```text
lab/11_strategy_factory/python/strategy_factory/
```

CLI:

```powershell
python .\lab\11_strategy_factory\sf.py --help
```

MQL5 shared contracts:

```text
lab/11_strategy_factory/mql5/Include/AlphaLab/StrategyFactory/
```

## Add a new anatomy

```powershell
python .\lab\11_strategy_factory\sf.py scaffold `
  EXP0019_new_anatomy `
  --output-root .\lab\03_experiments
```

The generated packet contains a manifest, doctrine, adapter scaffold, tests,
and fixture directory. The new strategy reuses the shared statistics,
anti-overfit, training, paper, risk, and execution architecture.

## Verification completed for this patch

- Python compile: passed
- Pytest: 20 passed
- Example manifest validation: passed
- New-strategy scaffold and generated-manifest validation: passed
- Reference bar-data audit: passed
- Reference end-to-end pipeline: passed
- MQL5 static compatibility scan: 0 errors, 0 warnings
- Alpha Lab engineering-policy validation: 0 errors, 0 warnings
- Obsidian internal-link audit: 0 broken links
- Collision audit against the supplied repository: 0 path collisions

## Important boundary

The patch includes MQL5 contracts, candidate/risk structures, a paper broker,
and a live bridge interface. It intentionally does **not** add `OrderSend`,
`OrderCheck`, or `CTrade` live authority. A broker-specific live adapter must be
implemented and promoted as a separate reviewed phase after paper validation.

The Python artifact writer uses Parquet when `pyarrow` is available. During QA
in the current container, `pyarrow` was unavailable, so the reference run used
the built-in CSV fallback. The repository already declares `pyarrow` in its
requirements; official production runs should install it and treat fallback as
a warning.
