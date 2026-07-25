$Zip = Get-ChildItem "$env:USERPROFILE\Downloads" -File -Filter "decision-alpha-lab-saed-v3-context-intelligence-edge-discovery-v3.0.0*.zip" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $Zip) { throw "SAED V3 ZIP not found in Downloads." }
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath . -Force
Remove-Item -LiteralPath $Zip.FullName -Force
Get-Content ".\SAED_V3_FILE_INDEX.txt" | Where-Object { $_.Trim() } | ForEach-Object { git add -- ":(literal)$_" }
git status --short
git commit -m "docs(strategy-factory): add SAED V3 institutional context intelligence platform"
git push origin main
