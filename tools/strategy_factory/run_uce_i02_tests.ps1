param([string]$RepoRoot = "")
$ErrorActionPreference = "Stop"
if ([string]::IsNullOrWhiteSpace($RepoRoot)) { $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path }
Push-Location $RepoRoot
try {
  python .\tools\engineering\run_engineering_policy.py .
  python .\tools\strategy_factory\check_uce_i02_boundaries.py .
  python .\tools\strategy_factory\check_uce_i02_mql5_static.py .
  python .\tools\strategy_factory\validate_uce_i02_delivery.py .
  $env:PYTHONPATH = (Resolve-Path ".\lab\11_strategy_factory\python").Path
  python -m compileall -q .\lab\11_strategy_factory\python\strategy_factory_contexts_v3
  pytest -q .\lab\11_strategy_factory\tests\phase_uce_i01_contracts .\lab\11_strategy_factory\tests\phase_uce_i02_contexts
  python -m strategy_factory_contexts_v3.cli run-reference-conformance synthetic
  python -m strategy_factory_contexts_v3.cli run-reference-conformance exp0017
  Write-Host "UCE-I02 local test gate: PASS"
} finally { Pop-Location }
