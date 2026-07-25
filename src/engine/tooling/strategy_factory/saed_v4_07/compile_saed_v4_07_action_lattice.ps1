param([string]$MetaEditorPath)
$ErrorActionPreference='Stop'
if (-not (Test-Path -LiteralPath $MetaEditorPath)) { throw 'MetaEditor executable not found.' }
$Targets = Get-ChildItem 'mql5/Experts/AlphaLab/StrategyFactory/Diagnostics' -Filter 'EXP_SAED_V4_07_*.mq5'
foreach ($Target in $Targets) { & $MetaEditorPath "/compile:$($Target.FullName)" /log; if ($LASTEXITCODE -ne 0) { throw "MetaEditor compile failed: $($Target.Name)" } }
Write-Host 'SAED V4-07 MetaEditor compilation completed. Attach generated logs as external evidence.'
