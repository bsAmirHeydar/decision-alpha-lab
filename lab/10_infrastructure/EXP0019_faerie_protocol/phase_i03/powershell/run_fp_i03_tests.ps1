[CmdletBinding()]
param([string]$RepoRoot='.')
$ErrorActionPreference='Stop'
$root=(Resolve-Path -LiteralPath $RepoRoot).Path
$env:PYTHONPATH=(Join-Path $root 'lab\10_infrastructure\EXP0019_faerie_protocol\phase_i02\python')+';'+(Join-Path $root 'lab\10_infrastructure\EXP0019_faerie_protocol\phase_i03\python')
python -m pytest -q (Join-Path $root 'lab\10_infrastructure\EXP0019_faerie_protocol\phase_i03\tests')
if($LASTEXITCODE-ne 0){exit $LASTEXITCODE}
python (Join-Path $root 'tools\exp0019\check_fp_i03_boundaries.py') $root
if($LASTEXITCODE-ne 0){exit $LASTEXITCODE}
python (Join-Path $root 'tools\exp0019\check_fp_i03_mql5_static.py') $root
if($LASTEXITCODE-ne 0){exit $LASTEXITCODE}
python (Join-Path $root 'tools\exp0019\generate_fp_i03_vectors.py') $root --verify-only
exit $LASTEXITCODE
