$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path
$env:PYTHONPATH = Join-Path $RepoRoot "src/engine/packages"
python -m compileall -q (Join-Path $RepoRoot "src/engine/packages/strategy_factory_contracts_v3")
python (Join-Path $PSScriptRoot "check_uce_i01_boundaries.py") $RepoRoot
python (Join-Path $PSScriptRoot "check_uce_i01_mql5_static.py") $RepoRoot
python (Join-Path $PSScriptRoot "validate_uce_i01_delivery.py") $RepoRoot
python -m strategy_factory_contracts_v3.cli check-vector-file (Join-Path $RepoRoot "tests/fixtures/legacy/strategy_factory/v3/uce_i01_cross_language_vectors.json")
pytest -q (Join-Path $RepoRoot "tests/legacy/strategy_factory/v1/phase_uce_i01_contracts")
