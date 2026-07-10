param([string]$RepoRoot = ".")
$ErrorActionPreference = "Stop"
$Root = (Resolve-Path $RepoRoot).Path
python "$Root\lab\10_infrastructure\EXP0018_daye_trader\tools\validate_exp0018_phase03_period_aggregation_v2.py" $Root
python -m pytest "$Root\lab\10_infrastructure\EXP0018_daye_trader\tests\test_exp0018_phase03_period_aggregation_v2.py" -q
if (Test-Path "$Root\tools\engineering\check_mql5_compatibility.py") {
  python "$Root\tools\engineering\check_mql5_compatibility.py" $Root
}
Write-Host "EXP0018 Phase 03 checks completed. MetaEditor compile remains required." -ForegroundColor Green
