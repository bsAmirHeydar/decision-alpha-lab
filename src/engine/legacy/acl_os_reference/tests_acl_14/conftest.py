from __future__ import annotations
from tools.repository_paths import find_repository_root
import copy,json
from pathlib import Path
import pytest

ROOT=find_repository_root(__file__)
FIX=ROOT/'src/engine/legacy/acl_os_reference/fixtures/acl_14'
ACL13=ROOT/'src/engine/legacy/acl_os_reference/fixtures/acl_13/reference_one_hour_assessment'

def load(name):
    return json.loads((FIX/name).read_text(encoding='utf-8'))

@pytest.fixture
def root():
    return ROOT

@pytest.fixture
def acl13_root():
    return ACL13

@pytest.fixture
def permit():
    return copy.deepcopy(load('authority_permit.json'))

@pytest.fixture
def pilot_request():
    return copy.deepcopy(load('pilot_request.json'))

@pytest.fixture
def policy():
    return copy.deepcopy(load('pilot_policy.json'))
