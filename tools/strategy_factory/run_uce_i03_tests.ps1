param([string]$RepoRoot = ".")
$ErrorActionPreference = "Stop"
Set-Location $RepoRoot
python .\tools\engineering\run_engineering_policy.py .
python .\tools\strategy_factory\check_uce_i03_boundaries.py .
python .\tools\strategy_factory\check_uce_i03_mql5_static.py .
python .\tools\strategy_factory\validate_uce_i03_delivery.py .
$env:PYTHONPATH = (Resolve-Path ".\lab\11_strategy_factory\python").Path
python -m compileall -q .\lab\11_strategy_factory\python\strategy_factory_treatments_v3
python -m strategy_factory_treatments_v3.cli conformance
pytest -q --import-mode=importlib .\lab\11_strategy_factory\tests\phase_uce_i01_contracts .\lab\11_strategy_factory\tests\phase_uce_i02_contexts .\lab\11_strategy_factory\tests\phase_uce_i03_treatments
