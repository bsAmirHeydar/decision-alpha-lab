from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[4]

@pytest.fixture
def root():
    return ROOT

@pytest.fixture
def acl10(root):
    return root / 'lab/11_strategy_factory/acl_os/fixtures/acl_10/reference_promotion'

@pytest.fixture
def permit(root):
    from tools.strategy_factory.acl_os.acl_11.io import load_json
    return load_json(root / 'lab/11_strategy_factory/acl_os/fixtures/acl_11/authority_permit.json')
