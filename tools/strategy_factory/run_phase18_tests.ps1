$ErrorActionPreference = "Stop"
python .\tools\engineering\run_engineering_policy.py .
python .\tools\strategy_factory\check_sf18_boundaries.py .
python .\tools\strategy_factory\check_sf18_mql5_static.py .
pytest -q .\lab\11_strategy_factory\tests\phase18_live
