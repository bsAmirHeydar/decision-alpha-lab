---
title: RTHP MT5 Automation — Implementation Release and Operator Command
status: implemented-reference-ready-for-real-terminal-smoke
version: 1.0.0
updated: 2026-07-22
---

# Implementation Release

The context-owned package `strategy_factory_rthp_mt5_activation_v1` implements:

- lazy loading of the official MetaTrader 5 Python bridge;
- read-only terminal discovery, initialization, health checks, and shutdown;
- exact or case-insensitive broker-symbol resolution;
- Market Watch selection and immutable symbol-metadata capture;
- automatic common-range acquisition of closed M1 bars;
- chunked UTC requests with overlap, retry, deduplication, and receipts;
- rejection of incomplete current bars and every sub-M1 canonical source;
- session-aware paired-symbol quality gates;
- immutable M1 source freezing and source binding;
- M1 interval-censored RTHP materialization without synthetic ticks;
- delegation to the existing RTHP Train Activation package and shared trainers;
- immutable run verification and hash-ledger emission.

No central Strategy Factory, SAED, UCEE, ACL, dataset, trainer, validation, promotion, runtime, canonical Context, order, or capital engine is modified.

## Symbol-only operator command

The default command requires only the two MetaTrader symbol names. The terminal is auto-discovered and the immutable output is placed outside the repository under `%LOCALAPPDATA%\AlphaLab\runs\rthp_mt5` unless `ALPHA_LAB_RUN_ROOT` is set.

```powershell
$env:PYTHONPATH = "lab\11_strategy_factory\python"
python -m strategy_factory_rthp_mt5_activation_v1 preflight-symbols --primary <PRIMARY_MT5_SYMBOL> --secondary <SECONDARY_MT5_SYMBOL>
python -m strategy_factory_rthp_mt5_activation_v1 run-symbols --primary <PRIMARY_MT5_SYMBOL> --secondary <SECONDARY_MT5_SYMBOL>
```

Optional controls such as an explicit terminal path, output root, lookback, task selection, and family filters are advanced run configuration only. They do not change Context semantics.

## Explicit configuration command

```powershell
$env:PYTHONPATH = "lab\11_strategy_factory\python"
python -m strategy_factory_rthp_mt5_activation_v1 validate-config --config <resolved-config.json>
python -m strategy_factory_rthp_mt5_activation_v1 preflight --config <resolved-config.json>
python -m strategy_factory_rthp_mt5_activation_v1 run --config <resolved-config.json>
python -m strategy_factory_rthp_mt5_activation_v1 verify-run --run-root <immutable-run-root>
```
