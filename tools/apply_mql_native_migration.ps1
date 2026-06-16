param(
    [string]$TerminalDataPath = ""
)

$ErrorActionPreference = "Stop"

Write-Host "Decision Alpha Lab | applying MQL-native migration"

# Remove active Python/UI/runtime artifacts from the repository working tree.
$remove = @(
    "apps",
    "node_modules",
    ".pytest_cache",
    "lab\cache_data",
    "lab\cache_metrics",
    "lab\cache_nodes"
)

foreach ($path in $remove) {
    if (Test-Path $path) {
        Write-Host "Removing $path"
        Remove-Item $path -Recurse -Force
    }
}

Get-ChildItem -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
Get-ChildItem -Recurse -File -Include "*.py","*.pyc","*.pyo","*.parquet" -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch "\\.git\\" } |
    Remove-Item -Force

Remove-Item -Force pnpm-lock.yaml,pnpm-workspace.yaml,package-lock.json,package.json -ErrorAction SilentlyContinue
Remove-Item -Force quant_lab_*.zip,quant_lab_*.patch -ErrorAction SilentlyContinue

if ($TerminalDataPath -ne "") {
    $mqlRoot = Join-Path $TerminalDataPath "MQL5"
    Write-Host "Copying MQL files to $mqlRoot"

    Copy-Item -Path ".\mql5\Experts\*" -Destination (Join-Path $mqlRoot "Experts") -Recurse -Force
    Copy-Item -Path ".\mql5\Include\*" -Destination (Join-Path $mqlRoot "Include") -Recurse -Force
    Copy-Item -Path ".\mql5\Scripts\*" -Destination (Join-Path $mqlRoot "Scripts") -Recurse -Force
}

Write-Host "Done. Compile: MQL5\Experts\DecisionAlphaLab\M0001\M0001_LiveVisualLab.mq5"
