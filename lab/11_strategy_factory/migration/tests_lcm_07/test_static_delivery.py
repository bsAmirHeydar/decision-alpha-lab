from pathlib import Path

from tools.strategy_factory.lcm.lcm_07.schema_validation import validate
from tools.strategy_factory.lcm.lcm_07.static_validation import scan


def test_no_forbidden_api_in_python_package():
    root = Path(__file__).resolve().parents[4]
    assert scan(root / "tools/strategy_factory/lcm/lcm_07") == []


def test_schemas_are_draft_2020_12_valid():
    root = Path(__file__).resolve().parents[4]
    result = validate(root / "registry/legacy_context_migration/lcm_07/schemas/v1", root)
    assert result["passed"]
    assert result["schema_count"] >= 20


def test_mql_static_mirror_has_no_order_api():
    root = Path(__file__).resolve().parents[4]
    text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in (root / "lab/11_strategy_factory/mql5/Include/AlphaLab/ACL_OS/LCM07").glob("*.mqh")
    )
    assert "OrderSend(" not in text
    assert "trade.Buy(" not in text
