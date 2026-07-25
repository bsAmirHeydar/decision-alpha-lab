$ErrorActionPreference = "Stop"
$Zip = Get-ChildItem . -File -Filter "decision-alpha-lab-saed-v4-36-research-memory-active-planner-v1.0.0*.zip" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $Zip) { throw "SAED V4-36 ZIP patch was not found in the repository root." }
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath . -Force
Remove-Item -LiteralPath $Zip.FullName -Force
python tools/strategy_factory/saed_v4_36/run_saed_v4_36_full_qa.py
if ($LASTEXITCODE -ne 0) { throw "SAED V4-36 full QA failed." }
python tools/strategy_factory/saed_v4_36/validate_saed_v4_36_delivery.py
if ($LASTEXITCODE -ne 0) { throw "SAED V4-36 delivery validation failed." }
git add --pathspec-from-file=SAED_V4_36_FILE_INDEX.txt
if ($LASTEXITCODE -ne 0) { throw "Git staging failed." }
git diff --cached --check
if ($LASTEXITCODE -ne 0) { throw "Git staged diff check failed." }
git commit -F COMMIT_MESSAGE.md
if ($LASTEXITCODE -ne 0) { throw "Git commit failed." }
git push
if ($LASTEXITCODE -ne 0) { throw "Git push failed." }
