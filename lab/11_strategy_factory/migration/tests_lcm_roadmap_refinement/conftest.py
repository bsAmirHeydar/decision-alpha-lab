from pathlib import Path
import pytest

@pytest.fixture
def repo_root():
    return Path(__file__).resolve().parents[4]
