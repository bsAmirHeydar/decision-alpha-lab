#!/usr/bin/env python3
"""Static contract checks for the NDS lightweight Strategy Tester runtime."""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
EA = ROOT / "mql5/Experts/FlagCounting/NDSHookLimitF123Backtest.mq5"
BT_ENGINE = ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSBacktestEngine.mqh"
BT_TYPES = ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSBacktestTypes.mqh"
TRADE_CORE = ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeExecutionCore.mqh"
TRADE_ENGINE = ROOT / "mql5/Include/FlagCountingPhoenix/FP_NDSHookTradeEngine.mqh"
HOOK_CORE = ROOT / "mql5/Include/FlagCountingPhoenix/FP_HookPhase02DetectionCore.mqh"
HOOK_ENGINE = ROOT / "mql5/Include/FlagCountingPhoenix/FP_HookPhase02Engine.mqh"

failures: list[str] = []
passes: list[str] = []


def check(condition: bool, label: str) -> None:
    (passes if condition else failures).append(label)


def text(path: Path) -> str:
    check(path.is_file(), f"file exists: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8") if path.is_file() else ""


ea = text(EA)
bt_engine = text(BT_ENGINE)
text(BT_TYPES)
trade_core = text(TRADE_CORE)
trade_engine = text(TRADE_ENGINE)
hook_core = text(HOOK_CORE)
hook_engine = text(HOOK_ENGINE)

check("FP_NDSBacktestEngine.mqh" in ea, "EA includes dedicated backtest engine")
check("FP_RunNDSLightweightBacktestCycle" in ea, "EA calls lightweight cycle")
check("current_open_bar == g_nds_bt_last_open_bar" in ea, "one execution per new bar gate")
check("MQL_TESTER" in ea and "INIT_FAILED" in ea, "tester-only runtime guard")
check("send_live_orders = false" in ea, "non-tester safety forces no-send")
check("InpBTResetUsedSetupsOnInit = true" in ea, "deterministic used-setup reset default")
check("cfg.export_csv = false" in ea, "trade CSV disabled in backtest")
check("cfg.draw_sequences = false" in ea, "Hook visuals disabled in backtest")
check("cfg.draw_nodes = false" in ea, "node visuals disabled in backtest")

for forbidden in (
    "FP_LicenseEngine.mqh",
    "FP_Renderer.mqh",
    "FP_StateGateEngine.mqh",
    "FP_EntryBridgeEngine.mqh",
    "FP_PaperIntentEngine.mqh",
    "FP_PaperLifecycleEngine.mqh",
    "FP_BrokerDryRunEngine.mqh",
    "FP_BrokerValidatorEngine.mqh",
    "FP_HookPhase03Engine.mqh",
    "FP_HookPhase04Engine.mqh",
    "FP_HookPhase05Engine.mqh",
    "FP_HookPhase06Engine.mqh",
    "FP_HookPhase07Engine.mqh",
    "FP_HookPhase08Engine.mqh",
    "FP_HookPhase09Engine.mqh",
    "FP_HookPhase10Engine.mqh",
):
    check(forbidden not in ea and forbidden not in bt_engine, f"heavy module absent: {forbidden}")

for forbidden_api in ("ObjectCreate(", "ChartRedraw(", "EventSetTimer(", "OnTimer(", "OnChartEvent("):
    check(forbidden_api not in ea and forbidden_api not in bt_engine,
          f"runtime side effect absent: {forbidden_api}")

check("FP_HookPhase02DetectionCore.mqh" in bt_engine,
      "backtest uses detection-only Hook core")
check("FP_NDSHookTradeExecutionCore.mqh" in bt_engine,
      "backtest uses no-export execution core")
check("FP_RunHookPhase02DetectionCore" in bt_engine,
      "backtest calls Hook core directly")
check("FP_RunNDSHookLimitF123ExecutionCore" in bt_engine,
      "backtest calls trade core directly")
check("skip_hook_rebuild_while_position_open" in bt_engine,
      "position fast path is implemented")
check("FP_NDSClearStructureSnapshot" in bt_engine,
      "position fast path clears stale Hook snapshot")

check("FP_RunNDSHookLimitF123ExecutionCore" in trade_engine,
      "production trade engine wraps shared execution core")
check("FP_NDSHookTradeExportReport" in trade_engine,
      "production wrapper preserves export sink")
check("FP_NDSHookTradeExportReport" not in trade_core,
      "shared trade core has no CSV side effect")
check("FP_NDSHookTradeFinalizeReport" in trade_core,
      "shared trade core preserves finalization")

check("FP_RunHookPhase02DetectionCore" in hook_engine,
      "production Hook engine wraps shared detection core")
check("FP_HookP02DrawSequences" in hook_engine,
      "production wrapper preserves optional visuals")
check("FP_HookP02ExportSequences" in hook_engine,
      "production wrapper preserves optional export")
check("FP_HookP02DrawSequences" not in hook_core,
      "shared Hook core has no chart drawing")
check("FP_HookP02ExportSequences" not in hook_core,
      "shared Hook core has no CSV export")

check("cfg.requested_bars = 1200" in bt_engine and "cfg.scale_l4 = 8" in bt_engine,
      "FAST profile bounded to 1200 bars and four scales")
check("cfg.requested_bars = 5000" in bt_engine and "cfg.scale_l8 = 55" in bt_engine,
      "PARITY profile preserves full historical profile")

print(f"PASS={len(passes)} FAIL={len(failures)}")
for item in passes:
    print(f"PASS: {item}")
for item in failures:
    print(f"FAIL: {item}")

sys.exit(1 if failures else 0)
