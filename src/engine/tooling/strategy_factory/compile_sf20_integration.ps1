param([string]$RepoRoot=".",[string]$MetaEditor="")
$ErrorActionPreference="Stop"
if(-not $MetaEditor){$candidates=@("$env:ProgramFiles/MetaTrader 5/metaeditor64.exe","$env:ProgramFiles/MetaTrader 5/MetaEditor64.exe","$env:ProgramFiles(x86)/MetaTrader 5/metaeditor64.exe");$MetaEditor=$candidates|Where-Object{Test-Path $_}|Select-Object -First 1}
if(-not $MetaEditor -or -not(Test-Path $MetaEditor)){throw "MetaEditor not found. Pass -MetaEditor explicitly."}
$targets=@("mql5/Experts/StrategyFactory/SF20_EXP0017PilotHost.mq5","mql5/Experts/StrategyFactory/SF20_EXP0017Diagnostic.mq5","mql5/Tests/Experts/StrategyFactory/SF20_EXP0017IntegrationSelfTest.mq5")
foreach($target in $targets){$file=(Resolve-Path "$RepoRoot/$target").Path;$log="$file.compile.log";& $MetaEditor "/compile:$file" "/log:$log";if($LASTEXITCODE-ne 0){throw "Compile failed: $target"};$text=Get-Content $log -Raw;if($text-match "[1-9][0-9]* errors"){throw "MetaEditor errors: $target`n$text"};Write-Host "PASS $target"}
