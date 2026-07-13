# Install UCEE I11 Patch

Run all commands from the repository root.

## Preconditions

- UCE-I10 is already applied.
- Git working tree changes unrelated to I11 are not staged.
- Python and pytest dependencies used by the existing repository are available.
- The I11 patch ZIP is downloaded, normally into `%USERPROFILE%\Downloads`.

## Apply and validate

1. Expand the patch into the repository root.
2. Remove the downloaded ZIP after successful expansion.
3. Run:

```powershell
$env:PYTHONPATH = ".\lab\11_strategy_factory\python"
python -m pytest -q --import-mode=importlib .\lab\11_strategy_factory\tests\phase_uce_i11_experiments
python .\tools\strategy_factory\check_uce_i11_boundaries.py
python .\tools\strategy_factory\check_uce_i11_mql5_static.py
python .\tools\strategy_factory\validate_uce_i11_delivery.py
python .\tools\engineering\run_engineering_policy.py .
```

4. Stage only paths in `UCEE_I11_FILE_INDEX.txt`.
5. Commit and push.

## Local MetaEditor gate

Static MQL5 validation is included in the patch. Actual compilation requires a Windows MetaTrader installation:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\strategy_factory\compile_uce_i11_experiment_orchestration.ps1 -RepoRoot . -MetaEditorPath "C:\path\to\metaeditor64.exe"
```

Until those logs show zero errors, the phase status remains `pending_local_windows` for MetaEditor.

## Rollback

Use the exact paths in `UCEE_I11_FILE_INDEX.txt` to review or remove the phase. Do not delete I10 artifacts or any I11 evidence already consumed by UCE-I12.
