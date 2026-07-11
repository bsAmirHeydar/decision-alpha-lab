$ErrorActionPreference = "Stop"
python -m compileall -q .\lab\11_strategy_factory\python\strategy_factory_training
pytest -q .\lab\11_strategy_factory\tests\phase13_training
python .\tools\strategy_factory\check_sf13_boundaries.py .
python .\tools\engineering\run_engineering_policy.py .
