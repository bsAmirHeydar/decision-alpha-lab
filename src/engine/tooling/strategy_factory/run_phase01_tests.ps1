$ErrorActionPreference = "Stop"
$env:PYTHONPATH = ".\src\engine\packages"
python -m compileall .\src\engine\packages\strategy_factory_contracts
pytest -q .\tests\legacy\strategy_factory\v1\phase01_contracts
python .\tools\engineering\check_mql5_compatibility.py .
python -m strategy_factory_contracts.cli validate-registry `
  .\schemas\legacy\strategy_factory\v1\contract_registry.json
