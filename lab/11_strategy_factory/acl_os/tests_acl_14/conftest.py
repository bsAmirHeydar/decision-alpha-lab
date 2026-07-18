from __future__ import annotations
import copy,json
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[4]
FIX=ROOT/'lab/11_strategy_factory/acl_os/fixtures/acl_14'
ACL13=ROOT/'lab/11_strategy_factory/acl_os/fixtures/acl_13/reference_one_hour_assessment'

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
