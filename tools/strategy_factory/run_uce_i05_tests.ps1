param([string]$RepositoryRoot='.')
$ErrorActionPreference='Stop'; Set-Location $RepositoryRoot
python .\tools\engineering\run_engineering_policy.py .
python .\tools\strategy_factory\check_uce_i05_boundaries.py .
python .\tools\strategy_factory\check_uce_i05_mql5_static.py .
python .\tools\strategy_factory\validate_uce_i05_delivery.py .
$env:PYTHONPATH=(Resolve-Path '.\lab\11_strategy_factory\python').Path
python -m compileall -q .\lab\11_strategy_factory\python\strategy_factory_economics_v3
python -m strategy_factory_economics_v3.cli conformance
pytest -q --import-mode=importlib .\lab\11_strategy_factory\tests\phase_uce_i01_contracts .\lab\11_strategy_factory\tests\phase_uce_i02_contexts .\lab\11_strategy_factory\tests\phase_uce_i03_treatments .\lab\11_strategy_factory\tests\phase_uce_i04_treatment_compiler .\lab\11_strategy_factory\tests\phase_uce_i05_economics
