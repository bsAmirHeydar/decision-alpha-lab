# Install Phase 14

1. Extract the patch into the repository root with overwrite enabled.
2. Run `python .\tools\engineering\run_engineering_policy.py .`.
3. Run `powershell -ExecutionPolicy Bypass -File .\tools\strategy_factory\run_phase14_tests.ps1`.
4. Compile all three SF14 Expert Advisors locally with MetaEditor.
5. Confirm that the self-test prints `SF14 self-test PASS`.
6. Do not enable inference or broker execution; those authorities are intentionally absent.

The patch is additive except for the Python package metadata update from version 0.13.0 to 0.14.0.
