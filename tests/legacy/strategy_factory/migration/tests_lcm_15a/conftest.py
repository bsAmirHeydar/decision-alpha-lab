from tools.repository_paths import find_repository_root
import json
from pathlib import Path
import pytest
@pytest.fixture(scope="session")
def repo_root(): return find_repository_root(__file__)
@pytest.fixture(scope="session")
def proof_root(repo_root): return repo_root/"registry/history/lcm/deletion_candidate_proofs/DELCAND_DBF53BE0F1838F171906F990E05930D6"
@pytest.fixture
def load(proof_root):
    return lambda rel: json.loads((proof_root/rel).read_text(encoding="utf-8"))
@pytest.fixture
def loadl(proof_root):
    return lambda rel: [json.loads(x) for x in (proof_root/rel).read_text(encoding="utf-8").splitlines() if x.strip()]
