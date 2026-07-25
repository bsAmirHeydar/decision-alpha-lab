from __future__ import annotations
from tools.repository_paths import find_repository_root
import sys
from pathlib import Path
import pytest
REPO_ROOT=find_repository_root(__file__)
if str(REPO_ROOT) not in sys.path: sys.path.insert(0,str(REPO_ROOT))
@pytest.fixture
def repo_root(): return REPO_ROOT
@pytest.fixture
def survey_root(repo_root):
    roots=sorted((repo_root/'registry/legacy_context_migration/surveys').glob('SURVEY_*'))
    assert roots; return roots[-1]
