from tools.repository_paths import find_repository_root
from pathlib import Path
import pytest

@pytest.fixture
def repo_root():
    return find_repository_root(__file__)
