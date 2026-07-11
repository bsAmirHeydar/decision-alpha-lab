param(
 [Parameter(Mandatory=$true)][string]$MetaEditorPath,
 [Parameter(Mandatory=$true)][string]$TerminalMql5Root
)
$ErrorActionPreference="Stop"
$repo=(Resolve-Path ".").Path
$includeSource=Join-Path $repo "mql5\Include\AlphaLab\StrategyFactory"
$expertSource=Join-Path $repo "mql5\Experts\StrategyFactory"
$testSource=Join-Path $repo "mql5\Experts\StrategyFactoryTests\SF04_PluginRegistrySelfTest.mq5"
$includeTarget=Join-Path $TerminalMql5Root "Include\AlphaLab\StrategyFactory"
$expertTarget=Join-Path $TerminalMql5Root "Experts\StrategyFactory"
$testTarget=Join-Path $TerminalMql5Root "Experts\StrategyFactoryTests"
New-Item -ItemType Directory -Force $includeTarget,$expertTarget,$testTarget | Out-Null
Copy-Item "$includeSource\*" $includeTarget -Recurse -Force
Copy-Item (Join-Path $expertSource "SF04_StrategyHost.mq5") $expertTarget -Force
Copy-Item (Join-Path $expertSource "SF04_PluginRegistryDiagnostic.mq5") $expertTarget -Force
Copy-Item $testSource $testTarget -Force
$targets=@(
 (Join-Path $expertTarget "SF04_StrategyHost.mq5"),
 (Join-Path $expertTarget "SF04_PluginRegistryDiagnostic.mq5"),
 (Join-Path $testTarget "SF04_PluginRegistrySelfTest.mq5")
)
$logs=Join-Path $repo "artifacts\strategy_factory\phase04_compile"
New-Item -ItemType Directory -Force $logs | Out-Null
foreach($target in $targets){
 $log=Join-Path $logs ((Split-Path $target -Leaf)+".log")
 & $MetaEditorPath "/compile:$target" "/log:$log"
 if($LASTEXITCODE -ne 0){throw "MetaEditor process failed for $target"}
 $text=Get-Content $log -Raw
 if($text -match "([1-9][0-9]*) error") {throw "Compilation errors in $target. See $log"}
}
Write-Host "SF04 MetaEditor compile: PASS"
