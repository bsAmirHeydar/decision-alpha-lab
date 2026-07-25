$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path
$env:PYTHONPATH = Join-Path $Root "src/engine/packages"
python -m pytest -q (Join-Path $Root "tests/legacy/strategy_factory/v1/phase_uce_i19_production_operations") --import-mode=importlib
python (Join-Path $Root "src/engine/tooling/strategy_factory/check_uce_i19_boundaries.py")
python (Join-Path $Root "src/engine/tooling/strategy_factory/check_uce_i19_mql5_static.py")
python (Join-Path $Root "src/engine/tooling/strategy_factory/validate_uce_i19_delivery.py")
