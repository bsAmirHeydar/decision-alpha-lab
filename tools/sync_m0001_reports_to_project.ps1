param(
    [string]$TerminalDataPath = "",
    [string]$SearchRoot = "",
    [string]$ProjectReportPath = ".\reports\mql_native\M0001",
    [string]$ReportRelativePath = "reports\mql_native\M0001"
)

$ErrorActionPreference = "Stop"

function Add-IfExists {
    param(
        [System.Collections.Generic.List[string]]$List,
        [string]$Path
    )

    if ($Path -and (Test-Path $Path)) {
        $full = (Resolve-Path $Path).Path
        if (-not $List.Contains($full)) {
            [void]$List.Add($full)
        }
    }
}

Write-Host "Decision Alpha Lab | syncing M0001 reports to project"

New-Item -ItemType Directory -Path $ProjectReportPath -Force | Out-Null

$roots = [System.Collections.Generic.List[string]]::new()

if ($TerminalDataPath -ne "") {
    Add-IfExists $roots (Join-Path $TerminalDataPath "MQL5\Files\$ReportRelativePath")
    Add-IfExists $roots (Join-Path $TerminalDataPath "Tester")
}

if ($SearchRoot -ne "") {
    Add-IfExists $roots $SearchRoot
}

# Broad fallback for Strategy Tester agents. MT5 often writes tester files under
# AppData\Roaming\MetaQuotes\Tester\<agent>\MQL5\Files.
$metaQuotesRoaming = Join-Path $env:APPDATA "MetaQuotes"
Add-IfExists $roots $metaQuotesRoaming

$patterns = @(
    "*_M0001_full_audit_report.xls",
    "*_M0001_nodes.csv",
    "*_M0001_node_audit_states.csv",
    "*_M0001_events.csv"
)

$files = @()
foreach ($root in $roots) {
    Write-Host "Searching $root"
    foreach ($pattern in $patterns) {
        $files += Get-ChildItem -Path $root -Recurse -File -Filter $pattern -ErrorAction SilentlyContinue
    }
}

$files = $files | Sort-Object LastWriteTime -Descending -Unique

if (-not $files -or $files.Count -eq 0) {
    Write-Host "No M0001 report files found."
    Write-Host "Make sure InpWriteExcelReport=true or InpWriteValidationJournal=true and run the tester once."
    exit 1
}

foreach ($file in $files) {
    $target = Join-Path $ProjectReportPath $file.Name
    Copy-Item -Path $file.FullName -Destination $target -Force
    Write-Host "Copied $($file.Name)"
}

Write-Host "Done. Project report folder: $ProjectReportPath"
