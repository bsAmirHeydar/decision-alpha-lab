$ErrorActionPreference = "Stop"
$TestFile = Join-Path $PSScriptRoot "..\tests\test_phase13_controlled_model_comparison.py"
python $TestFile
exit $LASTEXITCODE
