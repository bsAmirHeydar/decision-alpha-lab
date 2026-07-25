param([string]$RepoRoot = ".")
$ErrorActionPreference = "Stop"
Set-Location $RepoRoot
python .\tools\engineering\run_engineering_policy.py .
python .\src\engine\tooling\strategy_factory\check_uce_i03_boundaries.py .
python .\src\engine\tooling\strategy_factory\check_uce_i03_mql5_static.py .
python .\src\engine\tooling\strategy_factory\validate_uce_i03_delivery.py .
$env:PYTHONPATH = (Resolve-Path ".\src\engine\packages").Path
python -m compileall -q .\src\engine\packages\strategy_factory_treatments_v3
python -m strategy_factory_treatments_v3.cli conformance
pytest -q --import-mode=importlib .\tests\legacy\strategy_factory\v1\phase_uce_i01_contracts .\tests\legacy\strategy_factory\v1\phase_uce_i02_contexts .\tests\legacy\strategy_factory\v1\phase_uce_i03_treatments
