[CmdletBinding()]
param(
    [string]$RepoRoot = ".",
    [string]$SourceRoot = "",
    [switch]$SkipPreviousContextPythonTest,
    [switch]$SkipEngineeringPolicy
)

$ErrorActionPreference = "Stop"
$Repo = (Resolve-Path -LiteralPath $RepoRoot).Path
$PhaseRoot = Join-Path $Repo "contexts\legacy\infrastructure\exp0019_faerie_protocol\phase_i00"
$PythonRoot = Join-Path $PhaseRoot "python"
$Runner = Join-Path $PhaseRoot "run_phase_i00.py"
$Tests = Join-Path $PhaseRoot "tests"
$Policy = Join-Path $PhaseRoot "config\FP_I00_GOVERNANCE_POLICY.v1.json"
$Artifacts = Join-Path $PhaseRoot "artifacts"

if (-not (Test-Path -LiteralPath $Runner)) {
    throw "FP-I00 runner not found: $Runner"
}
if (-not (Test-Path -LiteralPath $Policy)) {
    throw "FP-I00 policy not found: $Policy"
}

$PreviousPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = $PythonRoot

    Write-Host "[FP-I00] Regenerating baseline and governance evidence..."
    & python $Runner $Repo --generate --json
    if ($LASTEXITCODE -ne 0) { throw "FP-I00 governance validation failed." }

    Write-Host "[FP-I00] Running phase tests..."
    & python -m pytest -q $Tests
    if ($LASTEXITCODE -ne 0) { throw "FP-I00 pytest suite failed." }

    if ($SourceRoot) {
        $ResolvedSource = (Resolve-Path -LiteralPath $SourceRoot).Path
        $Contract = Join-Path $Repo "docs\execution\EXP0019_faerie_protocol_contextual_divergence\source_audit\SOURCE_HASHES.sha256"
        Write-Host "[FP-I00] Verifying external source package..."
        @"
from pathlib import Path
import json, sys
sys.path.insert(0, r'$PythonRoot')
from fp_i00_governance.source_verify import verify_source_directory
report = verify_source_directory(Path(r'$ResolvedSource'), Path(r'$Contract'))
print(json.dumps(report, indent=2, sort_keys=True))
Path(r'$Artifacts\FP_I00_EXTERNAL_SOURCE_VERIFICATION.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n', encoding='utf-8')
raise SystemExit(0 if report['passed'] else 1)
"@ | python -
        if ($LASTEXITCODE -ne 0) { throw "External FP source package does not match the frozen source hashes." }
    }

    if (-not $SkipPreviousContextPythonTest) {
        $PreviousTest = Join-Path $Repo "contexts\legacy\infrastructure\exp0018_daye_trader\tests\test_exp0018_phase00_doctrine_v2.py"
        if (Test-Path -LiteralPath $PreviousTest) {
            Write-Host "[FP-I00] Running previous-context Python compatibility test..."
            & python $PreviousTest
            if ($LASTEXITCODE -ne 0) { throw "EXP0018 previous-context compatibility test failed." }
        }
    }

    if (-not $SkipEngineeringPolicy) {
        $EngineeringPolicy = Join-Path $Repo "tools\engineering\run_engineering_policy.py"
        if (Test-Path -LiteralPath $EngineeringPolicy) {
            Write-Host "[FP-I00] Running repository engineering policy..."
            & python $EngineeringPolicy $Repo
            if ($LASTEXITCODE -ne 0) { throw "Repository engineering policy failed." }
        }
    }

    Write-Host "[FP-I00] PASS — governance baseline is ready for FP-I01 handoff."
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
}
