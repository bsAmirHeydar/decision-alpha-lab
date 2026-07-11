param(
  [Parameter(Mandatory=$true)][string]$MetaEditorPath,
  [Parameter(Mandatory=$true)][string]$TerminalMql5Root
)

$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path

$IncludeSource = Join-Path $RepoRoot "mql5\Include\AlphaLab\StrategyFactory"
$IncludeTarget = Join-Path $TerminalMql5Root "Include\AlphaLab\StrategyFactory"
$ExpertsSource = Join-Path $RepoRoot "mql5\Experts"
$ExpertsTarget = Join-Path $TerminalMql5Root "Experts"

New-Item -ItemType Directory -Force -Path $IncludeTarget | Out-Null
Copy-Item -Recurse -Force (Join-Path $IncludeSource "*") $IncludeTarget

New-Item -ItemType Directory -Force -Path (Join-Path $ExpertsTarget "StrategyFactory") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $ExpertsTarget "StrategyFactoryTests") | Out-Null
Copy-Item -Force `
  (Join-Path $ExpertsSource "StrategyFactory\SF03_MarketServicesDiagnostic.mq5") `
  (Join-Path $ExpertsTarget "StrategyFactory")
Copy-Item -Force `
  (Join-Path $ExpertsSource "StrategyFactoryTests\SF03_MarketServicesSelfTest.mq5") `
  (Join-Path $ExpertsTarget "StrategyFactoryTests")

$Targets = @(
  (Join-Path $ExpertsTarget "StrategyFactoryTests\SF03_MarketServicesSelfTest.mq5"),
  (Join-Path $ExpertsTarget "StrategyFactory\SF03_MarketServicesDiagnostic.mq5")
)

foreach($Target in $Targets) {
  $Log = "$Target.compile.log"
  & $MetaEditorPath "/compile:$Target" "/log:$Log"
  if($LASTEXITCODE -ne 0) {
    throw "MetaEditor process failed for $Target"
  }
  $Text = Get-Content -Raw $Log
  if($Text -match "([1-9][0-9]*) errors") {
    throw "Compile errors in $Target. See $Log"
  }
  Write-Host "Compiled: $Target"
}

Write-Host "Run SF03_MarketServicesSelfTest in MetaTrader and attach Journal evidence."
