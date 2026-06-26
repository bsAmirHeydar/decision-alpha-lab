param(
  [string]$Asset = "NAS100",
  [string]$Timeframe = "M1",
  [Parameter(Mandatory=$true)][string]$From,
  [Parameter(Mandatory=$true)][string]$To,
  [string]$PreferredCsv = "",
  [switch]$ForceBuild,
  [double]$BrokerGmtOffsetHours = 3.0,
  [string]$OutCsv = "",
  [string]$NatalLabel = "",
  [string]$NatalLocalDatetime = "",
  [Nullable[double]]$NatalUtcOffsetHours = $null,
  [Nullable[double]]$NatalLat = $null,
  [Nullable[double]]$NatalLon = $null
)
$ErrorActionPreference = "Stop"
$Common = Join-Path $env:APPDATA "MetaQuotes\Terminal\Common\Files"
$Script = Join-Path $PSScriptRoot "resolve_astro_feature_store.py"
$ArgsList = @($Script, "--asset", $Asset, "--timeframe", $Timeframe, "--from", $From, "--to", $To, "--common-files", $Common, "--broker-gmt-offset-hours", $BrokerGmtOffsetHours)
if ($PreferredCsv -ne "") { $ArgsList += @("--preferred-csv", $PreferredCsv) }
if ($ForceBuild) { $ArgsList += "--force-build" }
if ($OutCsv -ne "") { $ArgsList += @("--out-csv", $OutCsv) }
if ($NatalLabel -ne "") { $ArgsList += @("--natal-label", $NatalLabel) }
if ($NatalLocalDatetime -ne "") { $ArgsList += @("--natal-local-datetime", $NatalLocalDatetime) }
if ($null -ne $NatalUtcOffsetHours) { $ArgsList += @("--natal-utc-offset-hours", $NatalUtcOffsetHours) }
if ($null -ne $NatalLat) { $ArgsList += @("--natal-lat", $NatalLat) }
if ($null -ne $NatalLon) { $ArgsList += @("--natal-lon", $NatalLon) }
python @ArgsList
