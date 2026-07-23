# Commands

## Install the Windows-only MetaTrader bridge

```powershell
python -m pip install -r "lab\11_strategy_factory\generated_contexts\rthp_cross_symbol_cycle_divergence\mt5_activation\v1\requirements-windows.txt"
```

## Set the repository Python path

```powershell
$env:PYTHONPATH = (Resolve-Path 'lab\11_strategy_factory\python').Path
```

## Real terminal preflight

```powershell
python -m strategy_factory_rthp_mt5_activation_v1 preflight-symbols --primary '#USSPX500' --secondary '#USNDAQ100' --lookback-days 60 --minimum-common-days 30
```

## Short real Train smoke

```powershell
$RunRoot = Join-Path $env:LOCALAPPDATA ("AlphaLab\runs\rthp_mt5\smoke_train_" + (Get-Date -Format 'yyyyMMdd_HHmmss'))
python -m strategy_factory_rthp_mt5_activation_v1 run-symbols --primary '#USSPX500' --secondary '#USNDAQ100' --lookback-days 14 --minimum-common-days 10 --task-id 'rthp.hunter.polarity_aligned_direction.15m' --output-root $RunRoot
python -m strategy_factory_rthp_mt5_activation_v1 verify-run --run-root $RunRoot
```

## Long-horizon Train after calendar hardening

The `AUTO` session calendar resolves both US index CFD symbols to `US_INDEX_CFD_NY_V1`. Declared holiday closures are recorded, never forward-filled, and no longer treated as unexplained outages when paired boundary evidence exists.

```powershell
$RunRoot = Join-Path $env:LOCALAPPDATA ("AlphaLab\runs\rthp_mt5\train_60d_" + (Get-Date -Format 'yyyyMMdd_HHmmss'))
python -m strategy_factory_rthp_mt5_activation_v1 run-symbols --primary '#USSPX500' --secondary '#USNDAQ100' --lookback-days 60 --minimum-common-days 30 --task-id 'rthp.hunter.polarity_aligned_direction.15m' --output-root $RunRoot
python -m strategy_factory_rthp_mt5_activation_v1 verify-run --run-root $RunRoot
```

## Explicit configuration workflow

```powershell
python -m strategy_factory_rthp_mt5_activation_v1 validate-config --config <config>
python -m strategy_factory_rthp_mt5_activation_v1 preflight --config <config>
python -m strategy_factory_rthp_mt5_activation_v1 run --config <config>
python -m strategy_factory_rthp_mt5_activation_v1 verify-run --run-root <run-root>
```

The default immutable output is written outside the repository under `%LOCALAPPDATA%\AlphaLab\runs\rthp_mt5`. Set `ALPHA_LAB_RUN_ROOT` or pass `--output-root` to override it.
