param(
  [Parameter(Mandatory=$true)][string]$MetaEditorPath,
  [Parameter(Mandatory=$true)][string]$TerminalMql5Root,
  [string]$RepositoryRoot = ".",
  [string]$LogPath = ".\sf01_contract_compile.log",
  [switch]$NoStage
)

$ErrorActionPreference = "Stop"
$repo = (Resolve-Path $RepositoryRoot).Path
$terminal = (Resolve-Path $TerminalMql5Root).Path
if (-not (Test-Path $MetaEditorPath)) { throw "MetaEditor64.exe not found: $MetaEditorPath" }
if (-not (Test-Path (Join-Path $terminal "Include"))) { throw "Invalid MQL5 root: $terminal" }

$sourceInclude = Join-Path $repo "mql5\Include\AlphaLab\StrategyFactory\Contracts"
$sourceExpert = Join-Path $repo "mql5\Experts\StrategyFactoryTests\SF01_ContractSelfTest.mq5"
$targetInclude = Join-Path $terminal "Include\AlphaLab\StrategyFactory\Contracts"
$targetExpertDir = Join-Path $terminal "Experts\StrategyFactoryTests"
$targetExpert = Join-Path $targetExpertDir "SF01_ContractSelfTest.mq5"

if (-not $NoStage) {
  New-Item -ItemType Directory -Force -Path $targetInclude,$targetExpertDir | Out-Null
  Copy-Item (Join-Path $sourceInclude "*.mqh") $targetInclude -Force
  Copy-Item $sourceExpert $targetExpert -Force
}
if (-not (Test-Path $targetExpert)) { throw "Staged self-test not found: $targetExpert" }

& $MetaEditorPath "/compile:$targetExpert" "/log:$LogPath"
$exit = $LASTEXITCODE
if (Test-Path $LogPath) { Get-Content $LogPath }
if ($exit -ne 0) { throw "MetaEditor compile returned exit code $exit" }
if (Select-String -Path $LogPath -Pattern "[1-9][0-9]* error" -Quiet) { throw "Compile log contains errors" }
Write-Host "SF01 compile passed. Attach the log to Phase 01 evidence, then run SF01_ContractSelfTest in Strategy Tester."
