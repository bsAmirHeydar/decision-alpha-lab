$ErrorActionPreference = "Stop"

Write-Host "Running the exact GitHub Engineering Policy locally..."
python .\tools\engineering\run_engineering_policy.py .
if ($LASTEXITCODE -ne 0) {
    throw "Engineering Policy failed. Do not push until the failed stage above is fixed."
}

Write-Host "Running Phase 04-06 focused tests..."
pytest -q `
  .\tests\legacy\strategy_factory\v1\phase04_plugins `
  .\tests\legacy\strategy_factory\v1\phase05_generation `
  .\tests\legacy\strategy_factory\v1\phase06_anatomy
if ($LASTEXITCODE -ne 0) {
    throw "Phase 04-06 focused tests failed."
}

Write-Host "Repository pre-push verification passed."
