from pathlib import Path
import pytest
@pytest.fixture
def repo_root(): return Path(__file__).resolve().parents[4]
@pytest.fixture
def classification_root(repo_root):
    roots=sorted((repo_root/'registry/legacy_context_migration/classifications').glob('CLASSIFICATION_*'))
    assert roots; return roots[-1]
