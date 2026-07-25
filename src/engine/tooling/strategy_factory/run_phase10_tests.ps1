$ErrorActionPreference = "Stop"
python -m compileall -q .\src\engine\packages
pytest -q .\tests\legacy\strategy_factory\v1\phase10_research
python .\src\engine\tooling\strategy_factory\check_sf10_boundaries.py .
python .\tools\engineering\run_engineering_policy.py .
