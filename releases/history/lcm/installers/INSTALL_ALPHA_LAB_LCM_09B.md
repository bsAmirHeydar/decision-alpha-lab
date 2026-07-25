# Install Alpha Lab LCM-09B

Run `APPLY_ALPHA_LAB_LCM_09B.bat` from repository root with the ZIP beside it. The batch expands the archive, removes it, verifies the package, runs direct and bounded regression tests, stages exactly `LCM_09B_FILE_INDEX.txt`, commits and pushes.

Manual verification:

```powershell
python -m tools.strategy_factory.lcm.lcm_09b.cli verify-package --package-root "registry/legacy_context_migration/setup_package_migrations/SETUPMIGRATION_8F5CED333AA143A8F2A798BA01D550D9"
python -m tools.strategy_factory.lcm.lcm_09b.cli qa --repo-root . --package-root "registry/legacy_context_migration/setup_package_migrations/SETUPMIGRATION_8F5CED333AA143A8F2A798BA01D550D9"
python -m pytest -q lab/11_strategy_factory/migration/tests_lcm_09b
python -m pytest -q lab/11_strategy_factory/acl_os/tests_acl_04
```

Rollback uses Git to restore exactly the paths in `LCM_09B_FILE_INDEX.txt`. No legacy source file was moved or deleted.
