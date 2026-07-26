from tools.repository_paths import find_repository_root
from pathlib import Path
import json
import pytest
ROOT=find_repository_root(__file__)
QROOT=ROOT/'registry/history/lcm/quarantine_observations/QUARANTINE_F2B27A6A93EB63C1B264B84DAFA00C2D'
@pytest.fixture(scope="session")
def qroot(): return QROOT
@pytest.fixture(scope="session")
def load(): return lambda name: json.loads((QROOT/name).read_text(encoding="utf-8"))
