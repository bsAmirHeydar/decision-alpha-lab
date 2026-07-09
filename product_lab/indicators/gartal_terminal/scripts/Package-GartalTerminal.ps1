param(
  [string]$Version = "0.1.0-product-architecture"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$ReleaseDir = Join-Path $Root "release"
$Out = Join-Path $ReleaseDir "gartal-terminal-$Version.zip"

New-Item -ItemType Directory -Force -Path $ReleaseDir | Out-Null
if (Test-Path $Out) { Remove-Item $Out -Force }

$Files = @(
  "README.md",
  "00_OBSIDIAN_START_HERE.md",
  "mql5",
  "spec",
  "obsidian"
)

$Temp = Join-Path $ReleaseDir "_pack_gartal_terminal"
if (Test-Path $Temp) { Remove-Item $Temp -Recurse -Force }
New-Item -ItemType Directory -Force -Path $Temp | Out-Null

foreach ($item in $Files) {
  $src = Join-Path $Root $item
  if (Test-Path $src) {
    Copy-Item $src -Destination $Temp -Recurse -Force
  }
}

Compress-Archive -Path (Join-Path $Temp "*") -DestinationPath $Out -Force
Remove-Item $Temp -Recurse -Force
Write-Host "Created: $Out"
