param(
 [Parameter(Mandatory=$true)][string]$MetaEditorPath,
 [Parameter(Mandatory=$true)][string]$TerminalMql5Root
)
$ErrorActionPreference="Stop"
$includeSrc=Join-Path $PSScriptRoot "..\..\mql5\Include\AlphaLab\StrategyFactory\Outcome"
$includeDst=Join-Path $TerminalMql5Root "Include\AlphaLab\StrategyFactory\Outcome"
New-Item -ItemType Directory -Force -Path $includeDst | Out-Null
Copy-Item "$includeSrc\*" $includeDst -Recurse -Force
$fixtureSrc=Join-Path $PSScriptRoot "..\..\mql5\Include\AlphaLab\StrategyFactory\Testing\SF09_OutcomeFixtures.mqh"
$fixtureDst=Join-Path $TerminalMql5Root "Include\AlphaLab\StrategyFactory\Testing\SF09_OutcomeFixtures.mqh"
New-Item -ItemType Directory -Force -Path (Split-Path $fixtureDst) | Out-Null
Copy-Item $fixtureSrc $fixtureDst -Force
$experts=@("SF09_OutcomeEngineSelfTest.mq5","SF09_OutcomeDiagnostic.mq5","SF09_StrategyHost.mq5")
foreach($name in $experts){
 $src=(Get-ChildItem (Join-Path $PSScriptRoot "..\..\mql5\Experts") -Recurse -Filter $name | Select-Object -First 1).FullName
 $dst=Join-Path $TerminalMql5Root "Experts\StrategyFactoryTests\$name"
 New-Item -ItemType Directory -Force -Path (Split-Path $dst) | Out-Null
 Copy-Item $src $dst -Force
 & $MetaEditorPath "/compile:$dst" "/log:$dst.log"
 if($LASTEXITCODE -ne 0){throw "MetaEditor failed for $name"}
}
