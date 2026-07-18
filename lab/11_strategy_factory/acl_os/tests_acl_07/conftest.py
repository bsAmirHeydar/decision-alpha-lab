from __future__ import annotations
import json, sys
from pathlib import Path
import pytest

REPO = Path(__file__).resolve().parents[4]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

@pytest.fixture
def repo_root():
    return REPO

@pytest.fixture
def acl06_root():
    return REPO / 'lab/11_strategy_factory/acl_os/fixtures/acl_06/reference_run'

@pytest.fixture
def fixture_root():
    return REPO / 'lab/11_strategy_factory/acl_os/fixtures/acl_07'

@pytest.fixture
def permit(fixture_root):
    return json.loads((fixture_root / 'authority_permit.json').read_text(encoding='utf-8'))

@pytest.fixture
def policy(fixture_root):
    return json.loads((fixture_root / 'validation_policy.json').read_text(encoding='utf-8'))
