$ErrorActionPreference = "Stop"
$MetaEditor = $env:MT5_METAEDITOR
if (-not $MetaEditor) { throw "Set MT5_METAEDITOR to the MetaEditor64.exe path." }
$Harness = Resolve-Path "mql5/Experts/DecisionAlphaLab/StrategyFactory/SAED/V4_10/SAEDV410CompileHarness.mq5"
& $MetaEditor "/compile:$Harness" "/log:SAED_V4_10_METAEDITOR.log"
if ($LASTEXITCODE -ne 0) { throw "MetaEditor compilation failed." }
