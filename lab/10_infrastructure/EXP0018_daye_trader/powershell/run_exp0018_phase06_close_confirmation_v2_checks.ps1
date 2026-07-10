param([string]$RepoRoot = ".")
$ErrorActionPreference = "Stop"
$root = (Resolve-Path $RepoRoot).Path
python "$root/lab/10_infrastructure/EXP0018_daye_trader/tools/validate_exp0018_phase06_close_confirmation_v2.py" "$root"
python -m pytest "$root/lab/10_infrastructure/EXP0018_daye_trader/tests/test_exp0018_phase06_close_confirmation_v2.py" -q
