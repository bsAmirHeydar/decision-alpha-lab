from __future__ import annotations

from pathlib import Path

import pytest

from tools.repository_paths import RepositoryPaths


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return RepositoryPaths.discover(Path(__file__)).root
