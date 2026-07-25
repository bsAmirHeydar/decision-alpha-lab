param([Parameter(Mandatory=$true)][string]$MetaEditor,[Parameter(Mandatory=$true)][string]$MqlRoot)
$ErrorActionPreference="Stop"
$targets=@("Experts\StrategyFactory\UCE_I15_ContextTournamentDiagnostic.mq5","Experts\StrategyFactoryTests\UCE_I15_FixtureCannotPromoteSelfTest.mq5","Experts\StrategyFactoryTests\UCE_I15_FreezeAndCountSelfTest.mq5","Experts\StrategyFactoryTests\UCE_I15_ProspectiveReconciliationSelfTest.mq5")
foreach($target in $targets){$log=Join-Path $MqlRoot (($target -replace '[\/:*?"<>|]','_')+'.log');& $MetaEditor /compile:(Join-Path $MqlRoot $target) /log:$log;if($LASTEXITCODE -ne 0){throw "MetaEditor failed for $target"};Get-Content $log}
