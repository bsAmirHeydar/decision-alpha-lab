param(
    [string]$MetaEditor = "$env:ProgramFiles\MetaTrader 5\metaeditor64.exe",
    [string]$ProjectRoot = (Resolve-Path "$PSScriptRoot\..\..\..").Path
)
$ErrorActionPreference = "Stop"
if (-not (Test-Path -LiteralPath $MetaEditor)) { throw "MetaEditor not found: $MetaEditor" }
$Targets = @(
    "mql5\Experts\StrategyFactory\SAED_V4_00_ConstitutionDiagnostic.mq5",
    "mql5\Experts\StrategyFactoryTests\SAED_V4_00_AuthoritySelfTest.mq5",
    "mql5\Experts\StrategyFactoryTests\SAED_V4_00_EvidenceFirewallSelfTest.mq5"
)
foreach ($Target in $Targets) {
    $Source = Join-Path $ProjectRoot $Target
    & $MetaEditor "/compile:$Source" "/log"
    if ($LASTEXITCODE -ne 0) { throw "MetaEditor compilation failed: $Target" }
}
Write-Host "Actual MetaEditor compilation completed. Preserve the generated logs as external_actual evidence."
