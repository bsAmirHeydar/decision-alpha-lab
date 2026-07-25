param([string]$RepoRoot='.')
$ErrorActionPreference='Stop'
$root=(Resolve-Path $RepoRoot).Path
$env:PYTHONPATH=@(
 Join-Path $root 'contexts\legacy\infrastructure\exp0019_faerie_protocol\phase_i02\python',
 Join-Path $root 'contexts\legacy\infrastructure\exp0019_faerie_protocol\phase_i03\python',
 Join-Path $root 'contexts\legacy\infrastructure\exp0019_faerie_protocol\phase_i04\python',
 Join-Path $root 'contexts\legacy\infrastructure\exp0019_faerie_protocol\phase_i05\python'
) -join ';'
python -m pytest -q (Join-Path $root 'contexts\legacy\infrastructure\exp0019_faerie_protocol\phase_i05\tests')
if($LASTEXITCODE -ne 0){exit $LASTEXITCODE}
python (Join-Path $root 'contexts\legacy\tools\exp0019\check_fp_i05_boundaries.py') $root
python (Join-Path $root 'contexts\legacy\tools\exp0019\check_fp_i05_mql5_static.py') $root
python (Join-Path $root 'contexts\legacy\tools\exp0019\generate_fp_i05_vectors.py') $root --verify-only
python (Join-Path $root 'contexts\legacy\tools\exp0019\validate_fp_i05_delivery.py') $root
