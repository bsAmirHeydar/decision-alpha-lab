from __future__ import annotations
import json,shutil,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
@pytest.fixture
def root(): return ROOT
@pytest.fixture
def acl14_root(ROOT=ROOT): return ROOT/'lab/11_strategy_factory/acl_os/fixtures/acl_14/reference_first_real_context_pilot'
@pytest.fixture
def permit(ROOT=ROOT): return json.loads((ROOT/'lab/11_strategy_factory/acl_os/fixtures/acl_15/authority_permit.json').read_text())
@pytest.fixture
def policy(ROOT=ROOT): return json.loads((ROOT/'lab/11_strategy_factory/acl_os/fixtures/acl_15/fleet_closure_policy.json').read_text())
