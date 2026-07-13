param(
  [string]$RepoRoot = ".",
  [string]$MetaEditor = "$env:ProgramFiles\MetaTrader 5\metaeditor64.exe"
)
$ErrorActionPreference = "Stop"
$root = (Resolve-Path $RepoRoot).Path
if (-not (Test-Path -LiteralPath $MetaEditor)) { throw "MetaEditor not found: $MetaEditor" }
$targets = @(
  "mql5\Experts\StrategyFactory\UCE_I12_StatisticalPromotionDiagnostic.mq5",
  "mql5\Experts\StrategyFactoryTests\UCE_I12_PromotionContractsSelfTest.mq5",
  "mql5\Experts\StrategyFactoryTests\UCE_I12_NonCompensatoryGateSelfTest.mq5"
)
foreach ($relative in $targets) {
  $source = Join-Path $root $relative
  $log = "$source.compile.log"
  & $MetaEditor "/compile:$source" "/log:$log"
  if ($LASTEXITCODE -ne 0) { throw "MetaEditor failed: $relative" }
  $content = Get-Content -LiteralPath $log -Raw
  if ($content -notmatch "0 error\(s\)") { throw "Compile errors in $relative. Read $log" }
}
Write-Host "UCE-I12 MetaEditor compile PASS"
