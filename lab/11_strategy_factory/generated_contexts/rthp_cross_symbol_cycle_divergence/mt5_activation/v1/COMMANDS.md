# Commands

## Install the Windows-only MetaTrader bridge

```powershell
python -m pip install -r "lab\11_strategy_factory\generated_contexts\rthp_cross_symbol_cycle_divergence\mt5_activation\v1\requirements-windows.txt"
```

## Symbol-only one-click workflow

The terminal may be auto-discovered. The operator selects only the two symbols.

```powershell
$env:PYTHONPATH = "lab\11_strategy_factory\python"
python -m strategy_factory_rthp_mt5_activation_v1 preflight-symbols --primary <PRIMARY_MT5_SYMBOL> --secondary <SECONDARY_MT5_SYMBOL>
python -m strategy_factory_rthp_mt5_activation_v1 run-symbols --primary <PRIMARY_MT5_SYMBOL> --secondary <SECONDARY_MT5_SYMBOL>
```

The default immutable output is written outside the repository under `%LOCALAPPDATA%\AlphaLab\runs\rthp_mt5`. Set `ALPHA_LAB_RUN_ROOT` or pass `--output-root` to override it.

## Explicit configuration workflow

```powershell
$env:PYTHONPATH = "lab\11_strategy_factory\python"
python -m strategy_factory_rthp_mt5_activation_v1 validate-config --config <config>
python -m strategy_factory_rthp_mt5_activation_v1 preflight --config <config>
python -m strategy_factory_rthp_mt5_activation_v1 run --config <config>
python -m strategy_factory_rthp_mt5_activation_v1 verify-run --run-root <run-root>
```
