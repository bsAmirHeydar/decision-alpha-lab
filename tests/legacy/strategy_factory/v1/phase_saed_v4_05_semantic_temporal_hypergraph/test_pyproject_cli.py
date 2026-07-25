from tools.repository_paths import find_repository_root
from pathlib import Path


def test_pyproject_registers_package_and_cli():
    root = find_repository_root(__file__)
    text = (root / "src/engine/packages/pyproject.toml").read_text(encoding="utf-8")
    assert 'saed-v4-hypergraph="saed_v4_semantic_hypergraph.cli:main"' in text
    assert '"saed_v4_semantic_hypergraph*"' in text
