from tools.repository_paths import find_repository_root

from pathlib import Path
import importlib.util

ROOT = find_repository_root(__file__)
MODULE_PATH = ROOT / "contexts/legacy/infrastructure/exp0018_daye_trader/tools/validate_exp0018_phase02_data_sync_v2.py"
spec = importlib.util.spec_from_file_location("p02_validator", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_phase02_validator_passes():
    assert module.validate(ROOT) == []


def test_missing_bar_is_not_forward_filled():
    datasets = module.load_fixture(ROOT / "contexts/legacy/infrastructure/exp0018_daye_trader/fixtures/daye_multi_symbol_alignment_cases_v2.csv")
    common, only_a, only_b = module.align_exact(datasets["missing_b"]["A"], datasets["missing_b"]["B"])
    assert len(common) == 2
    assert len(only_a) == 1
    assert len(only_b) == 0


def test_shifted_timestamps_do_not_align_by_index():
    datasets = module.load_fixture(ROOT / "contexts/legacy/infrastructure/exp0018_daye_trader/fixtures/daye_multi_symbol_alignment_cases_v2.csv")
    common, _, _ = module.align_exact(datasets["shifted"]["A"], datasets["shifted"]["B"])
    assert common == []


def test_exact_alignment_preserves_three_common_bars():
    datasets = module.load_fixture(ROOT / "contexts/legacy/infrastructure/exp0018_daye_trader/fixtures/daye_multi_symbol_alignment_cases_v2.csv")
    common, only_a, only_b = module.align_exact(datasets["exact"]["A"], datasets["exact"]["B"])
    assert len(common) == 3
    assert only_a == []
    assert only_b == []
