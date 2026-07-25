param(
  [string]$RepoRoot = ".",
  [string]$ZipPath = ""
)
$ErrorActionPreference = "Stop"
$Root = (Resolve-Path $RepoRoot).Path
if (-not $ZipPath) {
  $Zip = Get-ChildItem "$env:USERPROFILE\Downloads" -Filter "decision-alpha-lab-ucee-i11-*.zip" |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1
  if (-not $Zip) { throw "UCE-I11 patch ZIP was not found in Downloads." }
  $ZipPath = $Zip.FullName
}
Expand-Archive -LiteralPath $ZipPath -DestinationPath $Root -Force
Remove-Item -LiteralPath $ZipPath -Force
Write-Host "UCE-I11 patch expanded into $Root and ZIP removed."
