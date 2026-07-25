param([string]$RepoRoot=".")
$ErrorActionPreference="Stop"
$root=(Resolve-Path $RepoRoot).Path
Push-Location $root
try {
  python .\tools\engineering\run_engineering_policy.py .
  python .\src\engine\tooling\strategy_factory\check_uce_i04_boundaries.py .
  python .\src\engine\tooling\strategy_factory\check_uce_i04_mql5_static.py .
  python .\src\engine\tooling\strategy_factory\validate_uce_i04_delivery.py .
  $env:PYTHONPATH=(Resolve-Path ".\src\engine\packages").Path
  python -m compileall -q .\src\engine\packages\strategy_factory_treatment_compiler_v3
  python -m strategy_factory_treatment_compiler_v3.cli conformance
  python .\src\engine\tooling\strategy_factory\generate_uce_i04_vectors.py . --verify-only
  pytest -q --import-mode=importlib `
    .\tests\legacy\strategy_factory\v1\phase_uce_i01_contracts `
    .\tests\legacy\strategy_factory\v1\phase_uce_i02_contexts `
    .\tests\legacy\strategy_factory\v1\phase_uce_i03_treatments `
    .\tests\legacy\strategy_factory\v1\phase_uce_i04_treatment_compiler
} finally { Pop-Location }
