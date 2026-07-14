param([string]$MetaEditor = "metaeditor64.exe")
$Root = Resolve-Path (Join-Path $PSScriptRoot "..\..\..\..\..")
& $MetaEditor /compile:"$Root\mql5\Experts\EXP0019\FaerieProtocol\EXP0019_FP_I09_LedgerDiagnostic.mq5" /log
& $MetaEditor /compile:"$Root\mql5\Experts\EXP0019\FaerieProtocolTests\EXP0019_FP_I09_LedgerSelfTest.mq5" /log
