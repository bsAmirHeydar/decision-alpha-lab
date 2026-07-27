$ErrorActionPreference = "Stop"
python tools/engineering/run_engineering_policy.py .
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m tools.consolidation.uc04w0.verify --repo-root . --skip-release-controls
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m tools.consolidation.uc04w1.characterize --repo-root .
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m tools.consolidation.uc04w1.verify --repo-root .
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q tests/consolidation/uc04w0 tests/consolidation/uc04w1
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest --collect-only -q
exit $LASTEXITCODE
