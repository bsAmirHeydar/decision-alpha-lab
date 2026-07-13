[CmdletBinding()]
param([string]$RepoRoot = (Get-Location).Path)
$ErrorActionPreference='Stop'
$repo=(Resolve-Path -LiteralPath $RepoRoot).Path
$env:PYTHONPATH=Join-Path $repo 'lab\10_infrastructure\EXP0019_faerie_protocol\phase_i01\python'
python -m pytest -q (Join-Path $repo 'lab\10_infrastructure\EXP0019_faerie_protocol\phase_i01\tests')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python (Join-Path $repo 'lab\10_infrastructure\EXP0019_faerie_protocol\phase_i01\run_phase_i01.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python (Join-Path $repo 'tools\exp0019\check_fp_i01_boundaries.py') $repo
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python (Join-Path $repo 'tools\exp0019\check_fp_i01_mql5_static.py') $repo
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python (Join-Path $repo 'tools\exp0019\validate_fp_i01_delivery.py') $repo
exit $LASTEXITCODE
