\
$ErrorActionPreference = "Stop"

Push-Location (Resolve-Path (Join-Path $PSScriptRoot "..\..\..\..\.."))
try {
    python -m pytest "lab/10_infrastructure/EXP0019_faerie_protocol/phase_i08/tests" -q
}
finally {
    Pop-Location
}
