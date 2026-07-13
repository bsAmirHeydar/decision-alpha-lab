# Install and Validate FP-I02

## Apply

Place the patch ZIP in the repository root, expand it into `.`, and remove the ZIP from the root only after extraction succeeds.

## Python and static validation

```powershell
$env:PYTHONPATH = Join-Path $PWD 'lab\10_infrastructure\EXP0019_faerie_protocol\phase_i02\python'
python -m pytest -q lab\10_infrastructure\EXP0019_faerie_protocol\phase_i02\tests
python lab\10_infrastructure\EXP0019_faerie_protocol\phase_i02\run_phase_i02.py
python tools\exp0019\check_fp_i02_boundaries.py .
python tools\exp0019\check_fp_i02_mql5_static.py .
python tools\exp0019\generate_fp_i02_vectors.py --verify-only
python tools\exp0019\validate_fp_i02_delivery.py .
```

Or run:

```powershell
& .\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i02\powershell\run_exp0019_fp_i02_checks.ps1 -RepoRoot $PWD
```

## MetaEditor compile gate

```powershell
& .\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i02\powershell\compile_exp0019_fp_i02_contracts.ps1 `
  -RepoRoot $PWD `
  -MetaEditor 'C:\Program Files\MetaTrader 5\metaeditor64.exe'
```

Retain both compile logs and verify `0 errors`. Static checks are not a substitute for compilation.

## Stage only FP-I02

```powershell
git add --pathspec-from-file="EXP0019_FP_I02_FILE_INDEX.txt"
git commit -F ".\COMMIT_MESSAGE.md"
git push origin main
```

## Rollback

Before commit, restore only paths in `EXP0019_FP_I02_FILE_INDEX.txt`. After a shared push, revert the FP-I02 commit rather than rewriting history.
