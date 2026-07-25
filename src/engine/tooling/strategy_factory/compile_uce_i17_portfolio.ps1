param([string]$MetaEditorPath = "")
$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "../..")).Path
if (-not $MetaEditorPath) { throw "Pass -MetaEditorPath pointing to metaeditor64.exe" }
$Files = Get-ChildItem (Join-Path $Root "mql5/Experts/AlphaLab/StrategyFactory/Diagnostics") -Filter "EXP_UCE_I17_*.mq5"
foreach ($File in $Files) { & $MetaEditorPath /compile:$($File.FullName) /log }
