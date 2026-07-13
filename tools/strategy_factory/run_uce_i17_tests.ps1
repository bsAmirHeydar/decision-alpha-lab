$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path
$env:PYTHONPATH = Join-Path $Root "lab/11_strategy_factory/python"
python -m pytest -q (Join-Path $Root "lab/11_strategy_factory/tests/phase_uce_i17_portfolio") --import-mode=importlib
python (Join-Path $Root "tools/strategy_factory/check_uce_i17_boundaries.py")
python (Join-Path $Root "tools/strategy_factory/check_uce_i17_mql5_static.py")
python (Join-Path $Root "tools/strategy_factory/validate_uce_i17_delivery.py")
