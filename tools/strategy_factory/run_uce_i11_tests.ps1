param([string]$RepoRoot = ".")
$ErrorActionPreference = "Stop"
$Root = (Resolve-Path $RepoRoot).Path
$env:PYTHONPATH = Join-Path $Root "lab\11_strategy_factory\python"
python -m pytest -q (Join-Path $Root "lab\11_strategy_factory\tests\phase_uce_i11_experiments")
python (Join-Path $Root "tools\strategy_factory\check_uce_i11_boundaries.py")
python (Join-Path $Root "tools\strategy_factory\check_uce_i11_mql5_static.py")
python (Join-Path $Root "tools\strategy_factory\validate_uce_i11_delivery.py")
