param([string]$Root = ".")
$ErrorActionPreference = "Stop"
Push-Location $Root
try {
  python .\tools\engineering\run_engineering_policy.py .
  python .\src\engine\tooling\strategy_factory\check_uce_i09_boundaries.py .
  python .\src\engine\tooling\strategy_factory\check_uce_i09_mql5_static.py .
  python .\src\engine\tooling\strategy_factory\validate_uce_i09_delivery.py .
  $env:PYTHONPATH = (Resolve-Path ".\src\engine\packages").Path
  python -m strategy_factory_advanced_tasks_v3.cli conformance
  python .\src\engine\tooling\strategy_factory\generate_uce_i09_vectors.py . --verify-only
  pytest -q --import-mode=importlib .\tests\legacy\strategy_factory\v1\phase_uce_i01_contracts .\tests\legacy\strategy_factory\v1\phase_uce_i02_contexts .\tests\legacy\strategy_factory\v1\phase_uce_i03_treatments .\tests\legacy\strategy_factory\v1\phase_uce_i04_treatment_compiler .\tests\legacy\strategy_factory\v1\phase_uce_i05_economics .\tests\legacy\strategy_factory\v1\phase_uce_i06_dataset .\tests\legacy\strategy_factory\v1\phase_uce_i07_trainers .\tests\legacy\strategy_factory\v1\phase_uce_i08_classical .\tests\legacy\strategy_factory\v1\phase_uce_i09_advanced_tasks
} finally { Pop-Location }
