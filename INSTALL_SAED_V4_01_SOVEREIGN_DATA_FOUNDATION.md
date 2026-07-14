# Install SAED V4-01

Apply the ZIP at the repository root. The patch assumes SAED V4 Architecture and SAED V4-00 are already present.

After extraction, stage only paths listed in `SAED_V4_01_FILE_INDEX.txt`.

## Validation

```powershell
python .	ools\strategy_factory\saed_v4_01un_saed_v4_01_tests.py
python .	ools\strategy_factory\saed_v4_01alidate_saed_v4_01_contracts.py
python .	ools\strategy_factory\saed_v4_01\check_saed_v4_01_mql5_static.py
python .	ools\strategy_factory\saed_v4_01\check_saed_v4_01_boundaries.py
python .	ools\strategy_factory\saed_v4_01alidate_saed_v4_01_delivery.py
```

Actual MetaEditor compilation is executed separately on Windows using `compile_saed_v4_01_data_foundation.ps1`.
