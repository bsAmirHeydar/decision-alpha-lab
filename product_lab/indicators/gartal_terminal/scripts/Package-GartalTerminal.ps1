param(
  [string]$Version = "1.0.0-beta",
  [ValidateSet("dev", "beta", "stable", "internal")]
  [string]$Channel = "beta",
  [switch]$IncludeSource,
  [switch]$RequireCompiledEx5
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$ReleaseDir = Join-Path $Root "release"
$PackageRoot = Join-Path $ReleaseDir "_pack_gartal_terminal_$Version"
$Out = Join-Path $ReleaseDir "gartal-terminal-$Version-$Channel.zip"

New-Item -ItemType Directory -Force -Path $ReleaseDir | Out-Null
if (Test-Path $PackageRoot) { Remove-Item $PackageRoot -Recurse -Force }
if (Test-Path $Out) { Remove-Item $Out -Force }
New-Item -ItemType Directory -Force -Path $PackageRoot | Out-Null

$CompiledIndicator = Join-Path $Root "mql5\GartalTerminal.ex5"
$CompiledDownloader = Join-Path $Root "mql5\experts\GartalNewsDownloaderEA.ex5"

if ($RequireCompiledEx5) {
  if (!(Test-Path $CompiledIndicator)) { throw "Missing compiled indicator: $CompiledIndicator" }
  if (!(Test-Path $CompiledDownloader)) { throw "Missing compiled downloader EA: $CompiledDownloader" }
}

$CustomerDirs = @(
  "MQL5\Indicators\GartalTerminal",
  "MQL5\Experts\GartalTerminal",
  "MQL5\Presets",
  "docs",
  "fixtures"
)
foreach ($d in $CustomerDirs) { New-Item -ItemType Directory -Force -Path (Join-Path $PackageRoot $d) | Out-Null }

if (Test-Path $CompiledIndicator) {
  Copy-Item $CompiledIndicator -Destination (Join-Path $PackageRoot "MQL5\Indicators\GartalTerminal\GartalTerminal.ex5") -Force
}
if (Test-Path $CompiledDownloader) {
  Copy-Item $CompiledDownloader -Destination (Join-Path $PackageRoot "MQL5\Experts\GartalTerminal\GartalNewsDownloaderEA.ex5") -Force
}

Copy-Item (Join-Path $Root "mql5\presets\*.set") -Destination (Join-Path $PackageRoot "MQL5\Presets") -Force -ErrorAction SilentlyContinue
Copy-Item (Join-Path $Root "release\customer_docs\*") -Destination (Join-Path $PackageRoot "docs") -Recurse -Force -ErrorAction SilentlyContinue
Copy-Item (Join-Path $Root "test_fixtures\*") -Destination (Join-Path $PackageRoot "fixtures") -Force -ErrorAction SilentlyContinue

if ($IncludeSource) {
  New-Item -ItemType Directory -Force -Path (Join-Path $PackageRoot "source") | Out-Null
  Copy-Item (Join-Path $Root "mql5\GartalTerminal.mq5") -Destination (Join-Path $PackageRoot "source") -Force
  Copy-Item (Join-Path $Root "mql5\experts") -Destination (Join-Path $PackageRoot "source\experts") -Recurse -Force
  Copy-Item (Join-Path $Root "mql5\include") -Destination (Join-Path $PackageRoot "source\include") -Recurse -Force
}

$Manifest = @"
product: gartal terminal
version: $Version
channel: $Channel
built_at_utc: $((Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ"))
include_source: $IncludeSource
indicator_ex5_present: $(Test-Path $CompiledIndicator)
downloader_ex5_present: $(Test-Path $CompiledDownloader)
source_model: EA downloader + local file bridge
"@
Set-Content -Path (Join-Path $PackageRoot "RELEASE_MANIFEST.txt") -Value $Manifest -Encoding UTF8

Compress-Archive -Path (Join-Path $PackageRoot "*") -DestinationPath $Out -Force
Remove-Item $PackageRoot -Recurse -Force
Write-Host "Created: $Out"
