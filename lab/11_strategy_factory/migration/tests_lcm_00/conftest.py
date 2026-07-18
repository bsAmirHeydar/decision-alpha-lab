from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

@pytest.fixture
def repo_root() -> Path:
    return REPO_ROOT

@pytest.fixture
def baseline_root(repo_root: Path) -> Path:
    roots = sorted((repo_root / "registry/legacy_context_migration/baselines").glob("BASELINE_*"))
    assert roots
    return roots[-1]
