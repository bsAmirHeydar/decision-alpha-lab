$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Push-Location $ProjectRoot

try {
    $mql5Root = Split-Path (Split-Path (Get-Location))

    New-Item -ItemType Directory -Force "$mql5Root\Experts\DecisionAlphaLab" | Out-Null
    New-Item -ItemType Directory -Force "$mql5Root\Include\DecisionAlphaLab" | Out-Null

    Copy-Item ".\mql5\Experts\DecisionAlphaLab\M0001_LiveVisualLab.mq5" "$mql5Root\Experts\DecisionAlphaLab\" -Force
    Copy-Item ".\mql5\Experts\DecisionAlphaLab\M0001_VisualLab.mq5" "$mql5Root\Experts\DecisionAlphaLab\" -Force -ErrorAction SilentlyContinue
    Copy-Item ".\mql5\Include\DecisionAlphaLab\M0001_*.mqh" "$mql5Root\Include\DecisionAlphaLab\" -Force

    Write-Host "Copied M0001 Live Visual Lab to:"
    Write-Host "  $mql5Root\Experts\DecisionAlphaLab"
    Write-Host "  $mql5Root\Include\DecisionAlphaLab"
    Write-Host ""
    Write-Host "Now compile in MetaEditor:"
    Write-Host "  Experts/DecisionAlphaLab/M0001_LiveVisualLab.mq5"
}
finally {
    Pop-Location
}
