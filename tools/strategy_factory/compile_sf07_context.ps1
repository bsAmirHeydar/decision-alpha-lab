param(
  [Parameter(Mandatory=$true)][string]$MetaEditorPath,
  [Parameter(Mandatory=$true)][string]$TerminalMql5Root
)
$ErrorActionPreference = "Stop"
$repo = (Resolve-Path ".").Path
$includeSource = Join-Path $repo "mql5\Include\AlphaLab"
$includeTarget = Join-Path $TerminalMql5Root "Include\AlphaLab"
$expertSource = Join-Path $repo "mql5\Experts\StrategyFactory"
$testSource = Join-Path $repo "mql5\Experts\StrategyFactoryTests"
$expertTarget = Join-Path $TerminalMql5Root "Experts\StrategyFactory"
$testTarget = Join-Path $TerminalMql5Root "Experts\StrategyFactoryTests"
New-Item -ItemType Directory -Force -Path $includeTarget,$expertTarget,$testTarget | Out-Null
Copy-Item "$includeSource\*" $includeTarget -Recurse -Force
Copy-Item "$expertSource\SF07_*.mq5" $expertTarget -Force
Copy-Item "$testSource\SF07_*.mq5" $testTarget -Force
$targets=@(
  (Join-Path $expertTarget "SF07_StrategyHost.mq5"),
  (Join-Path $expertTarget "SF07_ContextDiagnostic.mq5"),
  (Join-Path $testTarget "SF07_ContextEngineSelfTest.mq5")
)
foreach($target in $targets){
  $log="$target.compile.log"
  & $MetaEditorPath "/compile:$target" "/log:$log" | Out-Null
  if(!(Test-Path $log)){throw "Missing compile log: $log"}
  $text=Get-Content $log -Raw
  if($text -match "[1-9][0-9]* errors?"){throw "MQL5 compile failed: $target`n$text"}
}
Write-Host "SF07 MetaEditor compile PASS"
