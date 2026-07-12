param(
 [string]$RepoRoot = ".",
 [string]$MetaEditorPath = "",
 [string]$TerminalDataPath = ""
)
$ErrorActionPreference = "Stop"
$root=(Resolve-Path $RepoRoot).Path
if (-not $MetaEditorPath) {
 $candidates=@(
  "$env:ProgramFiles\MetaTrader 5\metaeditor64.exe",
  "$env:ProgramFiles\MetaTrader 5\MetaEditor64.exe",
  "$env:ProgramFiles(x86)\MetaTrader 5\metaeditor64.exe"
 )
 $MetaEditorPath=$candidates | Where-Object { Test-Path $_ } | Select-Object -First 1
}
if (-not $MetaEditorPath -or -not (Test-Path $MetaEditorPath)) { throw "MetaEditor64 not found. Pass -MetaEditorPath." }
if (-not $TerminalDataPath) { throw "Pass -TerminalDataPath pointing to the MT5 terminal data directory containing MQL5." }
$targets=@(
 "mql5\Experts\StrategyFactory\UCE_I07_TrainerSDKDiagnostic.mq5",
 "mql5\Experts\StrategyFactoryTests\UCE_I07_TrainerSDKSelfTest.mq5",
 "mql5\Experts\StrategyFactoryTests\UCE_I07_CapabilityParitySelfTest.mq5"
)
$includeSource=Join-Path $root "mql5\Include\AlphaLab\StrategyFactory\TrainerSDK"
$includeTarget=Join-Path $TerminalDataPath "MQL5\Include\AlphaLab\StrategyFactory\TrainerSDK"
New-Item -ItemType Directory -Force -Path $includeTarget | Out-Null
Copy-Item "$includeSource\*" $includeTarget -Recurse -Force
foreach($relative in $targets){
 $source=Join-Path $root $relative
 $leaf=Split-Path $relative -Leaf
 $category=if($relative -like "*StrategyFactoryTests*"){"StrategyFactoryTests"}else{"StrategyFactory"}
 $targetDir=Join-Path $TerminalDataPath "MQL5\Experts\$category"
 New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
 $target=Join-Path $targetDir $leaf;Copy-Item $source $target -Force
 $log=Join-Path $targetDir ($leaf+".compile.log")
 & $MetaEditorPath "/compile:$target" "/log:$log"
 if($LASTEXITCODE -ne 0){throw "MetaEditor failed for $leaf. See $log"}
 if((Get-Content $log -Raw) -notmatch "0 errors, 0 warnings"){throw "Compilation not clean for $leaf. See $log"}
 Write-Host "PASS $leaf"
}
