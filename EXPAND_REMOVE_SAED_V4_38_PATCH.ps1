$ErrorActionPreference = "Stop"
$Zip = Get-ChildItem . -File -Filter "decision-alpha-lab-saed-v4-38-immutable-runtime-mql5-parity-v1.0.0*.zip" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $Zip) { throw "SAED V4-38 ZIP patch was not found in the repository root." }
Expand-Archive -LiteralPath $Zip.FullName -DestinationPath . -Force
Remove-Item -LiteralPath $Zip.FullName -Force
python tools/strategy_factory/saed_v4_38/run_saed_v4_38_full_qa.py
if ($LASTEXITCODE -ne 0) { throw "SAED V4-38 full QA failed." }
python tools/strategy_factory/saed_v4_38/validate_saed_v4_38_delivery.py
if ($LASTEXITCODE -ne 0) { throw "SAED V4-38 delivery validation failed." }
git add --pathspec-from-file=SAED_V4_38_FILE_INDEX.txt
if ($LASTEXITCODE -ne 0) { throw "Git staging failed." }
git diff --cached --check
if ($LASTEXITCODE -ne 0) { throw "Git staged diff check failed." }
git commit -F COMMIT_MESSAGE.md
if ($LASTEXITCODE -ne 0) { throw "Git commit failed." }
git push
if ($LASTEXITCODE -ne 0) { throw "Git push failed." }
