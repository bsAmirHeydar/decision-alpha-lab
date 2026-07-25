$ErrorActionPreference = "Stop"
python -m compileall -q .\lab	_strategy_factory\python\strategy_factory_statistics
pytest -q .\lab	_strategy_factory	ests\phase11_statistics
python .	ools\strategy_factory\check_sf11_boundaries.py .
python .	ools\engineeringun_engineering_policy.py .
