$ErrorActionPreference = "Stop"

python -m compileall -q .\src\engine\packages

pytest -q `
  .\tests\legacy\strategy_factory\v1\phase01_contracts `
  .\tests\legacy\strategy_factory\v1\phase02_runtime `
  .\tests\legacy\strategy_factory\v1\phase03_market

python .\src\engine\tooling\strategy_factory\check_sf03_boundaries.py

Write-Host "Phase 03 Python and static architecture tests passed."
