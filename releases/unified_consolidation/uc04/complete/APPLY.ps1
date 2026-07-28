param(
    [ValidateSet("Install", "Rollback")]
    [string]$Action = "Install",
    [string]$RepositoryRoot = ".",
    [string]$StagingRoot = "",
    [string]$BackupStatePath = ""
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$ReleaseRelative = "releases\unified_consolidation\uc04\complete"

function Resolve-PythonCommand {
    $Python = Get-Command python -ErrorAction SilentlyContinue
    if ($Python) { return [pscustomobject]@{ Executable = $Python.Source; Prefix = @("-B") } }
    $Py = Get-Command py -ErrorAction SilentlyContinue
    if ($Py) { return [pscustomobject]@{ Executable = $Py.Source; Prefix = @("-3", "-B") } }
    throw "Python 3 was not found."
}

function Invoke-Python {
    param([psobject]$PythonCommand, [string[]]$Arguments)
    $Previous = $env:PYTHONDONTWRITEBYTECODE
    $env:PYTHONDONTWRITEBYTECODE = "1"
    try {
        & $PythonCommand.Executable @($PythonCommand.Prefix) @Arguments
        $ExitCode = $LASTEXITCODE
    }
    finally {
        if ($null -eq $Previous) { Remove-Item Env:PYTHONDONTWRITEBYTECODE -ErrorAction SilentlyContinue }
        else { $env:PYTHONDONTWRITEBYTECODE = $Previous }
    }
    if ($ExitCode -ne 0) {
        throw ("Python command failed with exit code {0}: {1}" -f $ExitCode, ($Arguments -join " "))
    }
}

function Get-Sha256 {
    param([string]$Path)
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Read-Index {
    param([string]$Path)
    $Rows = @(
        Get-Content -LiteralPath $Path |
            ForEach-Object { $_.Trim().Replace("\", "/") } |
            Where-Object { $_ }
    )
    if ($Rows.Count -eq 0) { throw "Patch index is empty." }
    if (($Rows | Sort-Object -Unique).Count -ne $Rows.Count) { throw "Patch index contains duplicate paths." }
    foreach ($Row in $Rows) {
        if ([System.IO.Path]::IsPathRooted($Row) -or $Row.Split("/") -contains "..") {
            throw "Unsafe patch path: $Row"
        }
    }
    return $Rows
}

function Read-Ledger {
    param([string]$Path)
    $Ledger = @{}
    foreach ($Line in Get-Content -LiteralPath $Path) {
        if ([string]::IsNullOrWhiteSpace($Line)) { continue }
        if ($Line -notmatch '^([0-9a-fA-F]{64})  (.+)$') { throw "Invalid hash ledger row: $Line" }
        $Ledger[$Matches[2].Replace("\", "/")] = $Matches[1].ToLowerInvariant()
    }
    return $Ledger
}

function Restore-FromState {
    param([string]$Root, [string]$StatePath)
    if (-not (Test-Path -LiteralPath $StatePath -PathType Leaf)) { throw "Backup state does not exist: $StatePath" }
    $State = Get-Content -LiteralPath $StatePath -Raw | ConvertFrom-Json
    foreach ($Entry in @($State.entries) | Sort-Object path -Descending) {
        $Target = Join-Path $Root ([string]$Entry.path).Replace("/", "\")
        if ([bool]$Entry.existed) {
            New-Item -ItemType Directory -Path (Split-Path -Parent $Target) -Force | Out-Null
            Copy-Item -LiteralPath ([string]$Entry.backup_path) -Destination $Target -Force
        }
        elseif (Test-Path -LiteralPath $Target -PathType Leaf) {
            Remove-Item -LiteralPath $Target -Force
        }
    }
    Write-Host "UC04 complete rollback: PASS"
}

$Root = (Resolve-Path -LiteralPath $RepositoryRoot).Path
if ($Action -eq "Rollback") {
    if ([string]::IsNullOrWhiteSpace($BackupStatePath)) { throw "-BackupStatePath is required for rollback." }
    Restore-FromState $Root $BackupStatePath
    exit 0
}

if ([string]::IsNullOrWhiteSpace($StagingRoot)) { throw "-StagingRoot is required for installation." }
$Stage = (Resolve-Path -LiteralPath $StagingRoot).Path
if (-not (Test-Path -LiteralPath (Join-Path $Root "AGENTS.md") -PathType Leaf)) { throw "RepositoryRoot is invalid: $Root" }

$ReleaseStage = Join-Path $Stage $ReleaseRelative
$IndexPath = Join-Path $ReleaseStage "PATCH_FILE_INDEX.txt"
$LedgerPath = Join-Path $ReleaseStage "PATCH_FILE_HASHES.sha256"
if (-not (Test-Path -LiteralPath $IndexPath -PathType Leaf)) { throw "PATCH_FILE_INDEX.txt is missing from staging." }
if (-not (Test-Path -LiteralPath $LedgerPath -PathType Leaf)) { throw "PATCH_FILE_HASHES.sha256 is missing from staging." }

$Paths = @(Read-Index $IndexPath)
$Ledger = Read-Ledger $LedgerPath
$LedgerExpected = @($Paths | Where-Object { $_ -ne "releases/unified_consolidation/uc04/complete/PATCH_FILE_HASHES.sha256" })
if ($Ledger.Count -ne $LedgerExpected.Count) { throw "Hash ledger membership count mismatch." }
foreach ($Relative in $LedgerExpected) {
    $Source = Join-Path $Stage $Relative.Replace("/", "\")
    if (-not (Test-Path -LiteralPath $Source -PathType Leaf)) { throw "Staged patch file missing: $Relative" }
    if (-not $Ledger.ContainsKey($Relative)) { throw "Hash ledger row missing: $Relative" }
    if ((Get-Sha256 $Source) -ne $Ledger[$Relative]) { throw "Staged patch hash mismatch: $Relative" }
}

$Dirty = @(& git -C $Root status --porcelain=v1 --untracked-files=all -- @Paths 2>&1)
if ($LASTEXITCODE -ne 0) { throw "Unable to inspect target-path Git state." }
if (@($Dirty | Where-Object { $_ }).Count -ne 0) {
    throw ("Patch target paths contain pre-existing changes:`n{0}" -f ($Dirty -join [Environment]::NewLine))
}

$Stamp = [DateTime]::UtcNow.ToString("yyyyMMddTHHmmssZ")
$BackupRoot = Join-Path $env:LOCALAPPDATA ("AlphaLab\patch_backups\UC04-COMPLETE\" + $Stamp + "-" + [Guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $BackupRoot -Force | Out-Null
$Entries = @()
foreach ($Relative in $Paths) {
    $Target = Join-Path $Root $Relative.Replace("/", "\")
    $Existed = Test-Path -LiteralPath $Target -PathType Leaf
    $Backup = ""
    if ($Existed) {
        $Backup = Join-Path $BackupRoot $Relative.Replace("/", "\")
        New-Item -ItemType Directory -Path (Split-Path -Parent $Backup) -Force | Out-Null
        Copy-Item -LiteralPath $Target -Destination $Backup -Force
    }
    $Entries += [ordered]@{ path = $Relative; existed = $Existed; backup_path = $Backup }
}
$StatePath = Join-Path $BackupRoot "INSTALL_STATE.json"
[ordered]@{ schema_version = "1.0.0"; repository_root = $Root; entries = $Entries } |
    ConvertTo-Json -Depth 6 |
    Set-Content -LiteralPath $StatePath -Encoding UTF8

try {
    foreach ($Relative in $Paths) {
        $Source = Join-Path $Stage $Relative.Replace("/", "\")
        $Target = Join-Path $Root $Relative.Replace("/", "\")
        New-Item -ItemType Directory -Path (Split-Path -Parent $Target) -Force | Out-Null
        $Temporary = $Target + ".uc04tmp"
        Copy-Item -LiteralPath $Source -Destination $Temporary -Force
        Move-Item -LiteralPath $Temporary -Destination $Target -Force
        if ($Relative -ne "releases/unified_consolidation/uc04/complete/PATCH_FILE_HASHES.sha256" -and (Get-Sha256 $Target) -ne $Ledger[$Relative]) {
            throw "Installed file hash mismatch: $Relative"
        }
    }

    $Python = Resolve-PythonCommand
    Push-Location -LiteralPath $Root
    try {
        Invoke-Python $Python @("tools/engineering/run_engineering_policy.py", ".")
        Invoke-Python $Python @("-m", "tools.consolidation.ci.verify_migration_continuity", "--repo-root", ".")
        Invoke-Python $Python @("-m", "tools.consolidation.uc03p3.verify", "--repo-root", ".", "--ci-fast")
        Invoke-Python $Python @("-m", "tools.consolidation.uc04complete.verify", "--repo-root", ".")
        Invoke-Python $Python @("-m", "pytest", "-q", "tests/consolidation/uc04w0", "tests/consolidation/uc04w1", "tests/consolidation/uc04w1b", "tests/consolidation/uc04w1bn1", "tests/consolidation/uc04complete", "tests/consolidation/ci", "-p", "no:cacheprovider")
        Invoke-Python $Python @("-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider")
    }
    finally { Pop-Location }

    Write-Host "UC04 complete static installation and mandatory gates: PASS" -ForegroundColor Green
    Write-Host "Rollback state: $StatePath"
    Write-Host "After committing this patch, run tools/consolidation/uc04complete/Invoke-UC04CompleteNativeSeal.ps1 with -FinalizeRepository."
}
catch {
    Write-Host ("Installation failed; automatic rollback started: {0}" -f $_.Exception.Message) -ForegroundColor Red
    Restore-FromState $Root $StatePath
    throw
}
