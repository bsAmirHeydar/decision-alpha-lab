param(
    [string]$RepoRoot = ".",
    [string]$MetaEditorPath = "",
    [string]$TerminalPath = "",
    [string]$TerminalDataPath = "",
    [string]$RuntimeSymbol = "EURUSD",
    [int]$RuntimeTimeoutSeconds = 180,
    [switch]$KeepTerminalTestFiles,
    [switch]$SkipCutoverCandidateGeneration
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$CandidateId = "ENGCAND_5F87C4D5849C4FD141DDBF29590235D8"
$EngineId = "ENG_9599AA665C5BC4B13B020EBA4213CB16"
$RuntimeRelative = "AlphaLab\UC04W1B\UC04W1B_DeterministicDateTimeFormatNativeRunner.csv"
$RuntimeScriptRelative = "AlphaLab\UC04W1B\UC04W1B_DeterministicDateTimeFormatNativeRunner.mq5"
$ReferenceIncludeRelative = "AlphaLab\UC04W1\AL_UC04W1_ReferenceDateTimeFormat.mqh"

function Get-Sha256([string]$Path) {
    return "sha256:" + (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Resolve-PythonCommand {
    $Python = Get-Command python -ErrorAction SilentlyContinue
    if ($Python) {
        return [pscustomobject]@{ Executable = $Python.Source; Prefix = @() }
    }
    $Py = Get-Command py -ErrorAction SilentlyContinue
    if ($Py) {
        return [pscustomobject]@{ Executable = $Py.Source; Prefix = @("-3") }
    }
    throw "Python 3 was not found."
}

function Resolve-MetaEditor([string]$ExplicitPath) {
    if (-not [string]::IsNullOrWhiteSpace($ExplicitPath)) {
        if (-not (Test-Path -LiteralPath $ExplicitPath -PathType Leaf)) {
            throw "MetaEditor does not exist: $ExplicitPath"
        }
        return (Resolve-Path -LiteralPath $ExplicitPath).Path
    }
    $Command = Get-Command metaeditor64.exe -ErrorAction SilentlyContinue
    if ($Command) { return $Command.Source }
    $Candidates = @(
        "$env:ProgramFiles\MetaTrader 5\metaeditor64.exe",
        "$env:ProgramFiles\MetaTrader 5\MetaEditor64.exe",
        "${env:ProgramFiles(x86)}\MetaTrader 5\metaeditor64.exe"
    )
    $Found = $Candidates | Where-Object { $_ -and (Test-Path -LiteralPath $_ -PathType Leaf) } | Select-Object -First 1
    if (-not $Found) { throw "MetaEditor64.exe was not found. Pass -MetaEditorPath explicitly." }
    return (Resolve-Path -LiteralPath $Found).Path
}

function Resolve-Terminal([string]$ExplicitPath, [string]$ResolvedMetaEditor) {
    if (-not [string]::IsNullOrWhiteSpace($ExplicitPath)) {
        if (-not (Test-Path -LiteralPath $ExplicitPath -PathType Leaf)) {
            throw "MetaTrader terminal does not exist: $ExplicitPath"
        }
        return (Resolve-Path -LiteralPath $ExplicitPath).Path
    }
    $Sibling = Join-Path (Split-Path -Parent $ResolvedMetaEditor) "terminal64.exe"
    if (Test-Path -LiteralPath $Sibling -PathType Leaf) {
        return (Resolve-Path -LiteralPath $Sibling).Path
    }
    $Command = Get-Command terminal64.exe -ErrorAction SilentlyContinue
    if ($Command) { return $Command.Source }
    throw "terminal64.exe was not found. Pass -TerminalPath explicitly."
}

function Resolve-TerminalData([string]$ExplicitPath, [string]$ResolvedTerminal) {
    if (-not [string]::IsNullOrWhiteSpace($ExplicitPath)) {
        if (-not (Test-Path -LiteralPath $ExplicitPath -PathType Container)) {
            throw "Terminal data directory does not exist: $ExplicitPath"
        }
        return (Resolve-Path -LiteralPath $ExplicitPath).Path
    }
    $TerminalInstall = (Split-Path -Parent $ResolvedTerminal).TrimEnd('\')
    $TerminalHome = Join-Path $env:APPDATA "MetaQuotes\Terminal"
    if (-not (Test-Path -LiteralPath $TerminalHome -PathType Container)) {
        throw "MetaTrader data root does not exist: $TerminalHome"
    }
    $Matches = @()
    foreach ($Directory in Get-ChildItem -LiteralPath $TerminalHome -Directory -ErrorAction SilentlyContinue) {
        $Origin = Join-Path $Directory.FullName "origin.txt"
        if (-not (Test-Path -LiteralPath $Origin -PathType Leaf)) { continue }
        $OriginValue = (Get-Content -LiteralPath $Origin -Raw).Trim().TrimEnd('\')
        if ([string]::Equals($OriginValue, $TerminalInstall, [System.StringComparison]::OrdinalIgnoreCase)) {
            $Matches += $Directory.FullName
        }
    }
    if ($Matches.Count -ne 1) {
        throw "Could not resolve exactly one terminal data directory for $TerminalInstall. Pass -TerminalDataPath explicitly."
    }
    return (Resolve-Path -LiteralPath $Matches[0]).Path
}

function Assert-TerminalNotRunning([string]$ResolvedTerminal) {
    $Processes = Get-CimInstance Win32_Process -Filter "Name='terminal64.exe'" -ErrorAction SilentlyContinue
    foreach ($Process in $Processes) {
        if (-not $Process.ExecutablePath) { continue }
        if ([string]::Equals($Process.ExecutablePath, $ResolvedTerminal, [System.StringComparison]::OrdinalIgnoreCase)) {
            throw "The target MetaTrader terminal is already running. Close it before native qualification: $ResolvedTerminal"
        }
    }
}

function Invoke-Python([psobject]$PythonCommand, [string[]]$Arguments) {
    $Prefix = @($PythonCommand.Prefix)
    & $PythonCommand.Executable @Prefix @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Python command failed with exit code $LASTEXITCODE"
    }
}

function Get-RelativePath([string]$BasePath, [string]$TargetPath) {
    $BaseFull = [System.IO.Path]::GetFullPath($BasePath).TrimEnd('\') + '\'
    $TargetFull = [System.IO.Path]::GetFullPath($TargetPath)
    $BaseUri = New-Object System.Uri($BaseFull)
    $TargetUri = New-Object System.Uri($TargetFull)
    return [System.Uri]::UnescapeDataString($BaseUri.MakeRelativeUri($TargetUri).ToString()).Replace('/', '\')
}

function Invoke-CleanCompile(
    [string]$MetaEditor,
    [string]$WorkspaceMql5,
    [string]$Source,
    [string]$OriginalSource,
    [string]$RelativeTarget,
    [string]$LogRoot,
    [string]$BinaryRoot,
    [string]$EvidenceRoot
) {
    $SafeName = ($RelativeTarget -replace '[^A-Za-z0-9_.-]', '_')
    $Log = Join-Path $LogRoot ($SafeName + ".log")
    & $MetaEditor "/compile:$Source" "/inc:$WorkspaceMql5" "/log:$Log"
    if ($LASTEXITCODE -ne 0) {
        throw "MetaEditor process failed for $RelativeTarget with exit code $LASTEXITCODE"
    }
    if (-not (Test-Path -LiteralPath $Log -PathType Leaf)) {
        throw "MetaEditor log was not produced for $RelativeTarget"
    }
    $LogText = Get-Content -LiteralPath $Log -Raw
    if ($LogText -notmatch '\b0\s+errors?\s*,\s*0\s+warnings?\b') {
        throw "Compile log is not clean for $RelativeTarget. See $Log"
    }
    $ProducedEx5 = [System.IO.Path]::ChangeExtension($Source, ".ex5")
    if (-not (Test-Path -LiteralPath $ProducedEx5 -PathType Leaf)) {
        throw "Compiled EX5 was not produced for $RelativeTarget"
    }
    $EvidenceEx5 = Join-Path $BinaryRoot ($SafeName + ".ex5")
    Copy-Item -LiteralPath $ProducedEx5 -Destination $EvidenceEx5 -Force
    return [ordered]@{
        source_path = $RelativeTarget
        source_sha256 = Get-Sha256 $OriginalSource
        errors = 0
        warnings = 0
        log_path = (Get-RelativePath $EvidenceRoot $Log).Replace('\', '/')
        log_sha256 = Get-Sha256 $Log
        ex5_path = (Get-RelativePath $EvidenceRoot $EvidenceEx5).Replace('\', '/')
        ex5_sha256 = Get-Sha256 $EvidenceEx5
    }
}

$Root = (Resolve-Path -LiteralPath $RepoRoot).Path
$MetaEditor = Resolve-MetaEditor $MetaEditorPath
$Terminal = Resolve-Terminal $TerminalPath $MetaEditor
$DataRoot = Resolve-TerminalData $TerminalDataPath $Terminal
$PythonCommand = Resolve-PythonCommand
Assert-TerminalNotRunning $Terminal

$Stamp = [DateTime]::UtcNow.ToString("yyyyMMddTHHmmssZ")
$EvidenceRoot = Join-Path $Root ".alpha\runs\uc04w1b\native_qualification\$Stamp"
$WorkspaceRoot = Join-Path $EvidenceRoot "compile_workspace"
$WorkspaceMql5 = Join-Path $WorkspaceRoot "mql5"
$LogRoot = Join-Path $EvidenceRoot "metaeditor_logs"
$BinaryRoot = Join-Path $EvidenceRoot "compiled_ex5"
$BackupRoot = Join-Path $EvidenceRoot "terminal_file_backup"
New-Item -ItemType Directory -Path $EvidenceRoot, $WorkspaceRoot, $LogRoot, $BinaryRoot, $BackupRoot -Force | Out-Null

Copy-Item -LiteralPath (Join-Path $Root "mql5") -Destination $WorkspaceMql5 -Recurse -Force
Get-ChildItem -LiteralPath $WorkspaceMql5 -Recurse -Filter "*.ex5" -File -ErrorAction SilentlyContinue | Remove-Item -Force

$Targets = @(
    "mql5/Experts/Debug/D0005_H5NoFutureWalkForwardAudit.mq5",
    "mql5/Experts/Debug/D0006_H5LiveTouchReplayAudit.mq5",
    "mql5/Experts/Execution/E0001_ReversalOneToOne.mq5",
    "mql5/Experts/Execution/E0002_CloseConfirmedMarket.mq5",
    "mql5/Experts/Execution/E0003_ContinuationCloseHunt.mq5",
    "mql5/Experts/Execution/E0004_ContinuationHeikinAshiFlip.mq5",
    "mql5/Experts/Execution/E0005_ContinuationCloseBreakFixedR.mq5",
    "mql5/Experts/Execution/E0006_AllZoneTouchLimitFixedR.mq5",
    "mql5/Experts/Execution/E0010_PureHeikinAshiMtfRoulette.mq5",
    "mql5/Experts/Execution/E0011_Donchian20Atr3Roulette.mq5",
    "mql5/Tests/Experts/UC04/UC04W1_DeterministicDateTimeFormatSelfTest.mq5",
    "mql5/Tests/Scripts/UC04/UC04W1B_DeterministicDateTimeFormatNativeRunner.mq5"
)

$CompileReceipts = @()
foreach ($RelativeTarget in $Targets) {
    $RelativeInsideMql5 = $RelativeTarget.Substring("mql5/".Length).Replace('/', '\')
    $Source = Join-Path $WorkspaceMql5 $RelativeInsideMql5
    $OriginalSource = Join-Path $Root $RelativeTarget.Replace('/', '\')
    if (-not (Test-Path -LiteralPath $Source -PathType Leaf)) {
        throw "Missing compile target in isolated workspace: $RelativeTarget"
    }
    $CompileReceipts += Invoke-CleanCompile $MetaEditor $WorkspaceMql5 $Source $OriginalSource $RelativeTarget $LogRoot $BinaryRoot $EvidenceRoot
}

$TerminalMql5 = Join-Path $DataRoot "MQL5"
$InstalledScriptEx5 = Join-Path (Join-Path $TerminalMql5 "Scripts") "AlphaLab\UC04W1B\UC04W1B_DeterministicDateTimeFormatNativeRunner.ex5"
$RuntimeCommonRoot = Join-Path $env:ProgramData "MetaQuotes\Terminal\Common\Files"
$RuntimeCsv = Join-Path $RuntimeCommonRoot $RuntimeRelative

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

    New-Item -ItemType Directory -Path (Split-Path -Parent $InstalledScriptEx5), (Split-Path -Parent $RuntimeCsv) -Force | Out-Null
    if (Test-Path -LiteralPath $RuntimeCsv -PathType Leaf) { Remove-Item -LiteralPath $RuntimeCsv -Force }

    $RuntimeCompileReceipt = $CompileReceipts | Where-Object { $_.source_path -eq "mql5/Tests/Scripts/UC04/UC04W1B_DeterministicDateTimeFormatNativeRunner.mq5" } | Select-Object -First 1
    if (-not $RuntimeCompileReceipt) { throw "Runtime script compile receipt is missing." }
    $RuntimeEvidenceEx5 = Join-Path $EvidenceRoot $RuntimeCompileReceipt.ex5_path.Replace('/', '\')
    if (-not (Test-Path -LiteralPath $RuntimeEvidenceEx5 -PathType Leaf)) { throw "Runtime script evidence EX5 is missing." }
    Copy-Item -LiteralPath $RuntimeEvidenceEx5 -Destination $InstalledScriptEx5 -Force

    $ConfigPath = Join-Path $EvidenceRoot "runtime_startup.ini"
    @"
[Experts]
AllowLiveTrading=0
AllowDllImport=0
Enabled=1
Account=0
Profile=0

[StartUp]
Script=AlphaLab\UC04W1B\UC04W1B_DeterministicDateTimeFormatNativeRunner
Symbol=$RuntimeSymbol
Period=M1
ShutdownTerminal=1
"@ | Set-Content -LiteralPath $ConfigPath -Encoding utf8

    $Process = Start-Process -FilePath $Terminal -ArgumentList @("/config:`"$ConfigPath`"") -PassThru
    if (-not $Process.WaitForExit($RuntimeTimeoutSeconds * 1000)) {
        Stop-Process -Id $Process.Id -Force -ErrorAction SilentlyContinue
        throw "MetaTrader runtime self-test exceeded $RuntimeTimeoutSeconds seconds."
    }
    if (-not (Test-Path -LiteralPath $RuntimeCsv -PathType Leaf)) {
        throw "Native runtime CSV was not produced: $RuntimeCsv"
    }

    $Rows = @(Import-Csv -LiteralPath $RuntimeCsv)
    $FixtureRows = @($Rows | Where-Object { $_.fixture_id -match '^UC04W1_DT_[0-9]{3}$' })
    $SummaryRows = @($Rows | Where-Object { $_.fixture_id -eq 'SUMMARY' })
    $FailedRows = @($FixtureRows | Where-Object {
        $_.status -ne 'PASS' -or
        $_.expected -ne $_.legacy_output -or
        $_.expected -ne $_.reference_output -or
        $_.expected.Length -ne 19
    })
    if ($FixtureRows.Count -ne 13) { throw "Native runtime receipt must contain exactly 13 fixture rows." }
    if ($SummaryRows.Count -ne 1 -or $SummaryRows[0].status -ne 'PASS') { throw "Native runtime receipt summary is not PASS." }
    if ($FailedRows.Count -ne 0) { throw "Native runtime receipt contains failed or non-equivalent rows." }

    $EvidenceRuntimeCsv = Join-Path $EvidenceRoot "UC04W1B_DeterministicDateTimeFormatNativeRunner.csv"
    Copy-Item -LiteralPath $RuntimeCsv -Destination $EvidenceRuntimeCsv -Force
    $RuntimeResult = [ordered]@{
        status = "PASS"
        runtime_csv_path = (Get-RelativePath $EvidenceRoot $EvidenceRuntimeCsv).Replace('\', '/')
        runtime_csv_sha256 = Get-Sha256 $EvidenceRuntimeCsv
        fixture_rows = $FixtureRows.Count
        failed_rows = $FailedRows.Count
        summary = $SummaryRows[0].status
        runtime_symbol = $RuntimeSymbol
    }

    $Receipt = [ordered]@{
        schema_version = "1.0.0"
        program_id = "UCPS"
        stage_id = "UC04-W1B-Q-NATIVE"
        receipt_id = "UC04_W1B_NATIVE_ACCEPTANCE_$Stamp"
        status = "PASS"
        candidate_id = $CandidateId
        engine_id = $EngineId
        captured_at_utc = [DateTime]::UtcNow.ToString("o")
        metaeditor_path = $MetaEditor
        metaeditor_sha256 = Get-Sha256 $MetaEditor
        metaeditor_build = (Get-Item -LiteralPath $MetaEditor).VersionInfo.FileVersion
        terminal_path = $Terminal
        terminal_sha256 = Get-Sha256 $Terminal
        terminal_build = (Get-Item -LiteralPath $Terminal).VersionInfo.FileVersion
        terminal_data_path = $DataRoot
        isolated_compile_workspace = $true
        tracked_source_mutation = $false
        compile_target_count = $CompileReceipts.Count
        compile_status = "PASS"
        compile_targets = $CompileReceipts
        runtime = $RuntimeResult
        implementation_authority = $false
        consumer_cutover_authority = $false
        deletion_authority = $false
        runtime_authority = $false
        order_authority = $false
        capital_authority = $false
    }
    $ReceiptPath = Join-Path $EvidenceRoot "native_acceptance_receipt.json"
    $Receipt | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $ReceiptPath -Encoding utf8

    $ReviewPath = Join-Path $EvidenceRoot "independent_native_review.json"
    Invoke-Python $PythonCommand @(
        "-m", "tools.consolidation.uc04w1b.native_review",
        "--repo-root", $Root,
        "--receipt", $ReceiptPath,
        "--output", $ReviewPath
    )

    if (-not $SkipCutoverCandidateGeneration) {
        Invoke-Python $PythonCommand @(
            "-m", "tools.consolidation.uc04w1b.cutover_candidate",
            "--repo-root", $Root,
            "--receipt", $ReceiptPath,
            "--review", $ReviewPath
        )
    }

    Write-Host "UC04-W1B native qualification: PASS" -ForegroundColor Green
    Write-Host "Receipt: $ReceiptPath"
    Write-Host "Independent review: $ReviewPath"
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
