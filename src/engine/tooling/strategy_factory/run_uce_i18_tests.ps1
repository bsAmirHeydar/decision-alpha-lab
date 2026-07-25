$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path
$env:PYTHONPATH = Join-Path $Root "src/engine/packages"
python -m pytest -q (Join-Path $Root "tests/legacy/strategy_factory/v1/phase_uce_i18_production_qualification") --import-mode=importlib
python (Join-Path $Root "src/engine/tooling/strategy_factory/check_uce_i18_boundaries.py")
python (Join-Path $Root "src/engine/tooling/strategy_factory/check_uce_i18_mql5_static.py")
python (Join-Path $Root "src/engine/tooling/strategy_factory/validate_uce_i18_delivery.py")
