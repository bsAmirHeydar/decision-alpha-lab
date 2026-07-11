param([string]$MetaEditorPath = "C:\Program Files\MetaTrader 5\metaeditor64.exe")
$ErrorActionPreference = "Stop"
if (-not (Test-Path $MetaEditorPath)) { throw "MetaEditor not found: $MetaEditorPath" }
$targets = @(
  ".\mql5\Experts\StrategyFactory\SF19_ObservabilityHost.mq5",
  ".\mql5\Experts\StrategyFactory\SF19_ObservabilityDiagnostic.mq5",
  ".\mql5\Experts\StrategyFactoryTests\SF19_ObservabilitySelfTest.mq5"
)
New-Item -ItemType Directory -Force ".\artifacts\sf19_compile" | Out-Null
foreach ($target in $targets) {
  $name = [IO.Path]::GetFileNameWithoutExtension($target)
  & $MetaEditorPath "/compile:$target" "/inc:.\mql5\Include" "/log:.\artifacts\sf19_compile\$name.log"
  if ($LASTEXITCODE -ne 0) { throw "MetaEditor failed for $target" }
  $log = Get-Content ".\artifacts\sf19_compile\$name.log" -Raw
  if ($log -notmatch "0 errors, 0 warnings") { throw "Compile is not clean for $target. Read artifacts/sf19_compile/$name.log" }
}
Write-Host "SF19 MetaEditor compile PASS"
