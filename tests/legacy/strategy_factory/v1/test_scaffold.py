from strategy_factory.manifest import load_manifest
from strategy_factory.scaffold import scaffold_strategy


def test_scaffold_creates_valid_minimal_packet(tmp_path):
    root = scaffold_strategy("EXP_TEST", tmp_path)
    assert (root / "adapter.py").is_file()
    assert (root / "ANATOMY_DOCTRINE.md").is_file()
    manifest = load_manifest(root / "strategy.json")
    assert manifest.strategy_id == "EXP_TEST"
