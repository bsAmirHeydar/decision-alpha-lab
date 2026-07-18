$ErrorActionPreference = "Stop"

function Invoke-NativeChecked {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Executable,

        [Parameter(Mandatory = $true)]
        [string[]] $Arguments,

        [Parameter(Mandatory = $true)]
        [string] $Step
    )

    & $Executable @Arguments
    $exitCode = $LASTEXITCODE

    if ($exitCode -ne 0) {
        throw "$Step failed with native exit code $exitCode. No commit or push was performed after this failure."
    }
}

$surveyRoot = Get-ChildItem `
    -Path ".\registry\legacy_context_migration\surveys" `
    -Directory `
    -Filter "SURVEY_*" |
    Sort-Object -Property Name |
    Select-Object -Last 1

if (-not $surveyRoot) {
    throw "LCM-01 survey package was not found."
}

Invoke-NativeChecked `
    -Executable "python" `
    -Arguments @(
        "-m", "tools.strategy_factory.lcm.lcm_01.cli",
        "verify-package",
        "--survey-root", $surveyRoot.FullName
    ) `
    -Step "LCM-01 package verification"

Invoke-NativeChecked `
    -Executable "python" `
    -Arguments @(
        "-m", "tools.strategy_factory.lcm.lcm_01.cli",
        "verify-installation",
        "--repo-root", ".",
        "--survey-root", $surveyRoot.FullName,
        "--patch-index", ".\LCM_01_FILE_INDEX.txt"
    ) `
    -Step "LCM-01 installation verification"

Invoke-NativeChecked `
    -Executable "python" `
    -Arguments @(
        "-m", "compileall", "-q", "-f",
        ".\tools\strategy_factory\lcm\lcm_01"
    ) `
    -Step "LCM-01 compileall"

Invoke-NativeChecked `
    -Executable "python" `
    -Arguments @(
        "-m", "pytest", "-q",
        ".\lab\11_strategy_factory\migration\tests_lcm_01"
    ) `
    -Step "LCM-01 tests"

Invoke-NativeChecked `
    -Executable "python" `
    -Arguments @(
        "-m", "pytest", "-q",
        ".\lab\11_strategy_factory\migration\tests_lcm_00"
    ) `
    -Step "LCM-00 regression tests"

Invoke-NativeChecked `
    -Executable "python" `
    -Arguments @(
        "-m", "pytest", "-q",
        ".\lab\11_strategy_factory\acl_os\tests_acl_15"
    ) `
    -Step "ACL-15 regression tests"

$temporaryDiagnostics = @(
    ".\LCM_01_CROSS_PLATFORM_DIAGNOSTIC.json",
    ".\LCM_01_CROSS_PLATFORM_DIAGNOSTIC_FAST.json"
)

foreach ($diagnostic in $temporaryDiagnostics) {
    if (Test-Path -LiteralPath $diagnostic) {
        Remove-Item -LiteralPath $diagnostic -Force
    }
}

Invoke-NativeChecked `
    -Executable "git" `
    -Arguments @(
        "add",
        "--pathspec-from-file=.\LCM_01_BIDIRECTIONAL_EOL_HOTFIX_FILE_INDEX.txt"
    ) `
    -Step "Git staging"

Invoke-NativeChecked `
    -Executable "git" `
    -Arguments @(
        "commit",
        "-F", ".\COMMIT_MESSAGE_LCM_01_BIDIRECTIONAL_EOL_HOTFIX.md"
    ) `
    -Step "Git commit"

Invoke-NativeChecked `
    -Executable "git" `
    -Arguments @("push") `
    -Step "Git push"
