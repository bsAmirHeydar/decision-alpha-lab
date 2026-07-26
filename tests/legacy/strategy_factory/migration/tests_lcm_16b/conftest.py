from tools.repository_paths import find_repository_root
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return find_repository_root(__file__)


@pytest.fixture(scope="session")
def package_root(repo_root: Path) -> Path:
    return repo_root / "registry/history/lcm/program_closures/PROGRAMCLOSE_34A677FF9F177118D7F29F6865D8367D"
