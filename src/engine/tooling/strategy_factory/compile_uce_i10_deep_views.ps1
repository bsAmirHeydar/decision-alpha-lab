param([string]$RepoRoot=(Resolve-Path "$PSScriptRoot/../..").Path,[string]$MetaEditor='')
$ErrorActionPreference='Stop'
if(-not $MetaEditor){$candidates=@("$env:ProgramFiles/MetaTrader 5/metaeditor64.exe","$env:ProgramFiles(x86)/MetaTrader 5/metaeditor64.exe");$MetaEditor=$candidates|Where-Object{Test-Path $_}|Select-Object -First 1}
if(-not $MetaEditor){throw 'MetaEditor was not found. Pass -MetaEditor <path-to-metaeditor64.exe>.'}
$targets=@('mql5/Experts/StrategyFactory/UCE_I10_DeepViewsDiagnostic.mq5','mql5/Tests/Experts/StrategyFactory/UCE_I10_DeepViewsSelfTest.mq5','mql5/Tests/Experts/StrategyFactory/UCE_I10_CausalitySafetySelfTest.mq5')
foreach($rel in $targets){$src=Join-Path $RepoRoot $rel;$log="$src.compile.log";& $MetaEditor /compile:$src /log:$log;Get-Content $log;if((Get-Content $log -Raw)-match '[1-9][0-9]* error'){throw "Compile failed: $rel"}}
