from tools.repository_paths import find_repository_root
from pathlib import Path

from tools.strategy_factory.lcm.lcm_09a.static_validation import (
    FORBIDDEN_API_TOKENS,
    scan_module,
)


REPO = find_repository_root(__file__)
MODULE_ROOT = REPO / "src/engine/tooling/strategy_factory/lcm/lcm_09a"


def test_phase_module_has_no_order_or_chart_api() -> None:
    result = scan_module(MODULE_ROOT)
    assert result["passed"] is True
    assert result["forbidden_hit_count"] == 0
    assert result["forbidden_tokens"] == list(FORBIDDEN_API_TOKENS)


def test_patch_index_contains_no_existing_implementation_paths() -> None:
    lines = (REPO / "releases/history/lcm/indexes/LCM_09A_FILE_INDEX.txt").read_text(encoding="utf-8").splitlines()
    forbidden_prefixes = (
        "mql5/",
        "lab/10_infrastructure/",
        "src/engine/packages/",
    )
    assert not [path for path in lines if path.startswith(forbidden_prefixes)]
