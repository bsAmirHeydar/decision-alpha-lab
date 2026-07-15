$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path
$env:PYTHONPATH = Join-Path $Root "lab/11_strategy_factory/python"
python -m pytest -q (Join-Path $Root "lab/11_strategy_factory/tests/phase_uce_i18_production_qualification") --import-mode=importlib
python (Join-Path $Root "tools/strategy_factory/check_uce_i18_boundaries.py")
python (Join-Path $Root "tools/strategy_factory/check_uce_i18_mql5_static.py")
python (Join-Path $Root "tools/strategy_factory/validate_uce_i18_delivery.py")
