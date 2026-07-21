# Operator Runbook

1. Expand the patch at repository root.
2. Verify `registry/legacy_context_migration/treatment_execution_closures/TREATCLOSE_3EBD9196597715D81966936D37F1DF91`.
3. Run schemas, static validation, package verification and direct/regression tests.
4. Stage only `LCM_10C_FILE_INDEX.txt`.
5. Commit only when live, paper and capital counts are zero.
