param([string]$MetaEditor = "C:\Program Files\MetaTrader 5\metaeditor64.exe")
$ErrorActionPreference = "Stop"
if (!(Test-Path $MetaEditor)) { throw "MetaEditor not found: $MetaEditor" }
$targets=@(
  ".\mql5\Experts\StrategyFactory\SF17_PaperShadowHost.mq5",
  ".\mql5\Experts\StrategyFactory\SF17_ExecutionDiagnostic.mq5",
  ".\mql5\Tests\Experts\StrategyFactory\SF17_PaperExecutionSelfTest.mq5"
)
foreach($target in $targets){ & $MetaEditor /compile:$target /log; if($LASTEXITCODE -ne 0){throw "Compile failed: $target"} }
