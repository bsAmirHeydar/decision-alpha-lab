from __future__ import annotations
from tools.repository_paths import find_repository_root

import json
import re
from pathlib import Path

ROOT = find_repository_root(__file__)
CONTRACT = ROOT / "contexts/legacy/infrastructure/exp0018_daye_trader/contracts/daye_phase10_hotfix002_visual_recovery.json"
EXPERT = ROOT / "mql5/Experts/DayeTrader/EXP0018_Daye_Visual_Anatomy.mq5"
ENGINE = ROOT / "mql5/Include/DayeTrader/EXP0018/DAYE_VisualEngine.mqh"
TYPES = ROOT / "mql5/Include/DayeTrader/EXP0018/DAYE_VisualTypes.mqh"
RESOLVER = ROOT / "mql5/Include/DayeTrader/EXP0018/DAYE_SymbolResolver.mqh"
LIFECYCLE_TEST = ROOT / "mql5/Include/DayeTrader/EXP0018/DAYE_LifecycleSelfTest.mqh"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    require(contract["hotfix_id"] == "EXP0018-P10-HF002", "wrong hotfix id")

    expert = EXPERT.read_text(encoding="utf-8")
    engine = ENGINE.read_text(encoding="utf-8")
    types = TYPES.read_text(encoding="utf-8")
    resolver = RESOLVER.read_text(encoding="utf-8")
    lifecycle = LIFECYCLE_TEST.read_text(encoding="utf-8")

    for token in (
        "InpAutoResolveBrokerSymbols",
        "InpPreferCurrentChartSymbol",
        "InpFailInitIfPairPipelineUnavailable",
        "InpAllowSingleSymbolTimeFallback",
        "DAYE_ResolveBrokerPair",
    ):
        require(token in expert, f"missing Expert recovery token: {token}")

    for token in (
        "BuildLocalPeriodsForChart",
        "ProcessLocalCurrentChart",
        "allow_single_symbol_time_fallback",
        "paired divergence source did not initialize",
        "object failure kind=",
    ):
        require(token in engine, f"missing engine recovery token: {token}")

    require("DAYE_VISUAL_SCHEMA_VERSION 3" in types, "visual schema not advanced")
    require("USNDAQ100" in resolver and "USSPX500" in resolver, "required broker aliases absent")
    require(re.search(r"\bconst\s+string\s+protected\b", lifecycle) is None, "reserved protected identifier remains")

    forbidden = ("OrderSend", "CTrade", "PositionOpen", "WebRequest")
    changed_code = expert + engine + types + resolver
    for token in forbidden:
        require(token not in changed_code, f"forbidden capability found: {token}")

    print("EXP0018 P10 Hotfix002 visual recovery validation: PASS")


if __name__ == "__main__":
    main()
