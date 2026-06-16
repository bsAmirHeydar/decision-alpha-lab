$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Push-Location $ProjectRoot

try {
    Write-Host "Decision Alpha Lab | applying MQL Live Visual Lab architecture..." -ForegroundColor Cyan

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

    Get-ChildItem -Path . -Filter "quant_lab_*.zip" -File -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
    Get-ChildItem -Path . -Filter "quant_lab_*.patch" -File -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
    Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    Get-ChildItem -Path . -Recurse -File -Filter "*.pyc" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue

    # Copy the MQL live visual lab to the actual terminal folders when this project
    # lives under MQL5\Shared Projects\decision-alpha-lab.
    if (Test-Path ".\tools\copy_mql_live_lab.ps1") {
        powershell -ExecutionPolicy Bypass -File ".\tools\copy_mql_live_lab.ps1"
    }

    Write-Host "" 
    Write-Host "Done. Compile in MetaEditor:" -ForegroundColor Green
    Write-Host "  Experts/DecisionAlphaLab/M0001_LiveVisualLab.mq5"
    Write-Host "" 
    Write-Host "Optional static artifact visualizer is also included:" -ForegroundColor Cyan
    Write-Host "  Experts/DecisionAlphaLab/M0001_VisualLab.mq5"
}
finally {
    Pop-Location
}
