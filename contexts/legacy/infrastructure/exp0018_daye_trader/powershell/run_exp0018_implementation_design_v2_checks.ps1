param([string]$RepoRoot = ".")
$ErrorActionPreference = "Stop"
python (Join-Path $RepoRoot "contexts/legacy/infrastructure/exp0018_daye_trader/tools/validate_exp0018_implementation_design_v2.py") $RepoRoot
python -m pytest (Join-Path $RepoRoot "contexts/legacy/infrastructure/exp0018_daye_trader/tests/test_exp0018_implementation_design_v2.py") -q
