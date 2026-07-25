param([string]$RepoRoot='.',[string]$MetaEditor='C:\Program Files\MetaTrader 5\metaeditor64.exe')
$ErrorActionPreference='Stop';$root=(Resolve-Path $RepoRoot).Path
if(-not (Test-Path $MetaEditor)){throw "MetaEditor not found: $MetaEditor"}
$targets=@(
 'mql5\Experts\EXP0019\FaerieProtocol\EXP0019_FP_I05_ReferenceDiagnostic.mq5',
 'mql5\Tests\Experts\EXP0019\FaerieProtocol\EXP0019_FP_I05_ReferenceSelfTest.mq5'
)
foreach($rel in $targets){$file=Join-Path $root $rel;$log="$file.compile.log";& $MetaEditor "/compile:$file" "/log:$log";if($LASTEXITCODE -ne 0){throw "Compile failed: $rel"}}
