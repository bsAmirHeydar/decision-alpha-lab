param(
  [string]$RepoRoot = ".",
  [string]$ZipPath = ""
)
$ErrorActionPreference = "Stop"
$root = (Resolve-Path $RepoRoot).Path
if (-not $ZipPath) {
  $match = Get-ChildItem "$env:USERPROFILE\Downloads" -File -Filter "decision-alpha-lab-ucee-i12-statistical-promotion-v1.0.0*.zip" |
    Sort-Object LastWriteTime -Descending | Select-Object -First 1
  if (-not $match) { throw "UCE-I12 patch ZIP not found in Downloads." }
  $ZipPath = $match.FullName
}
Expand-Archive -LiteralPath $ZipPath -DestinationPath $root -Force
Remove-Item -LiteralPath $ZipPath -Force
Write-Host "UCE-I12 expanded into $root and ZIP removed."
