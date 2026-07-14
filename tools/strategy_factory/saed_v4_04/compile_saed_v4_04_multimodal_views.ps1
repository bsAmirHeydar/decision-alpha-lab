param(
  [string]$MetaEditor = "C:\Program Files\MetaTrader 5\metaeditor64.exe",
  [string]$TerminalData = "$env:APPDATA\MetaQuotes\Terminal"
)
$ErrorActionPreference = "Stop"
if (-not (Test-Path $MetaEditor)) { throw "MetaEditor not found: $MetaEditor" }
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
$Targets = @(
  "mql5\Experts\AlphaLab\StrategyFactory\Diagnostics\EXP_SAED_V4_04_MultimodalViewDiagnostic.mq5",
  "mql5\Experts\AlphaLab\StrategyFactory\Diagnostics\EXP_SAED_V4_04_MultimodalViewSelfTest.mq5",
  "mql5\Experts\AlphaLab\StrategyFactory\Diagnostics\EXP_SAED_V4_04_ViewAuthoritySelfTest.mq5"
)
$Out = Join-Path $Root "lab\11_strategy_factory\artifacts\saed_v4_04\metaeditor"
New-Item -ItemType Directory -Force -Path $Out | Out-Null
foreach ($Rel in $Targets) {
  $File = Join-Path $Root $Rel
  $Log = Join-Path $Out ((Split-Path $File -Leaf) + ".log")
  & $MetaEditor "/compile:$File" "/log:$Log"
  if ($LASTEXITCODE -ne 0) { throw "MetaEditor compile failed for $Rel" }
}
Write-Host "MetaEditor compile evidence written to $Out"
