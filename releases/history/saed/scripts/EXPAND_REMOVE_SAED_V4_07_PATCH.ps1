$ErrorActionPreference='Stop'
$Zip=Get-ChildItem . -File -Filter 'decision-alpha-lab-saed-v4-07-constraint-solver-action-lattice-v1.0.0*.zip' | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if(-not $Zip){throw 'SAED V4-07 ZIP patch was not found in the repository root.'}
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath . -Force
Remove-Item -LiteralPath $Zip.FullName -Force
