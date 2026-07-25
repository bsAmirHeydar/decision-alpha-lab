param(
  [string]$RepoRoot = "."
)

$ErrorActionPreference = "Stop"
$ResolvedRoot = (Resolve-Path $RepoRoot).Path

python "$ResolvedRoot\contexts\legacy\infrastructure\exp0018_daye_trader\tools\validate_exp0018_phase01_time_kernel_v2.py" $ResolvedRoot
python -m pytest "$ResolvedRoot\contexts\legacy\infrastructure\exp0018_daye_trader\tests\test_exp0018_phase01_time_kernel_v2.py" -q

if (Test-Path "$ResolvedRoot\tools\engineering\check_mql5_compatibility.py") {
  python "$ResolvedRoot\tools\engineering\check_mql5_compatibility.py" $ResolvedRoot
}
