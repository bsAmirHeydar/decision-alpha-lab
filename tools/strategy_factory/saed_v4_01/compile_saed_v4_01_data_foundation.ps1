param([string]$MetaEditorPath="",[string]$ProjectRoot=".")
$ErrorActionPreference="Stop"
if (-not $MetaEditorPath) {
  $candidates=@("$env:ProgramFiles\MetaTrader 5\metaeditor64.exe","$env:ProgramFiles(x86)\MetaTrader 5\metaeditor64.exe")
  $MetaEditorPath=$candidates | Where-Object { Test-Path $_ } | Select-Object -First 1
}
if (-not $MetaEditorPath -or -not (Test-Path $MetaEditorPath)) { throw "MetaEditor executable not found." }
$files=@(
 "mql5\Experts\AlphaLab\StrategyFactory\Diagnostics\EXP_SAED_V4_01_DataFoundationDiagnostic.mq5",
 "mql5\Experts\AlphaLab\StrategyFactory\Diagnostics\EXP_SAED_V4_01_DataFoundationSelfTest.mq5",
 "mql5\Experts\AlphaLab\StrategyFactory\Diagnostics\EXP_SAED_V4_01_DataAuthoritySelfTest.mq5"
)
$out=@()
foreach($rel in $files){$src=Join-Path $ProjectRoot $rel;$log="$src.compile.log";& $MetaEditorPath /compile:"$src" /log:"$log";if(-not(Test-Path $log)){throw "Compile log missing: $log"};$text=Get-Content $log -Raw;$out+=[pscustomobject]@{file=$rel;log=$log;success=($text -match '0 errors, 0 warnings')}}
$out | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $ProjectRoot 'SAED_V4_01_METAEDITOR_COMPILE_RESULTS.json') -Encoding UTF8
if($out.success -contains $false){exit 1}
