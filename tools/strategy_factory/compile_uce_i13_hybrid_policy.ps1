param([Parameter(Mandatory=$true)][string]$MetaEditor,[Parameter(Mandatory=$true)][string]$MqlRoot)
$ErrorActionPreference="Stop"
$targets=@("Experts\StrategyFactory\UCE_I13_HybridPolicyDiagnostic.mq5","Experts\StrategyFactoryTests\UCE_I13_ManualParitySelfTest.mq5","Experts\StrategyFactoryTests\UCE_I13_AuthorityFallbackSelfTest.mq5")
foreach($target in $targets){$log=Join-Path $MqlRoot (($target -replace '[\/:*?"<>|]','_')+'.log');& $MetaEditor /compile:(Join-Path $MqlRoot $target) /log:$log; if($LASTEXITCODE -ne 0){throw "MetaEditor failed for $target"};Get-Content $log}
