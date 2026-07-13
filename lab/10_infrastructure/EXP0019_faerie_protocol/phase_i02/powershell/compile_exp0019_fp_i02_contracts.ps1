[CmdletBinding()]
param(
 [string]$RepoRoot='.',
 [string]$MetaEditor='C:\Program Files\MetaTrader 5\metaeditor64.exe'
)
$ErrorActionPreference='Stop'
$repo=(Resolve-Path -LiteralPath $RepoRoot).Path
if(-not (Test-Path -LiteralPath $MetaEditor)){throw "MetaEditor not found: $MetaEditor"}
$targets=@(
 'mql5\Experts\FaerieProtocolTests\EXP0019_FP_I02_ContractKernelSelfTest.mq5',
 'mql5\Experts\FaerieProtocol\EXP0019_FP_I02_ContractKernelDiagnostic.mq5'
)
$logs=Join-Path $repo 'lab\10_infrastructure\EXP0019_faerie_protocol\phase_i02\artifacts\metaeditor_logs'
New-Item -ItemType Directory -Force -Path $logs | Out-Null
foreach($relative in $targets){
 $source=Join-Path $repo $relative
 $name=[IO.Path]::GetFileNameWithoutExtension($source)
 $log=Join-Path $logs ($name+'.compile.log')
 & $MetaEditor "/compile:$source" "/log:$log"
 if(-not (Test-Path $log)){throw "Compile log missing: $log"}
 $content=Get-Content $log -Raw
 if($content -notmatch '0 errors'){throw "MetaEditor compile failed: $log`n$content"}
}
Write-Host 'FP-I02 MetaEditor compile PASS'
