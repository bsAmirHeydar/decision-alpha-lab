param([string]$MetaEditorPath = "C:\Program Files\MetaTrader 5\metaeditor64.exe")
$ErrorActionPreference = "Stop"
$targets = @("mql5\Experts\StrategyFactoryTests\SF13_TrainingContractsSelfTest.mq5","mql5\Experts\StrategyFactory\SF13_TrainingDiagnostic.mq5","mql5\Experts\StrategyFactory\SF13_DatasetExportResearchHost.mq5")
if (-not (Test-Path $MetaEditorPath)) { throw "MetaEditor not found: $MetaEditorPath" }
foreach ($target in $targets) { & $MetaEditorPath /compile:"$target" /log; if ($LASTEXITCODE -ne 0) { throw "MetaEditor compile failed: $target" } }
