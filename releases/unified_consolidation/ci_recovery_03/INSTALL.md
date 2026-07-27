# Install — UC04-W1B CI Recovery 01

Run from the Decision Alpha Lab repository root using Windows PowerShell 5.1 or newer.

## 1. Define paths and verify ZIP hash

```powershell
$ErrorActionPreference = "Stop"
$RepositoryRoot = (Resolve-Path -LiteralPath ".").Path
$Zip = Join-Path $RepositoryRoot "ALPHA_LAB_UC04_W1B_CI_LFS_RECOVERY_01.zip"
$ZipHashFile = "$Zip.sha256"
$ApprovedZipSha256 = ((Get-Content -LiteralPath $ZipHashFile -Raw).Trim() -split "\s+")[0].ToLowerInvariant()
$ActualZipSha256 = (Get-FileHash -LiteralPath $Zip -Algorithm SHA256).Hash.ToLowerInvariant()
if ($ActualZipSha256 -ne $ApprovedZipSha256) {
    throw "ZIP SHA-256 mismatch: $ActualZipSha256"
}
```

## 2. Extract into an external staging directory

```powershell
$Staging = Join-Path $env:TEMP ("AlphaLab-UC04-W1B-CI-Recovery-" + [Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $Staging -Force | Out-Null
Expand-Archive -LiteralPath $Zip -DestinationPath $Staging -Force
```

## 3. Validate membership and hashes

```powershell
$ReleaseRelative = "releases/unified_consolidation/ci_recovery_03"
$Index = Join-Path $Staging "$ReleaseRelative/PATCH_FILE_INDEX.txt"
$Ledger = Join-Path $Staging "$ReleaseRelative/PATCH_FILE_HASHES.sha256"
$Expected = @(Get-Content -LiteralPath $Index | Where-Object { $_ } | Sort-Object)
$Actual = @(Get-ChildItem -LiteralPath $Staging -Recurse -File | ForEach-Object {
    $_.FullName.Substring($Staging.Length + 1).Replace('\', '/')
} | Sort-Object)
$Difference = @(Compare-Object -ReferenceObject $Expected -DifferenceObject $Actual)
if ($Difference.Count -ne 0) {
    throw "Staging membership differs from PATCH_FILE_INDEX.txt"
}
foreach ($Line in Get-Content -LiteralPath $Ledger) {
    if (-not $Line) { continue }
    $Digest, $Relative = $Line -split '  ', 2
    $Target = Join-Path $Staging ($Relative.Replace('/', '\'))
    $ActualDigest = (Get-FileHash -LiteralPath $Target -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($ActualDigest -ne $Digest.ToLowerInvariant()) {
        throw "Staged file hash mismatch: $Relative"
    }
}
```

## 4. Copy staged files into the repository

```powershell
foreach ($Relative in $Expected) {
    $Source = Join-Path $Staging ($Relative.Replace('/', '\'))
    $Destination = Join-Path $RepositoryRoot ($Relative.Replace('/', '\'))
    $Parent = Split-Path -Parent $Destination
    New-Item -ItemType Directory -Path $Parent -Force | Out-Null
    Copy-Item -LiteralPath $Source -Destination $Destination -Force
}
Remove-Item -LiteralPath $Staging -Recurse -Force
Remove-Item -LiteralPath $Zip -Force
```

## 5. Run mandatory gates

```powershell
python tools/engineering/run_engineering_policy.py .
python -m tools.consolidation.ci.verify_migration_continuity --repo-root .
python -m tools.consolidation.uc03p3.verify --repo-root . --ci-fast
python -m tools.consolidation.uc04w0.verify --repo-root .
python -m tools.consolidation.uc04w1.verify --repo-root .
python -m tools.consolidation.uc04w1b.verify --repo-root .
python -m pytest -q tests/consolidation/uc04w0 tests/consolidation/uc04w1 tests/consolidation/uc04w1b tests/consolidation/ci -p no:cacheprovider
python -m pytest --collect-only -q -p no:cacheprovider
```

Do not commit if any command fails.

## 6. Stage and commit exact paths only

```powershell
$Patch = "releases/unified_consolidation/ci_recovery_03"
git add --pathspec-from-file="$Patch/PATCH_FILE_INDEX.txt"
git diff --cached --check
git commit -F "$Patch/COMMIT_MESSAGE.txt"
```

No push command is included.

## Rollback

Follow `ROLLBACK.md`. Before commit, restore/remove only the indexed paths. After commit, use `git revert`.
