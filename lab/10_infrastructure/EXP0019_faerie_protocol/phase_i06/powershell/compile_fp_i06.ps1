[CmdletBinding()]
param([string]$RepoRoot=".",[string]$MetaEditor="C:\Program Files\MetaTrader 5\metaeditor64.exe")
$ErrorActionPreference="Stop"
$root=(Resolve-Path -LiteralPath $RepoRoot).Path
if (-not (Test-Path -LiteralPath $MetaEditor)) { throw "MetaEditor not found: $MetaEditor" }
$targets=@("mql5\Experts\EXP0019\FaerieProtocol\EXP0019_FP_I06_RelationDiagnostic.mq5","mql5\Experts\EXP0019\FaerieProtocolTests\EXP0019_FP_I06_RelationSelfTest.mq5")
foreach($rel in $targets){$file=Join-Path $root $rel;$log="$file.compile.log";& $MetaEditor "/compile:$file" "/log:$log";if($LASTEXITCODE -ne 0){throw "Compile failed: $file"};$text=Get-Content $log -Raw;if($text -match "[1-9][0-9]* error"){throw "Compile errors in $log"}}
Write-Host "FP-I06 MetaEditor compile PASS"
