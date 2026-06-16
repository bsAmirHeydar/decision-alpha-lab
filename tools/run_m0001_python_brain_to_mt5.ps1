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
    [int]$RandomCount = 0,
    [int]$Seed = 42,

    # Recommended mode after Phase: Python brain + MQL input bridge.
    # In this mode MT5 Expert inputs write:
    #   MQL5\Files\DecisionAlphaLab\M0001\m0001_runtime_config.ini
    # and Python reads it every cycle.
    [switch]$UseMqlInputs,
    [switch]$EventBridge,
    [switch]$WaitForMqlInputs,
    [bool]$UseCommonFiles = $true,
    [string]$MqlConfigFile = "DecisionAlphaLab\M0001\m0001_runtime_config.ini"
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Push-Location $ProjectRoot

try {
    $mql5Root = Split-Path (Split-Path (Get-Location))

    if ($UseCommonFiles) {
        $terminalFilesRoot = Join-Path $env:APPDATA "MetaQuotes\Terminal\Common\Files"
    }
    else {
        $terminalFilesRoot = "$mql5Root\Files"
    }

    $configPath = Join-Path $terminalFilesRoot $MqlConfigFile

    New-Item -ItemType Directory -Force "$terminalFilesRoot\DecisionAlphaLab\M0001" | Out-Null

    $argsList = @(
        "tools/run_m0001_python_live_visual.py",
        "--interval", $Interval
    )

    if ($EventBridge) { $UseMqlInputs = $true }

    if ($UseMqlInputs) {
        $argsList += @(
            "--mql-config", $configPath,
            "--terminal-files-root", $terminalFilesRoot
        )
        if ($WaitForMqlInputs) { $argsList += "--wait-for-config" }

        Write-Host "Python brain is watching MT5 Expert inputs / event bridge" -ForegroundColor Cyan
        Write-Host "  Root:     $(if ($UseCommonFiles) { 'COMMON Files' } else { 'TERMINAL MQL5 Files' })"
        Write-Host "  Config:   $configPath"
        Write-Host "  Files:    $terminalFilesRoot"
        Write-Host ""
        Write-Host "Change M0001 parameters from MT5 Expert inputs, then press OK. MQL also streams chart candles to Python."
        Write-Host "Python will regenerate the visual CSV from those inputs."
        Write-Host ""
    }
    else {
        $localOut = ".\mql5\Files\DecisionAlphaLab\M0001\${Symbol}_${Timeframe}_visual.csv"
        $terminalOut = "$terminalFilesRoot\DecisionAlphaLab\M0001\${Symbol}_${Timeframe}_visual.csv"

        New-Item -ItemType Directory -Force (Split-Path $localOut) | Out-Null
        New-Item -ItemType Directory -Force (Split-Path $terminalOut) | Out-Null

        $argsList += @(
            "--symbol", $Symbol,
            "--timeframe", $Timeframe,
            "--bars", $Bars,
            "--L", $L,
            "--zone-ratio", $ZoneRatio,
            "--exit-gap", $ExitGap,
            "--mode", $Mode,
            "--output", $localOut,
            "--terminal-files-output", $terminalOut
        )

        if ($Random) {
            $argsList += "--random"
            if ($RandomCount -gt 0) { $argsList += @("--random-count", $RandomCount) }
            $argsList += @("--seed", $Seed)
        }

        Write-Host "Python brain -> MT5 visual contract from CLI parameters" -ForegroundColor Cyan
        Write-Host "  Local:    $localOut"
        Write-Host "  Terminal: $terminalOut"
        Write-Host ""
    }

    if ($Once) { $argsList += "--once" }

    py @argsList
}
finally {
    Pop-Location
}
