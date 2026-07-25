$ErrorActionPreference = "Stop"
python -m compileall -q .\lab	_strategy_factory\python
pytest -q .\lab	_strategy_factory	ests\phase01_contracts .\lab	_strategy_factory	ests\phase02_runtime .\lab	_strategy_factory	ests\phase03_market .\lab	_strategy_factory	ests\phase04_plugins .\lab	_strategy_factory	ests\phase05_generation .\lab	_strategy_factory	ests\phase06_anatomy .\lab	_strategy_factory	ests\phase07_context .\lab	_strategy_factory	ests\phase08_candidate
python .	ools\strategy_factory\check_sf08_boundaries.py .
python .	ools\engineeringun_engineering_policy.py .
