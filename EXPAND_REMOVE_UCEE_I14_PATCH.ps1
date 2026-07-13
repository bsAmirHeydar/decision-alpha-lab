$ErrorActionPreference = "Stop"
$Zip = Get-ChildItem "$env:USERPROFILE\Downloads" -File -Filter "decision-alpha-lab-ucee-i14-immutable-runtime-v1.0.0*.zip" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $Zip) { throw "UCE-I14 patch ZIP was not found in Downloads." }
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath . -Force
Remove-Item -LiteralPath $Zip.FullName -Force
Write-Host "UCE-I14 patch expanded and ZIP removed. Stage only UCEE_I14_FILE_INDEX.txt paths."
