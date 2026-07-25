$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..\..\..\..\..")
python -m pytest "$Root\lab_infrastructure\EXP0019_faerie_protocol\phase_i09	ests" -q
python "$Root	ools\exp0019alidate_fp_i09_delivery.py" "$Root"
python "$Root	ools\exp0019\check_fp_i09_boundaries.py" "$Root"
python "$Root	ools\exp0019\check_fp_i09_mql5_static.py" "$Root"
