$ErrorActionPreference = "Stop"
$env:PYTHONPATH = ".\lab\11_strategy_factory\python"
python -m compileall .\lab\11_strategy_factory\python\strategy_factory_contracts
pytest -q .\lab\11_strategy_factory\tests\phase01_contracts
python .\tools\engineering\check_mql5_compatibility.py .
python -m strategy_factory_contracts.cli validate-registry `
  .\lab\11_strategy_factory\schemas\v1\contract_registry.json
