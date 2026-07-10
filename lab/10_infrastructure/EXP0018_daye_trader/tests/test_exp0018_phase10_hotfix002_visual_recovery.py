from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
VALIDATOR = ROOT / "lab/10_infrastructure/EXP0018_daye_trader/tools/validate_exp0018_phase10_hotfix002_visual_recovery.py"
FIXTURES = ROOT / "lab/10_infrastructure/EXP0018_daye_trader/fixtures/daye_phase10_hotfix002_symbol_alias_cases.csv"
RESOLVER = ROOT / "mql5/Include/DayeTrader/EXP0018/DAYE_SymbolResolver.mqh"
ENGINE = ROOT / "mql5/Include/DayeTrader/EXP0018/DAYE_VisualEngine.mqh"


def normalize(value: str) -> str:
    return (
        value.upper()
        .replace("#", "")
        .replace(".", "")
        .replace("_", "")
        .replace("-", "")
        .replace(" ", "")
        .replace("/", "")
        .replace("\\", "")
        .replace("&", "AND")
    )


def test_validator_passes() -> None:
    subprocess.run([sys.executable, str(VALIDATOR)], cwd=ROOT, check=True)


def test_key_aliases_normalize() -> None:
    assert normalize("#USNDAQ100") == "USNDAQ100"
    assert normalize("#USSPX500") == "USSPX500"
    assert normalize("US500.cash") == "US500CASH"


def test_fixture_contract_is_populated() -> None:
    rows = list(csv.DictReader(FIXTURES.open(encoding="utf-8")))
    assert len(rows) >= 4
    assert any(row["current_chart"] == "#USNDAQ100" for row in rows)
    assert any(row["expected_pair_possible"] == "false" for row in rows)


def test_local_fallback_is_separate_from_divergence() -> None:
    resolver = RESOLVER.read_text(encoding="utf-8")
    engine = ENGINE.read_text(encoding="utf-8")
    assert "DAYE_AggregateSymbolBars" in engine
    assert "ProcessLocalCurrentChart" in engine
    assert "DAYE_ResolveBrokerPair" in resolver
    for token in ("OrderSend", "CTrade", "PositionOpen"):
        assert token not in resolver + engine
