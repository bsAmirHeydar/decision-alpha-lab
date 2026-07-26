from __future__ import annotations
from tools.repository_paths import find_repository_root
import json
from pathlib import Path
import pytest

@pytest.fixture(scope="session")
def repo_root()->Path:return find_repository_root(__file__)

@pytest.fixture(scope="session")
def inventory_root(repo_root:Path)->Path:
    roots=sorted((repo_root/'registry/history/lcm/visual_object_inventories').glob('VISINV_*'))
    assert roots
    return roots[-1]

@pytest.fixture(scope="session")
def inventory(inventory_root:Path):return json.loads((inventory_root/'visual_object_inventory.json').read_text(encoding='utf-8'))
