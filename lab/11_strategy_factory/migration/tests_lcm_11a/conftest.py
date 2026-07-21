from __future__ import annotations
import json
from pathlib import Path
import pytest

@pytest.fixture(scope="session")
def repo_root()->Path:return Path(__file__).resolve().parents[4]

@pytest.fixture(scope="session")
def inventory_root(repo_root:Path)->Path:
    roots=sorted((repo_root/'registry/legacy_context_migration/visual_object_inventories').glob('VISINV_*'))
    assert roots
    return roots[-1]

@pytest.fixture(scope="session")
def inventory(inventory_root:Path):return json.loads((inventory_root/'visual_object_inventory.json').read_text(encoding='utf-8'))
