$ErrorActionPreference = "Stop"
python .\tools\engineering\run_engineering_policy.py .
python .\src\engine\tooling\strategy_factory\check_sf18_boundaries.py .
python .\src\engine\tooling\strategy_factory\check_sf18_mql5_static.py .
pytest -q .\tests\legacy\strategy_factory\v1\phase18_live
