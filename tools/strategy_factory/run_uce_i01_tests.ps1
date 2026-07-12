$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path
$env:PYTHONPATH = Join-Path $RepoRoot "lab/11_strategy_factory/python"
python -m compileall -q (Join-Path $RepoRoot "lab/11_strategy_factory/python/strategy_factory_contracts_v3")
python (Join-Path $PSScriptRoot "check_uce_i01_boundaries.py") $RepoRoot
python (Join-Path $PSScriptRoot "check_uce_i01_mql5_static.py") $RepoRoot
python (Join-Path $PSScriptRoot "validate_uce_i01_delivery.py") $RepoRoot
python -m strategy_factory_contracts_v3.cli check-vector-file (Join-Path $RepoRoot "lab/11_strategy_factory/test_vectors/v3/uce_i01_cross_language_vectors.json")
pytest -q (Join-Path $RepoRoot "lab/11_strategy_factory/tests/phase_uce_i01_contracts")
