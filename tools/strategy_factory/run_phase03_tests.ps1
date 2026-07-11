$ErrorActionPreference = "Stop"

python -m compileall -q .\lab\11_strategy_factory\python

pytest -q `
  .\lab\11_strategy_factory\tests\phase01_contracts `
  .\lab\11_strategy_factory\tests\phase02_runtime `
  .\lab\11_strategy_factory\tests\phase03_market

python .\tools\strategy_factory\check_sf03_boundaries.py

Write-Host "Phase 03 Python and static architecture tests passed."
