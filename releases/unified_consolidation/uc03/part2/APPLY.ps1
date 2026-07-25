python -m tools.consolidation.uc03p2.apply --repo-root .
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m tools.consolidation.uc03p2.verify --repo-root .
exit $LASTEXITCODE
