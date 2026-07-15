# Install And Validate SAED V4-06 Treatment DSL

## Preconditions

Use a clean repository checkout containing the accepted V4-05 patch. Python 3.10 or later is required. The patch does not install external machine-learning, broker or network dependencies.

## Apply

Extract the patch into the repository root with overwrite enabled, then delete the ZIP. Do not extract into a nested directory.

## Validate

1. Run `python tools/strategy_factory/saed_v4_06/run_saed_v4_06_full_qa.py`.
2. Run `python tools/strategy_factory/saed_v4_06/validate_saed_v4_06_delivery.py`.
3. On Windows with MetaTrader 5 installed, run `tools/strategy_factory/saed_v4_06/compile_saed_v4_06_treatment_dsl.ps1` and retain the actual compiler logs as external evidence.
4. Stage only paths listed in `SAED_V4_06_FILE_INDEX.txt`.
5. Run `git diff --cached --check`, commit with `COMMIT_MESSAGE.md`, and push.

## Rollback

Before commit, restore modified files and remove new files listed in the index. After commit, use a normal revert commit. Never edit the hash ledger to force delivery validation.
