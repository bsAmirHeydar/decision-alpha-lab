# Install and Validate FP-I03

## Preconditions

- FP-I00, FP-I01, and FP-I02 are already applied.
- Run all commands from the repository root.
- Place the FP-I03 patch ZIP in the repository root.
- Python and pytest are available.
- MetaEditor is required only to close the local MQL5 compile gate.

## Apply patch

```powershell
$Zip = ".\decision-alpha-lab-exp0019-faerie-protocol-fp-i03-time-calendar-v1.0.0.zip"
Expand-Archive -LiteralPath $Zip -DestinationPath . -Force
Remove-Item -LiteralPath $Zip -Force
```

## Run phase validation

```powershell
$env:PYTHONPATH = ".\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i02\python;.\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i03\python"
python -m pytest -q .\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i03\tests
python .\tools\exp0019\check_fp_i03_boundaries.py .
python .\tools\exp0019\check_fp_i03_mql5_static.py .
python .\tools\exp0019\generate_fp_i03_vectors.py . --verify-only
python .\tools\exp0019\validate_fp_i03_delivery.py .
```

## Compile MQL5 on Windows

```powershell
& .\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i03\powershell\compile_fp_i03.ps1 `
  -RepoRoot $PWD `
  -MetaEditor "C:\Program Files\MetaTrader 5\metaeditor64.exe"
```

Retain both compile logs. Static validation must not be reported as successful MetaEditor compilation.

## Stage only FP-I03 files

```powershell
git add --pathspec-from-file="EXP0019_FP_I03_FILE_INDEX.txt"
git commit -F ".\COMMIT_MESSAGE.md"
git push origin main
```

## Rollback

Before commit, restore only the files listed in `EXP0019_FP_I03_FILE_INDEX.txt`. After a shared push, create a revert commit rather than rewriting branch history.
