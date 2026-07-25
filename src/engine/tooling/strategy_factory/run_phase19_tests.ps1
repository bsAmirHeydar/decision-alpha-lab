$ErrorActionPreference = "Stop"
python .\tools\engineering\run_engineering_policy.py .
python .\src\engine\tooling\strategy_factory\check_sf19_boundaries.py .
python .\src\engine\tooling\strategy_factory\check_sf19_mql5_static.py .
python -m compileall -q .\src\engine\packages\strategy_factory_monitoring
pytest -q .\tests\legacy\strategy_factory\v1\phase19_monitoring
