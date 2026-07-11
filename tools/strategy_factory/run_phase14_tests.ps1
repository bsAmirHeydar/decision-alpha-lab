$ErrorActionPreference = "Stop"
python .\tools\strategy_factory\check_sf14_boundaries.py .
python -m pytest -q .\lab\11_strategy_factory\tests\phase14_governance
python -m compileall -q .\lab\11_strategy_factory\python\strategy_factory_governance
python .\tools\engineering\run_engineering_policy.py .
