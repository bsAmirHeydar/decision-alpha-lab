$ErrorActionPreference = "Stop"
python -m compileall -q .\lab\11_strategy_factory\python
pytest -q .\lab\11_strategy_factory\tests\phase10_research
python .\tools\strategy_factory\check_sf10_boundaries.py .
python .\tools\engineering\run_engineering_policy.py .
