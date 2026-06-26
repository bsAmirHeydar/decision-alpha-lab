param(
  [string]$Asset = "NAS100",
  [string]$Symbol = "NAS100",
  [string]$Timeframe = "M1",
  [Parameter(Mandatory=$true)][string]$From,
  [Parameter(Mandatory=$true)][string]$To,
  [string]$AstroCsv = "",
  [string]$PriceCsv = "",
  [switch]$SkipMt5Fetch,
  [switch]$ForceFetchPrice,
  [switch]$StrictPriceCoverage,
  [switch]$ForceBuildAstro,
  [double]$BrokerGmtOffsetHours = 3.0,
  [string]$TerminalPath = "",
  [string]$NatalLabel = "",
  [string]$NatalLocalDatetime = "",
  [string]$NatalUtcOffsetHours = "",
  [string]$NatalLat = "",
  [string]$NatalLon = "",
  [string]$HouseLat = "",
  [string]$HouseLon = "",
  [ValidateSet("sanity", "direction_only", "professional")][string]$Preset = "professional",
  [string]$Horizons = "30,60,120",
  [switch]$RunWalkForward,
  [int]$TrainDays = 120,
  [int]$TestDays = 20,
  [int]$StepDays = 20,
  [int]$EmbargoBars = 120,
  [int]$CognitiveMinSupport = 80,
  [double]$CognitiveMinLift = 1.10,
  [double]$CognitiveMaxGap = 0.18,
  [switch]$SkipAntifragile,
  [string]$AntifragileTargets = "",
  [int]$AntifragileMinRuleSupport = 120,
  [int]$AntifragileMinOosSupport = 40,
  [double]$AntifragileMinLift = 1.08,
  [double]$AntifragileMaxGap = 0.14,
  [switch]$EnableNeuralChallenger,
  [int]$NeuralMinRows = 8000,
  [switch]$OpenAfter
)
$ErrorActionPreference = "Stop"
$Common = Join-Path $env:APPDATA "MetaQuotes\Terminal\Common\Files"
$Script = Join-Path $PSScriptRoot "run_astro_human_learning_protocol.py"
$ArgsList = @($Script, "--asset", $Asset, "--symbol", $Symbol, "--timeframe", $Timeframe, "--from", $From, "--to", $To, "--common-files", $Common, "--broker-gmt-offset-hours", $BrokerGmtOffsetHours, "--preset", $Preset, "--horizons", $Horizons, "--train-days", $TrainDays, "--test-days", $TestDays, "--step-days", $StepDays, "--embargo-bars", $EmbargoBars, "--cognitive-min-support", $CognitiveMinSupport, "--cognitive-min-lift", $CognitiveMinLift, "--cognitive-max-gap", $CognitiveMaxGap, "--antifragile-min-rule-support", $AntifragileMinRuleSupport, "--antifragile-min-oos-support", $AntifragileMinOosSupport, "--antifragile-min-lift", $AntifragileMinLift, "--antifragile-max-gap", $AntifragileMaxGap, "--neural-min-rows", $NeuralMinRows)
if ($AstroCsv -ne "") { $ArgsList += @("--astro-csv", $AstroCsv) }
if ($PriceCsv -ne "") { $ArgsList += @("--price-csv", $PriceCsv) }
if ($SkipMt5Fetch) { $ArgsList += "--skip-mt5-fetch" }
if ($ForceFetchPrice) { $ArgsList += "--force-fetch-price" }
if ($StrictPriceCoverage) { $ArgsList += "--strict-price-coverage" }
if ($ForceBuildAstro) { $ArgsList += "--force-build-astro" }
if ($TerminalPath -ne "") { $ArgsList += @("--terminal-path", $TerminalPath) }
if ($NatalLabel -ne "") { $ArgsList += @("--natal-label", $NatalLabel) }
if ($NatalLocalDatetime -ne "") { $ArgsList += @("--natal-local-datetime", $NatalLocalDatetime) }
if ($NatalUtcOffsetHours -ne "") { $ArgsList += @("--natal-utc-offset-hours", $NatalUtcOffsetHours) }
if ($NatalLat -ne "") { $ArgsList += @("--natal-lat", $NatalLat) }
if ($NatalLon -ne "") { $ArgsList += @("--natal-lon", $NatalLon) }
if ($HouseLat -ne "") { $ArgsList += @("--house-lat", $HouseLat) }
if ($HouseLon -ne "") { $ArgsList += @("--house-lon", $HouseLon) }
if ($RunWalkForward) { $ArgsList += "--run-walk-forward" }
if ($SkipAntifragile) { $ArgsList += "--skip-antifragile" }
if ($AntifragileTargets -ne "") { $ArgsList += @("--antifragile-targets", $AntifragileTargets) }
if ($EnableNeuralChallenger) { $ArgsList += "--enable-neural-challenger" }

$out = python @ArgsList | Tee-Object -Variable lines
$dirLine = ($lines | Select-String -Pattern "^HUMAN_LEARNING_PROTOCOL_DIR=" | Select-Object -First 1).ToString()
if ($OpenAfter -and $dirLine) {
  $dir = $dirLine.Substring("HUMAN_LEARNING_PROTOCOL_DIR=".Length)
  Invoke-Item $dir
}
