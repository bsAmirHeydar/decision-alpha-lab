$ErrorActionPreference = "Stop"
python -m compileall -q .\lab\11_strategy_factory\python\strategy_factory_validation
pytest -q .\lab\11_strategy_factory\tests\phase12_validation
python .\tools\strategy_factory\check_sf12_boundaries.py .
python .\tools\engineering\run_engineering_policy.py .
