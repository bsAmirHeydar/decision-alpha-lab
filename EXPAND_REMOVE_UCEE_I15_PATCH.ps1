$Zip = Get-ChildItem "$env:USERPROFILE\Downloads" -File -Filter "decision-alpha-lab-ucee-i15-context-tournament-v1.0.0*.zip" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $Zip) { throw "ZIP patch UCE-I15 not found in Downloads." }
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath . -Force
Remove-Item -LiteralPath $Zip.FullName -Force
Get-Content ".\UCEE_I15_FILE_INDEX.txt" | Where-Object { $_.Trim() } | ForEach-Object { git add -- ":(literal)$_" }
git commit -m "feat(ucee): implement I15 real-context tournament and prospective paper governance"
git push origin main
