$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path
Push-Location $RepoRoot
try {
    python ".\contexts\legacy\tools\flag_counting\run_nds_hook_864_cycle_r1_tests.py"
    if ($LASTEXITCODE -ne 0) {
        throw "NDS Hook 86.4 Cycle R1 bounded QA failed with exit code $LASTEXITCODE."
    }
}
finally {
    Pop-Location
}
