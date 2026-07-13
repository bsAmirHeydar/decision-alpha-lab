# Install and Validate UCE-I10 v1.1.0

## Preconditions

- Apply the patch to the intended Decision Alpha Lab repository root.
- Record the current Git branch and commit before changing files.
- Python 3.11+ and `pytest` must be available.
- MetaEditor is optional for Python/static QA but required to close the MQL5 compile gate.

## Safe automated application

```powershell
& .\tools\strategy_factory\apply_uce_i10_patch.ps1 `
  -PatchZip .\decision-alpha-lab-ucee-i10-deep-multiview-pack-v1.1.0.zip `
  -RepoRoot C:\path\to\decision-alpha-lab `
  -RemoveZipAfterSuccess
```

The script verifies the ZIP hash when a checksum file is supplied, expands into a temporary staging directory, rejects absolute/parent-traversal paths, copies files, runs the I10 validators, and removes the ZIP only after successful validation.

## Manual Expand + Remove-ZIP workflow

Run from the repository parent directory:

```powershell
$Patch = Resolve-Path .\decision-alpha-lab-ucee-i10-deep-multiview-pack-v1.1.0.zip
$Repo  = Resolve-Path .\decision-alpha-lab
$Stage = Join-Path $env:TEMP ("uce-i10-" + [guid]::NewGuid())
New-Item -ItemType Directory -Path $Stage | Out-Null
Expand-Archive -LiteralPath $Patch -DestinationPath $Stage -Force
Copy-Item -Path (Join-Path $Stage '*') -Destination $Repo -Recurse -Force
Set-Location $Repo
& .\tools\strategy_factory\run_uce_i10_tests.ps1 -RepoRoot $Repo
Remove-Item -LiteralPath $Patch -Force
Remove-Item -LiteralPath $Stage -Recurse -Force
```

Do not remove the ZIP before the validation command succeeds.

## Direct validation

```powershell
$env:PYTHONPATH = Join-Path $PWD 'lab\11_strategy_factory\python'
python -m pytest -q lab\11_strategy_factory\tests\phase_uce_i10_deep_views
python tools\strategy_factory\check_uce_i10_boundaries.py .
python tools\strategy_factory\check_uce_i10_mql5_static.py .
python tools\strategy_factory\generate_uce_i10_vectors.py . --verify-only
python tools\strategy_factory\validate_uce_i10_delivery.py .
```

## MQL5 compile gate

```powershell
& .\tools\strategy_factory\compile_uce_i10_deep_views.ps1 `
  -RepoRoot $PWD `
  -MetaEditor 'C:\Program Files\MetaTrader 5\metaeditor64.exe'
```

Retain all three `.compile.log` files. Update the phase evidence from `pending_local_windows` only after each log reports zero errors.

## Git review, commit, and push

```powershell
git status --short
git diff --check
git diff --stat
git add -A
git commit -F COMMIT_MESSAGE.md
git push origin HEAD
```

Push success must be verified from Git output or `git ls-remote`; a local commit alone is not a push.

## Rollback

Before commit:

```powershell
git restore --staged .
git restore .
git clean -fd
```

After commit but before push:

```powershell
git reset --hard HEAD~1
```

After push, create a revert commit rather than rewriting shared history:

```powershell
git revert <UCE-I10-commit>
git push origin HEAD
```
