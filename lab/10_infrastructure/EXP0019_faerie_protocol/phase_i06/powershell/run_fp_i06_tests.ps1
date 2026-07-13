[CmdletBinding()]
param([string]$RepoRoot = ".")
$ErrorActionPreference = "Stop"
$root=(Resolve-Path -LiteralPath $RepoRoot).Path
$env:PYTHONPATH = @("$root\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i02\python","$root\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i03\python","$root\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i04\python","$root\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i05\python","$root\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i06\python") -join ";"
python -m pytest -q "$root\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i06\tests"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python "$root\tools\exp0019\check_fp_i06_boundaries.py" "$root"
python "$root\tools\exp0019\check_fp_i06_mql5_static.py" "$root"
python "$root\tools\exp0019\generate_fp_i06_vectors.py" "$root" --verify-only
python "$root\tools\exp0019\validate_fp_i06_delivery.py" "$root"
