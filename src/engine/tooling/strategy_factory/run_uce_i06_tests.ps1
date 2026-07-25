param([string]$RepoRoot=".")
$ErrorActionPreference="Stop"
Push-Location $RepoRoot
try {
  python .\tools\engineering\run_engineering_policy.py .
  python .\src\engine\tooling\strategy_factory\check_uce_i06_boundaries.py .
  python .\src\engine\tooling\strategy_factory\check_uce_i06_mql5_static.py .
  python .\src\engine\tooling\strategy_factory\validate_uce_i06_delivery.py .
  $env:PYTHONPATH=(Resolve-Path ".\src\engine\packages").Path
  python -m compileall -q .\src\engine\packages\strategy_factory_dataset_v3
  python -m strategy_factory_dataset_v3.cli conformance
  pytest -q --import-mode=importlib .\tests\legacy\strategy_factory\v1\phase_uce_i01_contracts .\tests\legacy\strategy_factory\v1\phase_uce_i02_contexts .\tests\legacy\strategy_factory\v1\phase_uce_i03_treatments .\tests\legacy\strategy_factory\v1\phase_uce_i04_treatment_compiler .\tests\legacy\strategy_factory\v1\phase_uce_i05_economics .\tests\legacy\strategy_factory\v1\phase_uce_i06_dataset
} finally { Pop-Location }
