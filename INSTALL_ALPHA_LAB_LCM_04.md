# Install Alpha Lab LCM-04

Run from the repository root in PowerShell after copying the ZIP into the root.

```powershell
$ErrorActionPreference = "Stop"

Expand-Archive -LiteralPath ".\ALPHA_LAB_LCM_04_BEHAVIORAL_CHARACTERIZATION_AND_GOLDEN_TRACES_PATCH.zip" -DestinationPath "." -Force
Remove-Item -LiteralPath ".\ALPHA_LAB_LCM_04_BEHAVIORAL_CHARACTERIZATION_AND_GOLDEN_TRACES_PATCH.zip" -Force

$characterizationRoot = ".\registry\legacy_context_migration\characterizations\CHARACTERIZATION_55F06219A834717D91B7111A481DF3D3"

python -m tools.strategy_factory.lcm.lcm_04.cli verify-package --characterization-root $characterizationRoot
python -m tools.strategy_factory.lcm.lcm_04.cli verify-installation --repo-root "." --characterization-root $characterizationRoot --patch-index ".\LCM_04_FILE_INDEX.txt"
python -m tools.strategy_factory.lcm.lcm_04.cli qa --repo-root "." --characterization-root $characterizationRoot
python -m compileall -q -f ".\tools\strategy_factory\lcm\lcm_04"
python -m pytest -q ".\lab\11_strategy_factory\migration\tests_lcm_04"
python -m pytest -q ".\lab\11_strategy_factory\migration\tests_lcm_03"
python -m pytest -q ".\lab\11_strategy_factory\migration\tests_lcm_02"
python -m pytest -q ".\lab\11_strategy_factory\migration\tests_lcm_01"
python -m pytest -q ".\lab\11_strategy_factory\migration\tests_lcm_00"
python -m pytest -q ".\lab\11_strategy_factory\acl_os\tests_acl_15"

git add --pathspec-from-file=".\LCM_04_FILE_INDEX.txt"
git commit -F ".\COMMIT_MESSAGE_LCM_04.md"
git push
```
