param(
    [string]$Symbol = "GOLD",
    [string]$Timeframe = "M15",
    [int]$Bars = 1200,
    [int]$L = 5,
    [double]$ZoneRatio = 0.90,
    [int]$ExitGap = 6,
    [string]$Mode = "hunt",
    [double]$Interval = 2.0,
    [switch]$Once,
    [switch]$Random,
    [int]$Seed = 42
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Push-Location $ProjectRoot

try {
    $mql5Root = Split-Path (Split-Path (Get-Location))
    $localOut = ".\mql5\Files\DecisionAlphaLab\M0001\${Symbol}_${Timeframe}_visual.csv"
    $terminalOut = "$mql5Root\Files\DecisionAlphaLab\M0001\${Symbol}_${Timeframe}_visual.csv"

    New-Item -ItemType Directory -Force (Split-Path $localOut) | Out-Null
    New-Item -ItemType Directory -Force (Split-Path $terminalOut) | Out-Null

    $argsList = @(
        "tools/run_m0001_python_live_visual.py",
        "--symbol", $Symbol,
        "--timeframe", $Timeframe,
        "--bars", $Bars,
        "--L", $L,
        "--zone-ratio", $ZoneRatio,
        "--exit-gap", $ExitGap,
        "--mode", $Mode,
        "--output", $localOut,
        "--terminal-files-output", $terminalOut,
        "--interval", $Interval
    )

    if ($Once) { $argsList += "--once" }
    if ($Random) { $argsList += @("--random", "--seed", $Seed) }

    Write-Host "Python brain -> MT5 visual contract" -ForegroundColor Cyan
    Write-Host "  Local:    $localOut"
    Write-Host "  Terminal: $terminalOut"
    Write-Host ""

    py @argsList
}
finally {
    Pop-Location
}
