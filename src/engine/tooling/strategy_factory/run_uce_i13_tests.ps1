$ErrorActionPreference="Stop"
$env:PYTHONPATH="src/engine/packages"
python -m pytest -q --import-mode=importlib tests/legacy/strategy_factory/v1/phase_uce_i13_policy_graph
python src/engine/tooling/strategy_factory/check_uce_i13_boundaries.py
python src/engine/tooling/strategy_factory/check_uce_i13_mql5_static.py
python src/engine/tooling/strategy_factory/validate_uce_i13_delivery.py
