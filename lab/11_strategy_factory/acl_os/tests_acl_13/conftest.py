from pathlib import Path
import json,pytest
ROOT=Path(__file__).resolve().parents[4]
@pytest.fixture
def root(): return ROOT
@pytest.fixture
def fixture(root): return root/'lab/11_strategy_factory/acl_os/fixtures/acl_13'
@pytest.fixture
def acl12(root): return root/'lab/11_strategy_factory/acl_os/fixtures/acl_12/reference_security_hardening'
@pytest.fixture
def assessment_request(fixture): return json.loads((fixture/'assessment_request.json').read_text())
@pytest.fixture
def permit(fixture): return json.loads((fixture/'authority_permit.json').read_text())
@pytest.fixture
def budget(fixture): return json.loads((fixture/'one_hour_budget_profile.json').read_text())
