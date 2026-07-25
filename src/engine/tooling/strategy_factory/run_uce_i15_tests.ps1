$ErrorActionPreference="Stop"
$env:PYTHONPATH="src/engine/packages"
python -m pytest -q --import-mode=importlib tests/legacy/strategy_factory/v1/phase_uce_i15_real_context_tournament
python src/engine/tooling/strategy_factory/check_uce_i15_boundaries.py
python src/engine/tooling/strategy_factory/check_uce_i15_mql5_static.py
python src/engine/tooling/strategy_factory/validate_uce_i15_delivery.py
