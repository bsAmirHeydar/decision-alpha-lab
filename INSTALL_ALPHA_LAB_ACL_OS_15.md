# Install Alpha Lab ACL-15

1. Place `ACL_OS_15_FLEET_OPERATIONS_AND_CLOSURE_PATCH.zip` in the repository root.
2. Expand the ZIP into the repository root.
3. Remove the ZIP.
4. Stage exactly the root-relative paths from `ACL_OS_15_FILE_INDEX.txt` using `git add --pathspec-from-file`.
5. Commit with `COMMIT_MESSAGE.md` and push.

Verification:

```powershell
python -m tools.strategy_factory.acl_os.acl_15.cli verify --output "lab/11_strategy_factory/acl_os/fixtures/acl_15/reference_fleet_closure"
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD="1"
python -m pytest -q "lab/11_strategy_factory/acl_os/tests_acl_15"
```
