param(
    [Parameter(Mandatory = $true)][string]$MetaEditorPath,
    [Parameter(Mandatory = $true)][string]$RepoRoot,
    [Parameter(Mandatory = $true)][string]$EvidenceRoot,
    [string]$MetaEditorBuild = "UNKNOWN",
    [string]$TerminalBuild = "UNKNOWN"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Get-Sha256([string]$Path) {
    return "sha256:" + (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

$RepoRoot = (Resolve-Path -LiteralPath $RepoRoot).Path
$MetaEditorPath = (Resolve-Path -LiteralPath $MetaEditorPath).Path
New-Item -ItemType Directory -Path $EvidenceRoot -Force | Out-Null
$EvidenceRoot = (Resolve-Path -LiteralPath $EvidenceRoot).Path
$LogRoot = Join-Path $EvidenceRoot "metaeditor_logs"
$BinaryRoot = Join-Path $EvidenceRoot "compiled_ex5"
New-Item -ItemType Directory -Path $LogRoot -Force | Out-Null
New-Item -ItemType Directory -Path $BinaryRoot -Force | Out-Null

$Targets = @(
    "mql5/Experts/FlagCounting/NDSHook864CycleR1ContractSelfTest.mq5",
    "mql5/Experts/EXP0019/FaerieProtocol/EXP0019_FaerieProtocol_Paper.mq5",
    "mql5/Tests/Experts/EXP0019/FaerieProtocol/EXP0019_FP_I15_PaperSelfTest.mq5",
    "mql5/Experts/StrategyFactory/SAED/V4_38/SAEDV438ParityHarness.mq5",
    "mql5/Experts/StrategyFactory/SAED/V4_39/SAEDV439PaperQualificationHarness.mq5",
    "mql5/Experts/StrategyFactory/SAED/V4_41/SAEDV441SurveillanceParityProbe.mq5"
)

$Receipts = @()
foreach ($RelativeTarget in $Targets) {
    $Source = Join-Path $RepoRoot $RelativeTarget
    if (-not (Test-Path -LiteralPath $Source -PathType Leaf)) {
        throw "Missing compile target: $RelativeTarget"
    }
    $SafeName = ($RelativeTarget -replace '[^A-Za-z0-9_.-]', '_')
    $Log = Join-Path $LogRoot ($SafeName + ".log")
    & $MetaEditorPath "/compile:$Source" "/log:$Log"
    if ($LASTEXITCODE -ne 0) {
        throw "MetaEditor process failed for $RelativeTarget with exit code $LASTEXITCODE"
    }
    if (-not (Test-Path -LiteralPath $Log -PathType Leaf)) {
        throw "MetaEditor log was not produced: $Log"
    }
    $LogText = Get-Content -LiteralPath $Log -Raw
    if ($LogText -notmatch '\b0\s+errors?\s*,\s*0\s+warnings?\b') {
        throw "Compile log is not clean for $RelativeTarget"
    }
    $ProducedEx5 = [System.IO.Path]::ChangeExtension($Source, ".ex5")
    if (-not (Test-Path -LiteralPath $ProducedEx5 -PathType Leaf)) {
        throw "Compiled EX5 was not found beside source: $ProducedEx5"
    }
    $EvidenceEx5 = Join-Path $BinaryRoot ([System.IO.Path]::GetFileName($ProducedEx5))
    Copy-Item -LiteralPath $ProducedEx5 -Destination $EvidenceEx5 -Force
    $Receipts += [ordered]@{
        source_path = $RelativeTarget.Replace('\', '/')
        source_sha256 = Get-Sha256 $Source
        errors = 0
        warnings = 0
        log_path = [System.IO.Path]::GetRelativePath($EvidenceRoot, $Log).Replace('\', '/')
        log_path_sha256 = Get-Sha256 $Log
        ex5_path = [System.IO.Path]::GetRelativePath($EvidenceRoot, $EvidenceEx5).Replace('\', '/')
        ex5_sha256 = Get-Sha256 $EvidenceEx5
    }
}

$Dimension = [ordered]@{
    status = "PASS"
    metaeditor_build = $MetaEditorBuild
    terminal_build = $TerminalBuild
    targets = $Receipts
}
$Output = Join-Path $EvidenceRoot "metaeditor_dimension.json"
$Dimension | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $Output -Encoding utf8
Write-Host "LCM-16B MetaEditor evidence captured: $Output" -ForegroundColor Green
