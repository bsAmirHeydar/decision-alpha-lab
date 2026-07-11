$ErrorActionPreference = "Stop"
python .\tools\engineering\run_engineering_policy.py .
python .\tools\strategy_factory\check_sf19_boundaries.py .
python .\tools\strategy_factory\check_sf19_mql5_static.py .
python -m compileall -q .\lab\11_strategy_factory\python\strategy_factory_monitoring
pytest -q .\lab\11_strategy_factory\tests\phase19_monitoring
