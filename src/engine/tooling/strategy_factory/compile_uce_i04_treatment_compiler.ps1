param(
 [string]$MetaEditorPath="C:\Program Files\MetaTrader 5\metaeditor64.exe",
 [string]$Mql5Root="$env:APPDATA\MetaQuotes\Terminal\COMMON\Files\..\MQL5",
 [string]$RepoRoot="."
)
$ErrorActionPreference="Stop"
if(-not (Test-Path $MetaEditorPath)){throw "MetaEditor not found: $MetaEditorPath"}
$root=(Resolve-Path $RepoRoot).Path
$targets=@(
 "$root\mql5\Experts\StrategyFactory\UCE_I04_TreatmentCompilerDiagnostic.mq5",
 "$root\mql5\Tests\Experts\StrategyFactory\UCE_I04_TreatmentCompilerSelfTest.mq5"
)
foreach($target in $targets){
 $log="$target.compile.log"
 & $MetaEditorPath /compile:"$target" /inc:"$root\mql5\Include" /log:"$log"
 if($LASTEXITCODE -ne 0){throw "MetaEditor compile failed: $target"}
 $content=Get-Content $log -Raw
 if($content -match "[1-9][0-9]* error"){throw "Compile errors reported in $log"}
 Write-Host "Compiled: $target"
}
