[CmdletBinding()]
param([string]$RepoRoot='.')
$ErrorActionPreference='Stop'
$repo=(Resolve-Path -LiteralPath $RepoRoot).Path
Set-Location $repo
$env:PYTHONPATH=Join-Path $repo 'contexts\legacy\infrastructure\exp0019_faerie_protocol\phase_i02\python'
python -m pytest -q contexts\legacy\infrastructure\exp0019_faerie_protocol\phase_i02\tests
if($LASTEXITCODE -ne 0){exit $LASTEXITCODE}
python contexts\legacy\infrastructure\exp0019_faerie_protocol\phase_i02\run_phase_i02.py
if($LASTEXITCODE -ne 0){exit $LASTEXITCODE}
python contexts\legacy\tools\exp0019\check_fp_i02_boundaries.py .
if($LASTEXITCODE -ne 0){exit $LASTEXITCODE}
python contexts\legacy\tools\exp0019\check_fp_i02_mql5_static.py .
if($LASTEXITCODE -ne 0){exit $LASTEXITCODE}
python contexts\legacy\tools\exp0019\generate_fp_i02_vectors.py --verify-only
exit $LASTEXITCODE
