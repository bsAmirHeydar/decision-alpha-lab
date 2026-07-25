param(
  [string]$MetaEditorPath = "$env:ProgramFiles\MetaTrader 5\metaeditor64.exe",
  [string]$TerminalDataPath = "$env:APPDATA\MetaQuotes\Terminal",
  [string]$LogDirectory = ".\reports\saed_v4_05_metaeditor"
)

$ErrorActionPreference = "Stop"
if (-not (Test-Path -LiteralPath $MetaEditorPath)) { throw "MetaEditor not found: $MetaEditorPath" }
New-Item -ItemType Directory -Force -Path $LogDirectory | Out-Null
$experts = @(
  "mql5\Experts\AlphaLab\StrategyFactory\Diagnostics\EXP_SAED_V4_05_SemanticHypergraphSelfTest.mq5",
  "mql5\Experts\AlphaLab\StrategyFactory\Diagnostics\EXP_SAED_V4_05_HypergraphAuthoritySelfTest.mq5",
  "mql5\Experts\AlphaLab\StrategyFactory\Diagnostics\EXP_SAED_V4_05_HypergraphTemporalSelfTest.mq5"
)
foreach ($expert in $experts) {
  if (-not (Test-Path -LiteralPath $expert)) { throw "Expert missing: $expert" }
  $name = [IO.Path]::GetFileNameWithoutExtension($expert)
  $log = Join-Path $LogDirectory "$name.log"
  & $MetaEditorPath "/compile:$expert" "/log:$log"
  if ($LASTEXITCODE -ne 0) { throw "MetaEditor compile failed for $expert; inspect $log" }
}
Write-Host "MetaEditor compile commands completed. Retain logs as external actual evidence."
