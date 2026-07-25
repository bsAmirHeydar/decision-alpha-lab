$Zip = Get-ChildItem "$env:USERPROFILE\Downloads" -File -Filter "decision-alpha-lab-saed-v4-03-continuous-time-event-model-v1.0.0*.zip" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $Zip) { throw "ZIP patch SAED V4-03 was not found in Downloads." }
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath . -Force
Remove-Item -LiteralPath $Zip.FullName -Force
