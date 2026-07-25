$ErrorActionPreference = "Stop"
$Zip = Get-ChildItem . -File -Filter "decision-alpha-lab-acl-os-01-repository-identity-artifact-locator-v1.0.0*.zip" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $Zip) { throw "ACL-01 ZIP patch was not found." }
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath . -Force
Remove-Item -LiteralPath $Zip.FullName -Force
