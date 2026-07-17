$Zip = Get-ChildItem . -File -Filter "decision-alpha-lab-acl-os-02-context-standard-intake-v1.0.0*.zip" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $Zip) { throw "ACL-02 ZIP patch not found." }
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath . -Force
Remove-Item -LiteralPath $Zip.FullName -Force
