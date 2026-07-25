from tools.repository_paths import find_repository_root
from pathlib import Path
import json,pytest
@pytest.fixture(scope="session")
def repo_root():return find_repository_root(__file__)
@pytest.fixture(scope="session")
def migration_root(repo_root):return repo_root/'registry/legacy_context_migration/visualizer_migrations/VISMIG_0938A2A7868358466B7B877BD1E5251D'
@pytest.fixture(scope="session")
def load():return lambda p:json.loads(Path(p).read_text(encoding="utf-8"))
