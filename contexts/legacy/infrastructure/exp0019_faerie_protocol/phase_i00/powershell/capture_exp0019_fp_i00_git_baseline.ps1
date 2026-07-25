[CmdletBinding()]
param(
    [string]$RepoRoot = "."
)

$ErrorActionPreference = "Stop"
$Repo = (Resolve-Path -LiteralPath $RepoRoot).Path
$Runner = Join-Path $Repo "contexts\legacy\infrastructure\exp0019_faerie_protocol\phase_i00\run_phase_i00.py"
$PythonRoot = Join-Path $Repo "contexts\legacy\infrastructure\exp0019_faerie_protocol\phase_i00\python"
$PreviousPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = $PythonRoot
    & python $Runner $Repo --generate --json
    if ($LASTEXITCODE -ne 0) { throw "FP-I00 baseline capture failed." }
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
}
