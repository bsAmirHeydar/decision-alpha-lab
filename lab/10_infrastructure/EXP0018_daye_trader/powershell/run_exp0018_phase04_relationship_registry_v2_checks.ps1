param(
  [string]$RepoRoot = "."
)

$ErrorActionPreference = "Stop"
$ResolvedRoot = (Resolve-Path $RepoRoot).Path

python "$ResolvedRoot\lab\10_infrastructure\EXP0018_daye_trader\tools\validate_exp0018_phase04_relationship_registry_v2.py" "$ResolvedRoot"
python -m pytest "$ResolvedRoot\lab\10_infrastructure\EXP0018_daye_trader\tests\test_exp0018_phase04_relationship_registry_v2.py" -q
python -m py_compile `
  "$ResolvedRoot\lab\10_infrastructure\EXP0018_daye_trader\tools\validate_exp0018_phase04_relationship_registry_v2.py" `
  "$ResolvedRoot\lab\10_infrastructure\EXP0018_daye_trader\tests\test_exp0018_phase04_relationship_registry_v2.py"

Write-Host "EXP0018 Phase04 relationship registry checks passed." -ForegroundColor Green
