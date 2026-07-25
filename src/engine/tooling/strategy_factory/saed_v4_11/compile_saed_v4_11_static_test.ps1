$ErrorActionPreference = "Stop"
$RepositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..")).Path
$Source = Join-Path $RepositoryRoot "mql5\Experts\DecisionAlphaLab\StrategyFactory\SAED\V4_11\SAEDV411StaticContractTest.mq5"
if (-not (Test-Path $Source)) { throw "V4-11 static contract expert not found." }
$Candidates = @(
  "$env:ProgramFiles\MetaTrader 5\metaeditor64.exe",
  "${env:ProgramFiles(x86)}\MetaTrader 5\metaeditor64.exe"
) | Where-Object { $_ -and (Test-Path $_) }
if (-not $Candidates) { throw "MetaEditor was not found. Static validation is available, but compile evidence remains pending_local_windows." }
$Log = Join-Path $env:TEMP "saed_v4_11_metaeditor.log"
& $Candidates[0] /compile:"$Source" /log:"$Log"
if ($LASTEXITCODE -ne 0) { Get-Content $Log -ErrorAction SilentlyContinue; throw "MetaEditor compile failed." }
Get-Content $Log -ErrorAction SilentlyContinue
