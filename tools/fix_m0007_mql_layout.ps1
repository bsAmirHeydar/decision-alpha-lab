# Fix M0007 MQL5 layout after accidental H0007/DecisionAlphaLab duplicate placement.
# Run from repository root.

$ErrorActionPreference = "Stop"

# Move final M0007 files into previous M-series style if they still exist in the temporary folder.
New-Item -ItemType Directory -Force "mql5/Experts/M0007" | Out-Null
New-Item -ItemType Directory -Force "mql5/Include/M0007" | Out-Null

if (Test-Path "mql5/Experts/M0007_FlagCountingF1/DAL_M0007_F1_Adaptive_Draw.mq5") {
  Copy-Item -Force "mql5/Experts/M0007_FlagCountingF1/DAL_M0007_F1_Adaptive_Draw.mq5" "mql5/Experts/M0007/M0007_FlagCountingF1.mq5"
}

$copyMap = @{
  "mql5/Include/M0007_FlagCountingF1/DAL_M0007_F1_Types.mqh"        = "mql5/Include/M0007/DAL_M0007F1Types.mqh";
  "mql5/Include/M0007_FlagCountingF1/DAL_M0007_F1_NodeDetector.mqh" = "mql5/Include/M0007/DAL_M0007F1NodeDetector.mqh";
  "mql5/Include/M0007_FlagCountingF1/DAL_M0007_F1_Detector.mqh"     = "mql5/Include/M0007/DAL_M0007F1Detector.mqh";
  "mql5/Include/M0007_FlagCountingF1/DAL_M0007_F1_Renderer.mqh"     = "mql5/Include/M0007/DAL_M0007F1Renderer.mqh";
  "mql5/Include/M0007_FlagCountingF1/README.md"                    = "mql5/Include/M0007/README_M0007_FlagCountingF1.md";
}
foreach ($src in $copyMap.Keys) {
  if (Test-Path $src) { Copy-Item -Force $src $copyMap[$src] }
}

# Update include paths now that DecisionAlphaLab folder is removed from mql5/Include.
Get-ChildItem -Path "mql5" -Recurse -Include *.mq5,*.mqh | ForEach-Object {
  $p = $_.FullName
  $s = Get-Content $p -Raw
  $s = $s.Replace('<DecisionAlphaLab/', '<')
  $s = $s.Replace('<M0007_FlagCountingF1/DAL_M0007_F1_Types.mqh>', '<M0007/DAL_M0007F1Types.mqh>')
  $s = $s.Replace('<M0007_FlagCountingF1/DAL_M0007_F1_NodeDetector.mqh>', '<M0007/DAL_M0007F1NodeDetector.mqh>')
  $s = $s.Replace('<M0007_FlagCountingF1/DAL_M0007_F1_Detector.mqh>', '<M0007/DAL_M0007F1Detector.mqh>')
  $s = $s.Replace('<M0007_FlagCountingF1/DAL_M0007_F1_Renderer.mqh>', '<M0007/DAL_M0007F1Renderer.mqh>')
  Set-Content -Path $p -Value $s -NoNewline
}

# Remove only known duplicate/wrong M0007-H0007 placements. Do not remove old M0001..M0006 code.
$badPaths = @(
  "mql5/Experts/DAL_M0007_H0007_F1_Adaptive_Draw.mq5",
  "mql5/Experts/H0007_F1_Adaptive_Draw.mq5",
  "mql5/Experts/H0007_F1_Detector.mqh",
  "mql5/Experts/H0007_F1_NodeDetector.mqh",
  "mql5/Experts/H0007_F1_README.md",
  "mql5/Experts/H0007_F1_Renderer.mqh",
  "mql5/Experts/H0007_F1_Types.mqh",
  "mql5/Experts/M0007_FlagCountingF1",
  "mql5/Include/H0007_FlagCountingF1",
  "mql5/Include/M0007_FlagCountingF1",
  "lab/09_execution/mql5/H0007_FlagCountingF1"
)
foreach ($p in $badPaths) {
  if (Test-Path $p) { Remove-Item -Recurse -Force $p }
}

Write-Host "M0007 MQL layout fixed. Now run: git status --short"
