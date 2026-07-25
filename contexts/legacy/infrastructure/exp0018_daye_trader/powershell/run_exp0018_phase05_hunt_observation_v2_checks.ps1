param([string]$RepoRoot = ".")
$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path $RepoRoot).Path
python "$RepoRoot\contexts\legacy\infrastructure\exp0018_daye_trader\tools\validate_exp0018_phase05_hunt_observation_v2.py" $RepoRoot
python -m pytest "$RepoRoot\contexts\legacy\infrastructure\exp0018_daye_trader\tests\test_exp0018_phase05_hunt_observation_v2.py" -q
if (Test-Path "$RepoRoot\tools\engineering\check_mql5_compatibility.py") {
  python "$RepoRoot\tools\engineering\check_mql5_compatibility.py" $RepoRoot
}
