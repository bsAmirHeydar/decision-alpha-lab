param(
  [string]$RepoRoot = ".",
  [string]$MetaEditorPath = ""
)
$ErrorActionPreference = "Stop"
$Root = (Resolve-Path $RepoRoot).Path
if (-not $MetaEditorPath) {
  $Candidates = @(
    "$env:ProgramFiles\MetaTrader 5\metaeditor64.exe",
    "$env:ProgramFiles\MetaTrader 5\MetaEditor64.exe",
    "$env:ProgramFiles(x86)\MetaTrader 5\metaeditor64.exe"
  )
  $MetaEditorPath = $Candidates | Where-Object { Test-Path $_ } | Select-Object -First 1
}
if (-not $MetaEditorPath -or -not (Test-Path $MetaEditorPath)) {
  throw "MetaEditor64.exe not found. Pass -MetaEditorPath explicitly."
}
$Targets = @(
  "mql5\Experts\StrategyFactory\UCE_I11_ExperimentOrchestrationDiagnostic.mq5",
  "mql5\Experts\StrategyFactoryTests\UCE_I11_ExperimentContractsSelfTest.mq5",
  "mql5\Experts\StrategyFactoryTests\UCE_I11_BudgetAndReproSelfTest.mq5"
)
$LogDir = Join-Path $Root "reports\strategy_factory\uce_i11_metaeditor"
New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
foreach ($Relative in $Targets) {
  $Target = Join-Path $Root $Relative
  $Log = Join-Path $LogDir ((Split-Path $Relative -Leaf) + ".log")
  & $MetaEditorPath "/compile:$Target" "/log:$Log"
  if ($LASTEXITCODE -ne 0) { throw "MetaEditor failed for $Relative. See $Log" }
  $Text = Get-Content $Log -Raw
  if ($Text -notmatch "0 error\(s\)") { throw "Compilation errors detected for $Relative. See $Log" }
}
Write-Host "UCE-I11 MetaEditor compile gate: PASS"
