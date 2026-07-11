$ErrorActionPreference = "Stop"
python .\tools\strategy_factory\check_sf15_boundaries.py .
python -m pytest -q .\lab\11_strategy_factory\tests\phase15_inference
python -m compileall -q .\lab\11_strategy_factory\python\strategy_factory_inference
python .\tools\engineering\run_engineering_policy.py .
