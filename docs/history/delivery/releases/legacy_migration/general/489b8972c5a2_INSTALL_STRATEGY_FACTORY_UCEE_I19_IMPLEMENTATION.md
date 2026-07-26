# Install UCEE-I19 Production Operations Patch

## Preconditions

1. Run from the repository root.
2. UCEE-I18 v1.0.0 must already be installed.
3. The patch ZIP must be located at repository root.
4. The working tree should contain no unrelated staged changes.
5. Python and pytest must be available for reference QA.
6. Windows MetaEditor compilation is a separate external acceptance activity and is not represented as passed by this patch.

## Verification command

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\strategy_factory\run_uce_i19_tests.ps1
```

## External MetaEditor command

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\strategy_factory\compile_uce_i19_operations.ps1 -MetaEditorPath "C:\Path\To\metaeditor64.exe"
```

## External evidence scaffold

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\strategy_factory\new_uce_i19_external_run.ps1
```

External evidence under `local_evidence/` is intentionally not included in the source patch. It must be reviewed, scrubbed of secrets, hashed, and accepted against the exact release and target before any stage change.

## Rollback

Revert the atomic UCEE-I19 commit. Do not delete external evidence as a rollback mechanism. Revoke active leases, engage the kill switch, preserve incident and reconciliation artifacts, and follow the approved I18/I19 rollback runbook before altering a real terminal.
