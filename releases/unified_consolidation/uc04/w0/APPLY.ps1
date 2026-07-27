$ErrorActionPreference = "Stop"
python tools/engineering/run_engineering_policy.py .
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m tools.consolidation.ci.verify_migration_continuity --repo-root .
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m tools.consolidation.uc03p3.verify --repo-root . --ci-fast
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m tools.consolidation.uc04w0.verify --repo-root .
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q tests/consolidation/uc04w0
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest --collect-only -q
exit $LASTEXITCODE
