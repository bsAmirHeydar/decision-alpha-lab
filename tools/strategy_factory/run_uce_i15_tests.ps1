$ErrorActionPreference="Stop"
$env:PYTHONPATH="lab/11_strategy_factory/python"
python -m pytest -q --import-mode=importlib lab/11_strategy_factory/tests/phase_uce_i15_real_context_tournament
python tools/strategy_factory/check_uce_i15_boundaries.py
python tools/strategy_factory/check_uce_i15_mql5_static.py
python tools/strategy_factory/validate_uce_i15_delivery.py
