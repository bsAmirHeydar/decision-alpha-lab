[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$SourceRoot,
    [string]$RepoRoot = "."
)

$ErrorActionPreference = "Stop"
$Repo = (Resolve-Path -LiteralPath $RepoRoot).Path
$Source = (Resolve-Path -LiteralPath $SourceRoot).Path
$PythonRoot = Join-Path $Repo "contexts\legacy\infrastructure\exp0019_faerie_protocol\phase_i00\python"
$Contract = Join-Path $Repo "docs\operations\execution\EXP0019_faerie_protocol_contextual_divergence\source_audit\SOURCE_HASHES.sha256"
$PreviousPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = $PythonRoot
    @"
from pathlib import Path
import json, sys
sys.path.insert(0, r'$PythonRoot')
from fp_i00_governance.source_verify import verify_source_directory
report = verify_source_directory(Path(r'$Source'), Path(r'$Contract'))
print(json.dumps(report, indent=2, sort_keys=True))
raise SystemExit(0 if report['passed'] else 1)
"@ | python -
    if ($LASTEXITCODE -ne 0) { throw "FP source package verification failed." }
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
}
