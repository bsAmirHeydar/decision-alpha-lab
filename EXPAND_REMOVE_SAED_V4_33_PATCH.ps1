$ErrorActionPreference = "Stop"
$Zip = Get-ChildItem . -File -Filter "decision-alpha-lab-saed-v4-33-federated-confidential-research-v1.0.0*.zip" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $Zip) { throw "SAED V4-33 ZIP patch was not found in the repository root." }
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath . -Force
Remove-Item -LiteralPath $Zip.FullName -Force
python tools/strategy_factory/saed_v4_33/run_saed_v4_33_full_qa.py
if ($LASTEXITCODE -ne 0) { throw "SAED V4-33 full QA failed." }
python tools/strategy_factory/saed_v4_33/validate_saed_v4_33_delivery.py
if ($LASTEXITCODE -ne 0) { throw "SAED V4-33 delivery validation failed." }
git add --pathspec-from-file=SAED_V4_33_FILE_INDEX.txt
git diff --cached --check
git commit -F COMMIT_MESSAGE.md
git push
