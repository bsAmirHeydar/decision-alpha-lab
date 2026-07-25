# Installation — SAED V4-00

## Prerequisite

Apply the SAED V4 architecture patch first. This patch assumes the canonical V4 documentation tree exists but does not modify UCEE core implementations.

## Apply

Extract the ZIP into the repository root with overwrite enabled. The archive contains only paths listed in `SAED_V4_00_FILE_INDEX.txt`.

## Validate

```powershell
$env:PYTHONPATH = "lab/11_strategy_factory/python"
python tools/strategy_factory/saed_v4_00/run_saed_v4_00_tests.py
python tools/strategy_factory/saed_v4_00/validate_saed_v4_00_contracts.py
python tools/strategy_factory/saed_v4_00/check_saed_v4_00_mql5_static.py
python tools/strategy_factory/saed_v4_00/validate_saed_v4_00_delivery.py
```

## Windows-only external evidence

Run `tools/strategy_factory/saed_v4_00/compile_saed_v4_00_constitution.ps1` on the actual MetaTrader/MetaEditor environment and preserve logs as `external_actual` evidence. Static validation must not be relabeled as compilation.
