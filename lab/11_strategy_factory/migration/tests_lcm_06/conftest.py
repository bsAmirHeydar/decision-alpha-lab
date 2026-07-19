from pathlib import Path
import pytest
@pytest.fixture(scope="session")
def repo_root(): return Path(__file__).resolve().parents[4]
@pytest.fixture(scope="session")
def framework_root(repo_root):
    roots=sorted((repo_root/"registry/legacy_context_migration/frameworks").glob("FRAMEWORK_*"));assert roots;return roots[-1]
