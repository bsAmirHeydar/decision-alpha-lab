$ErrorActionPreference = "Stop"
python -m compileall -q .\src\engine\packages\strategy_factory_training
pytest -q .\tests\legacy\strategy_factory\v1\phase13_training
python .\src\engine\tooling\strategy_factory\check_sf13_boundaries.py .
python .\tools\engineering\run_engineering_policy.py .
