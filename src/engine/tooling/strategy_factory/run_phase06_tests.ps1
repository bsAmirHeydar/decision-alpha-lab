$ErrorActionPreference = "Stop"
python -m compileall -q .\src\engine\packages
pytest -q .\tests\legacy\strategy_factory\v1\phase01_contracts .\tests\legacy\strategy_factory\v1\phase02_runtime .\tests\legacy\strategy_factory\v1\phase03_market .\tests\legacy\strategy_factory\v1\phase04_plugins .\tests\legacy\strategy_factory\v1\phase05_generation .\tests\legacy\strategy_factory\v1\phase06_anatomy
python .\src\engine\tooling\strategy_factory\check_sf06_boundaries.py .
