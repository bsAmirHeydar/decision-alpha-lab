param([Parameter(Mandatory=$true)][string]$ZipPath,[string]$RepoRoot=".")
$ErrorActionPreference="Stop"
$zip=(Resolve-Path -LiteralPath $ZipPath).Path
$root=(Resolve-Path -LiteralPath $RepoRoot).Path
Expand-Archive -LiteralPath $zip -DestinationPath $root -Force
Remove-Item -LiteralPath $zip -Force
Write-Host "UCE-I13 patch expanded and ZIP removed."
