# Install and Verify UCEE-I18

1. Extract the patch at the repository root.
2. Verify hashes in `UCEE_I18_FILE_HASHES.sha256`.
3. Run `powershell -ExecutionPolicy Bypass -File tools/strategy_factory/run_uce_i18_tests.ps1`.
4. On Windows with MetaTrader installed, run `compile_uce_i18_qualification.ps1` with the exact `metaeditor64.exe` path.
5. Create external evidence under the git-ignored `local_evidence/uce_i18/` path. Do not commit broker credentials, account identifiers, private keys or raw personal data.
6. Keep `activation_allowed=false` until every external gate and explicit approval has passed.

Rollback is an atomic git revert of the UCE-I18 commit because the patch adds a bounded package, schemas, diagnostics, documentation and tools without changing existing I01-I17 runtime behavior.
