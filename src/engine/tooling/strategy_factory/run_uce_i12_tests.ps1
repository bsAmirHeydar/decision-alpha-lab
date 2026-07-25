param([string]$RepoRoot = ".")
$ErrorActionPreference = "Stop"
$root = (Resolve-Path $RepoRoot).Path
$env:PYTHONPATH = Join-Path $root "src\engine\packages"
python -m pytest -q (Join-Path $root "tests\legacy\strategy_factory\v1\phase_uce_i12_promotion")
python (Join-Path $root "src\engine\tooling\strategy_factory\check_uce_i12_boundaries.py")
python (Join-Path $root "src\engine\tooling\strategy_factory\check_uce_i12_mql5_static.py")
python (Join-Path $root "src\engine\tooling\strategy_factory\validate_uce_i12_delivery.py") $root
