from tools.repository_paths import find_repository_root
from pathlib import Path

from src.engine.tooling.strategy_factory.lcm.lcm_07.schema_validation import validate
from src.engine.tooling.strategy_factory.lcm.lcm_07.static_validation import scan


def test_no_forbidden_api_in_python_package():
    root = find_repository_root(__file__)
    assert scan(root / "src/engine/tooling/strategy_factory/lcm/lcm_07") == []


def test_schemas_are_draft_2020_12_valid():
    root = find_repository_root(__file__)
    result = validate(root / "registry/history/lcm/lcm_07/schemas/v1", root)
    assert result["passed"]
    assert result["schema_count"] >= 20


def test_mql_static_mirror_has_no_order_api():
    root = find_repository_root(__file__)
    text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in (root / "mql5/legacy/strategy_factory_lab/Include/AlphaLab/ACL_OS/LCM07").glob("*.mqh")
    )
    assert "OrderSend(" not in text
    assert "trade.Buy(" not in text
