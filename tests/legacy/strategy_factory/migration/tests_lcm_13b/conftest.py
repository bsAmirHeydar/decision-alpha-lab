from __future__ import annotations
from tools.repository_paths import find_repository_root
import glob
from pathlib import Path
import pytest

@pytest.fixture(scope="session")
def repo_root() -> Path:
    return find_repository_root(__file__)

@pytest.fixture(scope="session")
def cutover_root(repo_root: Path) -> Path:
    matches = sorted((repo_root / "registry/history/lcm/consumer_wave_cutovers").glob("CUTOVER_*"))
    assert len(matches) == 1
    return matches[0]
