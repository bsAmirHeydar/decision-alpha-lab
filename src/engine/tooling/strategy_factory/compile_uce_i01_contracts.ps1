param([string]$MetaEditorPath = "")
$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path
if ([string]::IsNullOrWhiteSpace($MetaEditorPath)) {
  $candidates = @(
    "$env:ProgramFiles\MetaTrader 5\metaeditor64.exe",
    "$env:ProgramFiles\MetaTrader 5\MetaEditor64.exe",
    "$env:ProgramFiles(x86)\MetaTrader 5\metaeditor64.exe"
  )
  $MetaEditorPath = $candidates | Where-Object { Test-Path $_ } | Select-Object -First 1
}
if (-not $MetaEditorPath -or -not (Test-Path $MetaEditorPath)) { throw "MetaEditor64.exe was not found. Pass -MetaEditorPath explicitly." }
$targets = @(
  "mql5/Tests/Experts/StrategyFactory/UCE_I01_ContractsV3SelfTest.mq5",
  "mql5/Experts/StrategyFactory/UCE_I01_ContractsV3Diagnostic.mq5"
)
foreach ($relative in $targets) {
  $source = Join-Path $RepoRoot $relative
  $log = "$source.compile.log"
  & $MetaEditorPath /compile:"$source" /log:"$log"
  if ($LASTEXITCODE -ne 0) { throw "MetaEditor failed for $relative. See $log" }
  $content = Get-Content $log -Raw
  if ($content -notmatch "0 error\(s\), 0 warning\(s\)") { throw "Compile gate failed for $relative. See $log" }
}
Write-Host "UCE-I01 MetaEditor compile gate: PASS"
