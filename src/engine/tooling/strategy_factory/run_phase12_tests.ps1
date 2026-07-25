$ErrorActionPreference = "Stop"
python -m compileall -q .\src\engine\packages\strategy_factory_validation
pytest -q .\tests\legacy\strategy_factory\v1\phase12_validation
python .\src\engine\tooling\strategy_factory\check_sf12_boundaries.py .
python .\tools\engineering\run_engineering_policy.py .
