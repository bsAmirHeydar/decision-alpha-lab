param(
  [Parameter(Mandatory=$true)][string]$Symbol,
  [string]$Timeframe = "M1",
  [Parameter(Mandatory=$true)][string]$From,
  [Parameter(Mandatory=$true)][string]$To,
  [string]$OutCsv = "",
  [string]$TerminalPath = "",
  [int]$Login = 0,
  [string]$Password = "",
  [string]$Server = ""
)

$ErrorActionPreference = "Stop"
$Common = Join-Path $env:APPDATA "MetaQuotes\Terminal\Common\Files"
$Script = Join-Path $PSScriptRoot "fetch_mt5_rates.py"

$ArgsList = @(
  $Script,
  "--symbol", $Symbol,
  "--timeframe", $Timeframe,
  "--from", $From,
  "--to", $To,
  "--common-files", $Common
)
if ($OutCsv -ne "") { $ArgsList += @("--out-csv", $OutCsv) }
if ($TerminalPath -ne "") { $ArgsList += @("--terminal-path", $TerminalPath) }
if ($Login -ne 0) { $ArgsList += @("--login", $Login) }
if ($Password -ne "") { $ArgsList += @("--password", $Password) }
if ($Server -ne "") { $ArgsList += @("--server", $Server) }

python @ArgsList
