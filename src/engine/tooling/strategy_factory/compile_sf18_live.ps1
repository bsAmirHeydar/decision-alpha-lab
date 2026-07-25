param([string]$MetaEditorPath="",[string]$RepositoryRoot=".")
$ErrorActionPreference="Stop"
if(-not $MetaEditorPath){
  $candidates=@("$env:ProgramFiles\MetaTrader 5\metaeditor64.exe","${env:ProgramFiles(x86)}\MetaTrader 5\metaeditor64.exe")
  $MetaEditorPath=$candidates|Where-Object{Test-Path $_}|Select-Object -First 1
}
if(-not $MetaEditorPath -or -not (Test-Path $MetaEditorPath)){throw "MetaEditor executable not found. Pass -MetaEditorPath."}
$targets=@(
 "mql5\Tests\Experts\StrategyFactory\SF18_LiveSafetySelfTest.mq5",
 "mql5\Experts\StrategyFactory\SF18_LiveSafetyDiagnostic.mq5",
 "mql5\Experts\StrategyFactory\SF18_MicroLiveHost.mq5")
foreach($target in $targets){
 $full=Join-Path (Resolve-Path $RepositoryRoot) $target
 & $MetaEditorPath "/compile:$full" "/log"
 if($LASTEXITCODE -ne 0){throw "MetaEditor compile failed: $target"}
}
