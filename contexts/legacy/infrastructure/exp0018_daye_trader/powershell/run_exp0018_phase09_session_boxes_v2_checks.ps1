param([string]$RepoRoot = ".")
$ErrorActionPreference = "Stop"
$Python = Get-Command python -ErrorAction SilentlyContinue
if (-not $Python) { throw "python command not found" }
& $Python.Source "$RepoRoot/contexts/legacy/infrastructure/exp0018_daye_trader/tools/validate_exp0018_phase09_session_boxes_v2.py" "$RepoRoot"
& $Python.Source -m pytest "$RepoRoot/contexts/legacy/infrastructure/exp0018_daye_trader/tests/test_exp0018_phase09_session_boxes_v2.py" -q
if (Test-Path "$RepoRoot/tools/engineering/check_mql5_compatibility.py") {
  & $Python.Source "$RepoRoot/tools/engineering/check_mql5_compatibility.py" --root "$RepoRoot/mql5"
}
Write-Host "EXP0018 Phase 09 checks completed. MetaEditor compile and chart inspection remain mandatory." -ForegroundColor Green
