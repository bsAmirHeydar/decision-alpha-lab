from __future__ import annotations
import json,sys
from pathlib import Path
import pytest
REPO=Path(__file__).resolve().parents[4]
if str(REPO) not in sys.path: sys.path.insert(0,str(REPO))
@pytest.fixture
def repo_root(): return REPO
@pytest.fixture
def acl08_root(): return REPO/'lab/11_strategy_factory/acl_os/fixtures/acl_08/reference_report'
@pytest.fixture
def fixture_root(): return REPO/'lab/11_strategy_factory/acl_os/fixtures/acl_09'
@pytest.fixture
def permit(fixture_root): return json.loads((fixture_root/'authority_permit.json').read_text())
@pytest.fixture
def memory_policy(fixture_root): return json.loads((fixture_root/'memory_policy.json').read_text())
@pytest.fixture
def planner_policy(fixture_root): return json.loads((fixture_root/'planner_policy.json').read_text())
