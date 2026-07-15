from pathlib import Path


def test_pyproject_registers_package_and_cli():
    root = Path(__file__).resolve().parents[4]
    text = (root / "lab/11_strategy_factory/python/pyproject.toml").read_text(encoding="utf-8")
    assert 'saed-v4-hypergraph="saed_v4_semantic_hypergraph.cli:main"' in text
    assert '"saed_v4_semantic_hypergraph*"' in text
