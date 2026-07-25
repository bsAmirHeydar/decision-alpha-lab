# Installation

Expand the ZIP into the repository root with overwrite enabled. The patch is additive except for the Strategy Factory Python `pyproject.toml`, which is advanced from 0.38.0 to 0.39.0 and registers `saed-v4-execution-twin`.

Validate with:

```powershell
python tools/strategy_factory/saed_v4_09/run_saed_v4_09_full_qa.py
python tools/strategy_factory/saed_v4_09/validate_saed_v4_09_delivery.py
```

Actual MetaEditor compilation, broker calibration, cross-broker transport, prospective paper, shadow, and I18 qualification remain external gates.
