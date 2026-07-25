# Install UCEE-I01

## Overlay

Extract this patch at the repository root with overwrite enabled. It is additive except for the Strategy Factory Python `pyproject.toml` and the UCEE implementation-program MOC, which are advanced to include the new package and phase delivery.

## Python and Static Verification

```powershell
python .\tools\engineering\run_engineering_policy.py .
python .\tools\strategy_factory\check_uce_i01_boundaries.py .
python .\tools\strategy_factory\check_uce_i01_mql5_static.py .
$env:PYTHONPATH = ".\lab\11_strategy_factory\python"
python -m compileall -q .\lab\11_strategy_factory\python\strategy_factory_contracts_v3
python -m strategy_factory_contracts_v3.cli check-vector-file `
  .\lab\11_strategy_factory\test_vectors\v3\uce_i01_cross_language_vectors.json
pytest -q .\lab\11_strategy_factory\tests\phase_uce_i01_contracts
```

## Native MQL5 Gate

```powershell
powershell -ExecutionPolicy Bypass `
  -File .\tools\strategy_factory\compile_uce_i01_contracts.ps1 `
  -MetaEditorPath "C:\Program Files\MetaTrader 5\metaeditor64.exe"
```

Then run `UCE_I01_ContractsV3SelfTest` in MT5 and retain terminal evidence showing every test passed and `failed=0`.

## Rollback

Remove only UCE-I01-owned paths and restore the prior `lab/11_strategy_factory/python/pyproject.toml` and implementation-program MOC from Git. Do not rewrite or delete SF01 or historical Strategy Factory evidence.
