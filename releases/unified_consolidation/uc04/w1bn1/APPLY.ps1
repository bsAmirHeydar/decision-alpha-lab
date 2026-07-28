param(
    [string]$RepositoryRoot = "."
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Resolve-PythonCommand {
    $Python = Get-Command python -ErrorAction SilentlyContinue
    if ($Python) { return [pscustomobject]@{ Executable = $Python.Source; Prefix = @("-B") } }
    $Py = Get-Command py -ErrorAction SilentlyContinue
    if ($Py) { return [pscustomobject]@{ Executable = $Py.Source; Prefix = @("-3", "-B") } }
    throw "Python 3 was not found."
}

function Invoke-Python {
    param([psobject]$PythonCommand, [string[]]$Arguments)
    $Previous = $env:PYTHONDONTWRITEBYTECODE
    $env:PYTHONDONTWRITEBYTECODE = "1"
    try {
        $Prefix = @($PythonCommand.Prefix)
        & $PythonCommand.Executable @Prefix @Arguments
        $ExitCode = $LASTEXITCODE
    }
    finally {
        if ($null -eq $Previous) { Remove-Item Env:PYTHONDONTWRITEBYTECODE -ErrorAction SilentlyContinue }
        else { $env:PYTHONDONTWRITEBYTECODE = $Previous }
    }
    if ($ExitCode -ne 0) {
        throw ("Python command failed with exit code {0}: {1}" -f $ExitCode, ($Arguments -join " "))
    }
}

$Root = (Resolve-Path -LiteralPath $RepositoryRoot).Path
$Release = Join-Path $Root "releases\unified_consolidation\uc04\w1bn1"
$Index = Join-Path $Release "PATCH_FILE_INDEX.txt"
$Ledger = Join-Path $Release "PATCH_FILE_HASHES.sha256"

if (-not (Test-Path -LiteralPath $Index -PathType Leaf)) { throw "Patch index missing: $Index" }
if (-not (Test-Path -LiteralPath $Ledger -PathType Leaf)) { throw "Patch hash ledger missing: $Ledger" }

$ExpectedPaths = @(
    Get-Content -LiteralPath $Index |
        ForEach-Object { $_.Trim() } |
        Where-Object { $_ }
)
if ($ExpectedPaths.Count -eq 0) { throw "Patch index is empty." }

$LedgerRows = @{}
foreach ($Line in Get-Content -LiteralPath $Ledger) {
    if ([string]::IsNullOrWhiteSpace($Line)) { continue }
    $Parts = $Line -split "  ", 2
    if ($Parts.Count -ne 2) { throw "Invalid hash ledger row: $Line" }
    $LedgerRows[$Parts[1]] = $Parts[0].ToLowerInvariant()
}

foreach ($Relative in $ExpectedPaths) {
    $Path = Join-Path $Root ($Relative.Replace('/', '\'))
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "Indexed patch file missing: $Relative" }
    if ($Relative -eq "releases/unified_consolidation/uc04/w1bn1/PATCH_FILE_HASHES.sha256") { continue }
    if (-not $LedgerRows.ContainsKey($Relative)) { throw "Hash ledger entry missing: $Relative" }
    $Actual = (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($Actual -ne $LedgerRows[$Relative]) { throw "Patch hash mismatch: $Relative" }
}

$PythonCommand = Resolve-PythonCommand
Invoke-Python $PythonCommand @("tools/engineering/run_engineering_policy.py", $Root)
Invoke-Python $PythonCommand @("-m", "tools.consolidation.ci.verify_migration_continuity", "--repo-root", $Root)
Invoke-Python $PythonCommand @("-m", "tools.consolidation.uc03p3.verify", "--repo-root", $Root, "--ci-fast")
Invoke-Python $PythonCommand @("-m", "tools.consolidation.uc04w0.verify", "--repo-root", $Root)
Invoke-Python $PythonCommand @("-m", "tools.consolidation.uc04w1.verify", "--repo-root", $Root)
Invoke-Python $PythonCommand @("-m", "tools.consolidation.uc04w1b.verify", "--repo-root", $Root)
Invoke-Python $PythonCommand @("-m", "tools.consolidation.uc04w1bn1.verify", "--repo-root", $Root)
Invoke-Python $PythonCommand @("-m", "pytest", "-q", "tests/consolidation/uc04w1bn1", "-p", "no:cacheprovider")
Invoke-Python $PythonCommand @("-m", "pytest", "--collect-only", "-q", "-p", "no:cacheprovider")

Write-Host "UC04-W1B-N1 installation and mandatory gates: PASS" -ForegroundColor Green
Write-Host "Native MetaEditor/MT5 execution is still pending and is not run by this installer."
