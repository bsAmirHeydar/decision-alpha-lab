$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Push-Location $ProjectRoot

try {
    Write-Host "Decision Alpha Lab | applying Python-brain / MQL-visual architecture..." -ForegroundColor Cyan

    # Remove the old React/FastAPI UI stack. This does NOT touch lab/cache_data,
    # lab/cache_nodes, or lab/cache_metrics.
    $pathsToRemove = @(
        "apps",
        "docs/ui",
        "node_modules",
        "apps/web/node_modules",
        "apps/web/dist",
        "apps/web/.vite",
        "pnpm-lock.yaml",
        "pnpm-workspace.yaml",
        "package-lock.json",
        "package.json",
        ".npmrc",
        "repair_lab_os.ps1"
    )

    foreach ($path in $pathsToRemove) {
        if (Test-Path $path) {
            Remove-Item -Recurse -Force $path -ErrorAction SilentlyContinue
            Write-Host "removed $path" -ForegroundColor DarkGray
        }
    }

    # Remove old MQL compute modules from the repo. Python is the only M0001 brain now.
    if (Test-Path ".\mql5\Include\DecisionAlphaLab") {
        Remove-Item ".\mql5\Include\DecisionAlphaLab\M0001_*.mqh" -Force -ErrorAction SilentlyContinue
    }

    Get-ChildItem -Path . -Filter "quant_lab_*.zip" -File -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
    Get-ChildItem -Path . -Filter "quant_lab_*.patch" -File -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
    Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    Get-ChildItem -Path . -Recurse -File -Filter "*.pyc" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue

    if (Test-Path ".\tools\copy_mql_live_lab.ps1") {
        powershell -ExecutionPolicy Bypass -File ".\tools\copy_mql_live_lab.ps1"
    }

    Write-Host "" 
    Write-Host "Done." -ForegroundColor Green
    Write-Host "Compile in MetaEditor:"
    Write-Host "  Experts/DecisionAlphaLab/M0001_LiveVisualLab.mq5"
    Write-Host ""
    Write-Host "Run Python brain to generate/update the MT5 visual contract:"
    Write-Host "  powershell -ExecutionPolicy Bypass -File .\tools\run_m0001_python_brain_to_mt5.ps1 -Symbol GOLD -Timeframe M15 -Bars 1200 -Once"
}
finally {
    Pop-Location
}
