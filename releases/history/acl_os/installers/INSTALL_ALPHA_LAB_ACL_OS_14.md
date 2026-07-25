# Install Alpha Lab ACL-14

1. Place `ACL_OS_14_FIRST_REAL_CONTEXT_PILOT_PATCH.zip` in the repository root.
2. Expand the ZIP into the root.
3. Remove the ZIP.
4. Stage exactly the paths in `ACL_OS_14_FILE_INDEX.txt` using Git pathspec-from-file.
5. Commit with `COMMIT_MESSAGE.md` and push.

Verification:

```powershell
python -m tools.strategy_factory.acl_os.acl_14.cli verify --output "lab/11_strategy_factory/acl_os/fixtures/acl_14/reference_first_real_context_pilot"
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD="1"
python -m pytest -q "lab/11_strategy_factory/acl_os/tests_acl_14"
```
