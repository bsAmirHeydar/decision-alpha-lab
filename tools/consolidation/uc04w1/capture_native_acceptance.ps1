param(
    [string]$RepoRoot = ".",
    [string]$MetaEditorPath = "",
    [string]$RuntimeCsv = "",
    [string]$MetaEditorBuild = "UNKNOWN",
    [string]$TerminalBuild = "UNKNOWN"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Get-Sha256([string]$Path) {
    return "sha256:" + (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
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
    if (-not $Found) {
        throw "MetaEditor64.exe was not found. Pass -MetaEditorPath explicitly."
    }
    return (Resolve-Path -LiteralPath $Found).Path
}

$Root = (Resolve-Path -LiteralPath $RepoRoot).Path
$MetaEditor = Resolve-MetaEditor $MetaEditorPath
$Stamp = [DateTime]::UtcNow.ToString("yyyyMMddTHHmmssZ")
$EvidenceRoot = Join-Path $Root ".alpha\runs\uc04w1\native_acceptance\$Stamp"
$WorkspaceRoot = Join-Path $EvidenceRoot "compile_workspace"
$WorkspaceMql5 = Join-Path $WorkspaceRoot "mql5"
$LogRoot = Join-Path $EvidenceRoot "metaeditor_logs"
$BinaryRoot = Join-Path $EvidenceRoot "compiled_ex5"
New-Item -ItemType Directory -Path $EvidenceRoot, $WorkspaceRoot, $LogRoot, $BinaryRoot -Force | Out-Null

# Compile from an isolated mirror so MetaEditor cannot dirty tracked MQL5 sources.
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
    "mql5/Tests/Experts/UC04/UC04W1_DeterministicDateTimeFormatSelfTest.mq5"
)

$CompileReceipts = @()
foreach ($RelativeTarget in $Targets) {
    $RelativeInsideMql5 = $RelativeTarget.Substring("mql5/".Length).Replace('/', '\')
    $Source = Join-Path $WorkspaceMql5 $RelativeInsideMql5
    if (-not (Test-Path -LiteralPath $Source -PathType Leaf)) {
        throw "Missing compile target in isolated workspace: $RelativeTarget"
    }
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
    $OriginalSource = Join-Path $Root $RelativeTarget.Replace('/', '\')
    $CompileReceipts += [ordered]@{
        source_path = $RelativeTarget
        source_sha256 = Get-Sha256 $OriginalSource
        errors = 0
        warnings = 0
        log_path = [System.IO.Path]::GetRelativePath($EvidenceRoot, $Log).Replace('\', '/')
        log_sha256 = Get-Sha256 $Log
        ex5_path = [System.IO.Path]::GetRelativePath($EvidenceRoot, $EvidenceEx5).Replace('\', '/')
        ex5_sha256 = Get-Sha256 $EvidenceEx5
    }
}

$RuntimeResult = [ordered]@{
    status = "PENDING"
    runtime_csv_path = $null
    runtime_csv_sha256 = $null
    fixture_rows = 0
    failed_rows = 0
    summary = $null
}
$OverallStatus = "COMPILE_PASS_RUNTIME_PENDING"
if (-not [string]::IsNullOrWhiteSpace($RuntimeCsv)) {
    $ResolvedRuntimeCsv = (Resolve-Path -LiteralPath $RuntimeCsv).Path
    $Rows = @(Import-Csv -LiteralPath $ResolvedRuntimeCsv)
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
    $EvidenceRuntimeCsv = Join-Path $EvidenceRoot "UC04W1_DeterministicDateTimeFormatSelfTest.csv"
    Copy-Item -LiteralPath $ResolvedRuntimeCsv -Destination $EvidenceRuntimeCsv -Force
    $RuntimeResult = [ordered]@{
        status = "PASS"
        runtime_csv_path = [System.IO.Path]::GetRelativePath($EvidenceRoot, $EvidenceRuntimeCsv).Replace('\', '/')
        runtime_csv_sha256 = Get-Sha256 $EvidenceRuntimeCsv
        fixture_rows = $FixtureRows.Count
        failed_rows = $FailedRows.Count
        summary = $SummaryRows[0].status
    }
    $OverallStatus = "PASS"
}

$Receipt = [ordered]@{
    schema_version = "1.0.0"
    program_id = "UCPS"
    stage_id = "UC04-W1B-NATIVE"
    receipt_id = "UC04_W1_NATIVE_ACCEPTANCE_$Stamp"
    status = $OverallStatus
    candidate_id = "ENGCAND_5F87C4D5849C4FD141DDBF29590235D8"
    engine_id = "ENG_9599AA665C5BC4B13B020EBA4213CB16"
    captured_at_utc = [DateTime]::UtcNow.ToString("o")
    metaeditor_path = $MetaEditor
    metaeditor_sha256 = Get-Sha256 $MetaEditor
    metaeditor_build = $MetaEditorBuild
    terminal_build = $TerminalBuild
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
Write-Host "UC04-W1 native acceptance capture: $OverallStatus" -ForegroundColor Green
Write-Host "Receipt: $ReceiptPath"
if ($OverallStatus -ne "PASS") {
    Write-Host "Compile evidence is complete; run the self-test in MetaTrader 5 and rerun with -RuntimeCsv <Common Files CSV>." -ForegroundColor Yellow
}
