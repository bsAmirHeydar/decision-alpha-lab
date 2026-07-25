$ErrorActionPreference = "Stop"
python .\src\engine\tooling\strategy_factory\check_sf14_boundaries.py .
python -m pytest -q .\tests\legacy\strategy_factory\v1\phase14_governance
python -m compileall -q .\src\engine\packages\strategy_factory_governance
python .\tools\engineering\run_engineering_policy.py .
