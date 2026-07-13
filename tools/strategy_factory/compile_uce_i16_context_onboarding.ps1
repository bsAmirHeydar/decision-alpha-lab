param([string]$MetaEditorPath="",[string]$RepoRoot="")
$ErrorActionPreference="Stop"
if(-not $RepoRoot){$RepoRoot=(Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path}
if(-not $MetaEditorPath){$MetaEditorPath=(Get-Command metaeditor64.exe -ErrorAction SilentlyContinue).Source}
if(-not $MetaEditorPath){throw "MetaEditor64 not found. Pass -MetaEditorPath explicitly."}
$Targets=@(
 "mql5\Experts\StrategyFactory\UCE_I16_ContextOnboardingDiagnostic.mq5",
 "mql5\Experts\StrategyFactoryTests\UCE_I16_ScaffoldIdentitySelfTest.mq5",
 "mql5\Experts\StrategyFactoryTests\UCE_I16_LegacyParitySelfTest.mq5",
 "mql5\Experts\StrategyFactoryTests\UCE_I16_CoreInvarianceSelfTest.mq5")
foreach($Target in $Targets){$Full=Join-Path $RepoRoot $Target;$Log="$Full.compile.log";& $MetaEditorPath "/compile:$Full" "/log:$Log";if($LASTEXITCODE -ne 0){throw "Compile failed: $Target"}}
