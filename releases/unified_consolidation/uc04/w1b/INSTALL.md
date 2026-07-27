# UC04-W1B-Q R4 — Safe PowerShell Installation

Run from the Decision Alpha Lab repository root. The ZIP and its `.sha256` sidecar may be in the repository root or another local directory. The staging directory is always created outside the repository.

## Install and verify

```powershell
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$env:PYTHONDONTWRITEBYTECODE = "1"

$RepositoryRoot = (Resolve-Path -LiteralPath (Get-Location)).Path
$Zip = Join-Path $RepositoryRoot "ALPHA_LAB_UC04_W1B_Q_INSTALLABLE_PATCH_R4_2026-07-27.zip"
$ZipHashFile = "$Zip.sha256"

if (-not (Test-Path -LiteralPath $Zip -PathType Leaf)) { throw "ZIP not found: $Zip" }
if (-not (Test-Path -LiteralPath $ZipHashFile -PathType Leaf)) { throw "ZIP hash sidecar not found: $ZipHashFile" }

$ExpectedZipSha256 = ((Get-Content -LiteralPath $ZipHashFile -Raw).Trim() -split '\s+')[0].ToLowerInvariant()
if ($ExpectedZipSha256 -notmatch '^[0-9a-f]{64}$') { throw "Invalid SHA-256 sidecar: $ZipHashFile" }
$ActualZipSha256 = (Get-FileHash -LiteralPath $Zip -Algorithm SHA256).Hash.ToLowerInvariant()
if ($ActualZipSha256 -ne $ExpectedZipSha256) {
    throw "ZIP SHA-256 mismatch. Expected $ExpectedZipSha256, actual $ActualZipSha256"
}

function Get-RelativePathCompat([string]$BasePath, [string]$TargetPath) {
    $BaseFull = [System.IO.Path]::GetFullPath($BasePath).TrimEnd('\') + '\'
    $TargetFull = [System.IO.Path]::GetFullPath($TargetPath)
    $BaseUri = New-Object System.Uri($BaseFull)
    $TargetUri = New-Object System.Uri($TargetFull)
    return [System.Uri]::UnescapeDataString($BaseUri.MakeRelativeUri($TargetUri).ToString()).Replace('/', '\')
}

Add-Type -AssemblyName System.IO.Compression.FileSystem
$Archive = [System.IO.Compression.ZipFile]::OpenRead($Zip)
try {
    $Seen = @{}
    foreach ($Entry in $Archive.Entries) {
        $Name = $Entry.FullName
        if ([string]::IsNullOrWhiteSpace($Name) -or $Name.EndsWith('/')) { throw "Directory/blank ZIP entry is forbidden: $Name" }
        if ($Name.Contains('\') -or $Name.StartsWith('/') -or $Name -match '^[A-Za-z]:' -or $Name.Split('/') -contains '..') {
            throw "Unsafe ZIP entry: $Name"
        }
        $Key = $Name.ToLowerInvariant()
        if ($Seen.ContainsKey($Key)) { throw "Duplicate or Windows case-colliding ZIP entry: $Name" }
        $Seen[$Key] = $true
    }
}
finally {
    $Archive.Dispose()
}

$StagingDirectory = Join-Path ([System.IO.Path]::GetTempPath()) ("AlphaLab-UC04-W1B-Q-" + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $StagingDirectory -Force | Out-Null

try {
    Expand-Archive -LiteralPath $Zip -DestinationPath $StagingDirectory -Force

    $StagedIndex = Join-Path $StagingDirectory "releases\unified_consolidation\uc04\w1b\PATCH_FILE_INDEX.txt"
    $StagedLedger = Join-Path $StagingDirectory "releases\unified_consolidation\uc04\w1b\PATCH_FILE_HASHES.sha256"
    if (-not (Test-Path -LiteralPath $StagedIndex -PathType Leaf)) { throw "PATCH_FILE_INDEX.txt missing from staging" }
    if (-not (Test-Path -LiteralPath $StagedLedger -PathType Leaf)) { throw "PATCH_FILE_HASHES.sha256 missing from staging" }

    $ExpectedFiles = @(Get-Content -LiteralPath $StagedIndex | ForEach-Object { $_.Trim() } | Where-Object { $_ })
    $ActualFiles = @(
        Get-ChildItem -LiteralPath $StagingDirectory -Recurse -File |
            ForEach-Object { (Get-RelativePathCompat $StagingDirectory $_.FullName).Replace('\', '/') } |
            Sort-Object
    )
    $MembershipDifference = @(Compare-Object -ReferenceObject ($ExpectedFiles | Sort-Object) -DifferenceObject $ActualFiles)
    if ($MembershipDifference.Count -ne 0) {
        throw "Staging membership differs from PATCH_FILE_INDEX.txt: $($MembershipDifference | Out-String)"
    }

    $Installer = Join-Path $StagingDirectory "releases\unified_consolidation\uc04\w1b\APPLY.ps1"
    & $Installer `
        -Action Install `
        -RepositoryRoot $RepositoryRoot `
        -StagingRoot $StagingDirectory `
        -ZipPath $Zip `
        -ExpectedZipSha256 $ExpectedZipSha256
}
finally {
    if (Test-Path -LiteralPath $StagingDirectory -PathType Container) {
        Remove-Item -LiteralPath $StagingDirectory -Recurse -Force
    }
}
```

The installer runs Python with `-B` plus process-scoped `PYTHONDONTWRITEBYTECODE=1`, proves the validation process does not mutate staging, disables Pytest cache creation with `-p no:cacheprovider`, and validates the staged tree against `PATCH_FILE_INDEX.txt` and `PATCH_FILE_HASHES.sha256`, validates `PATCH_MANIFEST.json` and `QA_REPORT.json` against their schemas, rejects LFS pointers/secrets/unsafe paths/incorrect line endings, backs up pre-existing targets, transfers files atomically, and executes all required gates. If any transfer or gate fails, it automatically rolls back.

Preserve the printed `Rollback state:` path.

## Exact Git staging and commit

Run only after the installer reports all gates `PASS`:

```powershell
$RepositoryRoot = (Resolve-Path -LiteralPath (Get-Location)).Path
$PatchRoot = Join-Path $RepositoryRoot "releases\unified_consolidation\uc04\w1b"
$Index = Join-Path $PatchRoot "PATCH_FILE_INDEX.txt"
$CommitMessage = Join-Path $PatchRoot "COMMIT_MESSAGE.txt"

Push-Location -LiteralPath $RepositoryRoot
try {
    git add --pathspec-from-file="$Index"
    if ($LASTEXITCODE -ne 0) { throw "git add failed" }

    git diff --cached --check
    if ($LASTEXITCODE -ne 0) { throw "git diff --cached --check failed" }

    $Expected = @(Get-Content -LiteralPath $Index | ForEach-Object { $_.Trim() } | Where-Object { $_ } | Sort-Object)
    $Staged = @(git diff --cached --name-only | Sort-Object)
    $Difference = @(Compare-Object -ReferenceObject $Expected -DifferenceObject $Staged)
    if ($Difference.Count -ne 0) { throw "Staged paths do not exactly match PATCH_FILE_INDEX.txt: $($Difference | Out-String)" }

    git commit -F "$CommitMessage"
    if ($LASTEXITCODE -ne 0) { throw "git commit failed" }
}
finally {
    Pop-Location
}
```

No push command is included. Push requires a separate explicit request.
