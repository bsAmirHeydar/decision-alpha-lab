param(
    [string]$MetaEditorPath = "C:\Program Files\MetaTrader 5\metaeditor64.exe",
    [string]$RepositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
)
$ErrorActionPreference = "Stop"
if (-not (Test-Path -LiteralPath $MetaEditorPath)) { throw "MetaEditor not found: $MetaEditorPath" }
$experts = Get-ChildItem (Join-Path $RepositoryRoot "mql5\Experts\AlphaLab\StrategyFactory\Diagnostics") -Filter "EXP_SAED_V4_06_*.mq5" -File | Sort-Object Name
if ($experts.Count -lt 3) { throw "Expected at least three V4-06 diagnostic experts." }
$logRoot = Join-Path $RepositoryRoot "releases\history\strategy_factory\artifacts\saed_v4_06\metaeditor"
New-Item -ItemType Directory -Path $logRoot -Force | Out-Null
foreach ($expert in $experts) {
    $log = Join-Path $logRoot ($expert.BaseName + ".log")
    & $MetaEditorPath "/compile:$($expert.FullName)" "/log:$log"
    if ($LASTEXITCODE -ne 0) { throw "MetaEditor failed for $($expert.Name)" }
    if (-not (Test-Path -LiteralPath $log)) { throw "Compiler log missing for $($expert.Name)" }
    $text = Get-Content -LiteralPath $log -Raw
    if ($text -notmatch "0 errors") { throw "Compiler errors detected for $($expert.Name). See $log" }
}
Write-Host "SAED V4-06 MetaEditor compilation passed for $($experts.Count) diagnostic experts."
