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
Copy-Item -Recurse -Force (Join-Path $ExpertsSource "StrategyFactory") $ExpertsTarget
Copy-Item -Recurse -Force (Join-Path $ExpertsSource "StrategyFactoryTests") $ExpertsTarget

$Targets = @(
  (Join-Path $ExpertsTarget "StrategyFactory\SF02_StrategyHost.mq5"),
  (Join-Path $ExpertsTarget "StrategyFactoryTests\SF02_RuntimeSelfTest.mq5")
)
foreach($Target in $Targets) {
  $Log = "$Target.compile.log"
  & $MetaEditorPath "/compile:$Target" "/log:$Log"
  if($LASTEXITCODE -ne 0) { throw "MetaEditor failed for $Target" }
  $Text = Get-Content -Raw $Log
  if($Text -match "([1-9][0-9]*) errors") { throw "Compile errors in $Target. See $Log" }
  Write-Host "Compiled: $Target"
}
