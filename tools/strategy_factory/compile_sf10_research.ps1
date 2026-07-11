param(
 [Parameter(Mandatory=$true)][string]$MetaEditorPath,
 [Parameter(Mandatory=$true)][string]$TerminalMql5Root
)
$ErrorActionPreference="Stop"
$repo=(Resolve-Path ".").Path
Copy-Item "$repo\mql5\Include\AlphaLab" "$TerminalMql5Root\Include" -Recurse -Force
Copy-Item "$repo\mql5\Experts\StrategyFactoryTests\SF10_ResearchHarnessSelfTest.mq5" "$TerminalMql5Root\Experts\StrategyFactoryTests" -Force
Copy-Item "$repo\mql5\Experts\StrategyFactory\SF10_StrategyTesterResearchHost.mq5" "$TerminalMql5Root\Experts\StrategyFactory" -Force
& $MetaEditorPath /compile:"$TerminalMql5Root\Experts\StrategyFactoryTests\SF10_ResearchHarnessSelfTest.mq5" /log:"$repo\sf10_selftest_compile.log"
& $MetaEditorPath /compile:"$TerminalMql5Root\Experts\StrategyFactory\SF10_StrategyTesterResearchHost.mq5" /log:"$repo\sf10_host_compile.log"
Get-Content "$repo\sf10_selftest_compile.log"
Get-Content "$repo\sf10_host_compile.log"
if((Select-String -Path "$repo\sf10_*_compile.log" -Pattern "error" -SimpleMatch)){throw "SF10 MetaEditor compile reported errors"}
