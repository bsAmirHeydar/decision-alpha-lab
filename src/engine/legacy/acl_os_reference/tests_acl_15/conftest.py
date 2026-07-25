from __future__ import annotations
from tools.repository_paths import find_repository_root
import json,shutil,sys
from pathlib import Path
import pytest
ROOT=find_repository_root(__file__)
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
@pytest.fixture
def root(): return ROOT
@pytest.fixture
def acl14_root(ROOT=ROOT): return ROOT/'src/engine/legacy/acl_os_reference/fixtures/acl_14/reference_first_real_context_pilot'
@pytest.fixture
def permit(ROOT=ROOT): return json.loads((ROOT/'src/engine/legacy/acl_os_reference/fixtures/acl_15/authority_permit.json').read_text())
@pytest.fixture
def policy(ROOT=ROOT): return json.loads((ROOT/'src/engine/legacy/acl_os_reference/fixtures/acl_15/fleet_closure_policy.json').read_text())
