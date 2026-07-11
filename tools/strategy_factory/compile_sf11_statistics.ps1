param(
  [Parameter(Mandatory=$true)][string]$MetaEditorPath,
  [Parameter(Mandatory=$true)][string]$TerminalMql5Root
)
$ErrorActionPreference = "Stop"
$repo = (Resolve-Path ".").Path
$includeSource = Join-Path $repo "mql5\Include\AlphaLab\StrategyFactory\Statistics"
$includeTarget = Join-Path $TerminalMql5Root "Include\AlphaLab\StrategyFactory\Statistics"
New-Item -ItemType Directory -Force -Path $includeTarget | Out-Null
Copy-Item "$includeSource\*" $includeTarget -Recurse -Force
$experts = @(
  "mql5\Experts\StrategyFactoryTests\SF11_StatisticsSelfTest.mq5",
  "mql5\Experts\StrategyFactory\SF11_StatisticsDiagnostic.mq5",
  "mql5\Experts\StrategyFactory\SF11_StatisticsResearchHost.mq5"
)
foreach($relative in $experts){
  $source=Join-Path $repo $relative
  $target=Join-Path $TerminalMql5Root ($relative -replace '^mql5\','')
  New-Item -ItemType Directory -Force -Path (Split-Path $target) | Out-Null
  Copy-Item $source $target -Force
  $log="$target.compile.log"
  & $MetaEditorPath "/compile:$target" "/log:$log"
  if(Test-Path $log){$text=Get-Content $log -Raw;if($text -match '[1-9][0-9]* error'){throw "MQL5 compile failed: $target`n$text"}}
}
Write-Host "SF11 MetaEditor compile completed."
