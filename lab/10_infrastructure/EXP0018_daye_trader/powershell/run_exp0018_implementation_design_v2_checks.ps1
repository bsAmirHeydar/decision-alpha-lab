param([string]$RepoRoot = ".")
$ErrorActionPreference = "Stop"
python (Join-Path $RepoRoot "lab/10_infrastructure/EXP0018_daye_trader/tools/validate_exp0018_implementation_design_v2.py") $RepoRoot
python -m pytest (Join-Path $RepoRoot "lab/10_infrastructure/EXP0018_daye_trader/tests/test_exp0018_implementation_design_v2.py") -q
