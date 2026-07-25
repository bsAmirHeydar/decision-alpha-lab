param([string]$RepoRoot = ".")
$ErrorActionPreference = "Stop"
$root = (Resolve-Path $RepoRoot).Path
python "$root/contexts/legacy/infrastructure/exp0018_daye_trader/tools/validate_exp0018_phase06_close_confirmation_v2.py" "$root"
python -m pytest "$root/contexts/legacy/infrastructure/exp0018_daye_trader/tests/test_exp0018_phase06_close_confirmation_v2.py" -q
