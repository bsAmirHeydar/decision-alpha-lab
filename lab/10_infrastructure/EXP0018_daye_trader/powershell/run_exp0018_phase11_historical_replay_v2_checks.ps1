param([string]$RepoRoot=".")
$ErrorActionPreference="Stop"
$Root=(Resolve-Path $RepoRoot).Path
python "$Root\lab\10_infrastructure\EXP0018_daye_trader\tools\validate_exp0018_phase11_historical_replay_v2.py" $Root
python -m pytest "$Root\lab\10_infrastructure\EXP0018_daye_trader\tests\test_exp0018_phase11_historical_replay_v2.py" -q
Write-Host "EXP0018 Phase 11 checks passed."
