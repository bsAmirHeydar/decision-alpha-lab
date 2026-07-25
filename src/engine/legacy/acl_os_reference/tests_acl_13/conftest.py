from tools.repository_paths import find_repository_root
from pathlib import Path
import json,pytest
ROOT=find_repository_root(__file__)
@pytest.fixture
def root(): return ROOT
@pytest.fixture
def fixture(root): return root/'src/engine/legacy/acl_os_reference/fixtures/acl_13'
@pytest.fixture
def acl12(root): return root/'src/engine/legacy/acl_os_reference/fixtures/acl_12/reference_security_hardening'
@pytest.fixture
def assessment_request(fixture): return json.loads((fixture/'assessment_request.json').read_text())
@pytest.fixture
def permit(fixture): return json.loads((fixture/'authority_permit.json').read_text())
@pytest.fixture
def budget(fixture): return json.loads((fixture/'one_hour_budget_profile.json').read_text())
