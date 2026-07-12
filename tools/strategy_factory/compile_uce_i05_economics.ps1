param([string]$MetaEditorPath='', [string]$RepositoryRoot='.')
$ErrorActionPreference='Stop'; if(-not $MetaEditorPath){$candidates=@("$env:ProgramFiles\MetaTrader 5\metaeditor64.exe","$env:ProgramFiles(x86)\MetaTrader 5\metaeditor64.exe");$MetaEditorPath=$candidates|Where-Object{Test-Path $_}|Select-Object -First 1}
if(-not $MetaEditorPath){throw 'MetaEditor64 not found. Pass -MetaEditorPath explicitly.'}
$files=@('mql5\Experts\StrategyFactory\UCE_I05_EconomicsDiagnostic.mq5','mql5\Experts\StrategyFactoryTests\UCE_I05_EconomicsSelfTest.mq5','mql5\Experts\StrategyFactoryTests\UCE_I05_LongShortSymmetrySelfTest.mq5')
foreach($f in $files){& $MetaEditorPath /compile:(Join-Path $RepositoryRoot $f) /inc:(Join-Path $RepositoryRoot 'mql5\Include') /log; if($LASTEXITCODE-ne 0){throw "MetaEditor failed for $f"}}
