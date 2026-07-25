[CmdletBinding()]
param([string]$RepoRoot='.',[string]$MetaEditor='C:\Program Files\MetaTrader 5\metaeditor64.exe')
$ErrorActionPreference='Stop'
$root=(Resolve-Path -LiteralPath $RepoRoot).Path
if(-not(Test-Path -LiteralPath $MetaEditor)){throw "MetaEditor not found: $MetaEditor"}
$targets=@(
 'mql5\Tests\Experts\FaerieProtocol\EXP0019_FP_I04_DataSyncSelfTest.mq5',
 'mql5\Experts\FaerieProtocol\EXP0019_FP_I04_DataSyncDiagnostic.mq5'
)
foreach($relative in $targets){
 $file=Join-Path $root $relative;$log=$file+'.compile.log'
 & $MetaEditor "/compile:$file" "/log:$log" | Out-Null
 if(-not(Test-Path $log)){throw "Compile log missing: $log"}
 $content=Get-Content $log -Raw
 if($content -match '(?m)^[^\r\n]*\b[1-9][0-9]* errors?'){throw "Compile failed: $relative`n$content"}
}
Write-Host 'FP-I04 MetaEditor compile PASS; retain both logs.'
