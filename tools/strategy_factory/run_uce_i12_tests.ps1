param([string]$RepoRoot = ".")
$ErrorActionPreference = "Stop"
$root = (Resolve-Path $RepoRoot).Path
$env:PYTHONPATH = Join-Path $root "lab\11_strategy_factory\python"
python -m pytest -q (Join-Path $root "lab\11_strategy_factory\tests\phase_uce_i12_promotion")
python (Join-Path $root "tools\strategy_factory\check_uce_i12_boundaries.py")
python (Join-Path $root "tools\strategy_factory\check_uce_i12_mql5_static.py")
python (Join-Path $root "tools\strategy_factory\validate_uce_i12_delivery.py") $root
