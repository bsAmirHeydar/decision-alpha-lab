param(
  [string]$RepoRoot = "."
)

$ErrorActionPreference = "Stop"
$Root = (Resolve-Path $RepoRoot).Path

python "$Root/contexts/legacy/infrastructure/exp0018_daye_trader/tools/validate_exp0018_phase10_hotfix002_visual_recovery.py"
python -m pytest -q "$Root/contexts/legacy/infrastructure/exp0018_daye_trader/tests/test_exp0018_phase10_hotfix002_visual_recovery.py"

if (Test-Path "$Root/tools/engineering/check_mql5_compatibility.py") {
  python "$Root/tools/engineering/check_mql5_compatibility.py" --root "$Root"
}

Write-Host "EXP0018 P10 Hotfix002 checks: PASS"
