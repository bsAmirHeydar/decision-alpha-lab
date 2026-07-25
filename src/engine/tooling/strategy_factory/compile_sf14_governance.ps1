param([string]$MetaEditor = "metaeditor64.exe")
$ErrorActionPreference = "Stop"
$targets = @(
  "mql5\Tests\Experts\StrategyFactory\SF14_GovernanceSelfTest.mq5",
  "mql5\Experts\StrategyFactory\SF14_GovernanceDiagnostic.mq5",
  "mql5\Experts\StrategyFactory\SF14_ModelGovernanceHost.mq5"
)
foreach ($target in $targets) {
  & $MetaEditor "/compile:$target" "/log"
  if ($LASTEXITCODE -ne 0) { throw "MetaEditor compile failed: $target" }
}
