$ErrorActionPreference = "Stop"

python -m tools.strategy_factory.lcm.lcm_01.apply_cross_platform_hotfix

$surveyRoot = Get-ChildItem `
    -Path ".\registry\legacy_context_migration\surveys" `
    -Directory `
    -Filter "SURVEY_*" |
    Sort-Object -Property Name |
    Select-Object -Last 1

if (-not $surveyRoot) {
    throw "LCM-01 survey package was not found."
}

python -m tools.strategy_factory.lcm.lcm_01.cli verify-package `
    --survey-root "$($surveyRoot.FullName)"

python -m tools.strategy_factory.lcm.lcm_01.cli verify-installation `
    --repo-root "." `
    --survey-root "$($surveyRoot.FullName)" `
    --patch-index ".\LCM_01_FILE_INDEX.txt"

python -m compileall -q -f ".\tools\strategy_factory\lcm\lcm_01"
python -m pytest -q ".\lab\11_strategy_factory\migration\tests_lcm_01"
python -m pytest -q ".\lab\11_strategy_factory\migration\tests_lcm_00"
python -m pytest -q ".\lab\11_strategy_factory\acl_os\tests_acl_15"

git add --pathspec-from-file=".\LCM_01_CROSS_PLATFORM_HOTFIX_FILE_INDEX.txt"
git commit -F ".\COMMIT_MESSAGE_LCM_01_CROSS_PLATFORM_HOTFIX.md"
git push
