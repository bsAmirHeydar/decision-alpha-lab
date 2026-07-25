param([Parameter(Mandatory=$true)][string]$MetaEditor)
$ErrorActionPreference="Stop"
$files=@(
 ".\mql5\Tests\Experts\StrategyFactory\SF15_InferenceContractsSelfTest.mq5",
 ".\mql5\Tests\Experts\StrategyFactory\SF15_OnnxRuntimeSmokeTest.mq5",
 ".\mql5\Experts\StrategyFactory\SF15_InferenceDiagnostic.mq5",
 ".\mql5\Experts\StrategyFactory\SF15_InferenceHost.mq5")
foreach($file in $files){
 & $MetaEditor "/compile:$file" "/log"
 if($LASTEXITCODE -ne 0){throw "MetaEditor compile failed: $file"}
}
