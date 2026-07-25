from tools.repository_paths import find_repository_root
from pathlib import Path
import pytest
@pytest.fixture
def repo_root(): return find_repository_root(__file__)
@pytest.fixture
def char_root(repo_root):
    roots=sorted((repo_root/'registry/legacy_context_migration/characterizations').glob('CHARACTERIZATION_*'))
    assert roots
    return roots[-1]
