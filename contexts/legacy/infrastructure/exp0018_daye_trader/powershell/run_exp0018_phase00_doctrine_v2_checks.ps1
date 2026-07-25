param([string]$RepoRoot = ".")
$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path $RepoRoot).Path
python (Join-Path $RepoRoot "contexts/legacy/infrastructure/exp0018_daye_trader/tools/validate_exp0018_phase00_doctrine_v2.py") $RepoRoot
python -m unittest discover -s (Join-Path $RepoRoot "contexts/legacy/infrastructure/exp0018_daye_trader/tests") -p "test_exp0018_phase00_doctrine_v2.py" -v
