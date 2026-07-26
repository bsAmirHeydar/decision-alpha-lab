python -m tools.consolidation.uc03p3.apply --repo-root .
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m tools.consolidation.uc03p3.verify --repo-root .
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q tests/consolidation/uc03p3
exit $LASTEXITCODE
