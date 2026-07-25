[CmdletBinding()]
param(
 [string]$RepoRoot=(Get-Location).Path,
 [string]$MetaEditor=''
)
$ErrorActionPreference='Stop'
$repo=(Resolve-Path -LiteralPath $RepoRoot).Path
if (-not $MetaEditor) {
 $candidates=@(
  'C:\Program Files\MetaTrader 5\metaeditor64.exe',
  'C:\Program Files (x86)\MetaTrader 5\metaeditor64.exe'
 )
 $MetaEditor=$candidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
}
if (-not $MetaEditor -or -not (Test-Path -LiteralPath $MetaEditor)) { throw 'MetaEditor not found. Pass -MetaEditor explicitly.' }
$targets=@(
 'mql5\Tests\Experts\FaerieProtocol\EXP0019_FP_I01_CompatibilitySelfTest.mq5',
 'mql5\Experts\FaerieProtocol\EXP0019_FP_I01_CompatibilityDiagnostic.mq5',
 'mql5\Experts\IntermarketDivergenceExecution\EXP0017_CG_Time_Anatomy.mq5',
 'mql5\Experts\IntermarketDivergenceExecution\EXP0017_CG_Reference_Anatomy.mq5',
 'mql5\Experts\IntermarketDivergenceExecution\EXP0017_CG_Hunt_Anatomy.mq5',
 'mql5\Experts\IntermarketDivergenceExecution\EXP0017_CG_Divergence_Anatomy.mq5',
 'mql5\Experts\IntermarketDivergenceExecution\EXP0017_CG_Visual_Ledger_Anatomy.mq5',
 'mql5\Experts\DayeTrader\EXP0018_Daye_Time_Foundation.mq5',
 'mql5\Experts\DayeTrader\EXP0018_Daye_Data_Sync_Anatomy.mq5',
 'mql5\Experts\DayeTrader\EXP0018_Daye_Hunt_Observation_Anatomy.mq5',
 'mql5\Experts\DayeTrader\EXP0018_Daye_Close_Confirmation_Anatomy.mq5',
 'mql5\Experts\DayeTrader\EXP0018_Daye_Reference_Lifecycle_Anatomy.mq5',
 'mql5\Experts\DayeTrader\EXP0018_Daye_Historical_Replay_Anatomy.mq5'
)
$logRoot=Join-Path $repo 'contexts\legacy\infrastructure\exp0019_faerie_protocol\phase_i01\artifacts\metaeditor_logs'
New-Item -ItemType Directory -Force -Path $logRoot | Out-Null
$failed=@()
foreach($relative in $targets) {
 $source=Join-Path $repo $relative
 if(-not (Test-Path -LiteralPath $source)) { $failed += "missing:$relative"; continue }
 $log=Join-Path $logRoot (([IO.Path]::GetFileNameWithoutExtension($source))+'.compile.log')
 & $MetaEditor "/compile:$source" "/log:$log"
 if(-not (Test-Path -LiteralPath $log)) { $failed += "no-log:$relative"; continue }
 $text=Get-Content -LiteralPath $log -Raw
 if($text -notmatch '0 errors') { $failed += "compile:$relative" }
}
if($failed.Count -gt 0) { $failed | ForEach-Object { Write-Error $_ }; exit 1 }
Write-Host "FP-I01 MetaEditor compile PASS: $($targets.Count) targets"
