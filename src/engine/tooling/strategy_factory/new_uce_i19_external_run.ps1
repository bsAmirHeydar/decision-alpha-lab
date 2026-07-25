param([string]$RunId = ("uce-i19-" + [DateTime]::UtcNow.ToString("yyyyMMddTHHmmssZ")))
$ErrorActionPreference = "Stop"
$Root=(Resolve-Path (Join-Path $PSScriptRoot "../..")).Path
$RunRoot=Join-Path $Root ("local_evidence/uce_i19/"+$RunId)
if(Test-Path -LiteralPath $RunRoot){throw "Evidence run already exists: $RunRoot"}
New-Item -ItemType Directory -Force -Path $RunRoot | Out-Null
@('00_inputs','01_compile','02_startup','03_telemetry','04_reconciliation','05_incidents','06_eod','07_rollback','08_ramp','09_bundle') | ForEach-Object { New-Item -ItemType Directory -Force -Path (Join-Path $RunRoot $_) | Out-Null }
Copy-Item -LiteralPath (Join-Path $Root 'releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/artifacts/uce_i19/first_external_run_manifest.json') -Destination (Join-Path $RunRoot '00_inputs/first_external_run_manifest.json')
Copy-Item -LiteralPath (Join-Path $Root 'releases/history/strategy_factory/program/implementation/universal_context_exploitation_engine/v3_implementation/artifacts/uce_i19/external_deployment_target_template.json') -Destination (Join-Path $RunRoot '00_inputs/deployment_target.json')
Set-Content -LiteralPath (Join-Path $RunRoot 'RUN_ID.txt') -Value $RunId -Encoding UTF8
Write-Output $RunRoot
