from tools.repository_paths import find_repository_root
from pathlib import Path
import shutil
import pytest
from tools.strategy_factory.acl_os.acl_10.io import load_json

REPO = find_repository_root(__file__)
ACL09 = REPO / "src/engine/legacy/acl_os_reference/fixtures/acl_09/reference_memory"
FIX = REPO / "src/engine/legacy/acl_os_reference/fixtures/acl_10"


@pytest.fixture
def repo():
    return REPO


@pytest.fixture
def acl09_root():
    return ACL09


@pytest.fixture
def permit():
    return load_json(FIX / "authority_permit.json")


@pytest.fixture
def policy():
    return load_json(FIX / "promotion_policy.json")


@pytest.fixture
def reference():
    return FIX / "reference_promotion"


@pytest.fixture
def copied_acl09(tmp_path):
    target = tmp_path / "acl09"
    shutil.copytree(ACL09, target)
    return target
