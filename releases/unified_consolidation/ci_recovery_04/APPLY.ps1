param(
    [string]$RepositoryRoot = (Get-Location).Path
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Invoke-Python {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments
    )

    $Python = (Get-Command python -ErrorAction Stop).Source
    $PreviousPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"

    try {
        $Output = @(& $Python -B @Arguments 2>&1)
        $ExitCode = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $PreviousPreference
    }

    foreach ($Line in $Output) {
        Write-Host $Line
    }

    if ($ExitCode -ne 0) {
        throw (
            "Python command failed with exit code {0}: python -B {1}" -f
            $ExitCode,
            ($Arguments -join " ")
        )
    }
}

$Root = (Resolve-Path -LiteralPath $RepositoryRoot).Path
$PreviousBytecodeSetting = [Environment]::GetEnvironmentVariable(
    "PYTHONDONTWRITEBYTECODE",
    "Process"
)

[Environment]::SetEnvironmentVariable(
    "PYTHONDONTWRITEBYTECODE",
    "1",
    "Process"
)

Push-Location -LiteralPath $Root

try {
    Invoke-Python @("tools/engineering/run_engineering_policy.py", ".")
    Invoke-Python @("-m", "tools.consolidation.ci.verify_migration_continuity", "--repo-root", ".")
    Invoke-Python @("-m", "tools.consolidation.uc03p3.verify", "--repo-root", ".", "--ci-fast")
    Invoke-Python @("-m", "tools.consolidation.uc04w0.verify", "--repo-root", ".")
    Invoke-Python @("-m", "tools.consolidation.uc04w1.verify", "--repo-root", ".")
    Invoke-Python @("-m", "tools.consolidation.uc04w1b.verify", "--repo-root", ".")
    Invoke-Python @(
        "-m", "pytest", "-q",
        "tests/consolidation/uc04w0",
        "tests/consolidation/uc04w1",
        "tests/consolidation/uc04w1b",
        "tests/consolidation/ci",
        "-p", "no:cacheprovider"
    )
    Invoke-Python @(
        "-m", "pytest", "--collect-only", "-q",
        "-p", "no:cacheprovider"
    )

    Write-Host "UC04 historical release integrity recovery: PASS"
}
finally {
    Pop-Location
    [Environment]::SetEnvironmentVariable(
        "PYTHONDONTWRITEBYTECODE",
        $PreviousBytecodeSetting,
        "Process"
    )
}
