param([string]$MetaEditor="metaeditor64.exe",[string]$LogDir=".\artifacts\saed_v4_02_compile")
$ErrorActionPreference="Stop"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$Experts=@(
 "mql5\Experts\AlphaLab\StrategyFactory\Diagnostics\EXP_SAED_V4_02_ContextTwinDiagnostic.mq5",
 "mql5\Experts\AlphaLab\StrategyFactory\Diagnostics\EXP_SAED_V4_02_ContextTwinSelfTest.mq5",
 "mql5\Experts\AlphaLab\StrategyFactory\Diagnostics\EXP_SAED_V4_02_TwinAuthoritySelfTest.mq5"
)
foreach($Expert in $Experts){$Name=[IO.Path]::GetFileNameWithoutExtension($Expert);& $MetaEditor /compile:"$Expert" /log:"$LogDir\$Name.log";if($LASTEXITCODE -ne 0){throw "MetaEditor compile failed for $Expert"}}
