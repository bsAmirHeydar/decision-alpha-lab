$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Push-Location $RepoRoot
try {
  $env:PYTHONPATH = Join-Path $RepoRoot "lab\11_strategy_factory\python"
  python -m pytest -q --import-mode=importlib "lab/11_strategy_factory/tests/phase_uce_i16_context_onboarding"
  python "tools/strategy_factory/validate_uce_i16_delivery.py"
} finally { Pop-Location }
