from __future__ import annotations
from tools.repository_paths import find_repository_root

import sys
from pathlib import Path

import pytest

REPO_ROOT = find_repository_root(__file__)
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

@pytest.fixture
def repo_root() -> Path:
    return REPO_ROOT

@pytest.fixture
def baseline_root(repo_root: Path) -> Path:
    roots = sorted((repo_root / "registry/history/lcm/baselines").glob("BASELINE_*"))
    assert roots
    return roots[-1]
