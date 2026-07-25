$ErrorActionPreference = "Stop"
python -m compileall -q .\src\engine\packages
pytest -q `
  .\tests\legacy\strategy_factory\v1\phase01_contracts `
  .\tests\legacy\strategy_factory\v1\phase02_runtime `
  .\tests\legacy\strategy_factory\v1\phase03_market `
  .\tests\legacy\strategy_factory\v1\phase04_plugins
python .\src\engine\tooling\strategy_factory\check_sf04_boundaries.py
Write-Host "SF04 Python, contract, inventory and boundary tests: PASS"
