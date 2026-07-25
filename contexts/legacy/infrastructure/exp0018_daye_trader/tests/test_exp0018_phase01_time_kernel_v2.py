from tools.repository_paths import find_repository_root
from pathlib import Path
import importlib.util

ROOT = find_repository_root(__file__)
MODULE_PATH = ROOT / "contexts/legacy/infrastructure/exp0018_daye_trader/tools/validate_exp0018_phase01_time_kernel_v2.py"
spec = importlib.util.spec_from_file_location("p01validator", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
import sys
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def test_phase01_contract_and_fixtures():
    assert module.validate(ROOT) == []


def test_dst_fall_has_two_0130_instants():
    from datetime import datetime, timezone
    a = module.classify(datetime(2026, 11, 1, 5, 30, tzinfo=timezone.utc))
    b = module.classify(datetime(2026, 11, 1, 6, 30, tzinfo=timezone.utc))
    assert a.ny.replace(tzinfo=None) == b.ny.replace(tzinfo=None)
    assert (a.fold, b.fold) == (0, 1)
    assert a.subcycle == b.subcycle == "l2"


def test_p4_is_exactly_thirty_wall_clock_minutes():
    contract = __import__("json").loads((ROOT / "contexts/legacy/infrastructure/exp0018_daye_trader/contracts/daye_time_contract_v2.json").read_text())
    assert contract["subcycles"]["p4"] == ["16:30:00", "17:00:00"]
