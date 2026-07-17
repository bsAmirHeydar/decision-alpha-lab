$ErrorActionPreference = "Stop"
$Zip = Get-ChildItem . -File -Filter "decision-alpha-lab-acl-os-00-constitution-unified-authority-v1.0.0*.zip" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $Zip) { throw "ACL-OS ACL-00 ZIP patch was not found." }
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath . -Force
Remove-Item -LiteralPath $Zip.FullName -Force
python -m tools.strategy_factory.acl_os.acl_00.run_acl_00_full_qa
if ($LASTEXITCODE -ne 0) { throw "ACL-00 full QA failed." }
python -m tools.strategy_factory.acl_os.acl_00.validate_acl_00_delivery
if ($LASTEXITCODE -ne 0) { throw "ACL-00 delivery validation failed." }
