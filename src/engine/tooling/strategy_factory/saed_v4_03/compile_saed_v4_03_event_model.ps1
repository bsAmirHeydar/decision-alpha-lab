param([string]$MetaEditorPath="")
if (-not $MetaEditorPath) { throw "Provide the full MetaEditor64.exe path." }
$Root=(Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
$Experts=@("EXP_SAED_V4_03_EventModelDiagnostic.mq5","EXP_SAED_V4_03_EventModelSelfTest.mq5","EXP_SAED_V4_03_EventAuthoritySelfTest.mq5")
foreach($Expert in $Experts){$File=Join-Path $Root "mql5\Experts\AlphaLab\StrategyFactory\Diagnostics\$Expert";$Log="$File.log";& $MetaEditorPath /compile:$File /log:$Log;if($LASTEXITCODE -ne 0){throw "MetaEditor compile failed: $Expert"}}
