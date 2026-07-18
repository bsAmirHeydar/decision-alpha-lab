from __future__ import annotations
import json, shutil
from pathlib import Path
import pytest
REPO_ROOT=Path(__file__).resolve().parents[4]
ACL11_ROOT=REPO_ROOT/'lab/11_strategy_factory/acl_os/fixtures/acl_11/reference_runtime_custody'
ACL12_ROOT=REPO_ROOT/'lab/11_strategy_factory/acl_os/fixtures/acl_12/reference_security_hardening'
PERMIT_PATH=REPO_ROOT/'lab/11_strategy_factory/acl_os/fixtures/acl_12/authority_permit.json'
@pytest.fixture
def permit(): return json.loads(PERMIT_PATH.read_text(encoding='utf-8'))
@pytest.fixture
def acl11_copy(tmp_path):
    dst=tmp_path/'acl11'; shutil.copytree(ACL11_ROOT,dst); return dst
@pytest.fixture
def ROOT(): return REPO_ROOT
@pytest.fixture
def ACL11(): return ACL11_ROOT
@pytest.fixture
def ACL12(): return ACL12_ROOT
