param([string]$ZipPath="")
$ErrorActionPreference="Stop"
if(-not $ZipPath){$ZipPath=(Get-ChildItem "$env:USERPROFILE\Downloads" -File -Filter "decision-alpha-lab-ucee-i16-context-onboarding-v1.0.0*.zip"|Sort-Object LastWriteTime -Descending|Select-Object -First 1).FullName}
if(-not $ZipPath){throw "UCE-I16 patch ZIP not found."}
Expand-Archive -LiteralPath $ZipPath -DestinationPath . -Force
Remove-Item -LiteralPath $ZipPath -Force
