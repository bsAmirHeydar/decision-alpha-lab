$ErrorActionPreference = "Stop"
$Zip = Get-ChildItem . -File -Filter "decision-alpha-lab-saed-v4-22-generative-path-stress-lab-v1.0.0*.zip" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $Zip) { throw "SAED V4-22 ZIP patch was not found in the repository root." }
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath . -Force
Remove-Item -LiteralPath $Zip.FullName -Force
