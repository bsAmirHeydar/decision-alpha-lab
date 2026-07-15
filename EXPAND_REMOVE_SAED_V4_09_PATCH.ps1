$Zip = Get-ChildItem . -File -Filter "decision-alpha-lab-saed-v4-09-execution-digital-twin-v1.0.0*.zip" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath . -Force
Remove-Item -LiteralPath $Zip.FullName -Force
