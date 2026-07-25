$ErrorActionPreference = "Stop"
$Zip = Get-ChildItem . -File -Filter "decision-alpha-lab-acl-os-architecture-v1.0.0*.zip" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $Zip) { throw "ACL-OS architecture ZIP patch was not found in the repository root." }
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath . -Force
Remove-Item -LiteralPath $Zip.FullName -Force
