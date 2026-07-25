from strategy_factory.scaffold_v2 import scaffold_strategy_v2


def test_scaffold_v2_builds_plugin_packet(tmp_path):
    root = scaffold_strategy_v2("new_alpha", tmp_path)
    assert (root / "strategy_v2.json").exists()
    assert (root / "adapter.py").exists()
    assert (root / "features.py").exists()
    assert (root / "tests" / "test_adapter.py").exists()
