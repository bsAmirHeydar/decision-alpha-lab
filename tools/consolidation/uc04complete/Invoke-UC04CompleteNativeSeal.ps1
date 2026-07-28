param(
    [string]$RepositoryRoot = ".",
    [string]$MetaEditorPath = "",
    [string]$TerminalPath = "",
    [string]$TerminalDataPath = "",
    [string]$TerminalCommonFilesPath = "",
    [string]$RuntimeSymbol = "#USSPX500",
    [int]$RuntimeTimeoutSeconds = 240,
    [switch]$FinalizeRepository,
    [switch]$KeepTerminalTestFiles
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$RuntimeRelative = "AlphaLab\UC04\UC04_Phase4SharedPrimitivesSelfTest.csv"
$RuntimeScriptRelative = "AlphaLab\UC04\UC04_Phase4SharedPrimitivesSelfTest.ex5"

function Write-Utf8NoBom {
    param([string]$Path, [string]$Text)
    $Encoding = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Text, $Encoding)
}

function Get-Sha256 {
    param([string]$Path)
    return "sha256:" + (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Get-RelativePathCompat {
    param([string]$BasePath, [string]$TargetPath)
    $BaseFull = [System.IO.Path]::GetFullPath($BasePath).TrimEnd('\') + '\'
    $TargetFull = [System.IO.Path]::GetFullPath($TargetPath)
    $BaseUri = New-Object System.Uri($BaseFull)
    $TargetUri = New-Object System.Uri($TargetFull)
    return [System.Uri]::UnescapeDataString(
        $BaseUri.MakeRelativeUri($TargetUri).ToString()
    ).Replace('/', '\')
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

function Invoke-Python {
    param([psobject]$PythonCommand, [string[]]$Arguments)
    $Previous = $env:PYTHONDONTWRITEBYTECODE
    $env:PYTHONDONTWRITEBYTECODE = "1"
    try {
        $Prefix = @($PythonCommand.Prefix)
        & $PythonCommand.Executable @Prefix @Arguments
        $ExitCode = $LASTEXITCODE
    }
    finally {
        if ($null -eq $Previous) {
            Remove-Item Env:PYTHONDONTWRITEBYTECODE -ErrorAction SilentlyContinue
        }
        else {
            $env:PYTHONDONTWRITEBYTECODE = $Previous
        }
    }
    if ($ExitCode -ne 0) {
        throw ("Python command failed with exit code {0}: {1}" -f $ExitCode, ($Arguments -join " "))
    }
}

function Invoke-GitRead {
    param([string]$Root, [string[]]$Arguments)
    $Output = @(& git -C $Root @Arguments 2>&1)
    $ExitCode = $LASTEXITCODE
    if ($ExitCode -ne 0) {
        throw ("Git read command failed with exit code {0}: git {1}`n{2}" -f $ExitCode, ($Arguments -join " "), ($Output -join [Environment]::NewLine))
    }
    return @($Output)
}

function Get-TrackedState {
    param([string]$Root)
    return @(
        Invoke-GitRead $Root @("status", "--porcelain=v1", "--untracked-files=no") |
            Where-Object { $_ } |
            Sort-Object
    )
}

function Resolve-TerminalDataFromRepository {
    param([string]$Root)
    $Current = Get-Item -LiteralPath $Root
    while ($null -ne $Current) {
        if ($Current.PSIsContainer -and $Current.Name -ieq "MQL5") {
            $Origin = Join-Path $Current.Parent.FullName "origin.txt"
            if (Test-Path -LiteralPath $Origin -PathType Leaf) {
                return $Current.Parent.FullName
            }
        }
        $Current = $Current.Parent
    }
    return ""
}

function Resolve-TerminalData {
    param([string]$ExplicitPath, [string]$Root)
    if (-not [string]::IsNullOrWhiteSpace($ExplicitPath)) {
        if (-not (Test-Path -LiteralPath $ExplicitPath -PathType Container)) {
            throw "Terminal data directory does not exist: $ExplicitPath"
        }
        return (Resolve-Path -LiteralPath $ExplicitPath).Path
    }
    $Derived = Resolve-TerminalDataFromRepository $Root
    if (-not [string]::IsNullOrWhiteSpace($Derived)) {
        return (Resolve-Path -LiteralPath $Derived).Path
    }
    throw "Terminal data directory could not be derived from the repository path. Pass -TerminalDataPath explicitly."
}

function Resolve-InstallPathFromOrigin {
    param([string]$DataRoot)
    $Origin = Join-Path $DataRoot "origin.txt"
    if (-not (Test-Path -LiteralPath $Origin -PathType Leaf)) {
        throw "origin.txt is missing from terminal data directory: $Origin"
    }
    $Install = (Get-Content -LiteralPath $Origin -Raw).Trim().TrimEnd('\')
    if ([string]::IsNullOrWhiteSpace($Install) -or -not (Test-Path -LiteralPath $Install -PathType Container)) {
        throw "origin.txt does not resolve to a valid terminal installation: $Origin"
    }
    return (Resolve-Path -LiteralPath $Install).Path
}

function Resolve-MetaEditor {
    param([string]$ExplicitPath, [string]$InstallRoot)
    if (-not [string]::IsNullOrWhiteSpace($ExplicitPath)) {
        if (-not (Test-Path -LiteralPath $ExplicitPath -PathType Leaf)) {
            throw "MetaEditor does not exist: $ExplicitPath"
        }
        return (Resolve-Path -LiteralPath $ExplicitPath).Path
    }
    foreach ($Name in @("metaeditor64.exe", "MetaEditor64.exe")) {
        $Candidate = Join-Path $InstallRoot $Name
        if (Test-Path -LiteralPath $Candidate -PathType Leaf) {
            return (Resolve-Path -LiteralPath $Candidate).Path
        }
    }
    throw "MetaEditor64.exe was not found under the terminal installation. Pass -MetaEditorPath explicitly."
}

function Resolve-Terminal {
    param([string]$ExplicitPath, [string]$InstallRoot)
    if (-not [string]::IsNullOrWhiteSpace($ExplicitPath)) {
        if (-not (Test-Path -LiteralPath $ExplicitPath -PathType Leaf)) {
            throw "MetaTrader terminal does not exist: $ExplicitPath"
        }
        return (Resolve-Path -LiteralPath $ExplicitPath).Path
    }
    $Candidate = Join-Path $InstallRoot "terminal64.exe"
    if (Test-Path -LiteralPath $Candidate -PathType Leaf) {
        return (Resolve-Path -LiteralPath $Candidate).Path
    }
    throw "terminal64.exe was not found under the terminal installation. Pass -TerminalPath explicitly."
}

function Resolve-CommonFilesCandidates {
    param([string]$ExplicitPath)
    $Candidates = @()
    if (-not [string]::IsNullOrWhiteSpace($ExplicitPath)) {
        $Candidates += $ExplicitPath
    }
    if (-not [string]::IsNullOrWhiteSpace($env:ProgramData)) {
        $Candidates += (Join-Path $env:ProgramData "MetaQuotes\Terminal\Common\Files")
    }
    if (-not [string]::IsNullOrWhiteSpace($env:APPDATA)) {
        $Candidates += (Join-Path $env:APPDATA "MetaQuotes\Terminal\Common\Files")
    }
    return @($Candidates | Select-Object -Unique)
}

function Assert-TerminalNotRunning {
    param([string]$ResolvedTerminal)
    $Processes = Get-CimInstance Win32_Process -Filter "Name='terminal64.exe'" -ErrorAction SilentlyContinue
    foreach ($Process in $Processes) {
        if (-not $Process.ExecutablePath) { continue }
        if ([string]::Equals($Process.ExecutablePath, $ResolvedTerminal, [System.StringComparison]::OrdinalIgnoreCase)) {
            throw "The target MetaTrader terminal is already running. Close it before native qualification: $ResolvedTerminal"
        }
    }
}

function Invoke-CleanCompile {
    param(
        [string]$MetaEditor,
        [string]$WorkspaceMql5,
        [string]$Source,
        [string]$OriginalSource,
        [string]$RelativeTarget,
        [string]$LogRoot,
        [string]$BinaryRoot,
        [string]$EvidenceRoot
    )
    $SafeName = ($RelativeTarget -replace '[^A-Za-z0-9_.-]', '_')
    $AdjacentLog = [System.IO.Path]::ChangeExtension($Source, ".log")
    $ProducedEx5 = [System.IO.Path]::ChangeExtension($Source, ".ex5")
    Remove-Item -LiteralPath $AdjacentLog -Force -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $ProducedEx5 -Force -ErrorAction SilentlyContinue
    $Started = [DateTime]::UtcNow

    & $MetaEditor "/compile:$Source" "/include:$WorkspaceMql5" "/log"
    $ProcessExitCode = $LASTEXITCODE

    if (-not (Test-Path -LiteralPath $AdjacentLog -PathType Leaf)) {
        throw "MetaEditor log was not produced for $RelativeTarget (process exit code $ProcessExitCode)."
    }
    if (-not (Test-Path -LiteralPath $ProducedEx5 -PathType Leaf)) {
        throw "MetaEditor EX5 was not produced for $RelativeTarget (process exit code $ProcessExitCode)."
    }
    if ((Get-Item -LiteralPath $AdjacentLog).LastWriteTimeUtc -lt $Started.AddSeconds(-2)) {
        throw "MetaEditor log appears stale for $RelativeTarget."
    }
    if ((Get-Item -LiteralPath $ProducedEx5).LastWriteTimeUtc -lt $Started.AddSeconds(-2)) {
        throw "MetaEditor EX5 appears stale for $RelativeTarget."
    }

    $LogText = Get-Content -LiteralPath $AdjacentLog -Raw
    if ($LogText -notmatch '\b0\s+errors?\s*,\s*0\s+warnings?\b') {
        throw "Compile log is not clean for $RelativeTarget. See $AdjacentLog"
    }

    $EvidenceLog = Join-Path $LogRoot ($SafeName + ".log")
    $EvidenceEx5 = Join-Path $BinaryRoot ($SafeName + ".ex5")
    Copy-Item -LiteralPath $AdjacentLog -Destination $EvidenceLog -Force
    Copy-Item -LiteralPath $ProducedEx5 -Destination $EvidenceEx5 -Force

    return [ordered]@{
        source_path = $RelativeTarget
        source_sha256 = Get-Sha256 $OriginalSource
        metaeditor_process_exit_code = $ProcessExitCode
        errors = 0
        warnings = 0
        log_path = (Get-RelativePathCompat $EvidenceRoot $EvidenceLog).Replace('\', '/')
        log_sha256 = Get-Sha256 $EvidenceLog
        ex5_path = (Get-RelativePathCompat $EvidenceRoot $EvidenceEx5).Replace('\', '/')
        ex5_sha256 = Get-Sha256 $EvidenceEx5
    }
}


$Root = (Resolve-Path -LiteralPath $RepositoryRoot).Path
if (-not (Test-Path -LiteralPath (Join-Path $Root "AGENTS.md") -PathType Leaf)) {
    throw "RepositoryRoot does not contain AGENTS.md: $Root"
}
if ([string]::IsNullOrWhiteSpace($RuntimeSymbol)) {
    throw "RuntimeSymbol must not be empty."
}

$PythonCommand = Resolve-PythonCommand
$TrackedStateBefore = Get-TrackedState $Root
if ($TrackedStateBefore.Count -ne 0) {
    throw ("Tracked working tree must be clean before native seal:`n{0}" -f ($TrackedStateBefore -join [Environment]::NewLine))
}

Invoke-Python $PythonCommand @("tools/engineering/run_engineering_policy.py", $Root)
Invoke-Python $PythonCommand @("-m", "tools.consolidation.ci.verify_migration_continuity", "--repo-root", $Root)
Invoke-Python $PythonCommand @("-m", "tools.consolidation.uc03p3.verify", "--repo-root", $Root, "--ci-fast")
Invoke-Python $PythonCommand @("-m", "tools.consolidation.uc04complete.verify", "--repo-root", $Root)

$ContractPath = Join-Path $Root "registry\consolidation\uc04\complete\native_acceptance_contract.json"
$Contract = Get-Content -LiteralPath $ContractPath -Raw | ConvertFrom-Json
$Targets = @($Contract.compile_targets)
if ($Targets.Count -ne [int]$Contract.compile_target_count) {
    throw "Native contract target count is inconsistent."
}
$RuntimeSourceRelative = [string]$Contract.runtime_self_test

$DataRoot = Resolve-TerminalData $TerminalDataPath $Root
$InstallRoot = Resolve-InstallPathFromOrigin $DataRoot
$MetaEditor = Resolve-MetaEditor $MetaEditorPath $InstallRoot
$Terminal = Resolve-Terminal $TerminalPath $InstallRoot
Assert-TerminalNotRunning $Terminal

$Stamp = [DateTime]::UtcNow.ToString("yyyyMMddTHHmmssZ")
$RunParent = Join-Path $env:LOCALAPPDATA "AlphaLab\runs\uc04_complete\native_seal"
$EvidenceRoot = Join-Path $RunParent $Stamp
$WorkspaceRoot = Join-Path $EvidenceRoot "compile_workspace"
$WorkspaceMql5 = Join-Path $WorkspaceRoot "MQL5"
$LogRoot = Join-Path $EvidenceRoot "metaeditor_logs"
$BinaryRoot = Join-Path $EvidenceRoot "compiled_ex5"
$BackupRoot = Join-Path $EvidenceRoot "terminal_file_backup"
$ArtifactRoot = Join-Path $EvidenceRoot "native_artifacts"
New-Item -ItemType Directory -Path $WorkspaceRoot, $LogRoot, $BinaryRoot, $BackupRoot, $ArtifactRoot -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $Root "mql5") -Destination $WorkspaceMql5 -Recurse -Force
Get-ChildItem -LiteralPath $WorkspaceMql5 -Recurse -Filter "*.ex5" -File -ErrorAction SilentlyContinue | Remove-Item -Force
Get-ChildItem -LiteralPath $WorkspaceMql5 -Recurse -Filter "*.log" -File -ErrorAction SilentlyContinue | Remove-Item -Force

$CompileReceipts = @()
foreach ($RelativeTarget in $Targets) {
    $Inside = $RelativeTarget.Substring("mql5/".Length).Replace('/', '\')
    $Source = Join-Path $WorkspaceMql5 $Inside
    $OriginalSource = Join-Path $Root $RelativeTarget.Replace('/', '\')
    if (-not (Test-Path -LiteralPath $Source -PathType Leaf)) {
        throw "Missing compile target in isolated workspace: $RelativeTarget"
    }
    $CompileReceipts += Invoke-CleanCompile $MetaEditor $WorkspaceMql5 $Source $OriginalSource $RelativeTarget $LogRoot $BinaryRoot $EvidenceRoot
}

$TerminalMql5 = Join-Path $DataRoot "MQL5"
$InstalledScriptEx5 = Join-Path (Join-Path $TerminalMql5 "Scripts") $RuntimeScriptRelative
$CommonCandidates = Resolve-CommonFilesCandidates $TerminalCommonFilesPath
$RuntimeCandidates = @($CommonCandidates | ForEach-Object { Join-Path $_ $RuntimeRelative })
$ManagedFiles = @($InstalledScriptEx5)
$Backups = @{}

try {
    foreach ($Managed in $ManagedFiles) {
        if (Test-Path -LiteralPath $Managed -PathType Leaf) {
            $Safe = ($Managed -replace '[^A-Za-z0-9_.-]', '_')
            $Backup = Join-Path $BackupRoot $Safe
            Copy-Item -LiteralPath $Managed -Destination $Backup -Force
            $Backups[$Managed] = $Backup
        }
    }
    foreach ($RuntimeCandidate in $RuntimeCandidates) {
        Remove-Item -LiteralPath $RuntimeCandidate -Force -ErrorAction SilentlyContinue
    }

    New-Item -ItemType Directory -Path (Split-Path -Parent $InstalledScriptEx5) -Force | Out-Null
    $RuntimeCompileReceipt = $CompileReceipts | Where-Object { $_.source_path -eq $RuntimeSourceRelative } | Select-Object -First 1
    if (-not $RuntimeCompileReceipt) { throw "Runtime self-test compile receipt is missing." }
    $RuntimeEvidenceEx5 = Join-Path $EvidenceRoot $RuntimeCompileReceipt.ex5_path.Replace('/', '\')
    Copy-Item -LiteralPath $RuntimeEvidenceEx5 -Destination $InstalledScriptEx5 -Force

    $ConfigPath = Join-Path $EvidenceRoot "runtime_startup.ini"
    $ConfigText = @"
[Experts]
AllowLiveTrading=0
AllowDllImport=0
Enabled=1
Account=0
Profile=0

[StartUp]
Script=AlphaLab\UC04\UC04_Phase4SharedPrimitivesSelfTest
Symbol=$RuntimeSymbol
Period=M1
ShutdownTerminal=1
"@
    Write-Utf8NoBom $ConfigPath $ConfigText

    $Argument = "/config:`"$ConfigPath`""
    $Process = Start-Process -FilePath $Terminal -ArgumentList $Argument -PassThru
    if (-not $Process.WaitForExit($RuntimeTimeoutSeconds * 1000)) {
        Stop-Process -Id $Process.Id -Force -ErrorAction SilentlyContinue
        throw "MetaTrader runtime self-test exceeded $RuntimeTimeoutSeconds seconds."
    }
    if ($Process.ExitCode -ne 0) {
        throw "MetaTrader runtime process exited with code $($Process.ExitCode)."
    }

    $RuntimeCsv = $null
    $RuntimeCommonFiles = $null
    $Deadline = [DateTime]::UtcNow.AddSeconds(30)
    do {
        $Matches = @($RuntimeCandidates | Where-Object { Test-Path -LiteralPath $_ -PathType Leaf })
        if ($Matches.Count -gt 1) {
            throw ("Runtime CSV was produced in multiple common-file roots:`n{0}" -f ($Matches -join [Environment]::NewLine))
        }
        if ($Matches.Count -eq 1) {
            $RuntimeCsv = $Matches[0]
            $RuntimeCommonFiles = @($CommonCandidates | Where-Object {
                [string]::Equals((Join-Path $_ $RuntimeRelative), $RuntimeCsv, [System.StringComparison]::OrdinalIgnoreCase)
            })[0]
            break
        }
        Start-Sleep -Milliseconds 500
    } while ([DateTime]::UtcNow -lt $Deadline)

    if ($null -eq $RuntimeCsv) {
        throw ("Native runtime CSV was not produced. Checked:`n{0}" -f ($RuntimeCandidates -join [Environment]::NewLine))
    }

    $Rows = @(Import-Csv -LiteralPath $RuntimeCsv)
    $TestRows = @($Rows | Where-Object { $_.test_id -ne 'SUMMARY' })
    $SummaryRows = @($Rows | Where-Object { $_.test_id -eq 'SUMMARY' })
    $FailedRows = @($TestRows | Where-Object { $_.status -ne 'PASS' })
    if ($TestRows.Count -lt 20) { throw "Native runtime receipt must contain the complete primitive corpus." }
    if ($SummaryRows.Count -ne 1 -or $SummaryRows[0].status -ne 'PASS') { throw "Native runtime receipt summary is not PASS." }
    if ($SummaryRows[0].detail -notmatch 'failed=0') { throw "Native runtime receipt summary does not prove zero failures." }
    if ($FailedRows.Count -ne 0) { throw "Native runtime receipt contains failed rows." }

    $EvidenceRuntimeCsv = Join-Path $ArtifactRoot "UC04_Phase4SharedPrimitivesSelfTest.csv"
    Copy-Item -LiteralPath $RuntimeCsv -Destination $EvidenceRuntimeCsv -Force
    Copy-Item -LiteralPath $LogRoot -Destination (Join-Path $ArtifactRoot "metaeditor_logs") -Recurse -Force
    Copy-Item -LiteralPath $BinaryRoot -Destination (Join-Path $ArtifactRoot "compiled_ex5") -Recurse -Force

    $ArtifactBundle = Join-Path $EvidenceRoot "UC04_COMPLETE_NATIVE_ARTIFACTS_$Stamp.zip"
    $BundleJson = & $PythonCommand.Executable @($PythonCommand.Prefix) -m tools.consolidation.uc04complete.evidence_bundle --source-root $ArtifactRoot --output $ArtifactBundle
    if ($LASTEXITCODE -ne 0) { throw "Native artifact bundle creation failed." }
    $BundleResult = $BundleJson | ConvertFrom-Json

    $RuntimeResult = [ordered]@{
        status = "PASS"
        runtime_csv_path = (Get-RelativePathCompat $EvidenceRoot $EvidenceRuntimeCsv).Replace('\', '/')
        runtime_csv_sha256 = Get-Sha256 $EvidenceRuntimeCsv
        test_rows = $TestRows.Count
        failed_rows = $FailedRows.Count
        summary = $SummaryRows[0].status
        runtime_symbol = $RuntimeSymbol
    }

    $Receipt = [ordered]@{
        '$schema' = "../../../../schemas/consolidation/uc04/complete/native_seal_receipt.schema.json"
        program_id = "UCPS"
        stage_id = "UC04-COMPLETE-NATIVE-SEAL"
        schema_version = "1.0.0"
        status = "PASS"
        captured_at_utc = [DateTime]::UtcNow.ToString("o")
        compile_target_count = $CompileReceipts.Count
        compile_targets = $CompileReceipts
        runtime = $RuntimeResult
        evidence_bundle_sha256 = [string]$BundleResult.sha256
        production_source_mutation = $false
        semantic_change_authority = $false
        deletion_authority = $false
        runtime_authority = $false
        order_authority = $false
        capital_authority = $false
    }
    $ReceiptPath = Join-Path $EvidenceRoot "native_seal_receipt.json"
    Write-Utf8NoBom $ReceiptPath ($Receipt | ConvertTo-Json -Depth 12)

    $ReviewPath = Join-Path $EvidenceRoot "independent_native_review.json"
    Invoke-Python $PythonCommand @("-m", "tools.consolidation.uc04complete.native_review", "--repo-root", $Root, "--receipt", $ReceiptPath, "--output", $ReviewPath)

    $TrackedStateAfterQualification = Get-TrackedState $Root
    if (($TrackedStateAfterQualification -join "`n") -ne ($TrackedStateBefore -join "`n")) {
        throw ("Tracked repository state changed during native qualification.`nBefore:`n{0}`nAfter:`n{1}" -f ($TrackedStateBefore -join "`n"), ($TrackedStateAfterQualification -join "`n"))
    }

    if ($FinalizeRepository) {
        Invoke-Python $PythonCommand @("-m", "tools.consolidation.uc04complete.finalize", "--repo-root", $Root, "--receipt", $ReceiptPath, "--review", $ReviewPath)
    }

    Write-Host ""
    Write-Host "UC04 complete native seal: PASS" -ForegroundColor Green
    Write-Host "Evidence root: $EvidenceRoot"
    Write-Host "Native artifacts bundle: $ArtifactBundle"
    if ($FinalizeRepository) {
        Write-Host "UC04 acceptance and UC05 handoff records were materialized."
    }
    else {
        Write-Host "Repository was not modified. Re-run with -FinalizeRepository to materialize the accepted exit."
    }
    Write-Host "No production source, trading authority, or capital authority was changed."
}
finally {
    if (-not $KeepTerminalTestFiles) {
        foreach ($Managed in $ManagedFiles) {
            if (Test-Path -LiteralPath $Managed -PathType Leaf) {
                Remove-Item -LiteralPath $Managed -Force
            }
            if ($Backups.ContainsKey($Managed)) {
                New-Item -ItemType Directory -Path (Split-Path -Parent $Managed) -Force | Out-Null
                Copy-Item -LiteralPath $Backups[$Managed] -Destination $Managed -Force
            }
        }
    }
}
