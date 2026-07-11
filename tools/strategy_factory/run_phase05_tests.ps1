$ErrorActionPreference = "Stop"
python -m compileall -q .\lab\11_strategy_factory\python
pytest -q .\lab\11_strategy_factory\tests\phase01_contracts .\lab\11_strategy_factory\tests\phase02_runtime .\lab\11_strategy_factory\tests\phase03_market .\lab\11_strategy_factory\tests\phase04_plugins .\lab\11_strategy_factory\tests\phase05_generation
python .\tools\strategy_factory\check_sf05_boundaries.py .
