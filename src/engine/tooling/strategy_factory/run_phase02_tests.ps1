$ErrorActionPreference = "Stop"

python -m compileall -q .\src\engine\packages
pytest -q .\tests\legacy\strategy_factory\v1\phase01_contracts .\tests\legacy\strategy_factory\v1\phase02_runtime
python .\src\engine\tooling\strategy_factory\check_sf02_boundaries.py

Write-Host "Phase 02 Python/static tests passed."
