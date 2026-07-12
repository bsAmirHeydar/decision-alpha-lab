param([string]$MetaEditorPath="C:\Program Files\MetaTrader 5\metaeditor64.exe",[string]$Mql5Root=".",[string]$LogDir=".\artifacts\uce_i06_compile")
$ErrorActionPreference="Stop";New-Item -ItemType Directory -Force -Path $LogDir|Out-Null
$targets=@("mql5\Experts\StrategyFactory\UCE_I06_OutcomeDatasetDiagnostic.mq5","mql5\Experts\StrategyFactoryTests\UCE_I06_OutcomeDatasetSelfTest.mq5","mql5\Experts\StrategyFactoryTests\UCE_I06_LongShortCounterfactualSelfTest.mq5")
foreach($target in $targets){$full=(Resolve-Path (Join-Path $Mql5Root $target)).Path;$name=[IO.Path]::GetFileNameWithoutExtension($target);$log=(Join-Path $LogDir ($name+".log"));& $MetaEditorPath /compile:$full /log:$log /inc:$Mql5Root;if($LASTEXITCODE -ne 0){throw "MetaEditor compile failed: $target"};$text=Get-Content $log -Raw;if($text -notmatch "0 errors, 0 warnings"){throw "Compile log is not clean: $log"}}
Write-Host "UCE-I06 MetaEditor compilation PASS"
