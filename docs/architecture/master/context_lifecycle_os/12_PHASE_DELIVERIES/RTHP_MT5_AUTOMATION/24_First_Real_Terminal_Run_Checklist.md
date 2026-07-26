---
title: RTHP MT5 Automation — First Real Terminal Run Checklist
status: release-gate
version: 1.0.0
updated: 2026-07-22
---

# First Real Terminal Run

## Preconditions

1. Use Windows and the same Python environment used for Alpha Lab.
2. Install the context-owned Windows requirement file:

```powershell
python -m pip install -r "lab\11_strategy_factory\generated_contexts\rthp_cross_symbol_cycle_divergence\mt5_activation\v1\requirements-windows.txt"
```

3. Open and log in to the intended MetaTrader 5 terminal.
4. Verify that the terminal is connected to the intended server/account.
5. Increase the terminal's available chart history sufficiently for the requested lookback.
6. Confirm the exact broker-facing names of the two symbols.
7. Confirm that both symbols represent the intended contracts. The adapter does not silently stitch futures contracts.

## Preflight

```powershell
$env:PYTHONPATH = "lab\11_strategy_factory\python"
python -m strategy_factory_rthp_mt5_activation_v1 preflight-symbols --primary <PRIMARY_MT5_SYMBOL> --secondary <SECONDARY_MT5_SYMBOL>
```

Review:

- terminal and server receipt;
- hashed account identity;
- resolved symbols;
- frozen tick sizes and contract metadata;
- resolved common UTC range;
- canonical source floor `M1_CLOSED_BARS`;
- `sub_m1_requested = false`;
- absence of trading authority.

## One-click acquisition and train activation

```powershell
python -m strategy_factory_rthp_mt5_activation_v1 run-symbols --primary <PRIMARY_MT5_SYMBOL> --secondary <SECONDARY_MT5_SYMBOL>
```

The command automatically performs M1 acquisition, data-quality validation, immutable source freezing, RTHP materialization, feature/label compilation, batch freezing, shared-engine training, and run verification.

## Mandatory evidence review

Review the run's:

- terminal receipt;
- primary and secondary symbol metadata;
- chunk acquisition receipts;
- M1 quality report;
- source binding and SHA-256 hashes;
- occurrence, reference-state, cycle-instance, and role-price-path ledgers;
- M1 materialization report;
- feature and label materialization reports;
- immutable batch manifest;
- task results and train activation report;
- final hash ledger and completion marker.

A successful research run does not create production-capital authority, order authority, or a promoted trading policy.
