from tools.repository_paths import find_repository_root
from pathlib import Path
import pytest
@pytest.fixture
def repo_root():
    return find_repository_root(__file__)
@pytest.fixture
def reconciliation_root(repo_root):
    roots = sorted((repo_root / "registry/history/lcm/documentation_reconciliations").glob("DOCRECON_*"))
    assert roots
    return roots[-1]
