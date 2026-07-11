$ErrorActionPreference = "Stop"

python -m compileall -q .\lab\11_strategy_factory\python
pytest -q .\lab\11_strategy_factory\tests\phase01_contracts .\lab\11_strategy_factory\tests\phase02_runtime
python .\tools\strategy_factory\check_sf02_boundaries.py

Write-Host "Phase 02 Python/static tests passed."
