param([string]$MetaEditor = "metaeditor64.exe", [string]$RepoRoot = ".")
$ErrorActionPreference = "Stop"
$targets = @(
  "mql5\Experts\StrategyFactory\UCE_I09_AdvancedTasksDiagnostic.mq5",
  "mql5\Experts\StrategyFactoryTests\UCE_I09_AdvancedTasksSelfTest.mq5",
  "mql5\Experts\StrategyFactoryTests\UCE_I09_ActionSupportSafetySelfTest.mq5"
)
foreach ($target in $targets) {
  $full = Join-Path (Resolve-Path $RepoRoot) $target
  & $MetaEditor "/compile:$full" "/inc:$(Join-Path (Resolve-Path $RepoRoot) 'mql5')" "/log"
  if ($LASTEXITCODE -ne 0) { throw "MetaEditor compile failed for $target" }
}
