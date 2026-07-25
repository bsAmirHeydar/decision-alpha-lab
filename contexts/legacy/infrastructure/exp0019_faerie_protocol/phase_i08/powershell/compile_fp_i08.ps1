param([string]$MetaEditor = "metaeditor64.exe")
$Root = Resolve-Path (Join-Path $PSScriptRoot "..\..\..\..\..")
& $MetaEditor /compile:"$Root\mql5\Tests\Experts\EXP0019\FaerieProtocol\EXP0019_FP_I08_WeeklySelfTest.mq5" /log
& $MetaEditor /compile:"$Root\mql5\Experts\EXP0019\FaerieProtocol\EXP0019_FP_I08_WeeklyDiagnostic.mq5" /log
