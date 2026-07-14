param(
  [Parameter(Mandatory=$true)][string]$MetaEditor,
  [Parameter(Mandatory=$true)][string]$Mql5Root
)
$ErrorActionPreference = "Stop"
$EA = Join-Path $Mql5Root "Experts\EXP0019\FaerieProtocol\EXP0019_FaerieProtocol_Diagnostic.mq5"
$SelfTest = Join-Path $Mql5Root "Experts\EXP0019\FaerieProtocolTests\EXP0019_FP_I14_DiagnosticSelfTest.mq5"
$Indicator = Join-Path $Mql5Root "Indicators\EXP0019\FaerieProtocol\EXP0019_FaerieProtocol_Context.mq5"
foreach($Source in @($Indicator,$EA,$SelfTest)) {
  if(!(Test-Path $Source)){ throw "Missing source: $Source" }
  & $MetaEditor /compile:$Source /log
  if($LASTEXITCODE -ne 0){ throw "MetaEditor compile failed: $Source" }
}
Write-Host "Compile PASS. Run the FP-I14 self-test and Diagnostic EA on the same pair/config as the Indicator. Export both traces and compare them with tools/exp0019/compare_fp_i14_traces.py."
