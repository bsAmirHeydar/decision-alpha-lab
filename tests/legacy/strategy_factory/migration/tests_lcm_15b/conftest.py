from tools.repository_paths import find_repository_root
import json
from pathlib import Path
import pytest
@pytest.fixture(scope="session")
def repo_root():return find_repository_root(__file__)
@pytest.fixture(scope="session")
def package_root(repo_root):return repo_root/"registry/history/lcm/root_release_reorganizations/ROOTREORG_1D879F480AD3B6F4C6EDC307D43AA381"
@pytest.fixture
def load(package_root):return lambda rel:json.loads((package_root/rel).read_text(encoding="utf-8"))
@pytest.fixture
def loadl(package_root):return lambda rel:[json.loads(x) for x in (package_root/rel).read_text(encoding="utf-8").splitlines() if x.strip()]
