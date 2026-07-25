param(
 [Parameter(Mandatory=$true)][string]$MetaEditorPath,
 [Parameter(Mandatory=$true)][string]$TerminalMql5Root
)
$ErrorActionPreference="Stop"
$includeSrc=Join-Path $PSScriptRoot "..\..\mql5\Include\AlphaLab\StrategyFactory\Candidate"
$includeDst=Join-Path $TerminalMql5Root "Include\AlphaLab\StrategyFactory\Candidate"
New-Item -ItemType Directory -Force -Path $includeDst | Out-Null
Copy-Item "$includeSrc\*" $includeDst -Recurse -Force
$experts=@("SF08_CandidateEngineSelfTest.mq5","SF08_CandidateDiagnostic.mq5","SF08_StrategyHost.mq5")
foreach($name in $experts){
 $src=(Get-ChildItem (Join-Path $PSScriptRoot "..\..\mql5\Experts") -Recurse -Filter $name | Select-Object -First 1).FullName
 $dst=Join-Path $TerminalMql5Root "Experts\StrategyFactoryTests\$name"
 New-Item -ItemType Directory -Force -Path (Split-Path $dst) | Out-Null
 Copy-Item $src $dst -Force
 & $MetaEditorPath "/compile:$dst" "/log:$dst.log"
 if($LASTEXITCODE -ne 0){throw "MetaEditor failed for $name"}
}
