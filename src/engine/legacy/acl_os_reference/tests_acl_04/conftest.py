from tools.repository_paths import find_repository_root
from pathlib import Path
import sys
import json
import yaml
import pytest

ROOT=find_repository_root(__file__)
sys.path.insert(0,str(ROOT))
FIX=ROOT/'src/engine/legacy/acl_os_reference/fixtures/acl_04'
ACL03=ROOT/'src/engine/legacy/acl_os_reference/fixtures/acl_03/reference_compilation'

@pytest.fixture
def fixtures():
    return {
        'root':FIX,
        'acl03':ACL03,
        'permit':json.loads((FIX/'authority_permit.json').read_text()),
        'search':json.loads((FIX/'search_authority.json').read_text()),
        'envelope':json.loads((FIX/'treatment_envelope.json').read_text()),
        'registry':json.loads((FIX/'atom_registry.json').read_text()),
        'human':yaml.safe_load((FIX/'human_setup.yaml').read_text()),
        'ai':json.loads((FIX/'ai_request.json').read_text()),
    }
