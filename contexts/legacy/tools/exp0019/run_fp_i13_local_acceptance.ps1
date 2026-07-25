param(
    [string]$MetaEditor = "$env:ProgramFiles\MetaTrader 5\metaeditor64.exe",
    [string]$TerminalDataPath = ""
)
$ErrorActionPreference = "Stop"
if (-not (Test-Path $MetaEditor)) { throw "MetaEditor not found: $MetaEditor" }
if (-not $TerminalDataPath) { throw "Provide -TerminalDataPath pointing to the MetaTrader terminal data folder." }
$Indicator = Join-Path $TerminalDataPath "MQL5\Indicators\EXP0019\FaerieProtocol\EXP0019_FaerieProtocol_Context.mq5"
$SelfTest = Join-Path $TerminalDataPath "MQL5\Indicators\EXP0019\FaerieProtocolTests\EXP0019_FP_I13_ReleaseSelfTest.mq5"
& $MetaEditor /compile:"$Indicator" /log
if ($LASTEXITCODE -ne 0) { throw "Production indicator compile failed." }
& $MetaEditor /compile:"$SelfTest" /log
if ($LASTEXITCODE -ne 0) { throw "FP-I13 self-test compile failed." }
Write-Host "FP-I13 MetaEditor compile gate passed. Attach the self-test indicator and confirm PASS in Experts log."
