$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Push-Location $ProjectRoot

try {
    $mql5Root = Split-Path (Split-Path (Get-Location))

    New-Item -ItemType Directory -Force "$mql5Root\Experts\DecisionAlphaLab" | Out-Null
    New-Item -ItemType Directory -Force "$mql5Root\Files\DecisionAlphaLab\M0001" | Out-Null

    # MQL is now visual-only. Remove the old MQL compute include modules from the terminal
    # so MetaEditor cannot accidentally compile/inspect the obsolete MQL brain.
    if (Test-Path "$mql5Root\Include\DecisionAlphaLab") {
        Remove-Item "$mql5Root\Include\DecisionAlphaLab\M0001_*.mqh" -Force -ErrorAction SilentlyContinue
    }

    Copy-Item ".\mql5\Experts\DecisionAlphaLab\M0001_LiveVisualLab.mq5" "$mql5Root\Experts\DecisionAlphaLab\" -Force
    Copy-Item ".\mql5\Experts\DecisionAlphaLab\M0001_VisualLab.mq5" "$mql5Root\Experts\DecisionAlphaLab\" -Force -ErrorAction SilentlyContinue

    Write-Host "Copied Python-brain MQL visual lab to:" -ForegroundColor Cyan
    Write-Host "  $mql5Root\Experts\DecisionAlphaLab"
    Write-Host "  $mql5Root\Files\DecisionAlphaLab\M0001"
    Write-Host ""
    Write-Host "Compile in MetaEditor:" -ForegroundColor Green
    Write-Host "  Experts/DecisionAlphaLab/M0001_LiveVisualLab.mq5"
    Write-Host ""
    Write-Host "MQL does not compute M0001 anymore. Run Python to generate/update the CSV contract."
}
finally {
    Pop-Location
}
