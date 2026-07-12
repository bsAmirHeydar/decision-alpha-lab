param([string]$MetaEditor = "metaeditor64.exe", [string]$RepoRoot = ".")
$ErrorActionPreference = "Stop"
$root=(Resolve-Path $RepoRoot).Path
$files=@("mql5\Experts\StrategyFactory\UCE_I03_TreatmentAtomsDiagnostic.mq5","mql5\Experts\StrategyFactoryTests\UCE_I03_TreatmentAtomsSelfTest.mq5")
foreach($rel in $files){$source=Join-Path $root $rel; if(!(Test-Path $source)){throw "Missing $source"}; & $MetaEditor "/compile:$source" "/inc:$(Join-Path $root 'mql5')"; if($LASTEXITCODE -ne 0){throw "MetaEditor compile failed for $rel"}}
Write-Host "UCE-I03 MetaEditor compilation completed. Review .log files for zero errors and warnings."
