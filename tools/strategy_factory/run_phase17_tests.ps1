$ErrorActionPreference = "Stop"
python .	ools\engineering
un_engineering_policy.py .
python .	ools\strategy_factory\check_sf17_boundaries.py
pytest -q .\lab	_strategy_factory	ests\phase17_execution
