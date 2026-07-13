# Install and Validate FP-I04

## Preconditions

- FP-I00 through FP-I03 are already applied.
- The patch ZIP is placed in the repository root.
- Python 3.11+ and pytest are available.
- MetaEditor is required only to close the local Windows compile gate.

## Apply

```powershell
$Zip = ".\decision-alpha-lab-exp0019-faerie-protocol-fp-i04-data-sync-v1.0.0.zip"
Expand-Archive -LiteralPath $Zip -DestinationPath . -Force
Remove-Item -LiteralPath $Zip -Force
git add --pathspec-from-file="EXP0019_FP_I04_FILE_INDEX.txt"
git commit -F ".\COMMIT_MESSAGE.md"
git push origin main
```

## Validate

```powershell
& .\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i04\powershell\run_fp_i04_tests.ps1 -RepoRoot $PWD
```

## Compile MQL5 locally

```powershell
& .\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i04\powershell\compile_fp_i04.ps1 `
  -RepoRoot $PWD `
  -MetaEditor "C:\Program Files\MetaTrader 5\metaeditor64.exe"
```

Retain both compile logs. Static checks are not a substitute for actual MetaEditor compilation.

## Rollback

Before commit:

```powershell
git restore --staged --pathspec-from-file="EXP0019_FP_I04_FILE_INDEX.txt"
Get-Content ".\EXP0019_FP_I04_FILE_INDEX.txt" | ForEach-Object { if ($_ -and (Test-Path -LiteralPath $_)) { Remove-Item -LiteralPath $_ -Force } }
```

After a shared push, use a revert commit rather than rewriting branch history.
