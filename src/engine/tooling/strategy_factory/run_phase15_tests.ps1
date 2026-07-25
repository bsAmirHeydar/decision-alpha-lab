$ErrorActionPreference = "Stop"
python .\src\engine\tooling\strategy_factory\check_sf15_boundaries.py .
python -m pytest -q .\tests\legacy\strategy_factory\v1\phase15_inference
python -m compileall -q .\src\engine\packages\strategy_factory_inference
python .\tools\engineering\run_engineering_policy.py .
