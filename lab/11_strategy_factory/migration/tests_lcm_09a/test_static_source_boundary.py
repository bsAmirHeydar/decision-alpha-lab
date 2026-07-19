from pathlib import Path

from tools.strategy_factory.lcm.lcm_09a.static_validation import (
    FORBIDDEN_API_TOKENS,
    scan_module,
)


REPO = Path(__file__).resolve().parents[4]
MODULE_ROOT = REPO / "tools/strategy_factory/lcm/lcm_09a"


def test_phase_module_has_no_order_or_chart_api() -> None:
    result = scan_module(MODULE_ROOT)
    assert result["passed"] is True
    assert result["forbidden_hit_count"] == 0
    assert result["forbidden_tokens"] == list(FORBIDDEN_API_TOKENS)


def test_patch_index_contains_no_existing_implementation_paths() -> None:
    lines = (REPO / "LCM_09A_FILE_INDEX.txt").read_text(encoding="utf-8").splitlines()
    forbidden_prefixes = (
        "mql5/",
        "lab/10_infrastructure/",
        "lab/11_strategy_factory/python/",
    )
    assert not [path for path in lines if path.startswith(forbidden_prefixes)]
