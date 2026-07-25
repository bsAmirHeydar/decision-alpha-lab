param(
  [Parameter(Mandatory=$true)][string]$MetaEditor,
  [Parameter(Mandatory=$true)][string]$MqlRoot
)
$ErrorActionPreference = "Stop"
$targets = @(
  Join-Path $MqlRoot "Experts\EXP0019\FaerieProtocol\EXP0019_FaerieProtocol_Paper.mq5",
  Join-Path $MqlRoot "Experts\EXP0019\FaerieProtocolTests\EXP0019_FP_I15_PaperSelfTest.mq5"
)
foreach($target in $targets){
  $log = "$target.compile.log"
  & $MetaEditor "/compile:$target" "/log:$log"
  if($LASTEXITCODE -ne 0){ throw "MetaEditor compile failed: $target" }
  $text = Get-Content -Raw $log
  if($text -match "[1-9][0-9]* error"){ throw "Compile errors: $target" }
}
Write-Host "FP-I15 compile gate passed. Run EXP0019_FP_I15_PaperSelfTest on a test chart and archive Experts log."
