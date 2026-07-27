param(
    [ValidateSet("Install", "Rollback")]
    [string]$Action = "Install",

    [Parameter(Mandatory = $true)]
    [string]$RepositoryRoot,

    [string]$StagingRoot = "",
    [string]$ZipPath = "",
    [string]$ExpectedZipSha256 = "",
    [string]$BackupStatePath = ""
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$StageId = "UC04-W1B-Q"
$ReleaseRelative = "releases/unified_consolidation/uc04/w1b"
$IndexRelative = "$ReleaseRelative/PATCH_FILE_INDEX.txt"
$PackageModule = "tools.consolidation.uc04w1b.package_validation"

function Get-Sha256([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Resolve-PythonCommand {
    $Python = Get-Command python -ErrorAction SilentlyContinue
    if ($Python) {
        return [pscustomobject]@{ Executable = $Python.Source; Prefix = @("-B") }
    }
    $Py = Get-Command py -ErrorAction SilentlyContinue
    if ($Py) {
        return [pscustomobject]@{ Executable = $Py.Source; Prefix = @("-3", "-B") }
    }
    throw "Python 3 was not found."
}

function Invoke-Python(
    [psobject]$PythonCommand,
    [string[]]$Arguments,
    [string]$WorkingDirectory,
    [string]$LogPath = ""
) {
    $PreviousDontWriteBytecode = [Environment]::GetEnvironmentVariable(
        "PYTHONDONTWRITEBYTECODE",
        "Process"
    )
    [Environment]::SetEnvironmentVariable(
        "PYTHONDONTWRITEBYTECODE",
        "1",
        "Process"
    )

    Push-Location -LiteralPath $WorkingDirectory
    try {
        $Prefix = @($PythonCommand.Prefix)
        $Output = & $PythonCommand.Executable @Prefix @Arguments 2>&1
        $ExitCode = $LASTEXITCODE
        if ($LogPath) {
            $Parent = Split-Path -Parent $LogPath
            if ($Parent) { New-Item -ItemType Directory -Path $Parent -Force | Out-Null }
            @($Output) | Set-Content -LiteralPath $LogPath -Encoding utf8
        }
        @($Output) | ForEach-Object { Write-Host $_ }
        if ($ExitCode -ne 0) {
            throw ("Python command failed with exit code {0}: {1}" -f $ExitCode, ($Arguments -join ' '))
        }
    }
    finally {
        Pop-Location
        [Environment]::SetEnvironmentVariable(
            "PYTHONDONTWRITEBYTECODE",
            $PreviousDontWriteBytecode,
            "Process"
        )
    }
}

function Test-PathInside([string]$ChildPath, [string]$ParentPath) {
    $Child = [System.IO.Path]::GetFullPath($ChildPath).TrimEnd('\', '/') + [System.IO.Path]::DirectorySeparatorChar
    $Parent = [System.IO.Path]::GetFullPath($ParentPath).TrimEnd('\', '/') + [System.IO.Path]::DirectorySeparatorChar
    return $Child.StartsWith($Parent, [System.StringComparison]::OrdinalIgnoreCase)
}

function Assert-TargetPathsClean([string]$Root, [string[]]$Paths) {
    $Git = Get-Command git -ErrorAction SilentlyContinue
    if (-not $Git) {
        Write-Warning "Git was not found; target-path cleanliness could not be checked before installation."
        return
    }
    & $Git.Source -C $Root rev-parse --is-inside-work-tree *> $null
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "RepositoryRoot is not a Git working tree; target-path cleanliness check was skipped."
        return
    }
    $Status = @(& $Git.Source -C $Root status --porcelain=v1 --untracked-files=all -- @Paths 2>&1)
    if ($LASTEXITCODE -ne 0) {
        throw "git status failed while checking patch target paths."
    }
    if ($Status.Count -gt 0) {
        throw "Patch target paths contain uncommitted changes. Commit, restore, or remove them before installation:`n$($Status -join [Environment]::NewLine)"
    }
}

function Copy-Atomic([string]$Source, [string]$Destination, [string]$ExpectedSha256) {
    $Parent = Split-Path -Parent $Destination
    New-Item -ItemType Directory -Path $Parent -Force | Out-Null
    $Temporary = "$Destination.alpha-lab-tmp-$([Guid]::NewGuid().ToString('N'))"
    try {
        Copy-Item -LiteralPath $Source -Destination $Temporary -Force
        $Actual = Get-Sha256 $Temporary
        if ($Actual -ne $ExpectedSha256) {
            throw "Atomic copy hash mismatch for $Destination"
        }
        if (Test-Path -LiteralPath $Destination -PathType Leaf) {
            [System.IO.File]::Replace($Temporary, $Destination, $null, $true)
        }
        else {
            Move-Item -LiteralPath $Temporary -Destination $Destination
        }
    }
    finally {
        if (Test-Path -LiteralPath $Temporary -PathType Leaf) {
            Remove-Item -LiteralPath $Temporary -Force
        }
    }
}

function Assert-WindowsPathCapacity([string]$Root, [string[]]$Paths) {
    if ($env:OS -ne "Windows_NT") { return }
    $Longest = 0
    $LongestPath = ""
    foreach ($Relative in $Paths) {
        $Candidate = Join-Path $Root ($Relative -replace '/', '\')
        if ($Candidate.Length -gt $Longest) {
            $Longest = $Candidate.Length
            $LongestPath = $Candidate
        }
    }
    if ($Longest -lt 240) { return }
    $LongPathsEnabled = 0
    try {
        $LongPathsEnabled = [int](Get-ItemPropertyValue -LiteralPath "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name LongPathsEnabled -ErrorAction Stop)
    }
    catch {
        $LongPathsEnabled = 0
    }
    if ($LongPathsEnabled -ne 1) {
        throw "Longest destination path is $Longest characters and Windows LongPathsEnabled is not active. Enable long paths or use a shorter RepositoryRoot. Longest path: $LongestPath"
    }
    $Git = Get-Command git -ErrorAction SilentlyContinue
    if ($Git) {
        $GitLongPaths = (& $Git.Source -C $Root config --get core.longpaths 2>$null)
        if ($GitLongPaths -ne "true") {
            Write-Warning "Set git core.longpaths=true for this repository before staging long paths."
        }
    }
}

function Write-Json([object]$Value, [string]$Path) {
    $Parent = Split-Path -Parent $Path
    New-Item -ItemType Directory -Path $Parent -Force | Out-Null
    $Value | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath $Path -Encoding utf8
}

function Restore-InstallationState([string]$StatePath) {
    if (-not (Test-Path -LiteralPath $StatePath -PathType Leaf)) {
        throw "Rollback state does not exist: $StatePath"
    }
    $State = Get-Content -LiteralPath $StatePath -Raw | ConvertFrom-Json
    $Root = (Resolve-Path -LiteralPath $State.repository_root).Path
    foreach ($File in @($State.files)) {
        $Destination = Join-Path $Root ($File.path -replace '/', '\')
        if ([bool]$File.existed_before) {
            $Backup = [string]$File.backup_path
            if (-not (Test-Path -LiteralPath $Backup -PathType Leaf)) {
                throw "Rollback backup is missing: $Backup"
            }
            $BackupHash = Get-Sha256 $Backup
            if ($BackupHash -ne [string]$File.previous_sha256) {
                throw "Rollback backup hash mismatch: $($File.path)"
            }
            if (Test-Path -LiteralPath $Destination -PathType Leaf) {
                $CurrentHash = Get-Sha256 $Destination
                if ($CurrentHash -ne [string]$File.installed_sha256 -and $CurrentHash -ne [string]$File.previous_sha256) {
                    throw "Rollback refused because the installed file changed after installation: $($File.path)"
                }
            }
            Copy-Atomic $Backup $Destination $BackupHash
        }
        else {
            if (Test-Path -LiteralPath $Destination -PathType Leaf) {
                $CurrentHash = Get-Sha256 $Destination
                if ($CurrentHash -ne [string]$File.installed_sha256) {
                    throw "Rollback refused because a newly installed file changed after installation: $($File.path)"
                }
                Remove-Item -LiteralPath $Destination -Force
            }
        }
    }
    $RollbackReport = [ordered]@{
        schema_version = "1.0.0"
        stage_id = $StageId
        rollback_status = "PASS"
        repository_root = $Root
        source_state = $StatePath
        rolled_back_at_utc = [DateTime]::UtcNow.ToString("o")
    }
    $ReportPath = Join-Path (Split-Path -Parent $StatePath) "ROLLBACK_REPORT.json"
    Write-Json $RollbackReport $ReportPath
    Write-Host "Rollback completed: $ReportPath" -ForegroundColor Green
}

if ($Action -eq "Rollback") {
    if ([string]::IsNullOrWhiteSpace($BackupStatePath)) {
        throw "-BackupStatePath is required for rollback."
    }
    Restore-InstallationState $BackupStatePath
    exit 0
}

$Root = (Resolve-Path -LiteralPath $RepositoryRoot).Path
if (-not (Test-Path -LiteralPath (Join-Path $Root "AGENTS.md") -PathType Leaf)) {
    throw "RepositoryRoot does not contain AGENTS.md: $Root"
}
if ([string]::IsNullOrWhiteSpace($StagingRoot)) {
    throw "-StagingRoot is required for installation."
}
$Staging = (Resolve-Path -LiteralPath $StagingRoot).Path
if (Test-PathInside $Staging $Root) {
    throw "StagingRoot must be outside RepositoryRoot to avoid accidental Git staging: $Staging"
}
if (-not [string]::IsNullOrWhiteSpace($ZipPath)) {
    $ResolvedZip = (Resolve-Path -LiteralPath $ZipPath).Path
    if (-not [string]::IsNullOrWhiteSpace($ExpectedZipSha256)) {
        $Expected = $ExpectedZipSha256.ToLowerInvariant().Replace("sha256:", "")
        if ($Expected -notmatch '^[0-9a-f]{64}$') {
            throw "Expected ZIP SHA-256 must be 64 hexadecimal characters."
        }
        $ActualZipHash = Get-Sha256 $ResolvedZip
        if ($ActualZipHash -ne $Expected) {
            throw "ZIP SHA-256 mismatch. Expected $Expected, actual $ActualZipHash"
        }
    }
}

$PythonCommand = Resolve-PythonCommand
$StagedIndex = Join-Path $Staging ($IndexRelative -replace '/', '\')
if (-not (Test-Path -LiteralPath $StagedIndex -PathType Leaf)) {
    throw "Staged patch index is missing: $StagedIndex"
}

Invoke-Python $PythonCommand @(
    "-m", $PackageModule,
    "verify-tree",
    "--repo-root", $Staging,
    "--payload-only"
) $Staging

Invoke-Python $PythonCommand @(
    "-m", "tools.consolidation.uc04w0.verify",
    "--repo-root", $Root
) $Root
Invoke-Python $PythonCommand @(
    "-m", "tools.consolidation.uc04w1.verify",
    "--repo-root", $Root
) $Root

$IndexPaths = @(
    Get-Content -LiteralPath $StagedIndex |
        ForEach-Object { $_.Trim() } |
        Where-Object { $_ }
)
Assert-WindowsPathCapacity $Root $IndexPaths
Assert-TargetPathsClean $Root $IndexPaths

$BackupBase = if ($env:LOCALAPPDATA) {
    Join-Path $env:LOCALAPPDATA "AlphaLab\patch_backups\$StageId"
}
else {
    Join-Path ([System.IO.Path]::GetTempPath()) "AlphaLab\patch_backups\$StageId"
}
$RunId = [DateTime]::UtcNow.ToString("yyyyMMddTHHmmssZ") + "-" + [Guid]::NewGuid().ToString("N")
$BackupRoot = Join-Path $BackupBase $RunId
$BackupPayload = Join-Path $BackupRoot "previous_files"
$QaLogRoot = Join-Path $BackupRoot "qa_logs"
New-Item -ItemType Directory -Path $BackupPayload, $QaLogRoot -Force | Out-Null

$Files = @()
foreach ($Relative in $IndexPaths) {
    $Source = Join-Path $Staging ($Relative -replace '/', '\')
    $Destination = Join-Path $Root ($Relative -replace '/', '\')
    if (-not (Test-Path -LiteralPath $Source -PathType Leaf)) {
        throw "Staged source is missing: $Relative"
    }
    $InstalledHash = Get-Sha256 $Source
    $Existed = Test-Path -LiteralPath $Destination -PathType Leaf
    $PreviousHash = $null
    $BackupPath = $null
    if ($Existed) {
        $PreviousHash = Get-Sha256 $Destination
        $BackupPath = Join-Path $BackupPayload ($Relative -replace '/', '\')
        New-Item -ItemType Directory -Path (Split-Path -Parent $BackupPath) -Force | Out-Null
        Copy-Item -LiteralPath $Destination -Destination $BackupPath -Force
        if ((Get-Sha256 $BackupPath) -ne $PreviousHash) {
            throw "Backup verification failed: $Relative"
        }
    }
    $Files += [ordered]@{
        path = $Relative
        existed_before = $Existed
        previous_sha256 = $PreviousHash
        backup_path = $BackupPath
        installed_sha256 = $InstalledHash
    }
}

$StatePath = Join-Path $BackupRoot "INSTALL_STATE.json"
$State = [ordered]@{
    schema_version = "1.0.0"
    stage_id = $StageId
    install_status = "PLANNED"
    repository_root = $Root
    staging_root = $Staging
    zip_path = $ZipPath
    zip_sha256 = if ($ZipPath) { Get-Sha256 (Resolve-Path -LiteralPath $ZipPath).Path } else { $null }
    created_at_utc = [DateTime]::UtcNow.ToString("o")
    files = $Files
}
Write-Json $State $StatePath

try {
    foreach ($File in $Files) {
        $Source = Join-Path $Staging ($File.path -replace '/', '\')
        $Destination = Join-Path $Root ($File.path -replace '/', '\')
        Copy-Atomic $Source $Destination ([string]$File.installed_sha256)
    }

    $GateResults = @()
    $Gates = @(
        [ordered]@{ Name = "package_tree"; Arguments = @("-m", $PackageModule, "verify-tree", "--repo-root", $Root) },
        [ordered]@{ Name = "engineering_policy"; Arguments = @("tools/engineering/run_engineering_policy.py", ".") },
        [ordered]@{ Name = "migration_continuity"; Arguments = @("-m", "tools.consolidation.ci.verify_migration_continuity", "--repo-root", ".") },
        [ordered]@{ Name = "uc03_part3"; Arguments = @("-m", "tools.consolidation.uc03p3.verify", "--repo-root", ".", "--ci-fast") },
        [ordered]@{ Name = "uc04_w0"; Arguments = @("-m", "tools.consolidation.uc04w0.verify", "--repo-root", ".") },
        [ordered]@{ Name = "uc04_w1a"; Arguments = @("-m", "tools.consolidation.uc04w1.verify", "--repo-root", ".") },
        [ordered]@{ Name = "uc04_w1b"; Arguments = @("-m", "tools.consolidation.uc04w1b.verify", "--repo-root", ".") },
        [ordered]@{ Name = "targeted_pytest"; Arguments = @("-m", "pytest", "-p", "no:cacheprovider", "-q", "tests/consolidation/uc04w0", "tests/consolidation/uc04w1", "tests/consolidation/uc04w1b") },
        [ordered]@{ Name = "pytest_collection"; Arguments = @("-m", "pytest", "-p", "no:cacheprovider", "--collect-only", "-q") }
    )
    foreach ($Gate in $Gates) {
        $LogPath = Join-Path $QaLogRoot ($Gate.Name + ".log")
        Invoke-Python $PythonCommand $Gate.Arguments $Root $LogPath
        $GateResults += [ordered]@{
            gate = $Gate.Name
            status = "PASS"
            log_path = $LogPath
        }
    }

    $State["install_status"] = "PASS"
    $State["completed_at_utc"] = [DateTime]::UtcNow.ToString("o")
    $State["qa_logs"] = $QaLogRoot
    $State["gates"] = $GateResults
    Write-Json $State $StatePath

    Write-Host "UC04-W1B-Q installation and all mandatory gates: PASS" -ForegroundColor Green
    Write-Host "Rollback state: $StatePath"
    Write-Host "Stage only paths from: $(Join-Path $Root ($IndexRelative -replace '/', '\'))"
}
catch {
    $OriginalException = $_
    $Failure = $OriginalException.Exception.Message
    Write-Host "Installation failed; starting automatic rollback. Cause: $Failure" -ForegroundColor Red
    try {
        Restore-InstallationState $StatePath
    }
    catch {
        Write-Host "Automatic rollback also failed: $($_.Exception.Message)" -ForegroundColor Red
    }
    throw $OriginalException
}
