$ErrorActionPreference = "Stop"
$Zip = Get-ChildItem . -File -Filter "decision-alpha-lab-saed-v4-35-model-risk-supply-chain-v1.0.0*.zip" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $Zip) { throw "SAED V4-35 ZIP patch was not found in the repository root." }
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath . -Force
Remove-Item -LiteralPath $Zip.FullName -Force
python tools/strategy_factory/saed_v4_35/run_saed_v4_35_full_qa.py
if ($LASTEXITCODE -ne 0) { throw "SAED V4-35 full QA failed." }
python tools/strategy_factory/saed_v4_35/validate_saed_v4_35_delivery.py
if ($LASTEXITCODE -ne 0) { throw "SAED V4-35 delivery validation failed." }
git add --pathspec-from-file=SAED_V4_35_FILE_INDEX.txt
if ($LASTEXITCODE -ne 0) { throw "Git staging failed." }
git diff --cached --check
if ($LASTEXITCODE -ne 0) { throw "Git staged diff check failed." }
git commit -F COMMIT_MESSAGE.md
if ($LASTEXITCODE -ne 0) { throw "Git commit failed." }
git push
if ($LASTEXITCODE -ne 0) { throw "Git push failed." }
