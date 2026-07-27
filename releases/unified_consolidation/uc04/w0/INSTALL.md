# Installation

Apply the root-relative ZIP from the repository root. Stage only paths listed in `PATCH_FILE_INDEX.txt`, commit with `COMMIT_MESSAGE.txt`, and push after the repository preflight has passed.

## Verification contract

```text
python tools/engineering/run_engineering_policy.py .
python -m tools.consolidation.ci.verify_migration_continuity --repo-root .
python -m tools.consolidation.uc03p3.verify --repo-root . --ci-fast
python -m tools.consolidation.uc04w0.verify --repo-root .
python -m pytest -q tests/consolidation/uc04w0
python -m pytest --collect-only -q
```

A failed command blocks commit and push until the real cause is corrected and generated evidence is rebuilt.
