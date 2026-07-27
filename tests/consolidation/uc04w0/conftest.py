from __future__ import annotations

from pathlib import Path

import pytest

from tools.repository_paths import find_repository_root


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return find_repository_root(Path(__file__))
