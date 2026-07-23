from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


@pytest.fixture(scope="session")
def package_root(repo_root: Path) -> Path:
    return repo_root / "registry/legacy_context_migration/program_closures/PROGRAMCLOSE_34A677FF9F177118D7F29F6865D8367D"
