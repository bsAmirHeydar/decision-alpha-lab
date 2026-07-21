from __future__ import annotations
import glob
from pathlib import Path
import pytest

@pytest.fixture(scope="session")
def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]

@pytest.fixture(scope="session")
def cutover_root(repo_root: Path) -> Path:
    matches = sorted((repo_root / "registry/legacy_context_migration/consumer_wave_cutovers").glob("CUTOVER_*"))
    assert len(matches) == 1
    return matches[0]
