param([string]$RepoRoot=".")
$ErrorActionPreference="Stop"
$root=(Resolve-Path $RepoRoot).Path
Push-Location $root
try {
  python .\tools\engineering\run_engineering_policy.py .
  python .\tools\strategy_factory\check_uce_i04_boundaries.py .
  python .\tools\strategy_factory\check_uce_i04_mql5_static.py .
  python .\tools\strategy_factory\validate_uce_i04_delivery.py .
  $env:PYTHONPATH=(Resolve-Path ".\lab\11_strategy_factory\python").Path
  python -m compileall -q .\lab\11_strategy_factory\python\strategy_factory_treatment_compiler_v3
  python -m strategy_factory_treatment_compiler_v3.cli conformance
  python .\tools\strategy_factory\generate_uce_i04_vectors.py . --verify-only
  pytest -q --import-mode=importlib `
    .\lab\11_strategy_factory\tests\phase_uce_i01_contracts `
    .\lab\11_strategy_factory\tests\phase_uce_i02_contexts `
    .\lab\11_strategy_factory\tests\phase_uce_i03_treatments `
    .\lab\11_strategy_factory\tests\phase_uce_i04_treatment_compiler
} finally { Pop-Location }
