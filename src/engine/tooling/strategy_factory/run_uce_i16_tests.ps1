$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Push-Location $RepoRoot
try {
  $env:PYTHONPATH = Join-Path $RepoRoot "src\engine\packages"
  python -m pytest -q --import-mode=importlib "tests/legacy/strategy_factory/v1/phase_uce_i16_context_onboarding"
  python "src/engine/tooling/strategy_factory/validate_uce_i16_delivery.py"
} finally { Pop-Location }
