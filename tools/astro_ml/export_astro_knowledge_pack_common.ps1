param(
  [string]$Asset = "NAS100",
  [string]$Timeframe = "M1",
  [switch]$OpenAfter
)

$ErrorActionPreference = "Stop"
$Common = Join-Path $env:APPDATA "MetaQuotes\Terminal\Common\Files"
python "$PSScriptRoot\export_astro_knowledge_pack.py" `
  --asset $Asset `
  --timeframe $Timeframe `
  --common-files $Common

if ($OpenAfter) {
  $Pack = Join-Path $Common "astro_ml\memory\$Asset\$Timeframe\astro_knowledge_pack_${Asset}_${Timeframe}.md"
  if (Test-Path $Pack) { Start-Process $Pack }
}
