$ErrorActionPreference = "Stop"
$Zip = Get-ChildItem . -File -Filter "decision-alpha-lab-saed-v4-37-portfolio-execution-economics-v1.0.0*.zip" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $Zip) { throw "SAED V4-37 ZIP patch was not found in the repository root." }
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath . -Force
Remove-Item -LiteralPath $Zip.FullName -Force
python tools/strategy_factory/saed_v4_37/run_saed_v4_37_full_qa.py
if ($LASTEXITCODE -ne 0) { throw "SAED V4-37 full QA failed." }
python tools/strategy_factory/saed_v4_37/validate_saed_v4_37_delivery.py
if ($LASTEXITCODE -ne 0) { throw "SAED V4-37 delivery validation failed." }
git add --pathspec-from-file=SAED_V4_37_FILE_INDEX.txt
if ($LASTEXITCODE -ne 0) { throw "Git staging failed." }
git diff --cached --check
if ($LASTEXITCODE -ne 0) { throw "Git staged diff check failed." }
git commit -F COMMIT_MESSAGE.md
if ($LASTEXITCODE -ne 0) { throw "Git commit failed." }
git push
if ($LASTEXITCODE -ne 0) { throw "Git push failed." }
