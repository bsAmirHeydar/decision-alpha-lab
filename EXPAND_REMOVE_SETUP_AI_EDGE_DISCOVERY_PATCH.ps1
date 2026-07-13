$Zip = Get-ChildItem "$env:USERPROFILE\Downloads" -File -Filter "decision-alpha-lab-setup-ai-edge-discovery-architecture-v1.0.0*.zip" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $Zip) { throw "Patch ZIP not found in Downloads." }
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath . -Force
Remove-Item -LiteralPath $Zip.FullName -Force
Get-Content ".\SETUP_AI_EDGE_DISCOVERY_FILE_INDEX.txt" | Where-Object { $_.Trim() } | ForEach-Object { git add -- ":(literal)$_" }
git commit -m "docs(strategy-factory): add setup AI edge discovery and anti-overfit architecture"
git push origin main
