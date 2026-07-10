param([string]$RepoRoot = ".")
$ErrorActionPreference = "Stop"
$root = (Resolve-Path $RepoRoot).Path
python "$root\lab\10_infrastructure\EXP0018_daye_trader\tools\validate_exp0018_phase10_unified_visual_v2.py" "$root"
python -m pytest "$root\lab\10_infrastructure\EXP0018_daye_trader\tests\test_exp0018_phase10_unified_visual_v2.py" -q
if (Test-Path "$root\tools\engineering\check_mql5_compatibility.py") {
  python "$root\tools\engineering\check_mql5_compatibility.py" --root "$root" --paths `
    "mql5/Experts/DayeTrader/EXP0018_Daye_Visual_Anatomy.mq5" `
    "mql5/Include/DayeTrader/EXP0018/DAYE_VisualTypes.mqh" `
    "mql5/Include/DayeTrader/EXP0018/DAYE_VisualIdentity.mqh" `
    "mql5/Include/DayeTrader/EXP0018/DAYE_VisualObjectManager.mqh" `
    "mql5/Include/DayeTrader/EXP0018/DAYE_VisualSelfTest.mqh" `
    "mql5/Include/DayeTrader/EXP0018/DAYE_VisualEngine.mqh"
}
Write-Host "EXP0018 Phase 10 unified visual checks: PASS"
