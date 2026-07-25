@echo off
setlocal EnableExtensions

set "PATCH=ALPHA_LAB_LCM_09B_SETUP_MIGRATION_FACTORY_BINDING_PARITY_PATCH.zip"
set "PACKAGE_ROOT=registry\legacy_context_migration\setup_package_migrations\SETUPMIGRATION_8F5CED333AA143A8F2A798BA01D550D9"
set "INDEX=LCM_09B_FILE_INDEX.txt"
set "HASHES=LCM_09B_FILE_HASHES.sha256"

if not exist "%PATCH%" (
  echo [LCM-09B] Missing patch: %PATCH%
  exit /b 2
)

powershell -NoProfile -ExecutionPolicy Bypass -Command "Expand-Archive -LiteralPath '%PATCH%' -DestinationPath '.' -Force"
if errorlevel 1 goto :fail

del /f /q "%PATCH%"
if errorlevel 1 goto :fail

python -m compileall -q tools\strategy_factory\lcm\lcm_09b tools\strategy_factory\acl_os\acl_04\legacy_reference.py
if errorlevel 1 goto :fail

python -m tools.strategy_factory.lcm.lcm_09b.cli verify-patch --repo-root . --hash-ledger "%HASHES%"
if errorlevel 1 goto :fail

python -m tools.strategy_factory.lcm.lcm_09b.cli verify-package --package-root "%PACKAGE_ROOT%"
if errorlevel 1 goto :fail

python -m tools.strategy_factory.lcm.lcm_09b.cli verify-installation --repo-root . --package-root "%PACKAGE_ROOT%" --patch-index "%INDEX%"
if errorlevel 1 goto :fail

python -m tools.strategy_factory.lcm.lcm_09b.cli qa --repo-root . --package-root "%PACKAGE_ROOT%"
if errorlevel 1 goto :fail

python -m pytest -q lab\11_strategy_factory\migration\tests_lcm_09b
if errorlevel 1 goto :fail

python -m pytest -q lab\11_strategy_factory\acl_os\tests_acl_04
if errorlevel 1 goto :fail

git add --pathspec-from-file="%INDEX%"
if errorlevel 1 goto :fail

git diff --cached --check
if errorlevel 1 goto :fail

git status --short

git commit -F COMMIT_MESSAGE_LCM_09B.md
if errorlevel 1 goto :fail

git push
if errorlevel 1 goto :fail

echo [LCM-09B] Patch expanded, verified, exactly staged, committed and pushed.
exit /b 0

:fail
echo [LCM-09B] FAILED. No later step was executed. Review the first error above.
exit /b 1
