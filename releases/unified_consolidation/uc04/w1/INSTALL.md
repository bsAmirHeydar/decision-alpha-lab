# Installation and Verification

Apply the root-relative ZIP from the repository root. Stage only the paths in `PATCH_FILE_INDEX.txt` and commit with `COMMIT_MESSAGE.txt`.

## Repository verification contract

1. `python tools/engineering/run_engineering_policy.py .`
2. `python -m tools.consolidation.uc04w0.verify --repo-root . --skip-release-controls`
3. `python -m tools.consolidation.uc04w1.characterize --repo-root .`
4. `python -m tools.consolidation.uc04w1.verify --repo-root .`
5. `python -m pytest -q tests/consolidation/uc04w0 tests/consolidation/uc04w1`
6. `python -m pytest --collect-only -q`

## Native evidence capture

On the Windows MetaTrader 5 environment, run `tools/consolidation/uc04w1/capture_native_acceptance.ps1`. The tool compiles from an isolated `.alpha/runs` mirror so generated EX5 files do not dirty tracked MQL5 sources.

A compile-only run may produce `COMPILE_PASS_RUNTIME_PENDING`; this does not authorize implementation. After attaching the generated self-test to a chart, rerun the capture tool with the Common Files CSV. Only a receipt with compile and runtime status `PASS` is eligible for W1B review.
