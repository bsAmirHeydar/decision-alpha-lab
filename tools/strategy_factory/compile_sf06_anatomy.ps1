param([Parameter(Mandatory=$true)][string]$MetaEditorPath,[Parameter(Mandatory=$true)][string]$TerminalMql5Root)
$ErrorActionPreference="Stop"
$repo=(Resolve-Path ".").Path
$inc=Join-Path $TerminalMql5Root "Include\AlphaLab\StrategyFactory"
New-Item -ItemType Directory -Force -Path $inc | Out-Null
Copy-Item -Recurse -Force "$repo\mql5\Include\AlphaLab\StrategyFactory\*" $inc
$experts=Join-Path $TerminalMql5Root "Experts\StrategyFactoryTests";New-Item -ItemType Directory -Force -Path $experts|Out-Null
Copy-Item -Force "$repo\mql5\Experts\StrategyFactoryTests\SF06_ReferenceAnatomySelfTest.mq5" $experts
$host=Join-Path $TerminalMql5Root "Experts\StrategyFactory";New-Item -ItemType Directory -Force -Path $host|Out-Null
Copy-Item -Force "$repo\mql5\Experts\StrategyFactory\SF06_StrategyHost.mq5" $host
& $MetaEditorPath /compile:"$experts\SF06_ReferenceAnatomySelfTest.mq5" /log:"$repo\SF06_SELFTEST_COMPILE.log"
& $MetaEditorPath /compile:"$host\SF06_StrategyHost.mq5" /log:"$repo\SF06_HOST_COMPILE.log"
Get-Content "$repo\SF06_SELFTEST_COMPILE.log"
Get-Content "$repo\SF06_HOST_COMPILE.log"
