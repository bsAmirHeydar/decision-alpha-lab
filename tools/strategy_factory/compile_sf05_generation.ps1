param(
  [Parameter(Mandatory=$true)][string]$MetaEditorPath,
  [Parameter(Mandatory=$true)][string]$TerminalMql5Root
)
$ErrorActionPreference="Stop"
$repo=(Resolve-Path ".").Path
$includeSrc=Join-Path $repo "mql5\Include\AlphaLab"
$includeDst=Join-Path $TerminalMql5Root "Include\AlphaLab"
New-Item -ItemType Directory -Force -Path $includeDst | Out-Null
Copy-Item "$includeSrc\*" $includeDst -Recurse -Force
$experts=@("SF05_RuntimeGenerationSelfTest.mq5","SF05_GenerationDiagnostic.mq5","SF05_StrategyHost.mq5")
foreach($name in $experts){
  $src=if($name -like "*SelfTest*"){Join-Path $repo "mql5\Experts\StrategyFactoryTests\$name"}else{Join-Path $repo "mql5\Experts\StrategyFactory\$name"}
  $dstDir=if($name -like "*SelfTest*"){Join-Path $TerminalMql5Root "Experts\StrategyFactoryTests"}else{Join-Path $TerminalMql5Root "Experts\StrategyFactory"}
  New-Item -ItemType Directory -Force -Path $dstDir | Out-Null
  $dst=Join-Path $dstDir $name;Copy-Item $src $dst -Force
  $log=Join-Path $repo ("sf05_"+$name+".log")
  & $MetaEditorPath "/compile:$dst" "/log:$log" | Out-Null
  if(Select-String -Path $log -Pattern "[1-9][0-9]* errors" -Quiet){Get-Content $log;throw "MQL5 compile failed: $name"}
}
