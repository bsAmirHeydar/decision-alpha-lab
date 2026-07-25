from __future__ import annotations
from tools.repository_paths import find_repository_root
import json
from pathlib import Path
import pytest
@pytest.fixture(scope='session')
def repo_root(): return find_repository_root(__file__)
@pytest.fixture(scope='session')
def identity_root(repo_root):
    roots=sorted((repo_root/'registry/legacy_context_migration/identities').glob('IDENTITY_*'))
    assert roots
    return roots[-1]
