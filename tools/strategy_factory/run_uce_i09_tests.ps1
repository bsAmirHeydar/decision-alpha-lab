param([string]$Root = ".")
$ErrorActionPreference = "Stop"
Push-Location $Root
try {
  python .\tools\engineering\run_engineering_policy.py .
  python .\tools\strategy_factory\check_uce_i09_boundaries.py .
  python .\tools\strategy_factory\check_uce_i09_mql5_static.py .
  python .\tools\strategy_factory\validate_uce_i09_delivery.py .
  $env:PYTHONPATH = (Resolve-Path ".\lab\11_strategy_factory\python").Path
  python -m strategy_factory_advanced_tasks_v3.cli conformance
  python .\tools\strategy_factory\generate_uce_i09_vectors.py . --verify-only
  pytest -q --import-mode=importlib .\lab\11_strategy_factory\tests\phase_uce_i01_contracts .\lab\11_strategy_factory\tests\phase_uce_i02_contexts .\lab\11_strategy_factory\tests\phase_uce_i03_treatments .\lab\11_strategy_factory\tests\phase_uce_i04_treatment_compiler .\lab\11_strategy_factory\tests\phase_uce_i05_economics .\lab\11_strategy_factory\tests\phase_uce_i06_dataset .\lab\11_strategy_factory\tests\phase_uce_i07_trainers .\lab\11_strategy_factory\tests\phase_uce_i08_classical .\lab\11_strategy_factory\tests\phase_uce_i09_advanced_tasks
} finally { Pop-Location }
